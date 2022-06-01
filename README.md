# Wirtualny Asystent Lekcyjny w Pythonie -  WALP

Bot łączący się z API dziennika Vulcan UONET+ uzyskując w ten sposób różne informacje.

## Instalacja
### **Wymagania**
- [Python 3.8.10+](https://www.python.org/downloads/release/python-3810/)
- [Discord.py 2.0.0a+](https://github.com/Rapptz/discord.py/)
- [Tabulate](https://pypi.org/project/tabulate/)
- [Vulcan-API](https://github.com/kapi2289/vulcan-api)
- Pozostałe pakiety
<details>
<summary>Pakiety</summary>
aenum==3.1.11
aiodns==3.0.0
aiohttp==3.8.1
aiosignal==1.2.0
async-timeout==4.0.2
attrs==21.4.0
cchardet==2.1.7
cffi==1.15.0
charset-normalizer==2.0.12
cryptography==37.0.2
discord.py @ git+https://github.com/Rapptz/discord.py@348764583d95265f40b8a683e2f8ac73d6c173f5
frozenlist==1.3.0
future==0.18.2
idna==3.3
multidict==6.0.2
pycares==4.1.2
pycparser==2.21
pyOpenSSL==22.0.0
python-dateutil==2.8.2
pytz==2022.1
PyYAML==6.0
related==0.7.2
six==1.16.0
tabulate==0.8.9
uonet-request-signer-hebe==0.1.1
vulcan-api==2.1.1
yarl==1.7.2
</details>

### **Tokeny**
Skopiuj plik config-example.json, wklej tam poprawne tokeny, a następnie zmień jego nazwę na `config.json`

---

### **Komendy**
*W przypadku uczęszczania do obu szkół, używane będą dane tylko z pierwszej.*
<details>
<summary>Lista Komend</summary>

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

</details>

---

### **Plik konfiguracyjny**
<details>
<summary>Dokumentacja</summary>

- prefix
> Sama nazwa wskazuje na funkcję tej linii. 
> <br>Domyślna wartość - `"!"`

- token
> Token wymagany do uruchomienia bota. Uzyskasz go tworząc bota na [tej](https://discord.com/developers/applications 'Kliknij mnie!') stronie.
> <br>**Nie podawaj go nikomu.**
> <br>Domyślna wartość - `"TOKEN_GOES_HERE"`

- ownerID
> Pole zawierające Discord ID osoby zarządzacej botem. Uprawnia do ustawienia globalnych tokenów.
> <br>Domyślna wartość - `"00000000000"`

- errorChannel
> Zawiera ID Kanału na który wysyłane są wszystkie błędy, które występują podczas działania bota. 
> <br>Zalecane jest, by kanał był dostępny tylko dla osoby zarządzającej botem.
> <br>Domyślna wartość - `"00000000000"`

- debug
> Opcja używana do znalezenia błędów. Włączenie tej opcji spowoduje wysyłanie znacznie większej ilości logów do konsoli.
> <br>Domyślna wartość - `"false"`

**Konfiguracja Dziennika**

- dziennik_mode
> Tryb użytkowania dziennika. Posiada 3 opcje; `"global"`, `"user"` oraz `"both"`.
> <br>Opcja `"global"` oznacza ustawienie tokenu przez osobę zarządzającą. Informacje z dziennika będą pobierane z jej konta, zgodnie z ustawieniem `RODO`.
> <br>Opcja `"user"` zmusza każdego użytkownika do dodania własnego tokenu do bota poprzez komendę. 
> <br>Opcja `"both"` to hybryda obu powyższych opcji. Jeśli użytkownik nie ma ustawionego tokenu, użyty zostanie token globalny, zgodnie z ustawieniem `RODO`.

- api_name
> Nazwa API w interfejsie dziennika w celu łatwego rozróżnienia. Dodawana do nazwy bota, oznacza to że cała nazwa będzie brzmieć:
> <br>`Wirtualny Asystent Lekcyjny w Pythonie - <api_name>`. Dodatkowo do nazwy dodane zostanie [G] jeśli konto jest globalne.

- RODO
> Nazwa tej opcji powinna częściowo tłumaczyć jej funkcjonalność. Ustawienie tej opcji na `"true"` w przypadku trybów `global` oraz `both` spowoduje wyłączenie komend, które mogą zawierać dane które mogą być uznane za osobiste. Opcja ta ignoruje osobę zarządzająca. Aktualnie są to `!oceny`, `!ocena` oraz `!frekwencja`.
> <br>Domyślna wartość - `"true"`

- dziennik_lessonstatus
> Wyświetlanie aktualnej lekcji w statusie bota. Domyślnie aktualizuje się co 60 sekund.
> <br>Domyślna wartość - `"true"`

**Konfiguracja Embedów**

- footerCopyright
> Tekst wyświetlany w stopce embedów.
> <br>Domyślna wartość - `"Wafelowski.dev"`

- footerCopyrightImage
> Zawiera URL obrazka, który będzie wyświetlany w stopce embeda.
> <br>Domyślna wartość - `"https://i.imgur.com/g3a3tLo.png"`

</details>

---

### To-Do
- Wersja globalna, jeden bot dla wszystkich uczniów poprzez przypisywanie oraz szyfrowanie tokenów do konta Discord,
- Lepszy error handling,
- Wersja discord.js,
- Informacje o zakończeniu lekcji (dzwonku),
- Konfiguracja per-user (możliwość wyboru szkoły, studenta, wysyłanie wrażliwych komend poprzez DM)

---

### Uznanie Autorstwa
Podziękowania dla:
- Kapi2289 za [Vulcan-API](https://github.com/kapi2289/vulcan-api),
- Team [Wulkanowy](https://wulkanowy.github.io) za skradzione od nich pomysły, m.in. na przetworzenie informacji,
- Majroch za kod [planu Lekcji](https://github.com/Majroch/plan-lekcji), na którym do teraz bazuję,
- UONET+ za dziennik Vulcan ~~i zepsucie marzeń dzieciom~~,

--- 

## **Uwaga**

#### Wszelkie informacje logowania nie są w jakikolwiek sposób szyfrowane przed dostępem innych osób zewnętrznych lub nie, mogących otworzyć te pliki. Dodajesz swój token na **WŁASNĄ** odpowiedzialność. Pozwala to na prawie pełny dostęp do dziennika, taka osoba może wysyłać wiadomości bez potrzeby znania hasła, może również uzyskać twoje dane personalne.
#### Nie dodawaj swojego tokenu botowi, któremu nie ufasz. Ten bot nigdy nie został zaprojektowany by być bezpiecznym. <br>Rozważ użycie [wersji oficjalnej (Work in Progress)]("https://github.com/HeavyWolfPL/AsystentLekcyjnyPy/") bota, nie jest ona w pełni open-source. Kod odpowiadający za szyfrowanie jest niepubliczny, a wszystkie tokeny są trzymane na prywatnym serwerze z dostępem tylko jednej osoby.