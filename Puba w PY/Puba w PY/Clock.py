#from unittest.mock import _SentinelObject
from Dziedziczenie import NaEkranie

import pygame
import datetime

class Zegar(NaEkranie):
    """
        Zadaniem klasy zegar jest obsluga zegara gry
    """
    def __init__(self, game):
        """
            Ta metoda inicjalizuje obiekt zegara, który będzie wykorzystywany w grze.
            Przyjmuje obiekt gry jako argument.

            Inicjalizuje ustawienia czcionki, takie jak rozmiar czcionki i kolor (ustawiony na biały).
            Tworzy obiekt czcionki za pomocą modułu pygame.font.

            Tworzy obiekt zegara pygame.time.Clock(), który będzie służył do kontrolowania prędkości odświeżania gry.

            Pobiera aktualny czas w sekundach przy użyciu pygame.time.get_ticks() i zapisuje go w zmiennej self.current_time1.
            Jest to wykorzystywane jako punkt odniesienia do obliczania czasu wyświetlanego na zegarze.
        """
        self.game = game

        # Ustawienia czcionki
        self.font_size = 36
        self.font_color = (255, 255, 255)  # Bia�y
        self.font = pygame.font.SysFont(None, self.font_size)

        self.clock = pygame.time.Clock()
        self.current_time1 = pygame.time.get_ticks() // 1000  # Pobierz aktualny czas w sekundach

    def draw1(self):
        """
            Ta metoda rysuje zegar na ekranie gry, który wyświetla aktualny czas od momentu rozpoczęcia gry.
            Czas jest obliczany w sekundach i formatowany w postaci "mm:ss".
            Następnie sformatowany tekst jest wyświetlany na ekranie w wybranym miejscu.
        """
        current_time = pygame.time.get_ticks() // 1000  # Pobierz aktualny czas w sekundach
        current_time -= self.current_time1
        time_text = self.format_time(current_time)  # Formatowanie czasu
        text_surface = self.font.render(time_text, True, self.font_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (1280 // 2, 50)  # Pozycja zegara na �rodku g�rnego ekranu
        self.game.screen.blit(text_surface, text_rect)

    def format_time(self, seconds):
        """
            Ta metoda formatuje czas podany w sekundach na format "mm:ss" (minuty:sekundy) i zwraca sformatowany tekst czasu.
        """
        minutes = seconds // 60
        seconds = seconds % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        return time_text

    def get_elapsed_time(self):
        """
            Ta metoda oblicza upływający czas od momentu inicjalizacji obiektu w sekundach, 
            poprzez odejmowanie zapisanego czasu inicjalizacji (self.current_time1) od aktualnego czasu w sekundach.
        """
        current_time = pygame.time.get_ticks() // 1000  # Pobierz aktualny czas w sekundach
        elapsed_time = current_time - self.current_time1
        return int(elapsed_time)






