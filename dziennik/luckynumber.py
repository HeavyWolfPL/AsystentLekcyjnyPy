import json
import re
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

async def get_luckynumber():
    
    with open("key-config.json") as f:
        # load from a JSON string
        dziennikKeystore = Keystore.load(f.read())
    with open("acc-config.json") as f:
        # load from a JSON string
        dziennikAccount = Account.load(f.read())
    dziennikClient = Vulcan(dziennikKeystore, dziennikAccount)
    await dziennikClient.select_student()  # select the first available student
    print(dziennikClient.student)  # print the selected student
    students = await dziennikClient.get_students()
    dziennikClient.student = students[1]  # select the second student   
    lucky_number = await dziennikClient.data.get_lucky_number()
    await dziennikClient.close()
    print(f'{str(lucky_number)}')
    number = re.search('number=(.+?)\)', str(lucky_number))
    if number:
        lucky_number = number.group(1)
    return lucky_number