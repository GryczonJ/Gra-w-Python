
import pygame
from Dziedziczenie import NaEkranie
from pygame.math import Vector2
import random

pygame.init()
class Skala(NaEkranie):
    """
        Skała reprezentuje na ekranie, najbardzej podstawowego przeciwnika. 
    """
    def __init__(self, game):
        """
            Metoda __init__(self, game) inicjalizuje parametry i właściwości obiektu klasy Skala na podstawie przekazanego obiektu gry.

                - Przyjmuje parametr game, który reprezentuje obiekt gry.
                - Inicjalizuje pole self.game przypisując mu wartość parametru game.
                - Ustala wartości parametrów dla obiektu Skala, takie jak prędkość (self.speed), grawitacja (self.gravity) i obrazek (self.bochater).
                - Ustala początkową pozycję (self.pos) na losową wartość X między 5 a 1270, a Y na -80.
                - Inicjalizuje początkowe wartości prędkości (self.vel) i przyspieszenia (self.acc) jako wektory o wartościach (0, 0).
        """
        self.game = game
        self.speed =  0.5 #prendkosc obiekty
        self.gravity =  random.randint(2 , 5)/10 #0.1
        self.bochater = pygame.image.load("sakala1.png")
       
        self.pos = Vector2(random.randint(5,1270),-80) # pozition / pozycja 1280,720
        self.vel = Vector2(0,0) # pr�tk�� aktualna
        self.acc = Vector2(0,0) # przyspieszenie

    def tick(self):
        """
            Metoda tick(self) aktualizuje fizykę i położenie obiektu klasy Enemy na 
            podstawie parametrów takich jak prędkość, grawitacja i przyspieszenie.
            Dodatkowo, jeśli obiekt osiągnie określoną wysokość, zmienia obrazek na eksplozję.
        """
        # Physisc / Fizyka 
        self.vel *= 0.9

        # graitacja
        self.vel -= Vector2(0,-self.gravity)

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.pos[1] >= 680:
            self.bochater = pygame.image.load("bom1.png")

    #def draw1(self):
    #    self.game.screen.blit(self.bochater,(self.pos[0],self.pos[1]))

     
        
class Kometa(NaEkranie):
    """
        Kometa jest to drugi typ przeciwnika jaki możemy napotkać w grze. 
        Różni się od innych przeciwników tym, że nadlatuje z boku i ma zdecydowanie mniejszą prędkość.
        Zadaniem tej klasy jest reprezentowanie komety na ekranie i aktualizacja jej pozycji.
    """
    def __init__(self, game):
        """
            Metoda __init__(self, game) inicjalizuje obiekt klasy Kometa, ustawiając odpowiednie parametry takie jak położenie, 
            prędkość, obrazek oraz przyspieszenie.
            Decyzja o położeniu i prędkości obiektu jest losowa na podstawie rzutu monetą.
        """
        self.game = game
        
        moneta = random.randint(1,2)

        if 1 == moneta:
            self.pos = Vector2(0 , random.randint(15,700)) # pozition / pozycja 1280,720
            self.speed = Vector2( 0.3 ,0) #prendkosc obiekty
            self.bochater = pygame.image.load("skala3.png")
        else:
            self.pos = Vector2(1280 , random.randint(15,700))
            self.speed = Vector2( -0.3 ,0) #prendkosc obiekty
            self.bochater = pygame.image.load("skala4.png")

        self.vel = Vector2(2,0) # pr�tk�� aktualna
        self.acc = Vector2(0,0) # przyspieszenie

    def tick(self):
        """
            Metoda tick(self) aktualizuje pozycję obiektu na podstawie jego prędkości, 
            przemieszczając go o wartość prędkości w każdym kroku.
        """
        # Physisc / Fizyka
        self.pos += self.speed       

    #def draw1(self):
    #    self.game.screen.blit(self.bochater,(self.pos[0],self.pos[1]))

       
class Boss(NaEkranie):
    """
        Jest to specjalny rodzaj przeciwnika pojawiający się co okreslony czas i blokujący pozostałych przeciwników.
        Ma dawa rodzje ataków i stale się porusza. Ataki zmieniają się w zależności od punktów zdrowia przeciwnika.
        Zadaniem tej klasy jest reprezentowanie Bosa na ekranie, aktualizacja jego pozycji i obsługa jego ataków.
    """
    def __init__(self, game):
        """
            Metoda __init__(self, game) inicjalizuje obiekt klasy Boss ustawiając jego właściwości, 
            takie jak ilość trafień, odwołanie do obiektu gry, ekran, atak, prędkość, grawitację, obraz i pozycję.
        """
        self.trafienia = 20
        self.game = game
        self.screen = self.game.screen
        self.atak = AtakBosa(self)
        #prendkosc obiekty
        self.speed = Vector2(0,0.5) 
        self.gravity =  0.05 # 0.1
        self.bochater = pygame.image.load("boss.png")

       # pozition / pozycja 1280,720
        self.pos = Vector2(140,-80)

        # pr�tk�� aktualna
        self.vel = Vector2(0,0)

        # przyspieszenie
        self.acc = Vector2(0,0) 

    def tick(self):
        """
            Metoda tick(self) aktualizuje stan bossa, obsługuje ataki oraz kontroluje poruszanie się bossa w lewo i prawo.
                - Wywołać metodę ataki() w celu obsługi ataków bossa.
                - Wywołać metodę tick() dla obiektu atak w celu aktualizacji stanu ataku.
                - Zaktualizować pozycję bossa poprzez dodanie wartości wektora speed do pozycji.
                - Sprawdzić warunek, czy pozycja bossa na osi X jest większa lub równa 780.
                  Jeśli tak, zmienić wartość wektora speed na Vector2(-0.05, 0) w celu zmiany kierunku poruszania się bossa w lewo.
                - Sprawdzić warunek, czy pozycja bossa na osi X jest mniejsza lub równa 0. Jeśli tak, zmienić wartość wektora speed na Vector2(0.2, 0) w celu zmiany kierunku poruszania się bossa w prawo.
        """
        self.ataki()
        self.atak.tick()
        self.pos += self.speed
        if self.pos[0] >= 780:
            self.speed = Vector2(-0.05,0)
        if self.pos[0] <= 0:
            self.speed = Vector2(0.2,0)

    def wjazd(self):
        """
            Metoda wjazd(self) symuluje efekt wjazdu obiektu, zmieniając jego pozycję, 
            prędkość i grawitację, aż osiągnie poziom zero na osi Y.
            Zwraca wartość 1, gdy wjazd zostaje zakończony, w przeciwnym razie zwraca 0.
        """
       # Physisc / Fizyka 
        self.vel *= 0.9

        # graitacja
        self.vel -= Vector2(0,-self.gravity)

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.pos[1] >= 0:
            self.pos[1]= 0
            self.gravity = 0
            self.speed = Vector2( -0.2 , 0 )
            return 1
        return 0
    
    def ataki(self):
        """
            Metoda ataki(self) kontroluje wybór rodzaju ataku na podstawie liczby trafień, 
            wywołując atak zwykły lub specjalny zależnie od ilości trafień.
        """
        if self.trafienia >= 10:
           self.atak.zwykly(self.pos)
        else:
            self.atak.specjalny(self.pos)
         
    def draw1(self):
        """
            Metoda draw1(self) rysuje obiekt ataku oraz obraz postaci bossa na ekranie gry.
        """
        self.atak.draw1()
        self.game.screen.blit(self.bochater,(self.pos[0],self.pos[1]))


class AtakBosa(NaEkranie):
    """
        Zadaniem tej klasy jest reprezentowanie na ekranie, ataku Bosa. 
    """
    def __init__(self, game):
        """
            Konstruktor klasy AtakBosa inicjalizuje obiekt ataku Bosa na ekranie gry.
            Ustala parametry ataku, takie jak prędkość, grawitację, obraz ataku, pozycję, prędkość i przyspieszenie.
        """
        self.czas = pygame.time.get_ticks()
        #self.trafienia = 100
        self.game = game
        self.screen = self.game.screen
        self.speed =  Vector2(0,4)
        #self.szef= szef
        #self.speed =  0.5 #prendkosc obiekty
        self.gravity =  0.2 #0.1
        self.bochater = pygame.image.load("bosA.png")
        
        self.pos = [] #Vector2(random.randint(self.Szef.pos[0],self.Szef.pos[0]+450),0) # pozition
        #self.pos.append(Vector2(random.randint(self.Szef.pos[0],self.Szef.pos[0]+450),0))
        # pozycja 1280,720
        self.vel = Vector2(0,0) # pr�tk�� aktualna
        self.acc = Vector2(0,0) # przyspieszenie
        self.prawoLeow = 0
        
    def zwykly(self,pozycja):
        """
           Metoda zwykly dodaje trzy obiekty ataku (pozycje) do listy pos klasy AtakBosa. 
           Pozycje są losowo wybierane w zakresie od zaokrąglonej wartości pozycja[0] do zaokrąglonej wartości pozycja[0]+450. 
           Metoda sprawdza, czy wystąpił dostateczny czas od ostatniego ataku, aby uniknąć zbyt częstego tworzenia nowych obiektów ataku. 
        """
        now = pygame.time.get_ticks()
        if now - self.czas > 1000: # 1000
            self.pos.append(Vector2(random.randint(round(pozycja[0]),round(pozycja[0]+450)),0))
            self.pos.append(Vector2(random.randint(round(pozycja[0]),round(pozycja[0]+450)),0))
            self.pos.append(Vector2(random.randint(round(pozycja[0]),round(pozycja[0]+450)),0))
            self.czas = now
        
    def specjalny(self,pozycja):
        """
            Metoda specjalny dodaje kolejne obiekty ataku (pozycje) do listy pos klasy AtakBosa w sposób zależny od wartości zmiennej prawoLeow. 
            Jeśli prawoLeow wynosi 0, obiekty ataku są dodawane w prawo od ostatniego elementu listy. 
            Jeśli prawoLeow wynosi 1, obiekty ataku są dodawane w lewo od ostatniego elementu listy. 
            Wartość prawoLeow jest aktualizowana na podstawie pozycji ostatniego elementu listy pos względem wartości pozycja[0]+32 i pozycja[0]-32.
        """
        ostaniElement = self.pos[-1]
        
        if ostaniElement[0] < pozycja[0]+32:
           self.prawoLeow = 0
        elif ostaniElement[0] < pozycja[0]-32:
            self.prawoLeow = 1
            
        if self.prawoLeow == 0: # w prawo
            self.pos.append(ostaniElement[0]+32,0)
            self.pos.append(480,0)
        elif self.prawoLeow == 1:# w lewo
            self.pos.append(ostaniElement[0]-32,0)

    def tick(self):
        """
            Metoda tick aktualizuje pozycje obiektów ataku poprzez dodanie wektora prędkości speed do każdego elementu listy pos klasy AtakBosa. 
            Jeśli wartość p[1] przekroczy 740, czyli obiekty ataku opuszczą ekran, są one usuwane z listy pos.
        """
        for p in self.pos:
           p += self.speed
           if  p[1] > 740:
               self.pos.remove(p)
    
    def efekt(self, furia):
        """
            Metoda efekt usuwa podany obiekt furia z listy pos klasy, która reprezentuje efekty furii na ekranie.
        """
        self.pos.remove(furia)
    
    def trafienie(self):
        """
            Metoda trafienie zmniejsza licznik trafień (trafienia) o 1.
        """
        self.trafienia-=1
        
    def draw1(self):
        """
            Metoda draw1 rysuje na ekranie wszystkie elementy obiektu pos na podstawie wczytanego obrazu bochater.
        """
        for p in self.pos:
            self.game.screen.blit(self.bochater,(p[0],p[1])) #
