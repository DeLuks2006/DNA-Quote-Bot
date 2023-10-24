import discord
from discord.ext import commands

# [i] - info
# [-] - shits going down (error)
# [+] - everythin alr

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'[i] Logged on as {self.user}!')

    async def on_message(self, message):
        # make the bot not talk to it self
        if message.author.id == self.user.id:
            return

        if message.content.startswith('/hello'):
            await message.reply('Hello!', mention_author = True)
            print("[+] Bot replied to user!!")

        if message.content.startswith('/embed'):
            embed = discord.Embed(title="Quote Of The Day", description = "submitted by:\n \- user",color=0x8aff97) # // title and other shiz
            embed.add_field(name="the darker the night, the brighter the stars, the deeper the grief, the closer is god", value = "", inline = True) # // here comes the acutal quote /// value = "" must be there for some reason
            embed.set_footer(text="- Apollon Maykov") # // put here the authors name

            await message.reply(embed=embed)
            print("[+] created embed")

intents = discord.Intents.default()
intents.messages = True

client = MyClient(intents=intents)
client.run('')