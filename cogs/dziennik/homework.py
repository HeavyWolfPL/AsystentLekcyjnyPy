import discord, json, datetime, re
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate
from cogs.dziennik.dziennik_setup import DziennikSetup

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

help_description = """Nie wybrano tygodnia, ale spokojnie, możesz użyć poniższych przycisków.
Możesz również wpisać komendę od nowa, jeśli potrzebujesz zadania domowe z danego tygodnia.

W przypadku daty wystarczy, że podasz dowolny dzień wybranego tygodnia.
`!homework <data/dzień>`
```md
- 1.1.21
- 1.1.2021
- 1.10.2021
- 10.1.2021
- 01.10.2021

- 1/1/21
- 1/1/2021
- 1/10/2021
- 10/1/2021
- 01/10/2021

- dzisiaj/obecny/aktualny/ten_tydzień
- za_tydzień/następny/przyszły
```

**Aliasy:**
```
- hw
- zaddom
- zadane
- zadaniadomowe
- zadania_domowe
```"""

class ZadaniaDomowe(commands.Cog, name='Zadania domowe'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['zadania_domowe', 'zadane', 'zadaniadomowe', 'zaddom', 'hw'])
    async def homework(self, ctx, arg1):
        lista_dni = ["dzisiaj", "obecny", "aktualny", "ten_tydzień", "ten_tydzien", "za_tydzień", "za_tydzien", "następny", "nastepny", "przyszły", "przyszly"]
        regex = re.search(r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|20[0-9][0-9])$', arg1)
        if arg1 not in lista_dni:
            if regex == None:
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Homework_Button(ctx))
                return
            elif regex.group(0):
                try:
                    arg1 = datetime.datetime.strptime(str(regex.group(0)).replace(".", "/"), '%d/%m/%Y')
                except:
                    arg1 = datetime.datetime.strptime(str(regex.group(0)).replace(".", "/"), '%d/%m/%y')
            else:
                print("Wystąpił błąd")
                return
        await ctx.reply(f'{await self.get_homework(ctx.author.id, arg1)}', mention_author=False)

    @homework.error
    async def homework_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "arg1":
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Homework_Button(ctx))
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    class Homework_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx

        # primary/blurple = 1
        # secondary/grey/gray = 2
        # success/green = 3
        # danger/red = 4
        # link/url = 5

        @discord.ui.button(label="Aktualny tydzień", style=discord.ButtonStyle.blurple)
        async def aktualny(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'Sprawdziany oraz Kartkówki: \n```{await ZadaniaDomowe.get_homework(ZadaniaDomowe, interaction.user.id, "aktualny")}```', ephemeral=True)

        @discord.ui.button(label="Przyszły tydzień", style=discord.ButtonStyle.blurple)
        async def przyszly(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'Sprawdziany oraz Kartkówki: \n```{await ZadaniaDomowe.get_homework(ZadaniaDomowe, interaction.user.id, "przyszły")}```', ephemeral=True)
        
        @discord.ui.button(label="Anuluj", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
    
    async def get_homework(self, id, date):
        today = datetime.datetime.today()
        if date in ["dzisiaj", "obecny", "aktualny", "ten_tydzień", "ten_tydzien"]:
            first_day = today
            tmp = first_day.weekday()
            while tmp != 0: #Get first day of the week
                first_day = first_day - timedelta(days=1)
                tmp = tmp - 1
            last_day = first_day + timedelta(days=4)
        elif date in ["za_tydzień", "za_tydzien", "następny", "nastepny", "przyszły", "przyszly"]:
            first_day = today+datetime.timedelta(days=7)
            tmp = first_day.weekday()
            while tmp != 0: #Get first day of the week
                first_day = first_day - timedelta(days=1)
                tmp = tmp - 1
            last_day = first_day + timedelta(days=4)
        else:
            first_day = date
            tmp = first_day.weekday()
            while tmp != 0: #Get first day of the week
                first_day = first_day - timedelta(days=1)
                tmp = tmp - 1
            last_day = first_day + timedelta(days=4)

        first_day = datetime.date(first_day.year, first_day.month, first_day.day)
        last_day = datetime.date(last_day.year, last_day.month, last_day.day)

        try:
            dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(id))
            dziennikAccount = Account.load(await DziennikSetup.GetAccount(id))
        except FileNotFoundError:
            return f"<@{id}>, nie znaleziono danych twojego konta."
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

        tabela = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(tabela)
        x = """|  Data  |  Przedmiot  |  Treść  |
|--------+-------------+---------|"""
        if tabela == x:
            print("Nie ma zadań domowych na wybrany tydzień.")
            return "Nie ma zadań domowych na wybrany tydzień."
        else:
            print(tabela)
            return f"Zadania domowe z `{first_day.strftime('%d/%m/%Y')}` - `{last_day.strftime('%d/%m/%Y')}` ```\n{tabela}```"

def setup(bot):
    bot.add_cog(ZadaniaDomowe(bot))
    
