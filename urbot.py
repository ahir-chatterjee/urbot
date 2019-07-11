#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:56:21 2019

@author: ahir.chatterjee
"""

import discord

import discord

TOKEN = 'NTk4OTMxNzk1MzMyODI1MTA4.XSd1tQ.iHi4OcrwWwMqeJ7-Ja67o4AWNkw'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)