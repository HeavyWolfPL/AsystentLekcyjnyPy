import json, re, logging
from discord.ext import commands
from vulcan import Vulcan, Account, Keystore
from cogs.dziennik.dziennik_setup import DziennikSetup
from cogs.a_logging_handler import Logger
dziennik_log = Logger.dziennik_log

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Numerek(commands.Cog):
    def __init__(self, bot, intents):
        self.bot = bot
        
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

    @bot.command(aliases=["numerek", "szczęśliwynumerek", "szczesliwynumerek", "luckynumber"])
    async def numer(self, ctx):
        await ctx.channel.send(f'{await self.get_luckynumber()}')

    async def get_luckynumber(self):
        try:
            dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(id))
            dziennikAccount = Account.load(await DziennikSetup.GetAccount(id))
        except FileNotFoundError:
            return f"<@{id}>, nie znaleziono danych twojego konta."
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)
        
        await dziennikClient.select_student()  # select the first available student
        lucky_number = await dziennikClient.data.get_lucky_number()
        await dziennikClient.close()
        
        number = re.search('number=(.+?)\)', str(lucky_number))
        if number:
            lucky_number = number.group(1)
        if lucky_number == "0":
            lucky_number = "Brak"
        dziennik_log.debug("Numerek to: " + lucky_number)
        return f"Szczęśliwy Numerek: `{lucky_number}`"

def setup(bot):
    bot.add_cog(Numerek(bot))