from functools import partial
from bot.client import MyClient
from bot.custom.views.pagination import PaginationView
from bot.custom.views.quote_detail import QuoteDetailUserView, QuoteDetailAdminView
from bot.database.models import Quote
from discord import app_commands, Interaction, Embed, SelectOption
from discord.ext import commands
from math import ceil



class QuotesCog(commands.Cog):
    def __init__(self, bot: MyClient):
        self.bot = bot
        self.db = bot.db
        self.limit = 25
    
    def options_from_quotes(self, quotes: list[Quote]) -> list[SelectOption]:
        options = []
        for quote in quotes:
            author = quote.author
            text = quote.text
            if len(text) > 100:
                text = text[: 100 - 3] + "..."
            if len(author) > 100:
                author = author[: 100 - 3] + "..."
            options.append(SelectOption(label=text, description=author, value=quote.id))
        return options

    async def select_callback(
        self, view_template: QuoteDetailUserView | QuoteDetailAdminView,
        interaction: Interaction
    ):
        await interaction.response.defer()

        quote_id = interaction.data["values"][0]
        with self.db.sessionmaker() as session:
            quote = self.db.get_quote(session, quote_id)
        title = "Quote detail"
        if not quote:
            description = "Quote not found."
            embed = Embed(title=title, description=description)
            await interaction.followup.send(ephemeral=True, embed=embed)
        else:
            view = view_template(quote, self.db)
            await view.send(interaction.followup)

    @app_commands.command()
    async def submit(self, interaction: Interaction, quote: str, author: str) -> None:
        """
        Submit quote for later approval.
        """
        await interaction.response.defer(ephemeral=True, thinking=True)

        # Validation
        if len(quote) > 2096:
            return await interaction.followup.send(
                "Quote must not exceed 2096 characters."
            )
        if len(author) > 256:
            return await interaction.followup.send(
                "Author must not exceed 256 characters."
            )

        with self.db.sessionmaker() as session:
            if self.db.get_quote_by_text(session, text=quote) is not None:
                return await interaction.followup.send("Quote already exists.")

            self.db.add_quote(
                session, author, text=quote, submitter_id=interaction.user.id
            )

        # Build response
        title = "Quote submitted for approval"
        description = f"**{quote}**"
        embed = Embed(title=title, description=description)
        embed.set_footer(text=f"— {author}")

        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.choices(
        type=[
            app_commands.Choice(name="All", value="all"),
            app_commands.Choice(name="Unapproved", value="unapproved"),
        ]
    )
    async def submitted(
        self, interaction: Interaction, type: app_commands.Choice[str]
    ) -> None:
        """
        See list of submitted quotes by user.
        """
        await interaction.response.defer(ephemeral=True, thinking=True)

        # Query DB for submitted quotes by user
        only_unapproved = type.value == "unapproved"
        with self.db.sessionmaker() as session:
            quotes = self.db.get_quotes(
                session, interaction.user.id, only_unapproved=only_unapproved
            )

        if quotes is None:
            return await interaction.followup.send("No submitted quotes found.")

        # Build response
        options = self.options_from_quotes(quotes)
        pages = ceil((len(quotes) / self.limit) - 1)
        placeholder = "Submitted quotes:"
        select_callback = partial(self.select_callback, QuoteDetailUserView)

        pagination_view = PaginationView(
            options, pages, placeholder, select_callback, self.limit
        )
        return await pagination_view.send(interaction.followup)

    @app_commands.command()
    async def submissions(self, interaction: Interaction) -> None:
        """
        See list of submitted quotes by all users.
        """
        await interaction.response.defer(ephemeral=True, thinking=True)

        # Query DB for quotes awaiting approval
        with self.db.sessionmaker() as session:
            quotes = self.db.get_quotes(session, only_unapproved=True)
        if quotes is None:
            return await interaction.followup.send("No submitted quotes found.")

        # Build response
        options = self.options_from_quotes(quotes)
        pages = ceil((len(quotes) / self.limit) - 1)
        placeholder = "Submitted quotes:"
        select_callback = partial(self.select_callback, QuoteDetailAdminView)

        pagination_view = PaginationView(
            options, pages, placeholder, select_callback, self.limit
        )
        return await pagination_view.send(interaction.followup)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(QuotesCog(bot))
