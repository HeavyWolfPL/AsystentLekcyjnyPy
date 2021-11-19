import discord
import json
import datetime
from discord.ext import commands

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

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

def setup(bot):
    bot.add_cog(ErrorHandler(bot))