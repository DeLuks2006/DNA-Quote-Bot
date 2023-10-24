import discord

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

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author = True)
            print("[+] Bot replied to user!!")

intents = discord.Intents.default()
intents.messages = True

client = MyClient(intents=intents)
client.run('MTE2NjQyODc0NDE2OTMxMjM0OA.Gqkeie.s1ZIHVCV0kXFfgsp2uXy6KgFfOxEQHBM5bJzog')