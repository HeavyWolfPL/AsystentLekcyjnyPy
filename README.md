# Wirtualny Asystent Lekcyjny w Pythonie -  WALP

Bot łączący się z API dziennika Vulcan UONET+ uzyskując w ten sposób różne informacje.

## Instalacja
### **Wymagania**
- [Python 3.7.8+](https://www.python.org/downloads/release/python-378/)
- [Discord.py 1.7.3+](https://github.com/Rapptz/discord.py/tree/v1.7.3)
- [Tabulate](https://pypi.org/project/tabulate/)
- [Vulcan-API](https://github.com/kapi2289/vulcan-api)

### **Tokeny**
Skopiuj plik config-example.json, wklej tam poprawne tokeny, a następnie zmień jego nazwę na `config.json`

### **Komendy**
*W przypadku uczęszczania do obu szkół, używane będą dane tylko z pierwszej.*

- !plan <dzień>
> Wyświetla plan lekcji ucznia z danego dnia.
> Aliasy: `lekcje`, `planlekcji`
- !frekwencja <dzień>
> Wyświetla frekwencję ucznia z danego dnia. 
> Aliasy: `obecność`, `obecnosc`
- !oceny
> Wyświetla wszystkie oceny z aktualnego półrocza.
> Alias: `grades`
- !ocena <id oceny>
> Wyświetla szczegółowe informacje o ocenie. 
> Alias: `grade`
- !numerek
> Wysyła szczęśliwy numerek z dzisiejszego dnia.
> Aliasy: `numer`, `szczęśliwynumerek`, `szczesliwynumerek`, `luckynumber`
- !homework
> Wyświetla zadania domowe na aktualny tydzień.
> Aliasy: `zadania_domowe`, `zadane`, `zadaniadomowe`, `zaddom`, `hw`

---

### To-Do
- Wersja globalna, jeden bot dla wszystkich uczniów poprzez przypisywanie tokenów do konta Discord,
- Lepszy error handling,
- Debug mode,
- Wersja discord.js,
- Discord.py v2.0,
- Informacje o zakończeniu lekcji (dzwonku),
- Wersja self-hosted dla danej klasy, wyświetlająca w statusie aktualną lekcję.
