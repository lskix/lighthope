import os
import time

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

RCHANNEL_ID = "catras-diary"
DELAY_BASE = 5

client = discord.Client()

def calculateDelayTime(text):
    totalDelay = DELAY_BASE
    for x in len(text):
        if text[x] == " ":
            totalDelay += 1
    return totalDelay

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name== "catras-diary":
        time.sleep(calculateDelayTime(message.content))
        await message.delete()

client.run(TOKEN)
