import os
import discord

from src.status_bot import StatusBot

# Set intents
intents = discord.Intents.default()

# Create bot object
status_bot = StatusBot(intents = intents)

# Start bot
status_bot.run(os.getenv("DISCORD_BOT_TOKEN"))