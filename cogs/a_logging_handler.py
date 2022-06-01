import discord, json, datetime, logging, os
from pathlib import Path
from discord.ext import commands

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    debug = data["debug"]

class ErrorHandler(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

    # async def Report(self, error, cog, line):
    #     with open("config.json", "r") as config: 
    #         data = json.load(config)
    #         error_channel = data["errorChannel"]
    #         footer = data["footerCopyright"]
    #         footer_img = data["footerCopyrightImage"]
    #     print(self)
    #     channel = self.bot.get_channel(847040167353122856)
    #     embed=discord.Embed(title=f"{cog} - Linia {line}", description=error, color=0xff0000, timestamp=datetime.datetime.now())
    #     embed.set_author(name="PolishEmergencyV")
    #     embed.set_footer(text=footer, icon_url=footer_img)
    #     await channel.send(embed=embed)
    #     print(f"[ErrorHandler - {cog} ({line})] Wystąpił błąd: {error}")

class Logger(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

    logs_dir = Path("./logs")
    if (logs_dir.exists() == False) or (logs_dir.is_dir() == False):
        logs_dir.mkdir()
    logs_dir = Path("./logs/discord")
    if (logs_dir.exists() == False) or (logs_dir.is_dir() == False):
        logs_dir.mkdir()
    logs_dir = Path("./logs/dziennik")
    if (logs_dir.exists() == False) or (logs_dir.is_dir() == False):
        logs_dir.mkdir()
    logger = logging.getLogger('discord')
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    now = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    handler = logging.FileHandler(filename=f"logs/discord/[Di] {str(now)}.log", encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    dziennik_log = logging.getLogger('dziennik.logger')
    if debug:
        dziennik_log.setLevel(logging.DEBUG)
    else:
        dziennik_log.setLevel(logging.INFO)
    dziennik_handler = logging.FileHandler(filename=f"logs/dziennik/[Dz] {str(now)}.log", encoding='utf-8', mode='w')
    dziennik_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    dziennik_log.addHandler(dziennik_handler)
    print("[Logging] Aktywne.")
    dziennik_log.info("[Logging] Aktywne.")

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(Logger(bot))