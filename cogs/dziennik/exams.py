import json, datetime
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate
from cogs.dziennik.dziennik_setup import DziennikSetup

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Sprawdziany(commands.Cog, name='Kartkówki i Sprawdziany'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['tests', 'sprawdziany', 'spr', 'kartkówki', 'kartk'])
    async def testy(self, ctx):
        if "za tydzien" in ctx.message.content:
            await ctx.reply(f'Sprawdziany oraz Kartkówki: \n```{await self.get_tests("za tydzien")}```', mention_author=False)
        else: 
            await ctx.reply(f'Sprawdziany oraz Kartkówki: \n```{await self.get_tests("teraz")}```', mention_author=False)

    #Doesnt work?
    # @plan.error
    # async def plan_error(ctx, error):
    #     if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.channel.send("Instrukcja: `!plan <dzień> <grupa>`. \nLista dni: \n```dzisiaj, jutro, pojutrze, wczoraj, poniedzialek, poniedziałek, wtorek, środa, sroda, czwartek, piątek, piatek```")     
    
    async def get_tests(self, arg):

        dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(id))
        dziennikAccount = Account.load(await DziennikSetup.GetAccount(id))
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

        await dziennikClient.select_student()

        exams = await dziennikClient.data.get_exams()

        rows = []
        headers = ["Data", "Typ", "Przedmiot", "Treść"]
        all_info = {}

        if arg == "teraz":
            today = datetime.date.today()
            tmp = today.weekday()
            first_day = today
            while tmp != 0: #Get first day of the week
                first_day = first_day - timedelta(days=1)
                tmp = tmp - 1
            last_day = first_day + timedelta(days=4)
            print(last_day, first_day)
        else:
            today = datetime.date.today() + timedelta(days=7)
            tmp = today.weekday()
            first_day = today
            while tmp != 0: #Get first day of the next week
                first_day = first_day - timedelta(days=1)
                tmp = tmp - 1
            last_day = first_day + timedelta(days=4)
            print(last_day, first_day)

        exams = await dziennikClient.data.get_exams()
        number = 0
        async for exam in exams:
            if ((exam.deadline.date >= first_day) and (exam.deadline.date <= last_day)): #Check if exam is in the current week
                all_info[number] = [exam]
                number = number+1
                

        
        await dziennikClient.close()

        group = "Brak"
        groupsEnabled = False

        for key in sorted(all_info):
            exam = all_info[key][0]
            
            if exam.team_virtual != None:  
                groupsEnabled = True
            
            date = exam.deadline.date.strftime("%d.%m.%Y")

            if exam.type == "Sprawdzian":
                examtype = "Sprawdzian"
            else:
                examtype = "Kartkówka"

            if exam.subject:
                name = exam.subject.name
                if len(name) > 16:
                    name = exam.subject.code
                else:
                    name = exam.subject.name
            else:
                name = 'NO_INFO'

            if exam.topic != '':
                topic = exam.topic
            else:
                topic = 'Brak'
                
            if groupsEnabled:  
                #Date, Type, Subject name, Topic, Group
                headers = ["Data", "Typ", "Przedmiot", "Treść", "Grupa"]
                group = exam.team_virtual
                rows.append([date, examtype, name, topic, group])
            else:
                rows.append([date, examtype, name, topic])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(table)
        return table

def setup(bot):
    bot.add_cog(Sprawdziany(bot))
    
