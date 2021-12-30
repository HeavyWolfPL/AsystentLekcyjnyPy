import datetime
import discord, os, json, time
from vulcan import Account
from vulcan import Keystore
from vulcan import Vulcan
from discord.ext import commands
from discord.ext.tasks import loop
from asyncio import sleep
from cogs.dziennik.dziennik_setup import DziennikSetup

# Get configuration.json
with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    owner_id = data["ownerID"]
    lessonStatus = data["dziennik_lessonStatus"]

if token == "TOKEN":
    print("Ustaw token bota!")
    exit()

def __init__(self, bot):
    self.bot = bot
    self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
# The bot
bot = commands.Bot(command_prefix=str(prefix), intents = intents)
bot.help_command = None

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"[Cogs] Loaded - {filename[:-3]}")
    for filename in os.listdir("cogs/dziennik"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.dziennik.{filename[:-3]}")
            print(f"[Dziennik Cogs] Loaded - {filename[:-3]}")

######################
## Config validator ##
######################

async def config_validator():
    with open("config.json", "r") as config: 
        data = json.load(config)
        dziennik_mode = data["dziennik_mode"]
    if dziennik_mode not in ["user", "global", "both"]:
        return False
    else:
        return True
    
@loop(seconds=60)
async def lesson_status():
    try:
        dziennikKeystore = Keystore.load(await DziennikSetup.GetKeystore(owner_id, True))
        dziennikAccount = Account.load(await DziennikSetup.GetAccount(owner_id, True))
    except FileNotFoundError:
        return f"[Dziennik Status Lekcji] Nie znaleziono danych dla globalnego konta dziennika! Upewnij sie, ze owner_id jest prawidlowe oraz jest ustawiony globalny klucz."
    dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)
    await dziennikClient.select_student()

    target_date = datetime.date.today()
    now = datetime.datetime.now()
    ctime = datetime.time(now.hour, now.minute)
    
    lessons = await dziennikClient.data.get_lessons(date_from=target_date)
    tmp = []
    all_info = {}

    async for lesson in lessons:
        tmp.append(lesson)
    lessons = tmp
    await dziennikClient.close()

    if lessons == []:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name ="dzień wolny"))
        await sleep(900)

    for lesson in lessons:
        if lesson.visible:
                all_info[lesson.time.position] = [lesson]

    lessonFound = False
    for key in sorted(all_info):
        lesson = all_info[key][0]
        if ((lesson.time.from_ <= ctime) & (lesson.time.to > ctime)):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=lesson.subject.name))
            lessonFound = True
            break
    
    if lessonFound == False:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="przerwa"))

##################
### Bot events ###
##################


    

@bot.event
async def on_ready():
    print(f"""Zalogowano jako {bot.user}
Discord.py - {discord.__version__}
Bot by Wafelowski.dev""")
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name ="lekcje"))
    x = await config_validator()
    if (x == False):
        print("Konfig zawiera nieodpowiedni `dziennik_mode`. Wybierz jeden z trzech dostępnych: \n- user (każdy użytkownik musi dodać swoje tokeny) \n- global (administrator bota dodaje swój token) \n- both (gdy użytkownik nie posiada dodanego własnego tokenu, użyje tokenu administratora*)\n\n* Obowiązują ograniczenia co do komend.")
        # await ErrorHandler.Report(bot, f"Konfig zawiera nieodpowiedni `dziennik_mode`. Wybierz jeden z trzech dostępnych: \n- user (każdy użytkownik musi dodać swoje tokeny) \n- global (administrator bota dodaje swój token) \n- both (gdy użytkownik nie posiada dodanego własnego tokenu, użyje tokenu administratora*)\n\n* Obowiązują ograniczenia co do komend.", "Validator Konfigu", "69")
        exit()
    else:
        print("[Validator Konfigu] Brak błędów.")
    if lessonStatus == True:
        print("[Dziennik] Status Aktywny")
        lesson_status.start()

    

#@bot.listen('on_message')
async def on_message(message):
    if message.author.id != bot.user.id:
        print("on_message event works!")
        

@bot.event
async def when_mentioned(bot, message):
    if message.author.id != bot.user.id:
        await message.channel.send(f"Hej {message.author}, mój prefiks to {prefix}.")

#@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Witaj {member.mention}.'.format(member))

#@bot.event
async def on_reaction_add(reaction, user):
    channel = bot.get_channel(596428386100838400)
    await channel.send(f'Reakcja - {reaction}. User - {user}')

@bot.event
async def on_command_error(ctx, error):
    print(ctx)
    print(error)
    # await ErrorHandler.Report(bot, f"{ctx}", "on_command_error - Part 1", "X")
    # await ErrorHandler.Report(bot, f"{error}", "on_command_error - Part 2", "X")
    raise error

##################
## Bot commands ##
##################

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    msg = await ctx.channel.send("🏓 Pong !")
    ping = (time.monotonic() - before) * 1000
    await msg.edit(content=f"🏓 Pong !  `{int(ping)} ms`")

@bot.command(aliases=["wyłącz", "wylacz", "off"])
async def shutdown(ctx):
    if ctx.author.id == owner_id:
        await ctx.channel.send("Okej")
        exit()

@bot.command(aliases=["przeładuj", "przeladuj"])
async def reload(ctx, arg1):
    if ctx.author.id == owner_id:
        try:
            bot.reload_extension(arg1)
            ctx.send("Przeładowano pomyślnie!")
        except Exception as e:
            await ctx.channel.send(f"**Nie udało się przeładować coga!** Treść: ```\n{e}```")

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        error = error.original
    if isinstance(error, commands.errors.MissingRequiredArgument):
        if error.param.name == "arg1":
            await ctx.send("Nie podano nazwy coga!")
    elif isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("Brak uprawnień!")
        raise error
    else:
        await ctx.send(f"**Wystąpił błąd!** Treść: \n```{error}```")

bot.run(token)