import json, datetime, pathlib
from discord.ext import commands
from vulcan import Keystore, Account, Vulcan

with open("config.json", "r") as config:
    data = json.load(config)
    prefix = data["prefix"]
    owner_id = data["ownerID"] 
    dziennik_mode = data['dziennik_mode']
    if dziennik_mode == "global":
        dziennikToken = data["dziennikToken"]
        dziennikSymbol = data["dziennikSymbol"]
        dziennikPin = data["dziennikPIN"]

class DziennikSetup(commands.Cog, name='Ustawienia modułu dziennika'):
    def __init__(self, bot):
        self.bot = bot

    bot = commands.Bot(command_prefix=prefix)

    if dziennik_mode == "both":
        @bot.command(name='setup')
        async def setupcmd(self, ctx, arg1, arg2, arg3, arg4):
            #await ctx.message.delete()
            availableModes = "user"
            if str(ctx.author.id) == str(owner_id):
                availableModes = "user i global"
            if arg1 not in "user global":
                await ctx.channel.send(f"Musisz podać tryb, dla którego chcesz ustawić passy. \nDostępne: `{availableModes}`")
                return
            if (arg1 == "global") and ("global" not in availableModes):
                await ctx.channel.send("Nie posiadasz uprawnień do danych logowania.")
                return
            if len(arg2) != 7:
                await ctx.channel.send("Błędny token.")
                return
            if len(arg3) < 1:
                await ctx.channel.send("Błędny symbol.")
                return
            if len(arg4) != 6:
                await ctx.channel.send("Błędny numer PIN.")
                return
            if arg1 == "user":
                await ctx.channel.send(await self.RegisterAccount(ctx.author.id, arg2, arg3, arg4, "user"))
            if arg1 == "global":
                await ctx.channel.send(await self.RegisterAccount(ctx.author.id, arg2, arg3, arg4, "global"))
    else:
        @bot.command(name='setup')
        async def setupcmd(self, ctx, arg1, arg2, arg3):
            await ctx.message.delete()
            if (dziennik_mode == "global") and str(ctx.author.id) != str(owner_id):
                await ctx.channel.send("Nie posiadasz uprawnień do danych logowania.")
                return
            if len(arg1) != 7:
                await ctx.channel.send("Błędny token.")
                return
            if len(arg2) < 1:
                await ctx.channel.send("Błędny symbol.")
                return
            if len(arg3) != 6:
                await ctx.channel.send("Błędny numer PIN.")
                return
            await ctx.channel.send(await self.RegisterAccount(ctx.author.id, arg1, arg2, arg3, dziennik_mode))

    @setupcmd.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if error.param.name == "arg1":
                availableModes = "user"
                if str(ctx.author.id) == str(owner_id):
                    availableModes = ["user", "global"]
                await ctx.channel.send(f"Musisz podać tryb, dla którego chcesz ustawić passy. \nDostępne: `{availableModes}`")
            if error.param.name == "arg2":
                await ctx.channel.send("Błędny token.")
            if error.param.name == "arg3":
                await ctx.channel.send("Błędny symbol.")
            if error.param.name == "arg4":
                await ctx.channel.send("Błędny numer PIN.")
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("Brak uprawnień!")
            raise error
        else:
            await ctx.send(f"Wystąpił błąd! **Treść**: \n```{error}```")

    async def RegisterAccount(self, id, token, symbol, pin, mode):
        if (mode == "global") or dziennik_mode == "global":
            path = pathlib.Path(f'db/')
            path.mkdir(parents=True, exist_ok=True)
            keystore = Keystore.create(device_model="Wirtualny Aystent Lekcyjny w Pythonie")
            with open(f'db/key-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(keystore.as_json)
            account = await Account.register(keystore, token, symbol, pin)
            with open(f'db/acc-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(account.as_json)
            return "Konto oraz API zostało zarejestrowane w trybie Global."
        if (mode == "user") or dziennik_mode == "user":
            path = pathlib.Path(f'db/{id}/')
            path.mkdir(parents=True, exist_ok=True)
            keystore = Keystore.create(device_model="Wirtualny Aystent Lekcyjny w Pythonie")
            with open(f'db/{id}/key-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(keystore.as_json)
            account = await Account.register(keystore, token, symbol, pin)
            with open(f'db/{id}/acc-config.json', "w") as f:
                # write a formatted JSON representation
                f.write(account.as_json)
            return "Konto oraz API zostało zarejestrowane."
        
    async def GetAccount(id):
        if dziennik_mode == "both":
            path = pathlib.Path(f'db/{id}/acc-config.json')
            if pathlib.Path.exists(path):
                with open(f"db/{id}/acc-config.json") as f:
                    dziennikAccount = f.read()
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Account of {id} loaded...")
                    return dziennikAccount
            else:
                with open("db/acc-config.json") as f:
                    dziennikAccount = f.read()
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global account loaded...")
                    return dziennikAccount
        elif dziennik_mode == "global":
            with open("db/acc-config.json") as f:
                dziennikAccount = f.read()
                print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global account loaded...")
                return dziennikAccount
        elif dziennik_mode == "user":
            with open(f"db/{id}/acc-config.json") as f:
                dziennikAccount = f.read()
                print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Account of {id} loaded...")
                return dziennikAccount
        else: 
            print("Dziennik mode uległ zmianie od momentu uruchomienia bota. Anulowanie funkcji")
            return False

    async def GetKeystore(id):
        if dziennik_mode == "both":
            path = pathlib.Path(f'db/{id}/key-config.json')
            if pathlib.Path.exists(path):
                with open(f"db/{id}/key-config.json") as f:
                    dziennikKeystore = f.read()
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Keystore of {id} loaded...")
                    return dziennikKeystore
            else:
                with open("db/key-config.json") as f:
                    dziennikKeystore = f.read()
                    print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global keystore loaded...")
                    return dziennikKeystore
        elif dziennik_mode == "global":
            with open("db/key-config.json") as f:
                dziennikKeystore = f.read()
                print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Global keystore loaded...")
                return dziennikKeystore
        elif dziennik_mode == "user":
            with open(f"db/{id}/key-config.json") as f:
                dziennikKeystore = f.read()
                print(f"[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Keystore of {id} loaded...")
                return dziennikKeystore
        else: 
            # await ErrorHandler.Report(DziennikSetup.bot, f"Dziennik mode uległ zmianie od momentu uruchomienia bota. Anulowanie funkcji.", "Dziennik Setup/GetKeystore", "170")
            print("Dziennik mode uległ zmianie od momentu uruchomienia bota. Anulowanie funkcji")
            return False
                
def setup(bot):
    bot.add_cog(DziennikSetup(bot))