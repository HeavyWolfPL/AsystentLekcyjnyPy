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

# Get configuration.json
with open("config.json", "r") as config: 
	data = json.load(config)
	prefix = data["prefix"]
        token = data["token"]


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
	print(f"Zalogowano jako {bot.user}")
	print(f"Discord.py - {discord.__version__}")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name ="Przestworzach"))


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("!shutdown"):
		        await message.channel.send("Okej")
		        exit()
        if message.content.startswith("!ping"):
                before = time.monotonic()
                msg = await message.channel.send("🏓 Pong !")
                ping = (time.monotonic() - before) * 1000
                await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")
        if message.content.startswith("!report"):
            channel = message.channel
            def is_author(message):
                return message.author.id == msg.author.id
            await channel.send(f""""Zanim rozpoczniesz pisać zgłoszenie, przeczytaj instrukcję **ze zrozumieniem** !
                        ```md
* Jeden gracz jednocześnie może składać skargę.

* Wykonuj polecenia bota, nie obchodzi cię wzór!

* Jeśli nie posiadasz dowodu, żaden problem. Nie każde przewinienie wymaga dowodu.

* Bot czeka na każdą odpowiedź minutę.

* Przeczytaj przypięte wiadomości zanim zaczniesz !

* By anulować składanie skargi poczekaj 60 sekund od ostatniej odpowiedzi.

# Administracja ma prawo odrzucić skargę i zabrać dostęp do jej składania.```

- - - - - - - - - - - - - - - -

Czy zapoznałeś się z instrukcją? Wpisz _*Tak*_ lub _*Nie*_.

- - - - - - - - - - - - - - - -""")
            try:
                msg = await bot.wait_for('message', check=lambda msg: msg.author.id == message.author.id, timeout=60)
            except asyncio.TimeoutError:
                return await channel.send('Twój czas minął.')
            if msg.content.lower() == "nie":
                return
            elif msg.content.lower() == "tak":
                await channel.send("Podaj profil gracza.")
            else:
                await channel.send("Nie wybrałeś(-aś) poprawnej odpowiedzi. Wpisz komendę od nowa.")
                return
            try:
                msg = await bot.wait_for('message', check=is_author, timeout=60)
            except asyncio.TimeoutError:
                return await channel.send('Twój czas minął.')
            steamlink = re.compile(r'(?:https?:\/\/)?steamcommunity\.com\/(?:profiles|id)\/[a-zA-Z0-9]+')
            steamprofile = steamlink.search(msg.content)
            if not steamprofile:
                await channel.send("Podałeś(-aś) link który nie prowadzi do profilu")
            if steamprofile:
                steamprofile = steamprofile.group()
                await channel.send(f"Czy <{steamprofile}> to poprawny link?")
            try:
                msg = await bot.wait_for('message', check=is_author, timeout=60)
            except asyncio.TimeoutError:
                return await channel.send('Twój czas minął.')
            if msg.content.lower() == "tak":
                await channel.send("Podaj powód zgłoszenia.")
            elif msg.content.lower() == "nie":
                return
            else:
                await channel.send("Nie wybrałeś(-aś) poprawnej odpowiedzi. Wpisz komendę od nowa.")
                return
            try:
                powodmsg = await bot.wait_for('message', check=is_author, timeout=60)
            except asyncio.TimeoutError:
                return await channel.send('Twój czas minął.')
            powod = powodmsg.content
            steamvanityurl = urlparse(f'{steamprofile}')
            steamvanityurl = steamvanityurl.path.replace('/id/', '')
            steamid = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={steamapi}&vanityurl={steamvanityurl}").json()
            steamid = steamid['response']
            steamid = steamid['steamid']
            steamplayer = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v1/?key={steamapi}&steamids={steamid}").json()
            steamplayer = steamplayer['response']
            steamplayer = steamplayer['players']
            steamplayer = steamplayer['player'][0]
            steamnick = steamplayer['personaname']
            steamavatar = steamplayer['avatarfull']
            logchannel = bot.get_channel(847835852398395452)
            logmessages = await logchannel.history(limit=100, oldest_first=True).flatten()
            if logmessages is None:
                wizyta = "Brak"
            for logmessage in logmessages:
                if steamid in logmessage.content:
                    wizyta = logmessage.created_at
            #wizyta = logmessage.created_at
            wizyta_godz = wizyta.strftime("%H")
            wizyta_godz = int(wizyta_godz) + int(2)
            wizyta_reszta = wizyta.strftime(":%M  %d.%m.%Y")
            wizyta = f"{wizyta_godz}{wizyta_reszta}"
            embed=discord.Embed(title="ThemePark", url="https://polishemergencyv.com/", description=f"**Zgłaszający** - <@{message.author.id}>", color=0xff0000)
            embed.set_author(name="Nowa skarga")
            embed.set_thumbnail(url=f"{steamavatar}")
            embed.add_field(name="Nick", value=f"{steamnick}", inline=True)
            embed.add_field(name="SteamID", value=f"{steamid}", inline=True)
            embed.add_field(name="Profil Steam", value=f"{steamprofile}", inline=False)
            embed.add_field(name="Powód", value=f"{powod}", inline=False)
            embed.add_field(name="Ostatnia wizyta", value=f"{wizyta}", inline=False)
            embed.set_footer(text="ThemePark")
            await channel.send(embed=embed)
            skargichannel = bot.get_channel(847836632098799638)
            await skargichannel.send(embed=embed)
            await channel.send(f"""- - - - - - - - - - - - - - - -

Czy skarga się zgadza? (Wpisz *Tak* lub *Nie*)

- - - - - - - - - - - - - - - -""")
            try:
                msg = await bot.wait_for('message', check=is_author, timeout=60)
            except asyncio.TimeoutError:
                return await channel.send('Twój czas minął.')
            if msg.content.lower() == "tak":
                await channel.send("Skarga została przyjęta.")
            elif msg.content.lower() == "nie":
                return
            else:
                await channel.send("Nie wybrałeś(-aś) poprawnej odpowiedzi. Wpisz komendę od nowa.")
                return


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Witaj {member.mention}.'.format(member))

@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel(596428386100838400)
    await channel.send(f'Reakcja - {reaction}. User - {user}')


async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("!zabij" or "!shutdown" or "!s" or "!off"):
		        await message.channel.send("Okej")
		        exit()

async def on_message(message):
    if message.author.id != bot.user.id:
        if message.content.startswith("!ping"):
                before = time.monotonic()
                msg = await message.channel.send("🏓 Pong !")
                ping = (time.monotonic() - before) * 1000
                await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")

@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(847040167353122856)
    await channel.send(ctx) 
    await channel.send(error)
    raise error

bot.run(token)