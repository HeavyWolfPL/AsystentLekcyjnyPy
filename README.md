# Wirtualny Asystent Lekcyjny w Pythonie -  WALP

Bot łączący się z API dziennika Vulcan UONET+ uzyskując w ten sposób różne informacje.

## Instalacja
### **Wymagania**
- [Python 3.8.10+](https://www.python.org/downloads/release/python-378/)
- [Discord.py 2.0.0a+](https://github.com/Rapptz/discord.py/)
- [Tabulate](https://pypi.org/project/tabulate/)
- [Vulcan-API](https://github.com/kapi2289/vulcan-api)

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

- RODO
> Nazwa tej opcji powinna częściowo tłumaczyć jej funkcjonalność. Ustawienie tej opcji na `"true"` w przypadku trybów `global` oraz `both` spowoduje wyłączenie komend, które mogą zawierać dane które mogą być uznane za osobiste. Opcja ta ignoruje osobę zarządzająca. Aktualnie są to `!oceny`, `!ocena` oraz `!frekwencja`.
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
- Debug mode,
- Wersja discord.js,
- Informacje o zakończeniu lekcji (dzwonku),
- Wersja self-hosted dla danej klasy, wyświetlająca w statusie aktualną lekcję.
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
#### Nie dodawaj swojego tokenu botowi, któremu nie ufasz. Ten bot nigdy nie został zaprojektowany by być bezpiecznym. <br>Rozważ użycie [wersji oficjalnej]("https://github.com/HeavyWolfPL/AsystentLekcyjnyPy/") bota, nie jest ona w pełni open-source. Kod odpowiadający za szyfrowanie jest niepubliczny, a wszystkie tokeny są trzymane na prywatnym serwerze z dostępem tylko jednej osoby.