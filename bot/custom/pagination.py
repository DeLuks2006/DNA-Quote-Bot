from discord import (
    Interaction,
    Webhook,
    SelectOption,
)
from discord import ui


class PaginationView(ui.View):
    def __init__(
        self,
        options: list[SelectOption],
        pages: int,
        placeholder: str,
        select_callback,
        limit: int = 5,
        *args,
        **kwargs
    ):
        self.options = options
        self.pages = pages
        self.placeholder = placeholder
        self.select_callback = select_callback
        self.limit = limit
        self.page = 0

        super().__init__(*args, **kwargs)

    async def send(self, followup: Webhook) -> None:
        self.update_buttons()
        self.message = await followup.send(view=self, wait=True)
        await self.update_message()

    def get_page_options(self) -> list[SelectOption]:
        offset_start = self.page * self.limit
        offset_end = offset_start + self.limit
        return self.options[offset_start:offset_end]

    def create_select(self, options: list[SelectOption]) -> None:
        last_child = self.children[-1]
        if isinstance(last_child, ui.Select):
            last_child.options = options
        else:
            select = ui.Select(
                options=options,
                custom_id="select",
                placeholder=self.placeholder,
            )
            select.callback = self.select_callback
            self.add_item(select)

    def update_buttons(self) -> None:
        self.page_button.label = f"{self.page + 1}/{self.pages + 1}"
        if self.page == 0:
            self.first_page.disabled = True
            self.previous_page.disabled = True
        else:
            self.first_page.disabled = False
            self.previous_page.disabled = False

        if self.page == self.pages:
            self.last_page.disabled = True
            self.next_page.disabled = True
        else:
            self.last_page.disabled = False
            self.next_page.disabled = False

    async def update_message(self) -> None:
        self.update_buttons()
        options = self.get_page_options()
        self.create_select(options)
        await self.message.edit(view=self)

    @ui.button(label="⏪")
    async def first_page(
        self, interaction: Interaction, button: ui.Button
    ) -> None:
        await interaction.response.defer()
        self.page = 0
        await self.update_message()

    @ui.button(label="◀️")
    async def previous_page(
        self, interaction: Interaction, button: ui.Button
    ) -> None:
        await interaction.response.defer()
        self.page -= 1
        await self.update_message()

    @ui.button(label="Page", disabled=True)
    async def page_button(self, interaction: Interaction, button: ui.Button) -> None:
        pass

    @ui.button(label="▶️")
    async def next_page(
        self, interaction: Interaction, button: ui.Button
    ) -> None:
        await interaction.response.defer()
        self.page += 1
        await self.update_message()

    @ui.button(label="⏩")
    async def last_page(
        self, interaction: Interaction, button: ui.Button
    ) -> None:
        await interaction.response.defer()
        self.page = self.pages
        await self.update_message()
