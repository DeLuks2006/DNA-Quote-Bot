import discord
from discord import app_commands
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        """
        Says pong!
        """
        embed = discord.Embed(title="Pong!", description=f"Latency: {round(self.bot.latency, 2)}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def embed(self, interaction: discord.Interaction) -> None:
        """
        Sends an example embed, thanks Deluks
        """
        embed = discord.Embed(title="Quote Of The Day", description="submitted by:\n \- user",
                              color=0x8aff97)  # // title and other shiz
        embed.add_field(
            name="the darker the night, the brighter the stars, the deeper the grief, the closer is god", value="",
            inline=True)  # // here comes the acutal quote /// value = "" must be there for some reason
        embed.set_footer(text="- Apollon Maykov")  # // put here the authors name
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Test(bot))
