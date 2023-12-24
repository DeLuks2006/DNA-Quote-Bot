from discord import Interaction, Webhook, Embed, ButtonStyle
from discord import ui
from bot.database.models import Quote
from bot.database import Database


class QuoteDetailBaseView(ui.View):
    def __init__(self, quote: Quote, db: Database, *args, **kwargs):
        self.db = db
        self.quote = quote
        self.title = "Quote detail"

        super().__init__(*args, **kwargs)

    async def send(self, followup: Webhook) -> None:
        embed = self.build_embed()
        self.message = await followup.send(
            embed=embed, view=self, wait=True, ephemeral=True
        )

    async def update_message(self) -> None:
        await self.message.edit(view=self)

    def build_embed(self) -> Embed:
        approved = "✅" if self.quote.approved else "❌"
        description = f"**Quote:** {self.quote.text}"
        embed = Embed(title=self.title, description=description)
        embed.add_field(name="Author", value=self.quote.author)
        embed.add_field(name="Approved", value=approved)
        embed.add_field(name="Submitted at", value=self.quote.submitted_at)
        return embed


class QuoteDetailUserView(QuoteDetailBaseView):
    async def send(self, followup: Webhook) -> None:
        if not self.quote.approved:
            button = ui.Button(label="Unsubmit", style=ButtonStyle.danger)

            async def button_callback(interaction: Interaction) -> None:
                await interaction.response.defer()

                if self.quote.approved:
                    await interaction.response.send_message(
                        "Quote has been approved, can't unsubmit.", ephemeral=True
                    )
                else:
                    with self.db.sessionmaker() as session:
                        self.db.remove_quote(session, self.quote.id)
                    new_button = self.children[0]
                    new_button.label = "Unsubmitted"
                    new_button.disabled = True
                    await self.update_message()
                    
            button.callback = button_callback
            self.add_item(button)
        await super().send(followup)
