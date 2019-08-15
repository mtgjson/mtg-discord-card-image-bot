#!/usr/bin/python3
import os
import discord
from discord.ext import commands
import requests
import json

trigger = '!card'
client = discord.Client()

# Look up the card in Scryfall
def getCard(card):
    # Use Scryfall to get the card by fuzzy lookup
    response = requests.get(
        'https://api.scryfall.com/cards/named?fuzzy=' + card)
    response = response.json()
    return response

# On client connect
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# On client message
@client.event
async def on_message(message):
    # Ignore message if this bot sent the message
    if ((message.author == client.user) or (message.author.bot)) or not (message.content.startswith(trigger)):
        return
    cardName = message.content.split(trigger)[1]
    if (cardName):
        retrievedCard = getCard(cardName)

        # Success, we found a card that didnt 404
        if 'image_uris' in retrievedCard:
            await message.channel.send(retrievedCard['image_uris']['border_crop'])
            return
        # Failed to find a card so send the error message
        else:
            await message.channel.send(retrievedCard['details'])
            return
    else:
        await message.channel.send('Please supply a card name!')

client.run(os.environ['BOT_TOKEN'])
# https://discordapp.com/oauth2/authorize?&client_id=611462068716961813&scope=bot&permissions=55296
