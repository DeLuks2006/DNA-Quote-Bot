import discord
import logging
from discord.ext import commands
from .database import Database


class MyClient(commands.Bot):
    def __init__(self, db: Database, *args, **kwargs) -> None:
        self.db = db
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        await self.load_extension("bot.cogs.quotes")

        # If you don't specify a guild slash commands take up to 1 hour to sync
        # Remove in production pls
        TEST_GUILD = discord.Object(id=1159225022888554506)
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

    async def on_ready(self) -> None:
        logging.info(f"Logged on as {self.user}!")
