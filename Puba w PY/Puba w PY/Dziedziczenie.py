import pygame
from pygame.math import Vector2
class NaEkranie(object):
    """
        Klasa NaEkranie kalse dziedzicza: Zegar, Gracz, Strzal, Skala, Boss, Atak bosa
    """
    def __init__(self, game):
        """
            konstruktor klasy zegar
        """
        self.bochater = pygame.image.load("9.png")
        self.pos = Vector2(0,0)

    def tick(self):
        pass

    def draw1(self):
        """
            Najwarzniejszy element klasy NaEkranie czyli draw1 rysowanie obiektu na ekranie. 
            Dzieki temu nie nie trzeba uzupe³naiæ ka¿dej koasy o metode Draw1
        """
        self.game.screen.blit(self.bochater,(self.pos[0],self.pos[1]))

