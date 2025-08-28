import discord

class StatusBot(discord.Client):
    async def on_ready(self):
        print('Status Bot Ready')

