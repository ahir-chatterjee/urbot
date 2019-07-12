#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:56:21 2019

@author: ahir.chatterjee
"""

import discord
from discord.ext import commands
import os
import leaderboard
import requests
import json

token = "NTk4OTMxNzk1MzMyODI1MTA4.XSd1tQ.iHi4OcrwWwMqeJ7-Ja67o4AWNkw"
base = "https://discordapp.com/api"
tQuery = "?token=" + token

client = discord.Client()
bot = commands.Bot(command_prefix='!', description="eepa")

async def checkCommands(message):
    command = message.content[1:]
    print(command + " detected")
    channel = message.channel
    msg = ""
    update = False
    if(command == "d4"):
        msg = "<@103645519091355648> is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)
    if(command == "updateLeaderboard"):
        #leaderboard.runLeaderboard()
        endpoint = "channels/599280347087241228/messages"
        requests.get(base)
        command = "leaderboard"
        update = True
    if(command == "leaderboard"):
#        curPath = os.path.dirname(__file__)
#        path = os.path.relpath('../riot-scripts/currentLeaderboard.txt',curPath)
        lBoard = open("currentLeaderboard.txt",'r')
        msg += "**Updated every Sunday at 9 PM Central Time**\n"
        msg += "```\n"
        msg += "Rank Name       Score       Summoner Name     Changes\n"
        for line in lBoard:
            msg += line
        msg += "```\n"
        msg += """Want to get your name up here? Do you have another account you want linked to this leaderboard? Message <@103645519091355648> and get it updated."""
        if(not update):
            await channel.send(msg)
    if(command == "triumph"):
        msg = ":triumph:"
        print(message)
        print(message.author.id)
        if(message.author.id != 103645519091355648):
            msg = "You do not have permission for this command."
        await channel.send(msg)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if message.content.startswith('Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('!'):
        await checkCommands(message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.change_presence(activity=discord.Game("eepa"))
    
#@bot.command()
#async def d4(ctx):
#    await ctx.send("<103645519091355648> is a Hardstuck D4 Urgot Onetrick")

client.run(token)