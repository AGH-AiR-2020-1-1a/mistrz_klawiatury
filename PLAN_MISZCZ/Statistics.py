import sqlite3

import pygame
from keyboard import read_event

database = r"..\db\mistrz_klawiatury.db"
cx = sqlite3.connect(database, check_same_thread=False)
cu = cx.cursor()


def download_input(period, nick):
    """
    # Gustaw
    pobiera dane z bazy danych do przedstawienia w statystykach
    :param period: okres czasu (jeden z :dziś(1) / tydzień(2)/ miesiąc(3)/ od początku(4))
    :param nick:
    :return period_scores: lista ze słownikami : {'date' : <numer gry w dniu / data dnia / nr tygodnia/ nazwa miesiąca>(nie dluższe niz 12 znaków),
    'score' : <wynik z danego czasu> (int między 0 a 100 włacznia)}
    Gustaw ustal jak tu podzielimy te okresy
    (najlepiej żeby było max 10 wyników w jednym okresie żeby się pomieściły w oknie jakoś zgrabnie wraz z nazwami)
    """
    period_dict = {1: "today", 2: "week", 3: "month", 4: "ever"}
    period_scores = None
    cu.execute(
        "select rowid, date, score from " + nick + "_stat_" + period_dict[period] + " ORDER BY \"date\" DESC LIMIT 10")
    cx.commit()
    period_scores = cu.fetchall()
    return period_scores


def show_statistics(period, screen=None, player_nick=None):
    """
    # Ignacy - DONE
    #czyści okno i rysuje swoje
    używa download_input
    rysuje statystyki za pomocą pygame - najlepiej w tym samym oknie co gra
    wychodzi z nich po nacisnieciu klawisza E - kończy funkcję
    Ignacy to zrobi (już mam prawie gotowe bo się trochę bawiłem)
    wcisniecie q konczy funkcje
    :param: screen: - obiekt ```pygame.display.set_mode((size_x, size_y))```
    :param: period
    :param: player_nick - taki jak argument funkcji ```download_input```
    :return:
    """
    scores = download_input(period, player_nick)
    screen.fill([255, 255, 255])
    pygame.display.flip()
    amount_of_scores = len(scores)
    nic = False
    if amount_of_scores == 0:
        print("nie ma nic do pokazania")
        nic = True
        font = pygame.font.Font('freesansbold.ttf', 50)
        instr = font.render("Nie ma nic do pokazania", True, (0, 0, 0), (255, 255, 255))
        back = font.render("Powrót (ESC)", True, (0, 0, 0), (255, 255, 255))
        screen.blit(instr, (100, 100))
        screen.blit(back, (80, 280))
        pygame.display.flip()
    if nic is False:
        if amount_of_scores > 10:
            print('zbyt wiele wyników: ', len(scores))
        size_x = 1200
        size_y = 650
        # ustawienia pola rysowania
        x0 = int(size_x / 12)
        y0 = int(size_y / 6.5) + 22
        x_max = int(size_x / 1.33)
        y_max = int(size_y / 1.345)
        x_length = x_max - x0
        y_length = abs(y0 - y_max)
        unit_q = 2
        unit = x_length / (unit_q * amount_of_scores)
        pole_width = unit
        rectangles = [pygame.Rect(x0 + i * unit_q * int(unit), y_max, int(pole_width), 2) for i in
                      range(amount_of_scores)]

        # instrukcja
        font_b = pygame.font.Font('freesansbold.ttf', 50)
        back = font_b.render("Powrót (ESC)", True, (0, 0, 0), (255, 255, 255))
        screen.blit(back, (870, 595))

        # dane
        scores_points = [day[2] for day in scores]
        maxym = max(scores_points)
        scores_points = [i * 100 / maxym for i in scores_points]
        scores_high = [y_max - y_length * i / 84 for i in scores_points]

        # ładowanie tła pokazywania statystyk
        myimage = pygame.image.load('../Others/siatka2.png')
        imagerect = myimage.get_rect()
        image_loc = [-5, -22]
        screen.blit(myimage, [*image_loc, *imagerect[2:4]])

        # rysowanie przedziałów czasowych
        black = (0, 0, 0)
        font = pygame.font.Font('freesansbold.ttf', 20)
        for nr, score in enumerate(scores):
            napis = score[1]
            if len(napis) > 12:
                print("zbyt długi napis: ", napis, len(napis))
            napis = napis if len(napis) < 12 else napis[:12]
            text = font.render(napis, True, black)
            text = pygame.transform.rotate(text, -70)
            textRect = text.get_rect()
            centr = int(sum([rectangles[nr].bottomright[0], rectangles[nr].bottomleft[0]]) / 2) - 15
            # pygame.draw.rect(screen, (0, 150, 255), pygame.Rect(*rectangles[nr].bottomleft,10,10))
            textRect.topleft = (centr, rectangles[nr].bottomleft[1] + 5)
            pygame.draw.rect(screen, (0, 150, 100), pygame.Rect(*textRect.topleft, 10, 10))
            screen.blit(text, textRect)
            pygame.Rect(centr, rectangles[nr].bottomleft[1] + 5, 10, 10)
        pygame.display.update()

        running_flag = False  # gdy już słupki sie narysują wtedy przyjmuje wartosć False i wychodzi z pętli

        # pętla rysowania
        while not running_flag:
            # # sprawdzanie zamknięcia
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         close(0)

            running_flag = True

            for i in range(amount_of_scores):
                if rectangles[i].y >= scores_high[i]:
                    pygame.draw.rect(screen, (0, 150, 255), rectangles[i])
                    rectangles[i].y -= 1
                    running_flag = running_flag and False
                else:
                    running_flag = running_flag and True
            pygame.display.flip()

    while True:
        event = read_event()
        if 'esc' in str(event):
            return None
