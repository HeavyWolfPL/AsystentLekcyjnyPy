import json, datetime
import discord
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate
from cogs.dziennik.dziennik_setup import DziennikSetup

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]

class Oceny(commands.Cog, name='Oceny'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['oceny'])
    async def grades(self, ctx):
        await ctx.reply(f'\n```{await self.get_grades()}```', mention_author=False)
    
    @bot.command(aliases=['ocena'])
    async def grade(self, ctx, arg1):
        arg = str(arg1)
        if arg1 == "0":
            await ctx.reply('ID oceny musi być liczbą.', mention_author=False)
        # elif await self.get_grade_info(arg) == 'False':
        #     await ctx.reply('Nie znaleziono oceny o podanym ID.', mention_author=False)
        else:
            #await ctx.reply(f'Szczegóły oceny: \n{await self.get_grade_info(arg)}', mention_author=False)
            await ctx.reply(embed=await self.get_grade_info(arg), mention_author=False)

    async def get_grade_info(self, arg1):

        dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(id))
        dziennikAccount = Account.load(await DziennikSetup.GetAccount(id))
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

        await dziennikClient.select_student()

        all_info = {}

        grades = await dziennikClient.data.get_grades()
        number = 0
        async for grade in grades:
            all_info[number] = [grade]
            number = number+1
        
        await dziennikClient.close()

        for key in sorted(all_info):
            grade = all_info[key][0]

            GradeExists = None

            if GradeExists == True:
                break

            if str(grade.id) == str(arg1):
                if grade.column.subject:
                    name = grade.column.subject.name
                    if len(name) > 16:
                        name = grade.column.subject.code
                    else:
                        name = grade.column.subject.name
                else:
                    name = 'NO_INFO'
                #if grade.date_created.date.strftime("%d.%m.%Y") == grade.date_modified.date.strftime("%d.%m.%Y"):
                if grade.date_created.date == grade.date_modified.date:
                    date = grade.date_created.date.strftime("%d.%m.%Y")
                else:
                    date = f'{grade.date_created.date.strftime("%d.%m.%Y")} / {grade.date_modified.date.strftime("%d.%m.%Y")}'
                teacher = grade.teacher_modified.display_name
                if grade.comment == "":
                    comment = "Brak"
                else:
                    comment = grade.comment

                if grade.column.name == "":
                    category = "Brak"
                else:
                    category = grade.column.name
                weight = grade.column.weight
                grade_color = 0x03A9F4
                if "1" in grade.content:
                    grade_color = 0xff0000
                if "2" in grade.content:
                    grade_color = 0xff4E11
                if "3" in grade.content:
                    grade_color = 0xff8E15
                if "4" in grade.content:
                    grade_color = 0xFAB733
                if "5" in grade.content:
                    grade_color = 0xACB334
                if "6" in grade.content:
                    grade_color = 0x69B34C
                embed = discord.Embed(description=f'**Ocena**: `{grade.content}` \n\nData: {date}\nNauczyciel: {teacher}\nKomentarz: {comment}\nKategoria: {category}\nWaga: {weight}', color=grade_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f'ID: {grade.id}')
                GradeExists = True
            else: 
                GradeExists = False

        # if GradeExists == True:
        #     return embed
        # else:
        #     return 'False'
        return embed
    
    async def get_grades(self):

        with open("key-config.json") as f:
            # load from a JSON string
            dziennikKeystore = Keystore.load(f.read())
        with open("acc-config.json") as f:
            # load from a JSON string
            dziennikAccount = Account.load(f.read())
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

        await dziennikClient.select_student()

        grades = await dziennikClient.data.get_grades()

        rows = []
        headers = ["Przedmiot", "Ocena"]
        all_info = {}

        grades = await dziennikClient.data.get_grades()
        number = 0
        async for grade in grades:
            all_info[number] = [grade]
            number = number+1
        await dziennikClient.close()

        for key in sorted(all_info):
            grade = all_info[key][0]
            
            
            if grade.column.subject:
                name = grade.column.subject.name
                if len(name) > 16:
                    name = grade.column.subject.code
                else:
                    name = grade.column.subject.name
            else:
                name = 'NO_INFO'
            
            grade = f'{grade.content} ({grade.id})'
     
            rows.append([name, grade])

        table = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(table)
        return table

def setup(bot):
    bot.add_cog(Oceny(bot))
    
