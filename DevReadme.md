# Zapisanie tokenów
```py
with open("dziennik-config.json", "w") as config: 
        dziennikKeystore = Keystore.create(device_model="Python Vulcan API")
        json.dump(dziennikKeystore.as_dict, config)
        config.write(dziennikKeystore.as_json)
```
To samo z account