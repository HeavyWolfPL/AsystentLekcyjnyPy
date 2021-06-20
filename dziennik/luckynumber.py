import asyncio
import nest_asyncio
import json
from vulcan import Vulcan
from vulcan import Account
from vulcan import Keystore

# Get configuration.json
with open("config.json", "r") as config: 
    data = json.load(config)
    prefix = data["prefix"]
    token = data["token"]
    # Dziennik
    dziennik_enabled = data["dziennik_enabled"]
    if dziennik_enabled:
        dziennikToken = data["dziennikToken"]
        dziennikSymbol = data["dziennikSymbol"]
        dziennikPin = data["dziennikPIN"]
        


if not dziennik_enabled:
    print("Dziennik is disabled, this function should not run.")

async def get_luckynumber():
    with open("dziennik-config.json", "w") as config: 
        dziennikKeystore = Keystore.create(device_model="Python Vulcan API")
        #json.dump(dziennikKeystore.as_dict, config)
        config.write(dziennikKeystore.as_json)
    with open("acc-config.txt", "w") as config2: 
        dziennikAccount = Account.register(dziennikKeystore, dziennikToken, dziennikSymbol, dziennikPin)
        #json.dump(dziennikAccount.as_json, config2)
        config2.write(f'{dziennikAccount}')
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(dziennikAccount)
    dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)
    lucky_number = await dziennikClient.data.get_lucky_number()
    await dziennikClient.close()
    return lucky_number