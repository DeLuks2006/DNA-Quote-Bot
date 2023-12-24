from discord import Interaction, Webhook, Embed, ButtonStyle
from discord import ui
from bot.database.models import Quote
from bot.database import Database
from bot.custom.permissions import is_moderator


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


class QuoteDetailAdminView(QuoteDetailBaseView):
    async def check_permissions(self, interaction: Interaction) -> None:
        if not is_moderator(interaction):
            return await interaction.followup.send("Missing required permissions")

    async def send(self, followup: Webhook) -> None:
        async def approve_callback(interaction: Interaction) -> None:
            await interaction.response.defer()
            await self.check_permissions(interaction)
    
            with self.db.sessionmaker() as session:
                self.db.approve_quote(session, self.quote.id, interaction.user.id)
            button = self.children[0]
            button.label = "Approved"
            button.disabled = True
            await self.update_message()
        
        async def delete_callback(interaction: Interaction) -> None:
            await interaction.response.defer()
            await self.check_permissions(interaction)

            with self.db.sessionmaker() as session:
                self.db.remove_quote(session, self.quote.id)
            self.clear_items()
            button = ui.Button(label="Deleted", style=ButtonStyle.danger, disabled=True)
            self.add_item(button)
            await self.update_message()

        if self.quote.approved:
            approve_button = ui.Button(
                label="Approved", style=ButtonStyle.success, disabled=True
            )
        else:
            approve_button = ui.Button(label="Approve", style=ButtonStyle.success)
            approve_button.callback = approve_callback
        delete_button = ui.Button(label="Delete", style=ButtonStyle.danger)
        delete_button.callback = delete_callback
        self.add_item(approve_button)
        self.add_item(delete_button)
        await super().send(followup)
