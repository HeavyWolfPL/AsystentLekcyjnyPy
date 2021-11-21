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
```"""

class PlanLekcji(commands.Cog, name='Plan Lekcji'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    @bot.command(aliases=['lekcje', 'planlekcji'])
    async def plan(self, ctx, arg1):
        lista_dni = ["dzisiaj", "jutro", "pojutrze", "wczoraj", "poniedzialek", "poniedziałek", "wtorek", "środa", "sroda", "czwartek", "piątek", "piatek"]
        regex = re.search(r'^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|20[0-9][0-9])$', arg1)
        if arg1.lower() not in lista_dni:
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
        await ctx.send(embed=embed, view=self.Plan_RODO_Button(ctx, arg1))

    @plan.error
    async def plan_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "arg1":
                embed=discord.Embed(description=help_description, color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=self.Plan_Button(ctx))
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    class Plan_Button(discord.ui.View):
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
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "poniedziałek")}', ephemeral=True)

        @discord.ui.button(label="Wtorek", style=discord.ButtonStyle.blurple)
        async def wtorek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "wtorek")}', ephemeral=True)

        @discord.ui.button(label="Środa", style=discord.ButtonStyle.blurple)
        async def sroda(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "środa")}', ephemeral=True)

        @discord.ui.button(label="Czwartek", style=discord.ButtonStyle.blurple)
        async def czwartek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "czwartek")}', ephemeral=True)

        @discord.ui.button(label="Piątek", style=discord.ButtonStyle.blurple)
        async def piatek(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "piątek")}', ephemeral=True)

        @discord.ui.button(label="Wczoraj", style=discord.ButtonStyle.gray)
        async def wczoraj(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "wczoraj")}', ephemeral=True)

        @discord.ui.button(label="Dzisiaj", style=discord.ButtonStyle.gray)
        async def dzisiaj(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "dzisiaj")}', ephemeral=True)
        
        @discord.ui.button(label="Jutro", style=discord.ButtonStyle.gray)
        async def jutro(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "jutro")}', ephemeral=True)

        @discord.ui.button(label="Pojutrze", style=discord.ButtonStyle.gray)
        async def pojutrze(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, "pojutrze")}', ephemeral=True)
        
        @discord.ui.button(label="Usuń", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    class Plan_RODO_Button(discord.ui.View):
        def __init__(self, ctx, date):
            super().__init__()
            self.ctx = ctx
            self.date = date

        @discord.ui.button(label="Tak", style=discord.ButtonStyle.green)
        async def tak(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
                await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, self.date)}', ephemeral=True)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
            

        @discord.ui.button(label="Nie", style=discord.ButtonStyle.gray)
        async def nie(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.response.send_message(f'{await PlanLekcji.get_plan_lekcji(PlanLekcji, interaction.user.id, self.date)}', ephemeral=False)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
        
        @discord.ui.button(label="Anuluj", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)


    async def get_plan_lekcji(self, id, date):
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

        tabela = tabulate(rows, headers, tablefmt="orgtbl", stralign="center")
        x = """|  Lp.  |  Od - Do  |  Przedmiot  |  Sala  |
|-------+-----------+-------------+--------|"""
        if tabela == x:
            print("Nie ma planu na wybrany dzień.")
            return "Wybrany dzień nie posiada planu."
        else:
            print(tabela)
            return f"Plan lekcji z {target_date.strftime('%d/%m/%Y')}: ```\n{tabela}```"

def setup(bot):
    bot.add_cog(PlanLekcji(bot))
    
