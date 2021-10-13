import json
import re
from discord.ext import commands
from vulcan import Vulcan
from vulcan import Account
from vulcan import Keystore

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Numerek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=["numerek", "szczęśliwynumerek", "szczesliwynumerek", "luckynumber"])
    async def numer(self, ctx):
        await ctx.channel.send(f'Szczęśliwy Numerek: `{await self.get_luckynumber()}`')

    async def get_luckynumber(self):
        with open("key-config.json") as f:
            # load from a JSON string
            dziennikKeystore = Keystore.load(f.read())
        with open("acc-config.json") as f:
            # load from a JSON string
            dziennikAccount = Account.load(f.read())
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
        return lucky_number

def setup(bot):
    bot.add_cog(Numerek(bot))