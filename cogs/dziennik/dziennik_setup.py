import json, datetime, pathlib, discord, sys
from discord.ext import commands
from vulcan import Keystore, Account, Vulcan
from cogs.bot_info import BotInfo
from cogs.a_logging_handler import Logger
dziennik_log = Logger.dziennik_log

with open("config.json", "r") as config:
    data = json.load(config)
    prefix = data["prefix"]
    owner_id = data["ownerID"] 
    dziennik_mode = data['dziennik_mode']
    api_name = data['api_name']
    footer = data['footerCopyright']
    footer_img = data['footerCopyrightImage']

class DziennikSetup(commands.Cog, name='Ustawienia'):
    def __init__(self, bot, intents):
        self.bot = bot
        
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

    if dziennik_mode == "both":
        @bot.command(name='setup')
        async def setupcmd(self, ctx, tryb, token, symbol, pin):
            #await ctx.message.delete()
            availableModes = "user"
            if str(ctx.author.id) == str(owner_id):
                availableModes = "user i global"
            if tryb not in "user global":
                await ctx.channel.send(f"Musisz podać tryb, dla którego chcesz ustawić passy. \nDostępne: `{availableModes}`")
                return
            if (tryb == "global") and ("global" not in availableModes):
                await ctx.channel.send("Nie posiadasz uprawnień do danych logowania.")
                return
            if len(token) != 7:
                await ctx.channel.send("Błędny token.")
                return
            if len(symbol) < 1:
                await ctx.channel.send("Błędny symbol.")
                return
            if len(pin) != 6:
                await ctx.channel.send("Błędny numer PIN.")
                return
            if tryb == "user":
                await ctx.channel.send(await self.RegisterAccount(ctx.author.id, token, symbol, pin, "user"))
            if tryb == "global":
                await ctx.channel.send(await self.RegisterAccount(ctx.author.id, token, symbol, pin, "global"))
    else:
        @bot.command(name='setup')
        async def setupcmd(self, ctx, token, symbol, pin):
            await ctx.message.delete()
            if (dziennik_mode == "global") and str(ctx.author.id) != str(owner_id):
                await ctx.channel.send("Nie posiadasz uprawnień do danych logowania.")
                return
            if len(token) != 7:
                await ctx.channel.send("Błędny token.")
                return
            if len(symbol) < 1:
                await ctx.channel.send("Błędny symbol.")
                return
            if len(pin) != 6:
                await ctx.channel.send("Błędny numer PIN.")
                return
            await ctx.channel.send(await self.RegisterAccount(ctx.author.id, token, symbol, pin, dziennik_mode))

    @setupcmd.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "tryb":
                await BotInfo.show_command_info(self, ctx, "setup")
            if error.param.name == "token":
                await ctx.channel.send("Brakuje trzech argumentów")
            if error.param.name == "symbol":
                await ctx.channel.send("Brakuje dwóch argumentów.")
            if error.param.name == "pin":
                await ctx.channel.send("Brakuje jednego argumentu.")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

    @bot.command(name='delsetup')
    async def delsetupcmd(self, ctx):
        if dziennik_mode == "global":
            path = pathlib.Path(f'db/acc-config.json')
            path2 = pathlib.Path(f'db/key-config.json')
            if str(ctx.author.id) != str(owner_id):
                await ctx.channel.send("Brak uprawnień! Nie możesz usunąć globalnego konta.")
                return
            if (pathlib.Path.exists(path)) and (pathlib.Path.exists(path2)):
                embed=discord.Embed(description="Czy potwierdzasz usunięcie globalnego konta?", color=0xdaa454, timestamp=ctx.message.created_at)
                embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                await ctx.send(embed=embed, view=DziennikSetup.Confirm_Button(ctx, "global"))
                return
            else:
                await ctx.send("Konto globalne nie jest ustawione.")
        if dziennik_mode in ["user", "both"]:
            path = pathlib.Path(f'db/{ctx.author.id}/acc-config.json')
            path2 = pathlib.Path(f'db/{ctx.author.id}/key-config.json')
            pathg = pathlib.Path(f'db/acc-config.json')
            pathg2 = pathlib.Path(f'db/key-config.json')
            if (str(ctx.author.id) == str(owner_id)):
                if ((pathlib.Path.exists(pathg) and pathlib.Path.exists(pathg2)) and ((not pathlib.Path.exists(path)) and (not pathlib.Path.exists(path2)))): #If user is owner, only has global account
                    mode = "global"
                    description = "Czy potwierdzasz usunięcie globalnego konta?"
                elif ((pathlib.Path.exists(path) and pathlib.Path.exists(path2)) and ((not pathlib.Path.exists(pathg)) and (not pathlib.Path.exists(pathg2)))): #If user is owner, only has user account
                    mode = "user"
                    description = "Czy potwierdzasz usunięcie konta użytkownika?"
                elif ((pathlib.Path.exists(path) and pathlib.Path.exists(path2)) and (pathlib.Path.exists(pathg) and pathlib.Path.exists(pathg2))): #If user is owner, has both accounts
                    embed=discord.Embed(description="Wybierz konto do usunięcia.", color=0xdaa454, timestamp=ctx.message.created_at)
                    embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
                    embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
                    await ctx.send(embed=embed, view=DziennikSetup.SelectConfirm_Button(ctx))
                    return
            elif (pathlib.Path.exists(path) and pathlib.Path.exists(path2)): #If user isn't owner, has user account
                    mode = "user"
                    description = "Czy potwierdzasz usunięcie konta użytkownika?"
            elif (not pathlib.Path.exists(path)) and (not pathlib.Path.exists(path2)): #If user isn't owner, has no account
                await ctx.send(f"Nie posiadasz ustawionego konta!")
                return
            else:
                dziennik_log.error("Wystąpił błąd! [DziennikSetup - %s]", sys._getframe().f_lineno)
                await ctx.send(f"Wystąpił błąd! [DziennikSetup - {sys._getframe().f_lineno}]")
                return
            embed=discord.Embed(description=description, color=0xdaa454, timestamp=ctx.message.created_at)
            embed.set_author(name="Wirtualny Asystent Lekcyjny w Pythonie")
            embed.set_footer(text=f"{footer} | dla {ctx.author.name}#{ctx.author.discriminator}", icon_url=footer_img)
            await ctx.send(embed=embed, view=DziennikSetup.Confirm_Button(ctx, mode))
            

    class Confirm_Button(discord.ui.View):
        def __init__(self, ctx, mode):
            super().__init__()
            self.ctx = ctx
            self.mode = mode

        @discord.ui.button(label="Tak", style=discord.ButtonStyle.green)
        async def tak(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
                dziennik_log.info("Użytkownik %s#%s (%s) potwierdził usunięcie konta %s.", self.ctx.author.name, self.ctx.author.discriminator, self.ctx.author.id, self.mode)
                await interaction.response.send_message(f'{await DziennikSetup.DeleteAccount(DziennikSetup, interaction.user.id, self.mode)}', ephemeral=True)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
        
        @discord.ui.button(label="Nie", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await self.ctx.message.delete()
                dziennik_log.debug("Użytkownik %s#%s (%s) anulował usunięcie konta %s.", self.ctx.author.name, self.ctx.author.discriminator, self.ctx.author.id, self.mode)
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    class SelectConfirm_Button(discord.ui.View):
        def __init__(self, ctx):
            super().__init__()
            self.ctx = ctx

        @discord.ui.button(label="Globalne", style=discord.ButtonStyle.blurple)
        async def globalne(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
                dziennik_log.info("Użytkownik %s#%s (%s) potwierdził usunięcie globalnego konta.", self.ctx.author.name, self.ctx.author.discriminator, self.ctx.author.id)
                await interaction.response.send_message(f'{await DziennikSetup.DeleteAccount(DziennikSetup, interaction.user.id, "global")}', ephemeral=True)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
        
        @discord.ui.button(label="Użytkownika", style=discord.ButtonStyle.gray)
        async def uzytkownika(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await interaction.message.delete()
                dziennik_log.info("Użytkownik %s#%s (%s) potwierdził usunięcie konta użutkownika.", self.ctx.author.name, self.ctx.author.discriminator, self.ctx.author.id)
                await interaction.response.send_message(f'{await DziennikSetup.DeleteAccount(DziennikSetup, interaction.user.id, "user")}', ephemeral=True)
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)
        
        @discord.ui.button(label="Anuluj", style=discord.ButtonStyle.red)
        async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.ctx.author == interaction.user:
                await self.ctx.message.delete()
                dziennik_log.debug("Użytkownik %s#%s (%s) anulował usunięcie konta %s.", self.ctx.author.name, self.ctx.author.discriminator, self.ctx.author.id, self.mode)
                await interaction.message.delete()
            else:
                await interaction.response.send_message('Brak uprawnień!', ephemeral=True)

    async def DeleteAccount(self, id, mode):
        if mode == "global":
            if str(id) != str(owner_id):
                return "Brak uprawnień! Nie możesz usunąć globalnego konta."
            path = pathlib.Path(f'db/acc-config.json')
            path2 = pathlib.Path(f'db/key-config.json')
            if (pathlib.Path.exists(path)) and (pathlib.Path.exists(path2)):
                try: 
                    pathlib.Path.unlink(path)
                    pathlib.Path.unlink(path2)
                    dziennik_log.info("Globalne konto zostało usunięte.")
                    return "Usunięto globalne konto."
                except Exception as e:
                    dziennik_log.error("Wystąpił błąd podczas usuwania globalnego konta! Treść: \n%s", e)
                    return f"**Wystąpił błąd podczas usuwania globalnego konta!** Treść: \n```{e}```"
        if mode == "user":
            path = pathlib.Path(f'db/{id}/acc-config.json')
            path2 = pathlib.Path(f'db/{id}/key-config.json')
            if (pathlib.Path.exists(path)) and (pathlib.Path.exists(path2)):
                try: 
                    pathlib.Path.unlink(path)
                    pathlib.Path.unlink(path2)
                    dziennik_log.info("Konto użytkownika %s zostało usunięte.", id)
                    return "Usunięto konto użytkownika."
                except Exception as e:
                    dziennik_log.error("Wystąpił błąd podczas usuwania konta użytkownika %s! Treść: \n%s", id, e)
                    return f"**Wystąpił błąd podczas usuwania konta {id}!** Treść: \n```{e}```"
            elif (not pathlib.Path.exists(path)) and (not pathlib.Path.exists(path2)):
                return f"Nie posiadasz ustawionego konta!"
            else:
                dziennik_log.error("Wystąpił błąd! [DziennikSetup - %s]", sys._getframe().f_lineno)
                return f"Wystąpił błąd! [DziennikSetup - {sys._getframe().f_lineno}]"
        

    async def RegisterAccount(self, id, token, symbol, pin, mode):
        if (mode == "global") or dziennik_mode == "global":
            path = pathlib.Path(f'db/')
            path.mkdir(parents=True, exist_ok=True)
            keystore = Keystore.create(device_model=f"WALP - {api_name} [G]")
            with open(f'db/key-config.json', "w") as f:
                # write a formatted JSON 
                f.write(keystore.as_json)
            account = await Account.register(keystore, token, symbol, pin)
            with open(f'db/acc-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(account.as_json)
            dziennik_log.info("Konto oraz API zostało zarejestrowane w trybie Global.")
            return "Konto oraz API zostało zarejestrowane w trybie Global."
        if (mode == "user") or dziennik_mode == "user":
            path = pathlib.Path(f'db/{id}/')
            path.mkdir(parents=True, exist_ok=True)
            keystore = Keystore.create(device_model=f"WALP - {api_name}")
            with open(f'db/{id}/key-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(keystore.as_json)
            account = await Account.register(keystore, token, symbol, pin)
            with open(f'db/{id}/acc-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(account.as_json)
            dziennik_log.info("Konto i API użytkownika %s zostało zarejestrowane.", id)
            return "Konto oraz API zostało zarejestrowane."
        
    async def GetAccount(id, silent=False):
        if dziennik_mode == "both":
            path = pathlib.Path(f'db/{id}/acc-config.json')
            if pathlib.Path.exists(path):
                with open(f"db/{id}/acc-config.json") as f:
                    dziennikAccount = f.read()
                    if silent == False:
                        print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Account of {id} loaded...")
                        dziennik_log.debug("Account of %s loaded...", id)
                    return dziennikAccount
            else:
                with open("db/acc-config.json") as f:
                    dziennikAccount = f.read()
                    if silent == False:
                        print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global account loaded...")
                        dziennik_log.debug("Global account loaded...")
                    return dziennikAccount
        elif dziennik_mode == "global":
            with open("db/acc-config.json") as f:
                dziennikAccount = f.read()
                if silent == False:
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global account loaded...")
                    dziennik_log.debug("Global account loaded...")
                return dziennikAccount
        elif dziennik_mode == "user":
            with open(f"db/{id}/acc-config.json") as f:
                dziennikAccount = f.read()
                if silent == False:
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Account of {id} loaded...")
                    dziennik_log.debug("Account of %s loaded...", id)
                return dziennikAccount
        else: 
            temp = "Dziennik mode uległ zmianie od momentu uruchomienia bota. Anulowanie funkcji"
            print(temp)
            dziennik_log.error(temp)
            return False

    async def GetKeystore(id, silent=False):
        if dziennik_mode == "both":
            path = pathlib.Path(f'db/{id}/key-config.json')
            if pathlib.Path.exists(path):
                with open(f"db/{id}/key-config.json") as f:
                    dziennikKeystore = f.read()
                    if silent == False:
                        print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Keystore of {id} loaded...")
                        dziennik_log.debug("Keystore of %s loaded...", id)
                    return dziennikKeystore
            else:
                with open("db/key-config.json") as f:
                    dziennikKeystore = f.read()
                    if silent == False:
                        print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global keystore loaded...")
                        dziennik_log.debug(f"Global keystore loaded...")
                    return dziennikKeystore
        elif dziennik_mode == "global":
            with open("db/key-config.json") as f:
                dziennikKeystore = f.read()
                if silent == False:
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global keystore loaded...")
                    dziennik_log.debug(f"Global keystore loaded...")
                return dziennikKeystore
        elif dziennik_mode == "user":
            with open(f"db/{id}/key-config.json") as f:
                dziennikKeystore = f.read()
                if silent == False:
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Keystore of {id} loaded...")
                    dziennik_log.debug("Keystore of %s loaded...", id)
                return dziennikKeystore
        else: 
            # await ErrorHandler.Report(DziennikSetup.bot, f"Dziennik mode uległ zmianie od momentu uruchomienia bota. Anulowanie funkcji.", "Dziennik Setup/GetKeystore", "170")
            temp = "Dziennik mode uległ zmianie od momentu uruchomienia bota. Anulowanie funkcji"
            print(temp)
            dziennik_log.error(temp)
            return False
                
def setup(bot):
    bot.add_cog(DziennikSetup(bot))