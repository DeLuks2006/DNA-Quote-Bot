import os
import discord
from bot.client import MyClient
from bot.database import Database, create_session_maker


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    DB_URI = "sqlite:///data/database.db"

    intents = discord.Intents.default()
    intents.messages = True
    db = Database(sessionmaker=create_session_maker(DB_URI))
    bot = MyClient(intents=intents, command_prefix="/", db=db)  # Prefix doesn't matter here
    bot.run(TOKEN)
