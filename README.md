# Mistrz Klawiatury

## Wstęp

Mistrz klawiatury to gra polegająca na przepisywaniu wyświetlanych wyrazów w jak najkrótszym czasie. Wykorzystuje ona moduł ```pygame``` oraz bazę danych sqlite3.

## Uruchomienie

Aby włączyć grę, należy w katalogu ```PLAN_MISZCZ``` wykonać następujący skrypt:

```bash
    MAIN.py
```

## Struktura aplikacji

## ```MAIN.py```

W pliku ```MAIN.py``` zostały zdefiniowane funkcje inicjalizacyjne, które odpowiadają za przygotowanie wszystkich niezbędnych zmiennych oraz bazy danych do rozgrywki, wyniki z poprzedniego dnia trafiają do tabeli w bazie odpowiadającej za rejestrowanie wyników z całego tygodnia.

### ```do_order_in_database()```

```python
    cu.execute("SELECT nick FROM players")
    nicks = []
    nicks_from_db = cu.fetchall()
    for el in nicks_from_db:
        nicks.append(el[0])

    for playerdb in nicks:
        cu.execute(
            "SELECT SUM(\"score\"), \"date\" FROM " + playerdb + "_stat_today GROUP BY \"date\"")
        stats_from_today = cu.fetchall()
        for el in stats_from_today:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_week (\"score\", \"date\") VALUES (" + str(el[0]) + ", \"" + str(
                    el[1]) + "\")")
            cx.commit()

        cu.execute(
            "select strftime(\'%m\',\"date\") as \"miesiac\", sum(\"score\") as \"wynik\" from " + playerdb + "_stat_week group by strftime(\'%m\',\"date\")")
        stats_from_week = cu.fetchall()
        print(stats_from_week)
        for el in stats_from_week:
            cu.execute(
                "INSERT INTO " + playerdb + "_stat_month (\"score\", \"date\") VALUES (" + str(el[1]) + ", \"" + str(
                    el[0]) + "\")")
            cx.commit()
        cu.execute("DELETE FROM " + playerdb + "_stat_today")
        cx.commit()
```
Funkcja ```do_order_in_database``` pobiera z tabeli ```<player>_stat_today``` wyniki, następnie grupuje je po dacie, a wyniki sumuje, po czym wstawia je do tabeli ```<player>_stat_week```, a w końcu stosuje polecenie ``` DELETE``` do wyczyszczenia zawartości pierwszej z tabel. Dzieje się tak dla każdego gracza.

### ```window_maker()```

```python
    size_x = 1200
    size_y = 650
    global screen
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("Miszcz Klawiatury")
    icon = pygame.image.load('klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))
```
Funkcja odpowiada za utworzenie okna, w którym będą wyświetlane wybrane ramki.

### ```main()```

```python
    pygame.init()
    do_order_in_database()
    window_maker()
    global player
    player = choose_player()
    functions = {'sta': show_statistics,
                 'ler': game_loop_learn,
                 'cha': game_loop_chalange,
                 'log': choose_player,
                 'qui': exit}
    while True:
        option = main_window()
        args = option[1:]
        code = option[0]
        if bool(args):
            functions[code](args)
        else:
            functions[code]()
```

W funkcji ```main()``` po kolei zostają wywoływane funkcje, które odpowiadają za poprawną inicjalizację aplikacji.

## ```Game.py```

W tym module zaimplementowana została cała logika rozgrywki, jak na przykład losowanie wyrazów.

### ```save_score(level, score, nick)```

```python
    score_to_db = str(score * level)
    cu.execute("insert into " + nick + "_stat_today (score,date) values (" + score_to_db + ",date('now'))")
    cu.execute("insert into " + nick + "_stat_ever (score,date) values (" + score_to_db + ",date('now'))")
    cx.commit()
    print('Score saved.')
```

Powyższa funkcja przyjmuje 3 argumenty: ```level, score, nick```, gdzie ```level``` to liczba z zakresu 1-3 (1 - łatwy, 2 - trudny, 3 - średni), dwa pozostałe są oczywiste. Następnie wynik i poziom trudności są mnożone i wstawianie do tabeli z dnia obecnego ( ```<player>_stat_today``` ) oraz do tabeli historycznej, która agreguje wszystkie wyniki od początku ( ```<player>_stat_ever``` ).

## ```Statistics.py```

### ```download_input(period, nick)```

```python
    period_dict = {1: "today", 2: "week", 3: "month", 4: "ever"}
    period_scores = None
    cu.execute(
        "select rowid, date, score from " + nick + "_stat_" + period_dict[period] + " ORDER BY \"date\" DESC LIMIT 10")
    cx.commit()
    period_scores = cu.fetchall()
    return period_scores
```

```download_input()``` służy do pobierania z bazy danych wyników dla dowolnego gracza za wybrany okres (dzień, tydzień, miesiąc, od początku), wymaga ona podania jako argumentów nicku gracza oraz wartości liczbowej przypisanej danemu okresowi. Jakie są to wartości, widać w pierwszej linii. Funkcja zwraca listę trójelementowych krotek, każda w formacie (numer wiersza, data , wynik).

## ```Login.py```

Tu zawarta została mechanika logowania, oraz inicjalizacji nowego gracza.

### ```choose_player()```

```python

    # Zmienne pomocnicze

    gracze = download_users()
    font = pygame.font.Font('freesansbold.ttf', 50)
    zaznaczenie = 0
    len_gracze = len(gracze)

    # Ustawienia Okna
    screen.fill((255, 255, 255))

    # Pętla programu

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if zaznaczenie != len_gracze:
                            for x in gracze.keys():
                                check_pass(x, gracze[x], screen)
                        else:
                            sign_up(screen)
                    elif (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                        if zaznaczenie == 0:
                            zaznaczenie = len_gracze
                        else:
                            zaznaczenie -= 1
                    elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                        if zaznaczenie == len_gracze:
                            zaznaczenie = 0
                        else:
                            zaznaczenie += 1

        # wypisanie nazw
        n = 0
        instr = font.render("Wybór gracza:", True, (0, 0, 0), (255, 255, 255))
        screen.blit(instr, (100, 100))
        for gracz in gracze.keys():
            for nazwa in gracz:
                nazwa_ = nazwa
            if zaznaczenie == n:
                wypis = font.render(nazwa_, True, (0, 0, 0), (175, 255, 100))
            else:
                wypis = font.render(nazwa_, True, (0, 0, 0), (255, 255, 255))
            screen.blit(wypis, (115, (n * 60 + 160)))
            n += 1
        dodaj = font.render("+ Nowy gracz", True, (0, 0, 0),
                            ((175, 255, 100) if zaznaczenie == n else (255, 255, 255)))
        screen.blit(dodaj, (115, (n * 60 + 160)))
        pygame.display.flip()
```

Funkcja wyświetlająca menu wyboru gracza. Jako parametr przyjmuje okno, na którym rysuje. Pozwala na wybranie przy pomocy klawiatury jednego z listy graczy pobranej z bazy, lub na utworzenie nowego. Zwraca nazwę wybranego użytkownika.

### ```download_users()```

```python
    cu.execute("SELECT nick, password FROM players")
    cx.commit()
    gracze = cu.fetchall()
    nicknames = []
    passwords = []

    for el in gracze:
        nicknames.append(el[0])
        passwords.append(el[1])

    gracze = dict(zip(nicknames, passwords))
    return gracze
```

Funkcja może być wywołana, aby sprawdzić, czy logujący się użytkownik jest już w bazie, pobiera ona listę nicków oraz haseł, a nastęnie zwraca je w formie słownika, gdzie klucz to nick, a wartość to hasło.

### ```add_player(nick, password)```

```python
    cu.execute("SELECT COUNT(*) FROM players WHERE nick==?", (nick,))
    cx.commit()
    result = cu.fetchone()
    if result == (0,):
        cu.execute("INSERT INTO players (nick, password) VALUES (?,?)", (nick, password))
        cx.commit()
        cu.execute(
            "CREATE TABLE " + nick + "_stat_today (id integer primary key, score int, date text)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_week (id integer primary key, score int, date text)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_month (id integer primary key, score int, date text)")
        cu.execute(
            "CREATE TABLE " + nick + "_stat_ever (id integer primary key, score int, date text)")
        return True
    else:
        return False
```

Funkcja służy do dopisywania nowego gracza do bazy, jako poarametry przyjmuje nick, oraz hasło, które może być alfanumeryczne, następnie przeszukuję tabelę z użytkownikami w poszukiwaniu powtórzeń nicku, jeżeli nie znajdzie, zostaną utworzone cztery tabele na zapisywanie statystyk danego gracza, a sama funkcja zwróci wartość ```python True```, w przeciwnym wypadku, tabela nie zostaną utowrzone i zostanie zwrócone ```python False```.
