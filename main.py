import discord
from discord import app_commands
from discord.app_commands import tree
from dotenv import load_dotenv
import os

# [i] - info
# [-] - shits going down (error)
# [+] - everythin alr

TEST_GUILD = discord.Object(id=1159225022888554506)
load_dotenv()


class MyClient(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # We need a CommandTree to hold all the application commands (slash commands)
        # Since we're using discord.Client instead of commands.Bot, our bot doesn't
        # have a CommandTree by default
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # If you don't specify a guild slash commands take up to 1 hour to sync.
        # Remove in production pls
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)

    async def on_ready(self):
        print(f'[i] Logged on as {self.user}!')

    async def on_message(self, message):
        # make the bot not talk to it self
        if message.author.id == self.user.id:
            return

        if message.content.startswith('/hello'):
            await message.reply('Hello!', mention_author=True)
            print("[+] Bot replied to user!!")

        if message.content.startswith('/embed'):
            embed = discord.Embed(title="Quote Of The Day", description="submitted by:\n \- user",
                                  color=0x8aff97)  # // title and other shiz
            embed.add_field(
                name="the darker the night, the brighter the stars, the deeper the grief, the closer is god", value="",
                inline=True)  # // here comes the acutal quote /// value = "" must be there for some reason
            embed.set_footer(text="- Apollon Maykov")  # // put here the authors name

            await message.reply(embed=embed)
            print("[+] created embed")


intents = discord.Intents.default()
intents.messages = True
client = MyClient(intents=intents)


@client.tree.command()
async def ping(interaction: discord.Interaction):
    """
    Says pong!
    """
    embed = discord.Embed(title="Pong!", description=f"Latency: {round(client.latency, 2)}")
    await interaction.response.send_message(embed=embed)


client.run(os.getenv("TOKEN"))
