import json, datetime
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    dziennik_enabled = data["dziennik_enabled"]

class ZadaniaDomowe(commands.Cog, name='Zadania domowe'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['zadania_domowe', 'zadane', 'zadaniadomowe', 'zaddom', 'hw'])
    async def homework(self, ctx):
        if not dziennik_enabled:
            await ctx.reply("Moduł dziennika jest wyłączony!", mention_author=False)
            return
        await ctx.reply(f'Zadania domowe: \n```{await self.get_homework()}```', mention_author=False)

    #Doesnt work?
    # @plan.error
    # async def plan_error(ctx, error):
    #     if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.channel.send("Instrukcja: `!plan <dzień> <grupa>`. \nLista dni: \n```dzisiaj, jutro, pojutrze, wczoraj, poniedzialek, poniedziałek, wtorek, środa, sroda, czwartek, piątek, piatek```")     
    
    async def get_homework(self):

        with open("key-config.json") as f:
            # load from a JSON string
            dziennikKeystore = Keystore.load(f.read())
        with open("acc-config.json") as f:
            # load from a JSON string
            dziennikAccount = Account.load(f.read())
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

        await dziennikClient.select_student()

        lessons = await dziennikClient.data.get_lessons()
        tmp = []

        async for lesson in lessons:
            tmp.append(lesson)
        lessons = tmp

        homeworks = await dziennikClient.data.get_homework()
        tmp = []

        rows = []
        headers = ["Data", "Przedmiot", "Treść"]
        all_info = {}

        today = datetime.date.today()
        tmp = today.weekday()
        first_day = today
        while tmp != 0: #Get first day of the week
            first_day = first_day - timedelta(days=1)
            tmp = tmp - 1
        last_day = first_day + timedelta(days=4)

        homeworks = await dziennikClient.data.get_homework()
        number = 0
        async for hw in homeworks:
            if ((hw.deadline.date >= first_day) & (hw.deadline.date <= last_day)): #Check if homework is in the current week
                all_info[number] = [hw]
                number+1

        
        await dziennikClient.close()

        for key in sorted(all_info):
            homework = all_info[key][0]

            if homework.content:
                content = homework.content

            if homework.subject:
                name = homework.subject.name
                if len(name) > 16:
                    name = homework.subject.code
                else:
                    name = homework.subject.name
                print(name)
            else:
                name = 'NO_INFO'

            date = homework.deadline.date.strftime("%d.%m.%Y")
                
            rows.append([date, name, content])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(table)
        return table

def setup(bot):
    bot.add_cog(ZadaniaDomowe(bot))
    
