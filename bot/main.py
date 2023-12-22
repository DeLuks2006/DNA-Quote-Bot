import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from quotes import QuoteDB

# [i] - info
# [-] - shits going down (error)
# [+] - everythin alr

TEST_GUILD = discord.Object(id=1159225022888554506)
COG_FOLDER = "bot/cogs"
load_dotenv()

db = QuoteDB()
print(f"[i] Quotes: {db.quotes}")


class MyClient(commands.Bot):
    # If this class extended discord.Client
    # it would be more of a pain to get everything set up correctly

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # Nobody wants to specify the files manually
        found_cogs = []
        for file in os.listdir(COG_FOLDER):
            if file.endswith(".py"):
                found_cogs.append(f"cogs.{file[:-3]}")

        print(f"[i] Loading cogs...")
        for cog in found_cogs:
            await self.load_extension(cog)

        # If you don't specify a guild slash commands take up to 1 hour to sync.
        # Remove in production pls
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

    async def on_ready(self) -> None:
        print(f'[i] Logged on as {self.user}!')


intents = discord.Intents.default()
intents.messages = True
bot = MyClient(intents=intents, command_prefix="/")  # Prefix doesn't matter here

bot.run(os.getenv("TOKEN"))
