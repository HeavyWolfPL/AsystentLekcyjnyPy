import json, datetime
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class PlanLekcji(commands.Cog, name='Plan Lekcji'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['lekcje', 'planlekcji'])
    async def plan(self, ctx, arg1):
        lista_dni = ["dzisiaj", "jutro", "pojutrze", "wczoraj", "poniedzialek", "poniedziałek", "wtorek", "środa", "sroda", "czwartek", "piątek", "piatek"]
        if arg1.lower() not in lista_dni:
            await ctx.channel.send("Nie ma planu dla tego dnia.")
            return
        await ctx.reply(f'Plan lekcji: \n```{await self.get_plan_lekcji(arg1)}```')

    #Doesnt work?
    # @plan.error
    # async def plan_error(ctx, error):
    #     if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.channel.send("Instrukcja: `!plan <dzień> <grupa>`. \nLista dni: \n```dzisiaj, jutro, pojutrze, wczoraj, poniedzialek, poniedziałek, wtorek, środa, sroda, czwartek, piątek, piatek```")     
    
    async def get_plan_lekcji(self, date):
        MY_GROUP = None

        if date == "dzisiaj":
            target_date = datetime.datetime.now()
        elif date == "jutro":
            target_date = datetime.datetime.now() + timedelta(days=1)
        elif date == "pojutrze":
            target_date = datetime.datetime.now() + timedelta(days=2)
        elif date == "wczoraj":
            target_date = datetime.datetime.now() - timedelta(days=1)
        elif date in ["poniedzialek", "poniedziałek"]:
            today = datetime.date.today()
            target_date = today + datetime.timedelta( (0-today.weekday()) % 7 )
        elif date == "wtorek":
            today = datetime.date.today()
            target_date = today + datetime.timedelta( (1-today.weekday()) % 7 )
        elif date in ["środa", "sroda"]:
            today = datetime.date.today()
            target_date = today + datetime.timedelta( (2-today.weekday()) % 7 )
        elif date == "czwartek":
            today = datetime.date.today()
            target_date = today + datetime.timedelta( (3-today.weekday()) % 7 )
        elif date in ["piatek", "piątek"]:
            today = datetime.date.today()
            target_date = today + datetime.timedelta( (4-today.weekday()) % 7 )
        else:
            target_date = datetime.datetime.now()

        with open("key-config.json") as f:
            # load from a JSON string
            dziennikKeystore = Keystore.load(f.read())
        with open("acc-config.json") as f:
            # load from a JSON string
            dziennikAccount = Account.load(f.read())
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

        await dziennikClient.select_student()

        lessons = await dziennikClient.data.get_lessons(date_from=target_date)
        tmp = []

        async for lesson in lessons:
            tmp.append(lesson)
        lessons = tmp

        await dziennikClient.close()

        rows = []
        headers = ["Lp.", "Od - Do", "Przedmiot", "Sala"]
        all_info = {}

        for lesson in lessons:
            if lesson.visible:
                all_info[lesson.time.position] = [lesson]

        for key in sorted(all_info):
            try:
                sala = all_info[key][0].room.code
            except:
                sala = "N/A"

            lesson = all_info[key][0]

            if lesson.subject:
                name = lesson.subject.name
                if len(name) > 16:
                    name = lesson.subject.code
                else:
                    name = lesson.subject.name
            elif lesson.event:
                name = lesson.event
            else:
                name = 'NO_INFO'

            if not MY_GROUP:
                if all_info[key][0].group:
                    name = name + ' (' + all_info[key][0].group.name + ')'
                
            rows.append([str(lesson.time.position), lesson.time.displayed_time.split("-")[0] + " - " + lesson.time.displayed_time.split("-")[1], name, sala])

        lekcje = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(lekcje)
        return lekcje

def setup(bot):
    bot.add_cog(PlanLekcji(bot))
    
