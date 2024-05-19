
import pygame
from Dziedziczenie import NaEkranie
from pygame.math import Vector2

pygame.init()


class Gracz(NaEkranie):
    """
        Wyœwietlanie i obs³uga obiektu sterowanego przez gracza. 
    """
    def __init__(self, game):
        """
            Metoda __init__() inicjalizuje obiekt gracza, ustawiaj¹c parametry, 
            wczytuj¹c obraz gracza i ustawiaj¹c pocz¹tkowe wartoœci pozycji, prêdkoœci i przyspieszenia gracza.
            

            Na pocz¹tku metoda przypisuje referencjê do obiektu gry (game) do zmiennej self.game oraz referencjê do ekranu gry do zmiennej self.screen.

            Nastêpnie ustawiane s¹ parametry obiektu gracza:

            - self.speed reprezentuje prêdkoœæ gracza.
            - self.gravity reprezentuje wartoœæ grawitacji, która wp³ywa na ruch gracza.
            - self.bochater wczytuje obraz gracza z pliku "9.png".
            - self.strzal tworzy obiekt klasy Strzal.

            Nastêpnie, na podstawie rozmiaru ekranu gry, ustawiane s¹ pozycja (self.pos),
            prêdkoœæ (self.vel) i przyspieszenie (self.acc) gracza na wartoœci pocz¹tkowe.
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
            Metoda add_force(self, force) dodaje si³ê do przyspieszenia gracza.
            
            force -> Wektor si³y, który ma zostaæ dodany do przyspieszenia gracza.
        """
        self.acc += force

    def tick(self):
        """
            Metoda tick(self) jest odpowiedzialna za aktualizacjê stanu obiektu sterowanego na rzecz gracza.

            - self.strzal.tick(self.pos): Wywo³anie metody tick() obiektu strza³u gracza, przekazuj¹c mu aktualn¹ pozycjê gracza (self.pos).
            - Odczytujemy wciœniête klawisze za pomoc¹ pygame.key.get_pressed() i w zale¿noœci od wciœniêtych klawiszy dodajemy odpowiednie si³y do przyspieszenia gracza.
            - Sprawdzamy granice ekranu, aby zapewniæ, ¿e gracz nie wychodzi poza obszar gry.(Border)
            - Redukujemy prêdkoœæ gracza poprzez mno¿enie przez wartoœæ 0.9.
            - Dodajemy grawitacjê do prêdkoœci gracza, zmniejszaj¹c wartoœæ wektora prêdkoœci w kierunku przeciwnym do kierunku grawitacji.
            - Dodajemy przyspieszenie do prêdkoœci gracza.
            - Aktualizujemy pozycjê gracza na podstawie prêdkoœci.
            - Resetujemy przyspieszenie, ustawiaj¹c je na wektor zerowy.
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
            Metoda rysuj¹ca obiekt którym steruje gracz.
            Wywo³ujê rysowanie pocisków wystrzelonych przez gracza
        """
        self.strzal.draw1()
        self.game.screen.blit(self.bochater,(self.pos[0],self.pos[1]))

 #================================================================================================================================
 #================================================================================================================================

class Strzal(NaEkranie):

    """
        Jest to klasa maj¹ca reprezentowac strza³y oddane przez postaæ któr¹ steruje gracz.    
    """
    def __init__(self, game):
        """
             Konstruktor __init__(self, game) ustawia parametry obiektu strza³u, takie jak prêdkoœæ, 
             obraz i czas strza³u, oraz inicjalizuje pust¹ listê pozycji strza³u.

             - Przypisanie obiektu gry game do atrybutu self.game.
             - Przypisanie ekranu gry self.game.screen do atrybutu self.screen.
             - Ustalenie prêdkoœci strza³u na wektor o wartoœci (0, 10) za pomoc¹ Vector2.
             - Wczytanie obrazu strza³u gracza za pomoc¹ pygame.image.load("strzal.png") i przypisanie go do atrybutu self.bochater.
             - Pobranie aktualnego czasu w milisekundach za pomoc¹ pygame.time.get_ticks() i przypisanie go do atrybutu self.czas_strzalu.
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
            Metoda tick(self, pozycja) odpowiada za ruch strza³u, jego tworzenie i usuwanie na podstawie interakcji gracza oraz up³ywu czasu.
            Dla ka¿dej pozycji strza³u w liœcie self.pos, zmniejsz jej wartoœæ o wartoœæ prêdkoœci self.speed. Jeœli pozycja strza³u w osi Y staje siê mniejsza ni¿ -10, usuñ tê pozycjê z listy.

            - Pobiera aktualny czas w milisekundach za pomoc¹ pygame.time.get_ticks() i przypisz go do zmiennej now.
            - Sprawdza, czy klawisz Spacji (pygame.K_SPACE) jest wciœniêty (pressed[pygame.K_SPACE]) i czy up³yn¹³ wystarczaj¹cy czas od ostatniego strza³u (now - self.czas_strzalu > 1000).
            - Jeœli warunki s¹ spe³nione, dodaje now¹ pozycjê strza³u do listy self.pos. Pozycja ta ma wartoœæ (pozycja[0]+16, pozycja[1]), gdzie pozycja[0] to wartoœæ pozycji X gracza zwiêkszona o 16 (aby strza³ wydawa³ siê wychodziæ z centrum gracza), a pozycja[1] to wartoœæ pozycji Y gracza.
            - Aktualizuje czas strza³u self.czas_strzalu na obecny czas now.
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
            Metoda efekt(self, strzal) s³u¿y do usuwania strza³u z listy self.pos.

                - Przyjmuje parametr strzal, który reprezentuje pozycjê strza³u do usuniêcia.
                - Usuwa podan¹ pozycjê strzal z listy self.pos za pomoc¹ metody remove().
        """
        self.pos.remove(strzal)
        
    def draw1(self):
        """
            Metoda draw1(self) s³u¿y do rysowania strza³ów na ekranie.

            Dla ka¿dej pozycji strza³u p w liœcie self.pos, 
            wyœwietla obrazek strza³u self.bochater na ekranie gry self.game.screen na pozycji (p[0], p[1]).
        """
        for p in self.pos:
            self.game.screen.blit(self.bochater,(p[0],p[1]))

        
        
