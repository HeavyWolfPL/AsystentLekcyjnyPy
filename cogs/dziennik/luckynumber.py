import json
import re
from discord.ext import commands
from vulcan import Vulcan, Account, Keystore
from cogs.dziennik.dziennik_setup import DziennikSetup

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Numerek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

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
        print(dziennikClient.student)  # print the selected student 
        lucky_number = await dziennikClient.data.get_lucky_number()
        await dziennikClient.close()
        #print(f'{str(lucky_number)}')
        number = re.search('number=(.+?)\)', str(lucky_number))
        if number:
            lucky_number = number.group(1)
        if lucky_number == "0":
            lucky_number = "Brak"
        return f"Szczęśliwy Numerek: `{lucky_number}`"

def setup(bot):
    bot.add_cog(Numerek(bot))