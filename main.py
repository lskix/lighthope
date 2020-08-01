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
    for x in text:
        if x == " ":
            totalDelay += 1
    if totalDelay > 30:
        totalDelay = 30
    print(totalDelay)
    return totalDelay



async def log(string):
    logChannel = client.get_channel(739170928805806202)
    await logChannel.send(string)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name == "catras-diary":
        archiveChannel = client.get_channel(738415449582075924)
        await archiveChannel.send(message.author.name + ": " + message.content)
        time.sleep(calculateDelayTime(message.content))
        await message.delete()

@client.event
async def on_ready():
    await log("Lighthope OS is starting...")

client.run(TOKEN)
