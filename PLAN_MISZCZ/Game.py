import sqlite3

database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database)
cu = cx.cursor()


def pg_str_input():
    """
    #Ignacy
    odczytuje wciśnity na klawiaturze klawisz
    (funkcje należy umieśćić w pętli)
    uwzgldnia litery polskie,cyfry,cpacje,CAPS,SHIFT,BACKSPACE,ENTER
    funkcja do wklejenia w petle
    Ignacy to robi (prawie gotowe)
    :return: klawisz (klawisze) ktory został wciśnięty jako napis
    """

    """
    # Karol
    #czyści okno i rysuje swoje
    prowadzi grę w trybie wyzwanie czyli mierzy czas poprawnego wpisania wyrazu
    czysci okno (niech coś swojego rysuje)
    używa funkcji pg_str_input i chose_word
    wyswietla napis który ma zostać wpisany
    nie pozwala wpisywac wyrazu dluzszego niz przewidziany - zapala kontrolke z komunikatem
    wyswietla litery wpisywane wraz z podświetleniem na kolor zielony - ok / czerwony - błędny wpis
    mierzy czas wpisywania wyrazu od naciśnięcia enter do poprawnego skończenia / enter przerywa - nie zapisuje wyniku
    wykorzystuje funkcję save_score której przekazuje poziom gry
    :param level: poziom gry (easy/medium/hard)
    :return: None
    """


# Karol
code2letter = {97: 'a',
               98: 'b',
               99: 'c',
               100: 'd',
               101: 'e',
               102: 'f',
               103: 'g',
               104: 'h',
               105: 'i',
               106: 'j',
               107: 'k',
               108: 'l',
               109: 'm',
               110: 'n',
               111: 'o',
               112: 'p',
               113: 'q',
               114: 'r',
               115: 's',
               116: 't',
               117: 'u',
               118: 'v',
               119: 'w',
               120: 'x',
               121: 'y',
               122: 'z',
               8: ' ',
               13: '',
               32: ' '}


def game_loop_chalange(level):
    # Inicjalizacja
    pygame.init()

    # Wartosci Pomocznicze
    white = (255, 255, 255)
    green = (0, 255, 0)
    colour = (255, 0, 0)
    clock = pygame.time.Clock()
    delta = 0

    # Ustawienia Okna
    res = (1200, 650)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Mistrz Klawiatury")
    screen.fill(white)

    # Wartosci Początkowe
    n = 0
    word = choose_word()
    czas = 0
    warn = ""
    ipt = ""
    font = pygame.font.Font('freesansbold.ttf', 70)
    font1 = pygame.font.Font('freesansbold.ttf', 20)

    while True:
        for event in pygame.event.get():
            if n == 10:
                safe_score(level, czas)
            # Ostrzerzenie o liczbie liter
            if len(ipt) > len(word):
                warn = "Uwaga! Za duzo liter"
            else:
                warn = ""
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == 13 and ipt == "":
                    delta = 0
                if event.key == pygame.K_BACKSPACE:
                    if len(ipt):
                        ipt = ipt[:-1]
                else:
                    letter = code2letter[event.key]
                    ipt += letter
                # Zatwierdzanie Poprawnego Wyniku
                if ipt == word and event.key == 13:
                    word = choose_word()
                    ipt = ""
                    czas += delta
                    delta = 0
                    n += 1

        # Zarzadzanie kolorem czcionki
        if len(ipt) == 1:
            if ipt == word[0]:
                colour = (0, 255, 0)
            else:
                colour = (255, 0, 0)
        elif len(ipt) != 0:
            for i in range(len(ipt)):
                if ipt[:i + 1] == word[:i + 1]:
                    colour = (0, 255, 0)
                else:
                    colour = (255, 0, 0)

        # Zegar
        delta += clock.tick() / 1000.0

        # Rysowanie
        pygame.display.update()
        screen.fill(white)
        # Wyraz Wylosowany
        tekst = font.render(word, True, (0, 0, 0))
        tekst_prost = tekst.get_rect()
        tekst_prost.center = (600, 163)
        screen.blit(tekst, tekst_prost)
        # Wyraz Wpisany
        tekst1 = font.render(ipt, True, colour)
        tekst1_prost = tekst1.get_rect()
        tekst1_prost.center = (600, 325)
        screen.blit(tekst1, tekst1_prost)
        # Ostrzerzenie
        tekst2 = font.render(warn, True, (255, 0, 0))
        tekst2_prost = tekst2.get_rect()
        tekst2_prost.center = (600, 500)
        screen.blit(tekst2, tekst2_prost)
        # Czas
        tekst3 = font1.render("Czas odpowiedzi to " + str(czas)[:5] + " s", True, (0, 0, 0))
        tekst3_prost = tekst3.get_rect()
        tekst3_prost.center = (900, 30)
        screen.blit(tekst3, tekst3_prost)
        pygame.display.flip()

    # Karol

    """
    # Karol
    #czyści okno i rysuje swoje
    wyswietla litery
    wykorzystuje choose_letter
    jak jest poprawna podaje kolejną a jak nie to czeka aż będzie
    enter przerywa grę
    :return: None
    """


# Karol
def choose_letter():
    rand = random.randint(97, 122)
    return code2letter[rand]


# Karol
def game_loop_learn():
    # Inicjalizacja
    pygame.init()

    # Wartosci Pomocnicze
    white = (255, 255, 255)
    green = (0, 255, 0)

    # Ustawienia Okna
    res = (1200, 650)
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("Mistrz Klawiatury")
    screen.fill(white)

    # Wartosci Początkowe
    char = choose_letter()
    letter = ''
    font = pygame.font.Font('freesansbold.ttf', 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    sys.exit(0)
                letter = code2letter[event.key]
                if letter == char:
                    char = choose_letter()

        # Rysowanie
        pygame.display.update()
        screen.fill(white)
        # Litera Wylosowana
        tekst = font.render(char, True, (0, 0, 0))
        tekst_prost = tekst.get_rect()
        tekst_prost.center = (600, 163)
        screen.blit(tekst, tekst_prost)
        # Litera Wpisana
        tekst1 = font.render(letter, True, (0, 0, 0))
        tekst1_prost = tekst1.get_rect()
        tekst1_prost.center = (600, 325)
        screen.blit(tekst1, tekst1_prost)
        pygame.display.flip()


def choose_word(level):
    """
    # Adrian
    losuje hasło z bazy o zadanym lewelu
    uwzględnia czy hasło było ostatnio używane (baza powinna to obsługiwać przechowując
     powiązaną z każdym hasłem wartość [może też być dla każdego gracza własna]
      True gdy hasło było użyte lub False gdy nie)
    jeżeli wszystkie hasła mają wartość true zmiania wszystkie na False i losuje
    :param level: poziom gry (easy/medium/hard)
    :return: słowo
    """


def choose_letter():
    """
    # Adrian
    funkcja analogiczna jak chose_word tylko zamiast haseł losuje lieterę
    może być prostsza ale fajnie jak by też jakoś minimalizowała powtórki
    :return litera:
    """


def save_score(level, score, nick):
    """
    # Gustaw
    mnoży score razy jakąś wagę zależną od level i zapisuje do bazy
    :param level: poziom gry (1/2/3)
    :param score: wynik jako czas w decysekundach (1s/10)
    :param nick: nick
    :return:
    """

    score_to_db = str(score * level)
    cu.execute("insert into " + nick + "_stat_today (score,date) values (" + score_to_db + ",date('now'))")
    cx.commit()
