#!/usr/bin/python3
import os
import discord
import requests
from requests import HTTPError

trigger = '!card'
client = discord.Client()


# Look up the card in Scryfall
def get_card(card):
    # Use Scryfall to get the card by fuzzy lookup
    response = requests.get('https://api.scryfall.com/cards/named?fuzzy={card}'.format(card=card))
    response.raise_for_status()
    response = response.json()
    return response


# On client connect
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client.user))


# On client message
@client.event
async def on_message(message):
    # Ignore message if this bot sent the message
    if (message.author == client.user or message.author.bot) or not message.content.startswith(trigger):
        return

    card_name = message.content.split(trigger)[1]
    if not card_name:
        return await message.channel.send('Please supply a card name!')

    retrieved_card = get_card(card_name)

    # Success, we found a card that didnt 404
    try:
        return await message.channel.send(retrieved_card['image_uris']['border_crop'])
    # Failed to find a card so send the error message
    except HTTPError:
        return await message.channel.send(retrieved_card['details'])


client.run(os.environ['BOT_TOKEN'])
# https://discordapp.com/oauth2/authorize?&client_id=611462068716961813&scope=bot&permissions=55296
