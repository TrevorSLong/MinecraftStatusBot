#!/usr/bin/python3.4
#Minecraft Status Bot
#-------------------------------------------------
#Discord bot for showing a Minecraft servers status
#Created by DroTron (Trevor L)
#https://github.com/TrevorSLong/MinecraftStatusBot
#-------------------------------------------------
#This code may be used to help you build your own bot or to run on your own server
#Do not use my code for profit
#For help go to https://realpython.com/how-to-make-a-discord-bot-python/
#https://betterprogramming.pub/how-to-make-discord-bot-commands-in-python-2cae39cbfd55
#Have fun!
#-------------------------------------------------

##############Import Libraries###########################################################################################
import discord
import os
import time
import smtplib
import asyncio
import logging
import random
import json
import dbl
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands, tasks
from discord import Member
from discord import User
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import Bot, guild_only

from discord_slash import SlashCommand, SlashContext #Importing slash command library
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Grabs bot token from .env file
print("Logging in with Bot Token " + TOKEN)
SERVER = os.getenv('MCSERVER') #Grabs bot token from .env file
print("Pinging server: " + SERVER)

bot = commands.Bot(command_prefix='$') #, intents=discord.Intents.all()) #declare intents for bot
slash = SlashCommand(bot, sync_commands=True) #Declares command prefix

server = MinecraftServer.lookup(SERVER)
status = server.status()
print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
    
##############Changes bot status (working)###########################################################################################
async def background_task():
    
    while True:
        time = 120 # 86400
        server = MinecraftServer.lookup(SERVER)
        status = server.status()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{0} players play online!".format(status.players.online, status.latency)))
        await asyncio.sleep(time)
        


##############Reponds to ping (working)########################################################################################################
@slash.slash(
	description="Responds with Pong and the bots server latency", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
)
async def ping(ctx:SlashContext):
	await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.


##############Responds to mcping###########################################################################################
@slash.slash(
	description="Responds with player count and server latency", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
)
async def serverstatus(ctx:SlashContext):
    server = MinecraftServer.lookup(SERVER)
    status = server.status()

    await ctx.send("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency)) # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.

bot.loop.create_task(background_task())
bot.run(TOKEN)
