# IMPORT PLIKÓW
from Statistics import *
from Login import *
from Game import *

# FUNKCJE INICJALIZACYJNE
def do_order_in_database():
    """
    Gustaw
    robi pożądek w bazie danych
    wykonuje się tuż po uruchomieniu
    jak niema plików to je tworzy
    np przepisuje wyniki z poprzedniego dnia do tygodnia itp
    tutaj Gustaw może to rozplanować #order in data_base
    :return:
    """


def main_window():
    """
    #Ignacy
    funkcja wyswietlająca ekran wyboru: trybu gry,poziomu,przejscia do statystyk, wylogowania
    pobiera z klawiatury literke i przechodzi do odpowiedniej funkcji
    :return chose_option: tablica [kod operacji, *args]
    kody operacji:
    'sta' - pokaż statystyki *arg: wybrany okres (day,week,month,begin) - do zmiany
    'ler' - tryb nauki *arg: -
    'cha' - tryb challange *arg: poziom trudnośi (easy/medium/hard)
    'log' - log off *arg: -
    'qui' - zamknij grę *arg: -
    """

    operation_code = 'qui'  # wstępnie napisane żeby Pycharm nie marudził
    arg = None
    return [operation_code, arg]


def window_maker():
    """
    #Ignacy
    tworzy okno o jakiś wymiarach - można spróbować dopasować do ekranu
    :return:
    """
    global screen, size_x, size_y
    size_x = 1200  # rozmiary okna
    size_y = 650
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("Miszcz Klawiatury")
    icon = pygame.image.load('klawiatura.png')
    pygame.display.set_icon(icon)
    screen.fill((255, 255, 255))


# GŁÓWNA FUNKCJA PROGRAMU
def main():
    # testy
    window_maker()
    # inicjalizacja gry
    # Ignacy
    # inicjalizacja pygame
    pygame.init()
    # uporządkowanie bazy danych
    do_order_in_database()
    # stworzenie okna
    window_maker()

    # wyboór gracza
    global player
    player = choose_player()
    # słownik z funkcjami
    functions = {'sta': show_statistics,
                 'ler': game_loop_learn,
                 'cha': game_loop_chalange,
                 'log': choose_player,
                 'qui': close}

    # pętla gry
    while True:
        option = main_window()
        args = option[1:]
        code = option[0]
        if bool(args):
            functions[code](args)
        else:
            functions[code]()


# GRA
if __name__ == '__main__':
    main()