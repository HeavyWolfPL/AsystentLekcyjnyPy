import asyncio
from asyncio.tasks import wait_for
import discord
from discord import channel
from discord.ext import commands
import json
import time
import os
import re
import json
import requests
from urllib.parse import urlparse
from vulcan import Account
from vulcan import Keystore
from vulcan import Vulcan


# Get configuration.json
with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    # Dziennik
    dziennik_enabled = data["dziennik_enabled"]
    if dziennik_enabled:
        dziennikToken = data["dziennikToken"]
        dziennikSymbol = data["dziennikSymbol"]
        dziennikPIN = data["dziennikPIN"]
        keystoreDziennik = Keystore.create(device_model="Python Vulcan API")
        dziennikAccount = Account.register(keystoreDziennik, dziennikToken, dziennikSymbol, dziennikPIN)
        dziennikClient = Vulcan(keystoreDziennik, dziennikAccount)

if token == "TOKEN":
    print("Błędny token.")
    exit()

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
# The bot
bot = commands.Bot(prefix, intents = intents)

# Load cogs1
#if __name__ == '__main__':
#	for filename in os.listdir("Cogs"):
#		if filename.endswith(".py"):
#			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"""Zalogowano jako {bot.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="lekcje"))


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("!shutdown" or "!off" or "!zabij"):
                await message.channel.send("Okej")
                exit()
        if message.content.startswith("!ping"):
                before = time.monotonic()
                msg = await message.channel.send("🏓 Pong !")
                ping = (time.monotonic() - before) * 1000
                await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")
        if message.content.startswith("!plan" or "!planlekcji"):
            if dziennik_enabled == "true":
                await message.channel.send("True")  
                luckynumber = dziennikClient.data.get_lucky_number()
                print(luckynumber)              
            else:
                await message.channel.send("Moduł dziennika jest wyłączony.")
            await message.channel.send("Wczytuję plan [debug]")
        

@bot.event
async def when_mentioned(bot, message):
    if message.author.id != bot.user.id:
        await message.channel.send(f"Hej {message.author}, mój prefiks to {prefix}.")

#@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Witaj {member.mention}.'.format(member))

#@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel(596428386100838400)
    await channel.send(f'Reakcja - {reaction}. User - {user}')

@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(847040167353122856)
    await channel.send(ctx) 
    await channel.send(error)
    raise error

bot.run(token)