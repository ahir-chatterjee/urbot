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
import random

token = "NTk4OTMxNzk1MzMyODI1MTA4.XSd1tQ.iHi4OcrwWwMqeJ7-Ja67o4AWNkw"
base = "https://discordapp.com/api"
tQuery = "?token=" + token

client = discord.Client()
bot = commands.Bot(command_prefix='!', description="eepa")

idDict = {"Ahir" : 103645519091355648,
          "Urbot" : 598931795332825108,
          "Bo" : 117344493895811076,
          "Faiz" : 181294520388943872,
          "Shubham" : 504137209926909982,
          "Khayame" : 116037813757149186,
          "Peter" : 103660164585918464,
          "Hwang" : 144319918681227264,
          "Jonathan" : 210502732300288000,
          "Denis" : 277787166388518922,
          "Andy" : 197405594754351105,
          "Austin" : 148388944386588672,
          "Vincent" : 162728387348135936,
          "Bruce" : 267064851636027396,
          "David" : 131673939930775552,
          "Ty" : 191247351162077184,
          "Louis" : 130920011429707776,
          "Gavin" : 229059675444740096,
          "Caleb" : 264566173843193857,
          "Dustin" : 167829909052325899,
          "Michael" : 114560575232671745,
          "Ben" : 324609016175263744,
          "Mason" : 121820913875288064,
          "Clayton" : 164190805924380673,
          "Paul" : 214602165552021505,
          "Isaac" : 118119026747506690,
          "Raymond" : 336683086924218379,
          "Gary" : 166038505544351744,
          "Tailer" : 153021888656834560,
          "Tanner" : 337791672614125578,
          "Vic" : 137716762316636160,
          "Kevin" : 174326208778076162,
          "James" : 192452145868570624,
          "Zane" : 136636558479589378,
          "Nabil" : 299727617379008512
          }

inhouseCaptains = ["",""]
picksBeforeSwap = [0]
pickingTeam = [0]
inhouseTeams = [[],[]]
inhousePlayers = []

async def checkCommands(message):
    command = message.content[1:].split(" ")
    base = command[0]
    print(base + " detected")
    #print(message.guild.text_channels)
    guild = message.guild
    channel = message.channel
    msg = ""
    
    #enter switchcase for commands
    if(base == "d4"):
        msg = "<@103645519091355648> is a Hardstuck D4 Urgot Onetrick"
        await channel.send(msg)
    elif(base == "leaderboard"):
        if(await authCheck(message,channel,[idDict["Ahir"]])):
            leaderboard.runLeaderboard()
            await postLeaderboard(guild)
    elif(base == "triumph"):
        if(await authCheck(message,channel,[idDict["Ahir"]])):
            msg = ":triumph:"
            msgToEdit = await channel.fetch_message("600340498955370526")
            await msgToEdit.edit(content="test")
            await channel.send(msg)
    elif(base == "inhouse"):
        if(len(command) != 11):
            await channel.send("Please choose exactly 10 players for the inhouse.")
        elif(await authCheck(message,channel,[idDict["Ahir"]])):
            for index in range(1,len(command)):
                pId = command[index][2:len(command[index])-1]
                if(pId.find('!') > -1):
                    pId = pId[1:]
                inhousePlayers.append(getNameById(pId))
            await assignCaptains(channel)
            await sendRemainingPlayers(channel)
    elif(base == "pick"):
        if(activeInhouse()):
            if(await authCheck(message,channel,[idDict["Ahir"],idDict[inhouseCaptains[0]],idDict[inhouseCaptains[1]]])):
                if(len(inhouseTeams[0]) == 1 and len(inhouseTeams[1]) == 1):
                    picksBeforeSwap[0] = 1
                
                if(picksBeforeSwap[0] == 0):
                    picksBeforeSwap[0] = 2
                    if(pickingTeam[0] == 0):
                        pickingTeam[0] = 1
                    else:
                        pickingTeam[0] = 0
                    
                if(picksBeforeSwap[0] == 1 and len(command) > 2):
                    await channel.send("You can only pick 1 more player.")
                elif(len(command) > 3):
                    await channel.send("You can only pick 2 players in a round.")
                else:
                    picks = [command[1]]
                    if(len(command) == 3):
                        picks.append(command[2])
                    for pick in picks:
                        if(pick in inhousePlayers):
                            inhouseTeams[pickingTeam[0]].append(pick)
                            picksBeforeSwap[0] -= 1
                            inhousePlayers.remove(pick)
                        else:
                            await channel.send("\"" + pick + "\"" + " is not a valid player.")
                    await sendTeams(channel)
                    if(activeInhouse()):
                        await sendRemainingPlayers(channel)
                    else:
                        resetInhouse()
        else:
            await channel.send("Run !inhouse before picking players.")
            
def resetInhouse():
    inhouseCaptains[0] = ""
    inhouseCaptains[1] = ""
    picksBeforeSwap[0] = 0
    pickingTeam[0] = 0
    inhouseTeams[0] = []
    inhouseTeams[1] = []
    inhousePlayers.clear()
            
async def sendTeams(channel):
    for team in inhouseTeams:
        msg = "Team " + team[0] + ": "
        for player in team:
            msg += player + ", "
        msg = msg[:len(msg)-2]
        await channel.send(msg)
            
async def sendRemainingPlayers(channel):
    msg = "Remaining players: "
    for player in inhousePlayers:
        #msg += "<@" + (str)(idDict[player]) + ">, "
        msg += player + ", "
    msg = msg[:len(msg)-2]
    await channel.send(msg)
            
def activeInhouse():
    if(not len(inhousePlayers) == 0):
        return True
    return False
                
def getNameById(pId):
    for name in idDict:
        if((str)(idDict[name]) == pId):
            return name
        
async def assignCaptains(channel):
    lBoard = open("currentLeaderboard.txt",'r')
    print("assignCaptains")
    for line in lBoard:
        for player in inhousePlayers:
            if(line.find(player) > -1):
                if(inhouseCaptains[0] == ""):
                    inhouseCaptains[0] = player
                    inhouseTeams[0].append(player)
                    print("captain1 == " + player)
                    pick = "first pick."
                    oPick = "second round picks and side selection."
                    if(random.random() > .5):
                        temp = pick
                        pick = oPick
                        oPick = temp
                    await channel.send(player + " is a team captain and gets " + pick)
                elif(inhouseCaptains[1] == ""):
                    inhouseCaptains[1] = player
                    inhouseTeams[1].append(player)
                    print("captain2 == " + player)
                    await channel.send(player + " is a team captain and gets " + oPick)
    inhousePlayers.remove(inhouseCaptains[0])
    inhousePlayers.remove(inhouseCaptains[1])
    lBoard.close()
            
async def authCheck(message,channel,authorizedUsers):
    if(message.author.id not in authorizedUsers):
        await channel.send("You do not have permission for this command.")
        return False
    return True
            
async def postLeaderboard(guild):
    msg = ""
    lChannel = ""
    for c in guild.text_channels:
        if(c.name == "leaderboard"):
            lChannel = c
    lMessage = "600350921905668100"
    for m in await lChannel.history().flatten():
        if((str)(m.author.id) == "598931795332825108"):
            lMessage = m.id
    lBoard = open("currentLeaderboard.txt",'r')
    msg += "**Updated every Sunday at 9 PM Central Time**\n"
    msg += "```\n"
    msg += "Rank Name       Score       Summoner Name     Changes\n"
    for line in lBoard:
        msg += line
    msg += "```\n"
    msg += """Want to get your name up here? Do you have another account you want linked to this leaderboard? Message <@103645519091355648> and get it updated."""
    await (await lChannel.fetch_message(lMessage)).edit(content=msg)

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