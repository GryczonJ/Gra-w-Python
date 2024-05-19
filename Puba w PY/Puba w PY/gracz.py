
import pygame
from Dziedziczenie import NaEkranie
from pygame.math import Vector2

pygame.init()


class Gracz(NaEkranie):
    """
        Wy�wietlanie i obs�uga obiektu sterowanego przez gracza. 
    """
    def __init__(self, game):
        """
            Metoda __init__() inicjalizuje obiekt gracza, ustawiaj�c parametry, 
            wczytuj�c obraz gracza i ustawiaj�c pocz�tkowe warto�ci pozycji, pr�dko�ci i przyspieszenia gracza.
            

            Na pocz�tku metoda przypisuje referencj� do obiektu gry (game) do zmiennej self.game oraz referencj� do ekranu gry do zmiennej self.screen.

            Nast�pnie ustawiane s� parametry obiektu gracza:

            - self.speed reprezentuje pr�dko�� gracza.
            - self.gravity reprezentuje warto�� grawitacji, kt�ra wp�ywa na ruch gracza.
            - self.bochater wczytuje obraz gracza z pliku "9.png".
            - self.strzal tworzy obiekt klasy Strzal.

            Nast�pnie, na podstawie rozmiaru ekranu gry, ustawiane s� pozycja (self.pos),
            pr�dko�� (self.vel) i przyspieszenie (self.acc) gracza na warto�ci pocz�tkowe.
        """
        self.game = game
        self.screen = self.game.screen
        #Parametry obiektu:
        self.speed =  0.5 
        self.gravity =  0.2
        self.bochater = pygame.image.load("9.png")
        self.strzal = Strzal(self)

        size = self.screen.get_size()

        self.pos = Vector2(size[0]/2,size[1]/2)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

    def add_force(self,force):
        """
            Metoda add_force(self, force) dodaje si�� do przyspieszenia gracza.
            
            force -> Wektor si�y, kt�ry ma zosta� dodany do przyspieszenia gracza.
        """
        self.acc += force

    def tick(self):
        """
            Metoda tick(self) jest odpowiedzialna za aktualizacj� stanu obiektu sterowanego na rzecz gracza.

            - self.strzal.tick(self.pos): Wywo�anie metody tick() obiektu strza�u gracza, przekazuj�c mu aktualn� pozycj� gracza (self.pos).
            - Odczytujemy wci�ni�te klawisze za pomoc� pygame.key.get_pressed() i w zale�no�ci od wci�ni�tych klawiszy dodajemy odpowiednie si�y do przyspieszenia gracza.
            - Sprawdzamy granice ekranu, aby zapewni�, �e gracz nie wychodzi poza obszar gry.(Border)
            - Redukujemy pr�dko�� gracza poprzez mno�enie przez warto�� 0.9.
            - Dodajemy grawitacj� do pr�dko�ci gracza, zmniejszaj�c warto�� wektora pr�dko�ci w kierunku przeciwnym do kierunku grawitacji.
            - Dodajemy przyspieszenie do pr�dko�ci gracza.
            - Aktualizujemy pozycj� gracza na podstawie pr�dko�ci.
            - Resetujemy przyspieszenie, ustawiaj�c je na wektor zerowy.
        """
        self.strzal.tick(self.pos)

        # Input / Wejscie
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.add_force(Vector2(0,-self.speed))
        if pressed[pygame.K_s]:
            self.add_force(Vector2(0,self.speed))
        if pressed[pygame.K_a]:
            self.add_force(Vector2(-self.speed,0))
        if pressed[pygame.K_d]:
            self.add_force(Vector2(self.speed,0))
        
        # Border
        if self.pos[0] >= 1210:
            self.pos[0] = 1210

        if self.pos[0] <= 5:
            self.pos[0] = 5

        if self.pos[1] >= 650:
            self.pos[1] = 650

        if self.pos[1] <= 0:
            self.pos[1] = 0

        # Physisc / Fizyka 
        self.vel *= 0.9

        # graitacja
        self.vel -= Vector2(0,-self.gravity)

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

    def draw1(self):
        """
            Metoda rysuj�ca obiekt kt�rym steruje gracz.
            Wywo�uj� rysowanie pocisk�w wystrzelonych przez gracza
        """
        self.strzal.draw1()
        self.game.screen.blit(self.bochater,(self.pos[0],self.pos[1]))

 #================================================================================================================================
 #================================================================================================================================

class Strzal(NaEkranie):

    """
        Jest to klasa maj�ca reprezentowac strza�y oddane przez posta� kt�r� steruje gracz.    
    """
    def __init__(self, game):
        """
             Konstruktor __init__(self, game) ustawia parametry obiektu strza�u, takie jak pr�dko��, 
             obraz i czas strza�u, oraz inicjalizuje pust� list� pozycji strza�u.

             - Przypisanie obiektu gry game do atrybutu self.game.
             - Przypisanie ekranu gry self.game.screen do atrybutu self.screen.
             - Ustalenie pr�dko�ci strza�u na wektor o warto�ci (0, 10) za pomoc� Vector2.
             - Wczytanie obrazu strza�u gracza za pomoc� pygame.image.load("strzal.png") i przypisanie go do atrybutu self.bochater.
             - Pobranie aktualnego czasu w milisekundach za pomoc� pygame.time.get_ticks() i przypisanie go do atrybutu self.czas_strzalu.
             - Inicjalizacja listy self.pos jako pusta lista.
        """
        self.game = game
        self.screen = self.game.screen
        # parametry obiekty:
        self.speed =  Vector2(0,10) 
        self.bochater = pygame.image.load("strzal.png")
        self.czas_strzalu = pygame.time.get_ticks()

        # pozition / pozycja
        self.pos =[]

    def tick(self, pozycja):
       """
            Metoda tick(self, pozycja) odpowiada za ruch strza�u, jego tworzenie i usuwanie na podstawie interakcji gracza oraz up�ywu czasu.
            Dla ka�dej pozycji strza�u w li�cie self.pos, zmniejsz jej warto�� o warto�� pr�dko�ci self.speed. Je�li pozycja strza�u w osi Y staje si� mniejsza ni� -10, usu� t� pozycj� z listy.

            - Pobiera aktualny czas w milisekundach za pomoc� pygame.time.get_ticks() i przypisz go do zmiennej now.
            - Sprawdza, czy klawisz Spacji (pygame.K_SPACE) jest wci�ni�ty (pressed[pygame.K_SPACE]) i czy up�yn�� wystarczaj�cy czas od ostatniego strza�u (now - self.czas_strzalu > 1000).
            - Je�li warunki s� spe�nione, dodaje now� pozycj� strza�u do listy self.pos. Pozycja ta ma warto�� (pozycja[0]+16, pozycja[1]), gdzie pozycja[0] to warto�� pozycji X gracza zwi�kszona o 16 (aby strza� wydawa� si� wychodzi� z centrum gracza), a pozycja[1] to warto�� pozycji Y gracza.
            - Aktualizuje czas strza�u self.czas_strzalu na obecny czas now.
       """
       for p in self.pos:
           p -= self.speed
           if  p[1] < -10:
               self.pos.remove(p)

       now = pygame.time.get_ticks()
       pressed = pygame.key.get_pressed()
       if pressed[pygame.K_SPACE] and now - self.czas_strzalu > 1000:
           self.pos.append(Vector2 (pozycja[0]+16,pozycja[1] ))
           self.czas_strzalu=now
    
    def efekt(self, strzal):
        """
            Metoda efekt(self, strzal) s�u�y do usuwania strza�u z listy self.pos.

                - Przyjmuje parametr strzal, kt�ry reprezentuje pozycj� strza�u do usuni�cia.
                - Usuwa podan� pozycj� strzal z listy self.pos za pomoc� metody remove().
        """
        self.pos.remove(strzal)
        
    def draw1(self):
        """
            Metoda draw1(self) s�u�y do rysowania strza��w na ekranie.

            Dla ka�dej pozycji strza�u p w li�cie self.pos, 
            wy�wietla obrazek strza�u self.bochater na ekranie gry self.game.screen na pozycji (p[0], p[1]).
        """
        for p in self.pos:
            self.game.screen.blit(self.bochater,(p[0],p[1]))

        
        
