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
        # await handle_message(response, message.channel)


@dscClient.event
async def on_ready():
    await log("Lighthope OS is starting...")


def first_value(traits, trait):
    if trait not in traits:
        return None
    val = traits[trait][0]['value']
    if not val:
        return None
    return val


async def handle_message(response, channel):
    greetings = first_value(response['traits'], 'wit$greetings')
    getInformation = first_value(response['traits'], 'getInformation')
    text = "An error has occured in the Light Hopw operating system. Please contact Evelyn."
    if greetings:
        text = "hello!"
    elif getInformation:
        infoToGet = first_value(response['entities'], 'infoToGet')
        print("A request for info was made")
    else:
        text = "Query not recognised"

    await channel.send(text)


witClient = Wit(access_token=WIT_TOKEN)

dscClient.run(DSC_TOKEN)
