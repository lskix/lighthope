import os
import time

import discord
from dotenv import load_dotenv

from wit import Wit

load_dotenv()
DSC_TOKEN = os.getenv('DISCORD_TOKEN')
WIT_TOKEN = os.getenv('WIT_TOKEN')


RCHANNEL_ID = "catras-diary"
DELAY_BASE = 5

dscClient = discord.Client()


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
    logChannel = dscClient.get_channel(739170928805806202)
    await logChannel.send(string)

@dscClient.event
async def on_message(message):
    if message.author == dscClient.user:
        return
    if message.channel.name == "catras-diary":
        archiveChannel = dscClient.get_channel(738415449582075924)
        await archiveChannel.send(message.author.name + ": " + message.content)
        time.sleep(calculateDelayTime(message.content))
        await message.delete()

    if "lighthope" in message.content:
        response = witClient.message(msg=message.content)
        await handle_message(response, message.channel)

@dscClient.event
async def on_ready():
    await log("Lighthope OS is starting...")

def first_trait_value(traits, trait):
    """
    Returns first trait value
    """
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val


async def handle_message(response, channel):
    """
    Customizes our response to the message and sends it
    """
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings = first_trait_value(response['traits'], 'wit$greetings')
    if greetings:
        text = "hello!"
    else:
        text = "Query not recognised"
    # send message
    await channel.send(text)



# Setup Wit Client
witClient = Wit(access_token=WIT_TOKEN)

dscClient.run(DSC_TOKEN)
