import os
import signal
import discord

from src.status_bot import StatusBot

if __name__ == '__main__':
    # Set intents
    intents = discord.Intents.default()

    # Create bot object
    status_bot = StatusBot(intents=intents)

    def shutdown_bot(signum, frame):
        print(f"Signal {signum} received, closing bot...")
        status_bot.loop.create_task(status_bot.close())

    signal.signal(signal.SIGTERM, shutdown_bot)
    signal.signal(signal.SIGINT, shutdown_bot)

    # Start bot
    status_bot.run(os.getenv("DISCORD_BOT_TOKEN"))