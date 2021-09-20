import os
import discord
import time
import json
from vulcan import Account
from vulcan import Keystore
from vulcan import Vulcan
from discord.ext import commands


# Get configuration.json
with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    owner_id = data["ownerID"]
    # Dziennik
    dziennik_enabled = data["dziennik_enabled"]
    if dziennik_enabled:
        dziennikToken = data["dziennikToken"]
        dziennikSymbol = data["dziennikSymbol"]
        dziennikPin = data["dziennikPIN"]

if token == "TOKEN":
    print("Błędny token.")
    exit()

def __init__(self, bot):
    self.bot = bot
    self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
# The bot
bot = commands.Bot(command_prefix='!', intents = intents)

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



@bot.event
async def on_ready():
    print(f"""Zalogowano jako {bot.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="lekcje"))


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
        if message.content.startswith("!setup") and message.author.id == owner_id:
            dziennikKeystore = Keystore.create(device_model="Python Vulcan API")
            with open("key-config.json", "w") as f:
                # use one of the options below:
                # write a formatted JSON representation
                f.write(dziennikKeystore.as_json)
            dziennikAccount = await Account.register(dziennikKeystore, dziennikToken, dziennikSymbol, dziennikPin)
            with open("acc-config.json", "w") as f:
                # write a formatted JSON representation
                f.write(dziennikAccount.as_json)
            await message.channel.send("Account and Keystore created.")
        # if dziennik_enabled:
        #     #Frekwencja
        #     if message.content.startswith("!frekwencja"):
        #         await message.channel.send(f'Frekwencja: \n```\n{await get_frekwencja()}```')
        #     #Szczęśliwy numerek
        #     if message.content.startswith("!numerek" or "!szczęśliwynumerek" or "!szczesliwynumerek"):
        #         await message.channel.send(f'Szczęśliwy numerek to `{await get_luckynumber()}`')
        if not dziennik_enabled:
            await message.channel.send("Moduł dziennika jest wyłączony.")

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