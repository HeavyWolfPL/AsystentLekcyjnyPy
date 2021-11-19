import datetime
import os
import discord
import time
import json
from vulcan import Account
from vulcan import Keystore
from vulcan import Vulcan
from discord.ext import commands
from discord.ext.tasks import loop
from asyncio import sleep


# Get configuration.json
with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    owner_id = data["ownerID"]

if token == "TOKEN":
    print("Ustaw token bota!")
    exit()

def __init__(self, bot):
    self.bot = bot
    self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
# The bot
bot = commands.Bot(command_prefix=str(prefix), intents = intents)

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"[Cogs] Loaded - {filename[:-3]}")
    for filename in os.listdir("cogs/dziennik"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.dziennik.{filename[:-3]}")
            print(f"[Dziennik Cogs] Loaded - {filename[:-3]}")
        

# cogss = bot.get_cog('PlanLekcji')
# cmds = cogss.get_commands()
# print([c.name for c in cmds])

async def config_validator():
    with open("config.json", "r") as config: 
        data = json.load(config)
        dziennik_mode = data["dziennik_mode"]
    if dziennik_mode not in ["user", "global", "both"]:
        return False
    else:
        return True
    

@bot.event
async def on_ready():
    print(f"""Zalogowano jako {bot.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="lekcje"))
    x = await config_validator()
    if (x == False):
        print("Konfig zawiera nieodpowiedni `dziennik_mode`. Wybierz jeden z trzech dostępnych: \n- user (każdy użytkownik musi dodać swoje tokeny) \n- global (administrator bota dodaje swój token) \n- both (gdy użytkownik nie posiada dodanego własnego tokenu, użyje tokenu administratora*)\n\n* Obowiązują ograniczenia co do komend.")
        # await ErrorHandler.Report(bot, f"Konfig zawiera nieodpowiedni `dziennik_mode`. Wybierz jeden z trzech dostępnych: \n- user (każdy użytkownik musi dodać swoje tokeny) \n- global (administrator bota dodaje swój token) \n- both (gdy użytkownik nie posiada dodanego własnego tokenu, użyje tokenu administratora*)\n\n* Obowiązują ograniczenia co do komend.", "Validator Konfigu", "69")
        exit()
    else:
        print("[Validator Konfigu] Brak błędów.")
    

@bot.listen('on_message')
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("!off"):
                await message.channel.send("Okej")
                exit()
        if message.content.startswith("!ping"):
                before = time.monotonic()
                msg = await message.channel.send("🏓 Pong !")
                ping = (time.monotonic() - before) * 1000
                await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")
        

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
    print(ctx)
    print(error)
    # await ErrorHandler.Report(bot, f"{ctx}", "on_command_error - Part 1", "X")
    # await ErrorHandler.Report(bot, f"{error}", "on_command_error - Part 2", "X")
    raise error

bot.run(token)