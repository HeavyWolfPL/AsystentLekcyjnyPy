import json
from discord.ext import commands
import asyncio, datetime
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate

async def get_config():
    with open("config.json", "r") as config: 
        data = json.load(config)
        prefix = data["prefix"]
    return prefix

class PlanLekcji(commands.Cog, name='Plan Lekcji'):
    def __init__(self, bot):
        self.bot = bot
    print("PlanLekcji cog loaded")

    bot = commands.Bot(command_prefix='!')

    @bot.command(aliases=['lekcje', 'planlekcji'])
    async def plan(ctx, arg1):     
        print("T")
        lista_dni = ["dzisiaj", "jutro", "pojutrze", "wczoraj", "poniedzialek", "poniedziałek", "wtorek", "środa", "sroda", "czwartek", "piątek", "piatek", "sobota", "niedziela"]
        if arg1.lower() not in lista_dni:
            await ctx.channel.send("Nie ma planu dla tego dnia")
            return
        #await message.channel.send(f'Plan lekcji: \n```{await get_plan_lekcji()}```')
        await ctx.channel.send('Test')
    
    async def get_plan_lekcji(date, group):
        if date == 1:
            MY_GROUP = 'Grupa 1'
        if date == 2:
            MY_GROUP = 'Grupa 2'
        else: 
            MY_GROUP = 'Grupa 1'

        if date == "dzisiaj":
            target_date = datetime.datetime.now()
        elif date == "jutro":
            target_date = datetime.datetime.now() + timedelta(days=1)
        elif date == "pojutrze":
            target_date = datetime.datetime.now() + timedelta(days=2)
        elif date == "wczoraj":
            target_date = datetime.datetime.now() - timedelta(days=1)
        target_date = datetime.datetime.now() - timedelta(days=2)

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

        # attendance = await dziennikClient.data.get_attendance(date_from=target_date)
        # tmp = []
        # async for att in attendance:
        #     tmp.append(att)

        # attendance = tmp
        
        await dziennikClient.close()

        rows = []
        headers = ["Lp.", "Od - Do", "Przedmiot", "Sala"]
        all_info = {}

        for lesson in lessons:
            if lesson.visible:
                all_info[lesson.time.position] = [lesson]
        # for att in attendance:
        #     if att.time.position in all_info.keys():
        #         all_info[att.time.position].append(att)

        for key in sorted(all_info):
            try:
                sala = all_info[key][0].room.code
            except:
                sala = "N/A"

            lesson = all_info[key][0]

            if lesson.subject:
                name = lesson.subject.name

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
    
