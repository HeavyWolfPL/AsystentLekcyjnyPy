import discord, json, datetime, re, sys
from discord.ext import commands
from datetime import timedelta
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate
from cogs.dziennik.dziennik_setup import DziennikSetup
from cogs.a_logging_handler import Logger
dziennik_log = Logger.dziennik_log

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

help_description = """Nie wybrano tygodnia, ale spokojnie, możesz użyć poniższych przycisków.
Możesz również wpisać komendę od nowa, jeśli potrzebujesz sprawdziany i kartkówki z danego tygodnia.

W przypadku daty wystarczy, że podasz dowolny dzień wybranego tygodnia.
`!testy <data/dzień>`
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
- spr
- sprawdziany
- tests
- testy
- kartk
- kartkówki
```"""

class Sprawdziany(commands.Cog, name='Kartkówki i Sprawdziany'):
    def __init__(self, bot, intents):
        self.bot = bot
        
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

    @bot.command(aliases=['tests', 'sprawdziany', 'spr', 'kartkówki', "kartkowki", 'kartk'])
    async def testy(self, ctx, data):
        lista_dni = ["dzisiaj", "obecny", "aktualny", "ten_tydzień", "ten_tydzien", "za_tydzień", "za_tydzien", "następny", "nastepny", "przyszły", "przyszly"]
        if data not in lista_dni:
            regex = re.search(r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|20[0-9][0-9])$', data)
            if regex == None:
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Homework_Button(ctx))
                return
            elif regex.group(0):
                try:
                    data = datetime.datetime.strptime(str(regex.group(0)).replace(".", "/"), '%d/%m/%Y')
                except:
                    data = datetime.datetime.strptime(str(regex.group(0)).replace(".", "/"), '%d/%m/%y')
            else:
                dziennik_log.error("Wystąpił błąd! [Sprawdziany i Kartkówki - %s]", sys._getframe().f_lineno)
                return f"Wystąpił błąd! [Sprawdziany i Kartkówki - {sys._getframe().f_lineno}]"
        await ctx.reply(f'{await self.get_tests(ctx.author.id, data)}', mention_author=False)

    @testy.error
    async def plan_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "data":
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Testy_Button(ctx))
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    class Testy_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx

        # primary/blurple = 1
        # secondary/grey/gray = 2
        # success/green = 3
        # danger/red = 4
        # link/url = 5

        @discord.ui.button(label="Aktualny tydzień", style=discord.ButtonStyle.blurple)
        async def aktualny(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            dziennik_log.debug("Użytkownik {}#{} ({}) wybrał Sprawdziany i Kartkówki z aktualnego tygodnia.".format(interaction.user.name, interaction.user.discriminator, interaction.user.id))
            await interaction.followup.send(f'{await Sprawdziany.get_tests(Sprawdziany, interaction.user.id, "aktualny")}', ephemeral=True)

        @discord.ui.button(label="Przyszły tydzień", style=discord.ButtonStyle.blurple)
        async def przyszly(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            dziennik_log.debug("Użytkownik {}#{} ({}) wybrał Sprawdziany i Kartkówki z przyszłego tygodnia.".format(interaction.user.name, interaction.user.discriminator, interaction.user.id))
            await interaction.followup.send(f'{await Sprawdziany.get_tests(Sprawdziany, interaction.user.id, "przyszły")}', ephemeral=True)
        
        @discord.ui.button(label="Anuluj", style=discord.ButtonStyle.red)
        async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.followup.send('Brak uprawnień!', ephemeral=True)

    
    async def get_tests(self, id, date):

        try:
            dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(id))
            dziennikAccount = Account.load(await DziennikSetup.GetAccount(id))
        except FileNotFoundError:
            return f"<@{id}>, nie znaleziono danych twojego konta."
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

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

        await dziennikClient.select_student()

        rows = []
        headers = ["Data", "Typ", "Przedmiot", "Treść"]
        all_info = {}

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

        tabela = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        print(tabela)
        dziennik_log.debug(f"Wyświetlono sprawdziany i kartkówki z {first_day}-{last_day}.")
        return f"Sprawdziany oraz Kartkówki: \n```{tabela}```"

async def setup(bot):
    intents = discord.Intents.default()
    intents.members = True
    await bot.add_cog(Sprawdziany(bot, intents=intents))
    
