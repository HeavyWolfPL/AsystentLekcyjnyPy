import json, datetime
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class ZadaniaDomowe(commands.Cog, name='Zadania domowe'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['zadania_domowe', 'zadane', 'zadaniadomowe', 'zaddom', 'hw'])
    async def homework(self, ctx):
        lista_dni = ["dzisiaj", "jutro", "pojutrze", "wczoraj", "poniedzialek", "poniedziałek", "wtorek", "środa", "sroda", "czwartek", "piątek", "piatek"]
        arg1 = "dzisiaj"
        if arg1.lower() not in lista_dni:
            await ctx.channel.send("Nie ma zadań dla tego dnia.")
            return
        await ctx.reply(f'Plan lekcji: \n```{await self.get_homework()}```')

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
        tmp2 = []
        x = 0

        async for hw in homeworks:
            if x != 1:
                x = 1
                tmp.append(hw)
                tmp2.append(hw.deadline.date)
                time = hw.deadline.date
        homework = tmp
        print(tmp2)
        print(tmp)

        rows = []
        headers = ["Data", "Przedmiot", "Treść"]
        all_info = {}

        today = datetime.date.today()
        tmp = today.weekday()
        first_day = today
        while tmp != 0: #Get first day of the week
            first_day = first_day - timedelta(days=1)
            tmp = tmp - 1
        last_day = first_day + timedelta(days=5)

        homeworks = await dziennikClient.data.get_homework()
        number = 0
        async for hw in homeworks:
            if ((hw.deadline.date > first_day) & (hw.deadline.date < last_day)): #Check if homework is in the current week
                all_info[number] = [hw]
                print(f'Zad \n{all_info[number]} \n-----')
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

        lekcje = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(lekcje)
        return lekcje

def setup(bot):
    bot.add_cog(ZadaniaDomowe(bot))
    
