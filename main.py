import os
import time

import wikiFunctions

import discord
from dotenv import load_dotenv

from profanity_check import predict_prob

global blacklist

from wit import Wit

global started

load_dotenv()
DSC_TOKEN = os.getenv('DISCORD_TOKEN')
WIT_TOKEN = os.getenv('WIT_TOKEN')

RCHANNEL_ID = "catras-diary"
DELAY_BASE = 5

dscClient = discord.Client()

with open("blacklist.lhd", 'r') as dataObject:
    blacklist = dataObject.readlines()

def calculateDelayTime(text):
    totalDelay = DELAY_BASE
    for x in text:
        if x == " ":
            totalDelay += 1
    if totalDelay > 30:
        totalDelay = 30
    print(totalDelay)
    return totalDelay

for word in blacklist:
    print(word + " | " + word.replace(" ", ""))

async def log(string):
    logChannel = dscClient.get_channel(739170928805806202)
    await logChannel.send(string)

def messageContainsTriggerWord(message):
    messageLower = " " + message.content.lower()
    for word in blacklist:
        if word in messageLower or word.replace('\n', "") in messageLower or messageLower.startswith(word) or messageLower.endswith(word) or messageLower == word:
            return True
    return False

async def deleteBlacklistedMessage(message):
    await message.delete()
    await message.channel.send(message.author.mention + ", your message was deleted for containing a blacklisted/profane word.")

@dscClient.event
async def on_message(message):
    if message.author == dscClient.user:
        return
    print(str(predict_prob([message.content])[0]) + " " + str(message.guild))
    if predict_prob([message.content])[0] > .78 or messageContainsTriggerWord(message):

        await deleteBlacklistedMessage(message)

    if message.channel.name == "catras-diary":
        archiveChannel = dscClient.get_channel(738415449582075924)
        await archiveChannel.send(message.author.name + ": " + message.content)
        time.sleep(calculateDelayTime(message.content))
        try:
            await message.delete()
        except discord.errors.NotFound:
            await log("Someone deleted a message before me. Sneaky. System may reboot, this is normal behavior.")
    elif message.content.lower().startswith("lighthope") or message.content.lower().endswith("lighthope"):
        response = witClient.message(msg=message.content)
        await handle_message(response, message.channel)



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
    createSpiders = first_value(response['traits'], 'createSpiders')
    text = "An error has occured in the Light Hope operating system. Please contact Evelyn."
    if greetings:
        text = "hello!"
    elif createSpiders:
        text = ":spider: Are spiders useful?"
    elif getInformation:
        infoToGet = first_value(response['entities'], 'infoToGet:infoToGet')
        print("A request for info on " +infoToGet+"was made")
        if "evelyn" in infoToGet or "evie" in infoToGet:
            text = "Evie is the programmer who created me!"
        else:
            snippet = wikiFunctions.searchWiki(infoToGet)
            if snippet != "":
                text = snippet
            else:
                text = "That information has not yet loaded"
    else:
        text = "Query not recognised"

    await channel.send(text)


witClient = Wit(access_token=WIT_TOKEN)

dscClient.run(DSC_TOKEN)
