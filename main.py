import os
import time

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

RCHANNEL_ID = "catras-diary"
DELAY_TIME = 2

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name== "catras-diary":
        time.sleep(DELAY_TIME)
        await message.delete()

client.run(TOKEN)
