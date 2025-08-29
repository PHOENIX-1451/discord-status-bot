import os
import discord

from src.status_bot import StatusBot

if __name__ == "__main__":
    # Set intents
    intents = discord.Intents.default()

    # Create bot object
    status_bot = StatusBot(intents = intents)

    # Start bot
    status_bot.run(os.getenv("DISCORD_BOT_TOKEN"))