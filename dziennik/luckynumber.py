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
        dziennikKeystore = Keystore.create(device_model="Python Vulcan API")
        dziennikAccount = Account.register(dziennikKeystore, dziennikToken, dziennikSymbol, dziennikPin)
        #dziennikClient = Vulcan(keystoreDziennik, dziennikAccount)

if not dziennik_enabled:
    print("Dziennik is disabled, this function should not run.")

async def main():
    dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)
    lucky_number = await dziennikClient.data.get_lucky_number()
    return lucky_number