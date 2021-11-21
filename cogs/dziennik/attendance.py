import discord
import datetime, json, re, pathlib
from discord.ext import commands
from vulcan import Keystore, Account, Vulcan
from tabulate import tabulate
from cogs.dziennik.dziennik_setup import DziennikSetup

with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    dziennik_mode = data["dziennik_mode"]
    rodo = data["RODO"]
    footer = data["footerCopyright"]
    footer_img = data["footerCopyrightImage"]

help_description = """Nie podano poprawnego dnia tygodnia, ale możesz użyć poniższych przycisków.   
Możesz również wpisać komendę od nowa, jeśli potrzebujesz plan z danego dnia.

`!plan <data/dzień>`
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

- wczoraj/dzisiaj/jutro/pojutrze
- poniedziałek/wtorek/środa/czwartek/piątek
```

Aliasy:
```
- ob
- obecny
- obecność
- nieobecności
```"""

class Frekwencja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['obecność', 'obecnosc', 'ob', 'obecny', 'nieobecności', 'nieobecnosci'])
    async def frekwencja(self, ctx, arg1):
        arg1 = arg1.lower()
        if (dziennik_mode in ["both", "global"]) and (rodo == True):
            path = pathlib.Path(f'db/{id}/acc-config.json')
            if not pathlib.Path.exists(path):
                print("[RODO Mode - Attendance] Użytkownik nie posiada własnego tokenu. Anuluję...")
                await ctx.send("Nie mogę tego zrobić ze względu na włączony tryb **RODO**. Ustaw swój własny token, by móc użyć tej komendy.")
        lista_dni = ["dzisiaj", "wczoraj", "poniedzialek", "poniedziałek", "wtorek", "środa", "sroda", "czwartek", "piątek", "piatek"]
        regex = re.search(r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|20[0-9][0-9])$', arg1)
        if arg1 not in lista_dni:
            if regex == None:
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Frekwencja_Button(ctx))
                return
            elif regex.group(0):
                try:
                    arg1 = datetime.datetime.strptime(str(regex.group(0)).replace(".", "/"), '%d/%m/%Y')
                except:
                    arg1 = datetime.datetime.strptime(str(regex.group(0)).replace(".", "/"), '%d/%m/%y')
            else:
                print("Wystąpił błąd")
                return
        description = """**Czy chcesz wysłać plan jako widoczny tylko dla ciebie?** \nKliknięcie opcji Tak, spowoduje ukrycie go tylko dla ciebie. \nKliknięcie opcji Nie, spowoduje wysłanie planu jako publicznego."""
        embed=discord.Embed(description=description, color=0xdaa454, timestamp=ctx.message.created_at)
        embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
        embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
        await ctx.send(embed=embed, view=self.Frekwencja_RODO_Button(ctx, arg1))

    @frekwencja.error
    async def frekwencja_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "arg1":
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Frekwencja_Button(ctx))
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    class Frekwencja_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx

        # primary/blurple = 1
        # secondary/grey/gray = 2
        # success/green = 3
        # danger/red = 4
        # link/url = 5

        @discord.ui.button(label="Poniedziałek", style=discord.ButtonStyle.blurple)
        async def poniedzialek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "poniedziałek")}', ephemeral=True)

        @discord.ui.button(label="Wtorek", style=discord.ButtonStyle.blurple)
        async def wtorek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "wtorek")}', ephemeral=True)

        @discord.ui.button(label="Środa", style=discord.ButtonStyle.blurple)
        async def sroda(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "środa")}', ephemeral=True)

        @discord.ui.button(label="Czwartek", style=discord.ButtonStyle.blurple)
        async def czwartek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "czwartek")}', ephemeral=True)

        @discord.ui.button(label="Piątek", style=discord.ButtonStyle.blurple)
        async def piatek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "piątek")}', ephemeral=True)

        @discord.ui.button(label="Wczoraj", style=discord.ButtonStyle.gray)
        async def wczoraj(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "wczoraj")}', ephemeral=True)

        @discord.ui.button(label="Dzisiaj", style=discord.ButtonStyle.gray)
        async def dzisiaj(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, "dzisiaj")}', ephemeral=True)
                
        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    class Frekwencja_RODO_Button(discord.ui.View):
        def __init__(self, ctx, date):
            super().__init__()
            self.ctx = ctx
            self.date = date

        @discord.ui.button(label="Tak", style=discord.ButtonStyle.green)
        async def tak(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
                await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, self.date)}', ephemeral=True)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
            

        @discord.ui.button(label="Nie", style=discord.ButtonStyle.gray)
        async def nie(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.response.send_message(f'{await Frekwencja.get_frekwencja(Frekwencja, interaction.user.id, self.date)}', ephemeral=False)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
        
        @discord.ui.button(label="Anuluj", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    async def get_frekwencja(self, id, date):

        if date == "dzisiaj":
            target_date = datetime.datetime.now()
        elif date == "wczoraj":
            target_date = datetime.datetime.now() - datetime.timedelta(days=1)
        elif date in ["poniedzialek", "poniedziałek"]:
            today = datetime.date.today()
            target_date = today-datetime.timedelta(today.weekday())
        elif date == "wtorek":
            today = datetime.date.today()
            target_date = today-datetime.timedelta(today.weekday()-1)
        elif date in ["środa", "sroda"]:
            today = datetime.date.today()
            target_date = today-datetime.timedelta(today.weekday()-2)
        elif date == "czwartek":
            today = datetime.date.today()
            target_date = today-datetime.timedelta(today.weekday()-3)
        elif date in ["piatek", "piątek"]:
            today = datetime.date.today()
            target_date = today-datetime.timedelta(today.weekday()-4)
        else:
            target_date = date

        try:
            dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(id))
            dziennikAccount = Account.load(await DziennikSetup.GetAccount(id))
        except FileNotFoundError:
            return f"<@{id}>, nie znaleziono danych twojego konta."
        dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)

        await dziennikClient.select_student()

        lessons = await dziennikClient.data.get_lessons(date_from=target_date)
        tmp = []
        async for lesson in lessons:
            tmp.append(lesson)
        lessons = tmp
        
        attendance = await dziennikClient.data.get_attendance(date_from=target_date)
        tmp = []
        async for att in attendance:
            tmp.append(att)
        attendance = tmp
        
        await dziennikClient.close()

        # For one day only
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(await frekwencja())

        tabela = []
        headers = ["Lp.", "Od - Do", "Przedmiot", "Obecność"]
        all_info = {}

        for lesson in lessons:
            if lesson.visible:
                all_info[lesson.time.position] = [lesson]
        for att in attendance:
            if att.time.position in all_info.keys():
                all_info[att.time.position].append(att)

        godziny_nieobecne = []
        for key in sorted(all_info):
            try:
                symbol = all_info[key][1].presence_type.symbol
                if symbol == "▬":
                    godziny_nieobecne.append(str(all_info[key][1].time.position))
            except:
                symbol = "N/A"

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

            if all_info[key][0].group:
                name = name + ' (' + all_info[key][0].group.name + ')'
                
            tabela.append([str(all_info[key][0].time.position), all_info[key][0].time.displayed_time.split("-")[0] + " - " + all_info[key][0].time.displayed_time.split("-")[1], name, symbol])

        tabela = tabulate(tabela, headers, tablefmt="orgtbl", stralign="center")
        print(tabela)
        x = """|  Lp.  |  Od - Do  |  Przedmiot  |  Obecność  |
|-------+-----------+-------------+------------|"""
        if tabela == x:
            print("Nie ma frekwencji na wybrany dzień.")
            return "Wybrany dzień nie uwzględnia frekwencji."
        else:
            print(tabela)
            return f"Frekwencja z {target_date.strftime('%d/%m/%Y')}: ```\n{tabela}```"

        # For whole week
        # if target_date == 'week':
        #     # Get week start date
        #     dt = datetime.datetime.now()
        #     start = dt - datetime.timedelta(days=dt.weekday())

        #     week_info = {}
        #     for d in range(5):
        #         target_date = start + datetime.timedelta(days=d)
        #         #loop = asyncio.get_event_loop()
        #         #loop.run_until_complete(await frekwencja())

        #         week_info[d] = {}
        #         for lesson in lessons:
        #             week_info[d][lesson.time.position] = {'lesson': lesson}

        #         for att in attendance:
        #             week_info[d][att.time.position]['attendance'] = att

        #     print(week_info)

        #     tabela = []
        #     headers = ["Lp.", "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        #     all_info = {}

        #     # Transform it from `day: data` to `1_hour: data` so it can be displayed
        #     for hour in range(1,9):
        #         row = [str(hour)]
        #         for day in range(5):
        #             cell = week_info[day].get(hour, None)
        #             # print(cell)
        #             if cell:
        #                 lesson = cell['lesson']

        #                 if lesson.subject:
        #                     name = lesson.subject.name
        #                     if len(name) > 16:
        #                         out = lesson.subject.code
        #                     else:
        #                         out = lesson.subject.name
        #                 elif lesson.event:
        #                     out = lesson.event
        #                 else:
        #                     out = 'NO_INFO'

        #                 att = cell.get('attendance', None)
        #                 if att:
        #                     if att.presence_type:
        #                         symbol = att.presence_type.symbol
        #                     else:
        #                         symbol = "N/A"
        #                 else:
        #                     symbol = "N/A"

        #                 # Append group name, if MY_GROUP not specified
        #                 if lesson.group and not MY_GROUP:
        #                     out = out + ' (' + lesson.group.name + ')'
                            
        #                 out = symbol + ' ' + out
        #             else:
        #                 out = ''

        #             row.append(out)
        #     tabela = out    
        #     #     tabela.append([str(all_info[key][0].time.position), all_info[key][0].time.displayed_time.split("-")[0] + " - " + all_info[key][0].time.displayed_time.split("-")[1], name, symbol])
        #     # tabela = tabulate(tabela, headers, tablefmt="orgtbl", stralign="center")
        #     return tabela
        # else:

def setup(bot):
    bot.add_cog(Frekwencja(bot))