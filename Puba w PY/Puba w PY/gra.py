# class gra

from gracz import Gracz
from zrowie import Health
from Clock import Zegar
from przeciwnik import Kometa, Skala, Boss
import pygame, sys, random, pybind11
import biblioteka
class Game(object):
    """
        Klasa Game jest odpowiedzialna z przeprowadznie rozgrywki, wy�wietanie i zmian� obiekt�w na ekranie gry.
        A takrze za obs�ug� zda��.
    """
    def __init__(self, nick):
        """
        Konstruktor tej klasy inicjalizuje r�ne parametry i obiekty potrzebne do dzia�ania gry.
            - Przyjmuje argument nick, kt�ry jest nickiem gracza. Potrzebny do wpisania do tabeli po przegranej
            - Inicjalizuje zmienn� self.faza na warto�� 0. fazy zmieniaj� si� w czasie gry.
            - Ustawia maksymaln� warto�� self.tps_max na 100.0, kt�ra kontroluje pr�dko�� od�wie�ania gry.
            - Przypisuje warto�� argumentu nick do zmiennej self.imie.
            - Inicjalizuje modu� Pygame za pomoc� pygame.init().
            - Ustawia tytu� gry na "Wojna w Kosmosie" przy u�yciu pygame.display.set_caption().
            - �aduje ikon� gry z pliku "3.png" i ustawia j� jako ikon� okna gry. Logo.
            - Tworzy ekran gry o rozmiarze 1280x720 pikseli za pomoc� pygame.display.set_mode().
            - Inicjalizuje zegar self.tps_clock i zmienn� self.tps_delta do �ledzenia czasu od�wie�ania gry.
            - Ustala punkt odniesienia czasu dodania kamieni i komet na aktualny czas w milisekundach pygame.time.get_ticks().
            - Inicjalizuje obiekty gracza (self.player), zdrowia (self.zdrowie), zegara (self.zegarek).
            - Tworzy pust� list� kamieni i komet (self.kamienie, self.komety).
            - Inicjalizuje zmienn� self.zniszczone na 0.
            - Ustala warto�� self.Koniec na 1.
            - �aduje t�o gry z pliku "tlo1.png".
            - Rozpoczyna p�tl� obs�ugi zdarze� while self.Koniec == 1.
            - W p�tli obs�ugi zdarze� sprawdza zdarzenia takie jak zamykanie okna gry (pygame.QUIT).
            - Sprawdza r�wnie� naci�ni�cie klawisza ESC, co powoduje wyj�cie z p�tli i przechodzi do kolejnej fazy gry.
            - Je�li faza gry jest r�wna 0, sprawdza czy czas od ostatniego wydarzenia jest wi�kszy lub r�wny losowej warto�ci mi�dzy 30000 a 40000 milisekund.
            - Je�li tak, tworzy obiekt Szefa (self.Szef) i zwi�ksza warto�� self.faza o 1.
            - Wywo�uje metod� czas_na_kamienie().
            - Oblicza czas trwania programu i odmierza czas (self.tps_delta) z dok�adno�ci� do 1/self.tps_max.
            - Wywo�uje metody tick(), uwuwa_kamienie(), uwuwa_komete(), kolizje().
            - Wy�wietla t�o na ekranie gry self.screen.blit(tlo, (0, 0)).
            - Wywo�uje metody self.draw().
            - Od�wie�a ekran pygame.display.flip().
        """

        print(pybind11.get_include())
        self.faza = 0
        # Config/ konfiguracja
        #zegar
        self.tps_max = 100.0
        self.imie = nick
        # initlalization/ inicjalizacja programu
        pygame.init()

        # Nazwa Gry / Tytul
        pygame.display.set_caption("Wojna w Kosmosie")
        
        # ikonka
        icon = pygame.image.load("3.png")
        pygame.display.set_icon(icon)
        
        # Wyswietlanie a raczej ekran
        self.screen = pygame.display.set_mode((1280,720))
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.czas_dodania_kamienia = pygame.time.get_ticks()
        self.czas_dodania_komet = pygame.time.get_ticks()

        # Ustawienia czcionki
        self.zegar_gry = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

        self.player = Gracz(self)
        self.zdrowie = Health(self)
        self.zegarek =  Zegar(self)
        self.kamienie = []
        self.komety = []
        self.zniszczone = 0
        self.Koniec=1
        # kolor Ekran Gry
        tlo = pygame.image.load("tlo1.png")
        palza = True
        
        # obsluga zadarzen
        while self.Koniec == 1:
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    sys.exit(0)
                    #self.Koniec = 0
                if event.type == pygame.K_ESCAPE:
                    while palza:
                        for event in pygame.event.get():
                            if event.key == pygame.K_ESCAPE:
                                palza = False
                    paza = True                      

        #Fazy gry
            if self.faza == 0:
                now = pygame.time.get_ticks()
                if  now - self.zegar_gry  >= random.randint(30000,40000):
                    self.Szef = Boss(self)
                    self.faza += 1
                self.czas_na_kamienie()

            # wejscie na ekran self.faza == 1   
            #elif self.faza == 1:               
                
            # czas trwania programu: #dlata += clock.tick()
            # Tiking: Ticking
            self.tps_delta += self.tps_clock.tick()/1000

            while(self.tps_delta > 1 / self.tps_max):
                   self.tick()
                   self.tps_delta -= 1/self.tps_max
 
            self.uwuwa_kamienie()
            self.uwuwa_komete()
            self.kolizje()

            # Drawing
            #self.screen.fill((0,0,0))
            
            self.screen.blit(tlo, (0, 0))
            self.draw()
            pygame.display.flip()

    def tick(self):
        # gracz:
        self.player.tick()
        self.zdrowie.add_health(self.zniszczone)
        # przeciwnicy
        for k in self.kamienie:
            k.tick()

        for k in self.komety:
            k.tick()
            
        # przeciwnik bos
        if self.faza == 1:
            self.faza += self.Szef.wjazd()

        elif self.faza == 2:
            self.kolizjeBOS()
            self.Szef.tick()

    def draw(self):
        """
            Ta metoda tick() aktualizuje stan r�nych element�w gry w ka�dym kroku gry.
                - Wywo�uje metod� tick() dla obiektu gracza (self.player), co pozwala na aktualizacj� jego stanu.
                - Wywo�uje metod� add_health() dla obiektu zdrowia (self.zdrowie), przekazuj�c ilo�� zniszczonych obiekt�w jako argument, aby zwi�kszy� poziom zdrowia gracza.
                - Wywo�uje metod� tick() dla ka�dego obiektu kamienia w li�cie self.kamienie, co pozwala na ich aktualizacj�.
                - Wywo�uje metod� tick() dla ka�dego obiektu komety w li�cie self.komety, co pozwala na ich aktualizacj�.
                - Je�li faza gry jest r�wna 1, wykonuje odpowiednie operacje dla bossa (self.Szef), takie jak animacja wjazdu.
                - Je�li faza gry jest r�wna 2, wykonuje operacje zwi�zane z kolizjami z bossem (self.kolizjeBOS()) i aktualizuje stan bossa (self.Szef.tick()).
        """ 
        self.zegarek.draw1()
        self.player.draw1()
        self.zdrowie.draw1()
        for k in self.kamienie:
            k.draw1()
        for k in self.komety:
            k.draw1()
        if self.faza >= 1:
            self.Szef.draw1()

    def czas_na_kamienie(self):
        """
            Ta metoda sprawdza czas trwania gry i decyduje, czy dodawa� kamienie i komety na ekran.

            - Sprawdza aktualny czas za pomoc� pygame.time.get_ticks().
            - Je�li czas od ostatniego dodania kamienia przekracza 500 milisekund, 
            wywo�uje metod� dodaj_kamienie() w celu dodania nowych kamieni na ekran.

            - Aktualizuje czas ostatniego dodania kamienia na bie��cy czas.
            - Je�li czas od ostatniego dodania komety przekracza losow� warto�� mi�dzy 8000 a 10000 milisekund, 
            wywo�uje metod� dodaj_komete() w celu dodania nowych komet na ekran.

            - Aktualizuje czas ostatniego dodania komety na bie��cy czas.
        """

        now = pygame.time.get_ticks()
        if now - self.czas_dodania_kamienia > 500:#1000
            self.dodaj_kamienie()
            self.czas_dodania_kamienia = now

        if now - self.czas_dodania_komet > random.randint(8000 , 10000):
            self.dodaj_komete()
            self.czas_dodania_komet = now

    def dodaj_kamienie(self):
        """
            Ta metoda dodaje dwa obiekty klasy Skala do listy kamieni (self.kamienie) w celu umieszczenia ich na ekranie gry.
        """
        self.kamienie.append(Skala(self))
        self.kamienie.append(Skala(self))

    def dodaj_komete(self):
        """
            Dodaje obiekt komete do listy  w celu umieszczenia ich na ekranie gry.
        """
        self.komety.append(Kometa(self))
    
    def uwuwa_kamienie(self):
        """
            Ta metoda usuwa kamienie, kt�re wypad�y poza obszar ekranu gry.

                - Przechodzi przez ka�dy kamie� (k) w li�cie self.kamienie.
                - Dla ka�dego kamienia, pobiera indeks kamienia (index) w li�cie self.kamienie.
                - Przypisuje kamie� (zmienna) na podstawie indeksu.
                - Sprawdza, czy pozycja Y kamienia (zmienna.pos[1]) przekracza warto�� 720 (wysoko�� ekranu).
                - Je�li tak, usuwa kamie� z listy self.kamienie za pomoc� del self.kamienie[index].
        """     
        for k in self.kamienie:
            index = self.kamienie.index(k)
            zmienna = self.kamienie[index]
            #if k is None:
            #    index = self.kamienie.index(k)
            #    del self.kamienie[index]
            if  zmienna.pos[1] > 720:
                del self.kamienie[index]
    
    def uwuwa_komete(self):
        """
            Ta metoda usuwa komety, kt�re wysz�y poza obszar ekranu gry.

                - Przechodzi przez ka�d� komet� (k) w li�cie self.komety.
                - Dla ka�dej komety, pobiera indeks komety (index) w li�cie self.komety.
                - Przypisuje komet� (zmienna) na podstawie indeksu.
                - Sprawdza, czy pozycja X komety (zmienna.pos[0]) przekracza warto�� 1300 (szeroko�� ekranu). ( Poza ekranem )
                - Je�li tak, usuwa komet� z listy self.komety za pomoc� del self.komety[index].
                - Sprawdza r�wnie�, czy pozycja X komety (zmienna.pos[0]) jest mniejsza ni� -10. ( Poza ekranem )
                - Je�li tak, r�wnie� usuwa komet� z listy self.komety.
        """
        for k in self.komety:
            index = self.komety.index(k)
            zmienna = self.komety[index]
            #if k is None:
            #    index = self.kamienie.index(k)
            #    del self.kamienie[index]
            if  zmienna.pos[0] > 1300:
                del self.komety[index]
            elif  zmienna.pos[0] < -10:
                del self.komety[index]         

    def kolizje(self):
        """
            Ta metoda obs�uguje kolizje mi�dzy obiektami w grze:
                - Dla ka�dego kamienia (k) w li�cie self.kamienie:
                    - Sprawdza kolizj� mi�dzy pozycj� strza�u gracza (self.player.strzal.pos) a kamieniem, tworz�c prostok�ty dla obu obiekt�w i u�ywaj�c colliderect() do sprawdzenia kolizji.
                        - Je�li jest kolizja, usuwa kamie� z listy self.kamienie, wywo�uje efekt trafienia strza�u (self.player.strzal.efekt(p)) i zwi�ksza licznik zniszczonych obiekt�w (self.zniszczone).
                    - Sprawdza r�wnie� kolizj� mi�dzy pozycj� gracza (self.player.pos) a kamieniem.
                        - Je�li jest kolizja, usuwa kamie� z listy self.kamienie.
                        - Je�li zdrowie gracza (self.zdrowie.del_health()) wynosi 1, wywo�uje metod� przegrana().

                - Dla ka�dej komety (k) w li�cie self.komety:
                    - Sprawdza kolizj� mi�dzy pozycj� strza�u gracza (self.player.strzal.pos) a komet�, tworz�c prostok�ty dla obu obiekt�w i u�ywaj�c colliderect() do sprawdzenia kolizji.
                        - Je�li jest kolizja, usuwa komet� z listy self.komety, wywo�uje efekt trafienia strza�u (self.player.strzal.efekt(p)) i zwi�ksza licznik zniszczonych obiekt�w (self.zniszczone).
                    - Sprawdza r�wnie� kolizj� mi�dzy pozycj� gracza (self.player.pos) a kometa.
                        - Je�li jest kolizja, usuwa komet� z listy self.komety.
                        - Je�li zdrowie gracza (self.zdrowie.del_health()) wynosi 1, wywo�uje metod� przegrana()
        """
        # for k in self.kamienie:#72 Dla kamienia
        for k in self.kamienie:# strzelanie
            for p in self.player.strzal.pos:
                if pygame.Rect(p[0], p[1], 10, 20).colliderect(pygame.Rect(k.pos[0], k.pos[1], 32, 32)): # Kamien vs strzal
                    self.kamienie.remove(k)
                    self.player.strzal.efekt(p)
                    self.zniszczone+=1 

            if pygame.Rect(self.player.pos[0], self.player.pos[1], 60, 20).colliderect(pygame.Rect(k.pos[0], k.pos[1], 30, 30)):# Kamien vs MY
                self.kamienie.remove(k)
                if self.zdrowie.del_health() == 1:
                    self.przegrana()
        

        #for k in self.komety:#72 Dla komety
        for k in self.komety:# strzelanie
            for p in self.player.strzal.pos:
                if pygame.Rect(p[0], p[1], 10, 20).colliderect(pygame.Rect(k.pos[0], k.pos[1], 72, 72)): # Kometa vs Strzal
                    self.komety.remove(k)
                    self.player.strzal.efekt(p)
                    self.zniszczone+=2

            if pygame.Rect(self.player.pos[0], self.player.pos[1], 60, 20).colliderect(pygame.Rect(k.pos[0], k.pos[1], 72, 72)):# Kometa vs MY
                self.komety.remove(k)
                if self.zdrowie.del_health() == 1:
                    self.przegrana()
     
    def kolizjeBOS(self):
        # Muj atak w bos
        """
            Metoda kolizjeBOS() obs�uguje kolizje zwi�zane z bossem:
                - Sprawdza kolizj� mi�dzy pozycj� strza�u gracza (self.player.strzal.pos) a atakiem bossa (self.Szef.atak.pos).
                    - Je�li jest kolizja, wywo�uje efekt trafienia ataku bossa (self.Szef.atak.efekt(k)) oraz efekt trafienia strza�u gracza (self.player.strzal.efekt(p)) i zwi�ksza licznik zniszczonych obiekt�w (self.zniszczone).
                - Sprawdza r�wnie� kolizj� mi�dzy pozycj� gracza (self.player.pos) a bossem (self.Szef.pos).
                    - Je�li jest kolizja, wywo�uje efekt trafienia ataku bossa (self.Szef.atak.efekt(k)).
                    - Je�li liczba trafie� bossa (self.Szef.trafienia) wynosi 0 lub mniej, zmienia faz� gry na 0, usuwa obiekt bossa (self.Szef).
                - Sprawdza kolizj� mi�dzy pozycj� gracza (self.player.pos) a atakiem bossa (self.Szef.atak.pos).
                    - Je�li jest kolizja, wywo�uje efekt trafienia ataku bossa (self.Szef.atak.efekt(k)).
                    - Je�li zdrowie gracza (self.zdrowie.del_health()) wynosi 1, wywo�uje metod� przegrana().
        """
        for p in self.player.strzal.pos:
            for k in self.Szef.atak.pos:
                    if pygame.Rect(p[0], p[1], 10, 20).colliderect(pygame.Rect(k[0], k[1], 72, 72)): # Trafienie ataku bosa
                        self.Szef.atak.efekt(k)
                        self.player.strzal.efekt(p)
                        self.zniszczone+=1

            if pygame.Rect(p[0], p[1], 10, 20).colliderect(pygame.Rect(self.Szef.pos[0], self.Szef.pos[1], 72, 72)):# Trafienie bosa
                self.Szef.atak.efekt(k)
                self.Szef.trafienia -= 1

            if self.Szef.trafienia <= 0:
                self.faza = 0
                del self.Szef
            #koniec bosa del szef
            
                        
        for k in self.Szef.atak.pos:
             if pygame.Rect(self.player.pos[0], self.player.pos[1], 60, 20).colliderect(pygame.Rect(k[0], k[1], 72, 72)):
                self.Szef.atak.efekt(k)
                if self.zdrowie.del_health() == 1:
                    self.przegrana()
                
                        

    def przegrana(self):
        """
            Ta metoda obs�uguje sytuacj� przegranej w grze:
                - Tworzona jest instancja klasy TW z biblioteki biblioteka, kt�ra jest interfejsem do obs�ugi tabeli wynik�w.
                - Wywo�ywana jest metoda DodajWynik() na obiekcie TW, przekazuj�c aktualny czas gry (self.zegarek.get_elapsed_time()), 
                  nick gracza (self.imie) i liczb� zniszczonych obiekt�w (self.zniszczone) jako parametry.
                - Nast�pnie zmienna self.Koniec jest ustawiana na 0, co ko�czy g��wn� p�tl� gry i zamyka program.
        """
        TW = biblioteka.TW()
        TW.DodajWynik(self.zegarek.get_elapsed_time(),self.imie, self.zniszczone)
        self.Koniec = 0
  
 #================================================================================================================================

class TabelaWynikow:
        """
        Klasa TabelaWynikow jest odpowiedzialna z wy�wietlanie i aktualizacj� danych tabel 10 nalepszych wynik�w graczy.
        """
        def __init__(self):
            """
                Ten konstruktor inicjalizuje obiekt TabeliWynikow:
                    - Ustala kolory t�a, czcionki i nag��wka.
                    - Okre�la szeroko��, wysoko�� tabeli oraz odst�py mi�dzy kom�rkami.
                    - Definiuje rozmiar czcionki i kolor tekstu.
                    - Okre�la nazw� nag��wka tabeli oraz nazwy kolumn.
                    - Inicjalizuje zmienn� DATA jako pust� list�.
                    - Wywo�uje metod� update_data() w celu zaktualizowania danych w tabeli.
                    - Inicjalizuje bibliotek� Pygame.
                    - Tworzy okno Pygame o okre�lonej szeroko�ci i wysoko�ci.
                    - Utworzenie czcionki za pomoc� pygame.font.SysFont.
            """
            self.BACKGROUND_COLOR = (255, 255, 255)  # Bia�y
            self.TABLE_WIDTH = 1280
            self.TABLE_HEIGHT = 720
            self.CELL_PADDING = 10
            self.FONT_SIZE = 24
            self.FONT_COLOR = (0, 0, 0)  # Czarny
            self.HEADER_COLOR = (200, 200, 200)  # Szary
            self.HEADER_TEXT = "Tabela Wynikow"
            self.COLUMN_NAMES = ["Nazwa", "Czas", "Trafienia"]
            self.DATA = []
            self.update_data()

            # Inicjalizacja Pygame
            pygame.init()

            # Utworzenie okna Pygame
            self.window = pygame.display.set_mode((self.TABLE_WIDTH, self.TABLE_HEIGHT))
            pygame.display.set_caption("Tabela Wynikow")

            # Utworzenie czcionki
            self.font = pygame.font.SysFont(None, self.FONT_SIZE)

        def update_data(self):
            """
                Zadaniem tej metoda aktualizuje dane w tabeli wynik�w:
                    - Tworzona jest instancja klasy TW z biblioteki biblioteka modu�u C++.
                    - Tworzone s� puste listy nazwy, czasy_g, czasy_m, czasy_s i pks.
                    - Wywo�ywana jest metoda Wyswietanie() na obiekcie TW, kt�ra pobiera dane z tabeli wynik�w.
                    - Przypisywane s� odpowiednie warto�ci zwr�cone przez metody getNazwa(), getCzas_G(), getCzas_M(), getCzas_S() i getPPK() do odpowiednich list.
                    - Nast�pnie w p�tli for dla ka�dego indeksu w zakresie d�ugo�ci listy nazwy:
                        - Przypisywane s� warto�ci z poszczeg�lnych list do zmiennych nazwa, czas_g, czas_m, czas_s i pk.
                        - Tworzony jest nowy wiersz danych w formacie [nazwa, czas, pk], gdzie czas jest sformatowany jako "HH:MM:SS".
                        - Ten wiersz danych jest dodawany do listy DATA.
            """
            TW= biblioteka.TW()
            nazwy=[]
            czasy_g=[]
            czasy_m=[]
            czasy_s=[]
            pks=[]
            TW.Wyswietanie()
            nazwy = TW.getNazwa() 
            czasy_g = TW.getCzas_G()
            czasy_m = TW.getCzas_M()
            czasy_s = TW.getCzas_S()
            pks = TW.getPPK()
            for i in range(len(nazwy)):
                nazwa = nazwy[i]
                czas_g = czasy_g[i]
                czas_m = czasy_m[i]
                czas_s = czasy_s[i]
                pk = pks[i]
                self.DATA.append([nazwa, f"{czas_g:02d}:{czas_m:02d}:{czas_s:02d}", pk])

        def draw_table(self):
            """
                Ta metoda rysuje tabel� wynik�w na ekranie:
                    - Najpierw ustawiane jest t�o okna na kolor okre�lony przez BACKGROUND_COLOR.
                    - Nast�pnie rysowany jest nag��wek tabeli, kt�ry sk�ada si� z tekstu HEADER_TEXT. 
                    Tekst ten jest renderowany na powierzchni za pomoc� czcionki font i umieszczany w odpowiednim prostok�cie header_rect.
                    Pod tym nag��wkiem rysowany jest prostok�t w kolorze HEADER_COLOR.
                    - Kolejnym krokiem jest rysowanie kolumn. Szeroko�� ka�dej kolumny jest obliczana na podstawie liczby kolumn i szeroko�ci tabeli.
                   Dla ka�dej nazwy kolumny w COLUMN_NAMES tworzona jest powierzchnia tekstowa column_surface, kt�ra jest renderowana w odpowiednim prostok�cie column_rect.
                   Pod ka�d� kolumn� rysowany jest prostok�t w kolorze HEADER_COLOR.
                    - Nast�pnie rysowane s� dane w tabeli. W p�tli for dla ka�dego wiersza w DATA:
                        - Dla ka�dej warto�ci w wierszu tworzona jest powierzchnia tekstowa data_surface, kt�ra jest renderowana w odpowiednim prostok�cie data_rect.
                        Pod ka�d� warto�ci� rysowany jest prostok�t w kolorze BACKGROUND_COLOR.
                    - Na koniec aktualizowane jest okno Pygame za pomoc� pygame.display.update(),
                   co powoduje wy�wietlenie narysowanej tabeli na ekranie.
            """
            # Ustawienie t�a
            self.window.fill(self.BACKGROUND_COLOR)

            # Rysowanie nag��wka tabeli
            header_surface = self.font.render(self.HEADER_TEXT, True, self.FONT_COLOR)
            header_rect = header_surface.get_rect(center=(self.TABLE_WIDTH // 2, self.CELL_PADDING + self.FONT_SIZE // 2))
            pygame.draw.rect(self.window, self.HEADER_COLOR, pygame.Rect(self.CELL_PADDING, self.CELL_PADDING, self.TABLE_WIDTH - 2 * self.CELL_PADDING, self.FONT_SIZE + 2 * self.CELL_PADDING))
            self.window.blit(header_surface, header_rect)

            # Rysowanie kolumn
            column_width = (self.TABLE_WIDTH - 2 * self.CELL_PADDING) // len(self.COLUMN_NAMES)
            column_x = self.CELL_PADDING
            for column_name in self.COLUMN_NAMES:
                column_surface = self.font.render(column_name, True, self.FONT_COLOR)
                column_rect = column_surface.get_rect(center=(column_x + column_width // 2, self.CELL_PADDING + self.FONT_SIZE + self.CELL_PADDING // 2))
                pygame.draw.rect(self.window, self.HEADER_COLOR, pygame.Rect(column_x, self.CELL_PADDING, column_width, self.FONT_SIZE + self.CELL_PADDING))
                self.window.blit(column_surface, column_rect)
                column_x += column_width

            # Rysowanie danych
            data_y = self.CELL_PADDING + self.FONT_SIZE + self.CELL_PADDING
            for row in self.DATA:
                data_x = self.CELL_PADDING
                for value in row:
                    data_surface = self.font.render(str(value), True, self.FONT_COLOR)
                    data_rect = data_surface.get_rect(center=(data_x + column_width // 2, data_y + self.FONT_SIZE // 2))
                    pygame.draw.rect(self.window, self.BACKGROUND_COLOR, pygame.Rect(data_x, data_y, column_width, self.FONT_SIZE))
                    self.window.blit(data_surface, data_rect)
                    data_x += column_width
                data_y += self.FONT_SIZE

            # Aktualizacja okna Pygame
            pygame.display.update()

        def run_table(self):
            """
                Ta metoda jest g��wn� p�tl� programu tabeli wynik�w. 
                Wykonuje si� w niej p�tla while, kt�ra dzia�a dop�ki zmienna running ma warto�� True. 
                Wewn�trz p�tli nast�puje nas�uchiwanie zdarze� Pygame za pomoc� pygame.event.get(). 
                Dla ka�dego zdarzenia sprawdzane jest jego typ, 
                a je�li jest to zdarzenie pygame.QUIT (np. zamkni�cie okna), 
                to warto�� running ustawiana jest na False, co powoduje wyj�cie z p�tli i 
                zako�czenie dzia�ania programu tabeli wynik�w
            """
            # G��wna p�tla Tabeli
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Zamkni�cie Pygame
            #pygame.quit()

 #================================================================================================================================

class MainMenu(object):
    """
        Zadaniem tej klasy MainMenu jest wy�wielenie manu, obs�uga zda�en a takrze wybor�w gracza. 
        A takrze pobranie nick-u od gracza. 
    """
    def __init__(self):
        """
            W konstruktorze tej klasy inicjalizowane s� r�ne elementy gry. 
            �aduje si� obrazek t�a za pomoc� pygame.image.load(), 
            tworzone jest okno o rozmiarze 1280x720 pikseli za pomoc� pygame.display.set_mode(), 
            ustawiany jest tytu� okna za pomoc� pygame.display.set_caption(), 
            tworzony jest obiekt zegara gry za pomoc� pygame.time.Clock(), 
            a tak�e ustawiana jest czcionka tekstu za pomoc� pygame.font.Font(). 
            Tworzone s� r�wnie� przyciski "Start" i "High Scores" jako prostok�tne obszary pygame.Rect(), 
            a obrazek t�a wczytywany jest ponownie do zmiennej self.tlo.
        """
        self.tlo = pygame.image.load("tlo1.png")
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Wojna w Kosmosie")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)
        
        self.start_game_button = pygame.Rect(520, 300, 200, 50)
        self.high_scores_button = pygame.Rect(520, 400, 200, 50)
        self.tlo = pygame.image.load("tlo1.png")

    def run(self):
        """
            Metoda run() to g��wna p�tla menu, kt�ra dzia�a w niesko�czono��. 
            Wewn�trz p�tli sprawdzane s� zdarzenia generowane przez Pygame, takie jak naci�ni�cie przycisku zamykania okna lub klikni�cie mysz�. 
            Je�li zostanie naci�ni�ty przycisk zamykania, to gra zostaje zako�czona poprzez wywo�anie funkcji sys.exit(). 
            Je�li zostanie wykonane klikni�cie mysz�, sprawdzane jest, 
            czy naci�ni�ty przycisk to lewy przycisk myszy, 
            a nast�pnie sprawdzane s� kolizje z przyciskami "Start" i "High Scores" za pomoc� metody collidepoint(). 
            Je�li klikni�cie nast�pi�o na przycisku "Start", wywo�ywana jest metoda start_game(), 
            a je�li na przycisku "High Scores", wywo�ywana jest metoda top10().

            Nast�pnie od�wie�ane jest t�o ekranu gry przy u�yciu metody blit() wraz z obrazkiem t�a, 
            a nast�pnie rysowany jest tytu� gry i przyciski za pomoc� odpowiednich metod. 
            Na koniec aktualizowane jest okno Pygame przy u�yciu metody flip(), 
            a ograniczenie liczby klatek na sekund� jest ustawione na 60 za pomoc� clock.tick(60).
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = event.pos
                        if self.start_game_button.collidepoint(mouse_pos):
                            self.start_game()
                        elif self.high_scores_button.collidepoint(mouse_pos):
                            self.top10()

            #self.screen.fill((0, 0, 0))
            self.screen.blit(self.tlo, (0, 0))
            self.draw_title()
            self.draw_buttons()
            
            pygame.display.flip()
            self.clock.tick(60)

    def draw_buttons(self):
        """
            Metoda draw_buttons() s�u�y do rysowania przycisk�w na ekranie gry. 
            Wykorzystuje funkcj� pygame.draw.rect() do narysowania prostok�tnych kszta�t�w przycisk�w, 
            gdzie pierwszy argument to powierzchnia, na kt�rej maj� by� rysowane (w tym przypadku self.screen), 
            drugi argument to kolor przycisku, a trzeci argument to prostok�t definiuj�cy po�o�enie i 
            rozmiar przycisku.

            Nast�pnie, za pomoc� metody self.font.render() generowane s� powierzchnie z tekstem przycisk�w. 
            Tekst przycisku "Rozpocznij gre" jest renderowany z bia�ym kolorem, 
            a tekst przycisku "Tabela wynikow" jest r�wnie� renderowany z bia�ym kolorem. 
            Ka�da powierzchnia tekstu ma przypisane wsp�rz�dne, tak aby by�y wy�rodkowane.

            Na koniec, powierzchnie tekstu s� umieszczane na ekranie gry przy u�yciu metody blit(), 
            kt�ra kopiuje zawarto�� jednej powierzchni na drug�.
        """
        pygame.draw.rect(self.screen, (0, 230, 0), self.start_game_button)
        pygame.draw.rect(self.screen, (230, 0, 0), self.high_scores_button)

        start_game_text = self.font.render("Rozpocznij gre", True, (255, 255, 255))
        start_game_text_rect = start_game_text.get_rect(center=self.start_game_button.center)
        self.screen.blit(start_game_text, start_game_text_rect)

        high_scores_text = self.font.render("Tabela wynikow", True, (255, 255, 255))
        high_scores_text_rect = high_scores_text.get_rect(center=self.high_scores_button.center)
        self.screen.blit(high_scores_text, high_scores_text_rect)

    def draw_title(self):
        """
            Metoda draw_title() s�u�y do rysowania tytu�u gry na ekranie. 
            Wykorzystuje funkcj� self.font.render() do wygenerowania powierzchni z tekstem tytu�u. 
            Tekst tytu�u "Wojna w Kosmosie" jest renderowany z bia�ym kolorem.

            Nast�pnie, metoda get_rect() jest u�ywana na powierzchni tekstu, 
            aby uzyska� prostok�t okre�laj�cy po�o�enie i rozmiar tekstu. 
            W tym przypadku, prostok�t jest wy�rodkowany wzd�u� osi x na warto�ci 620, 
            a wysoko�� tekstu jest ustalona na warto�� 50.

            Na ko�cu, powierzchnia tekstu tytu�u jest umieszczana na ekranie gry przy u�yciu metody blit(), 
            kt�ra kopiuje zawarto�� jednej powierzchni na drug�.
        """
        title_text = self.font.render("Wojna w Kosmosie", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center = (620, 50))
        self.screen.blit(title_text, title_text_rect)

    def start_game(self):
        """
            Metoda start_game() umo�liwia graczowi wprowadzenie swojego nicku przed rozpocz�ciem gry, 
            a� do wprowadzenia poprawnego nicku.

            Metoda start_game() odpowiada za rozpocz�cie gry poprzez pobranie nicku od gracza. Na pocz�tku, 
            tytu� okna gry jest ustawiany na "Nick". Tworzony jest r�wnie� zegar (clock) oraz czcionka (font).

            Nast�pnie, tworzony jest prostok�t (input_rect), kt�ry s�u�y do przechowywania pola tekstowego, 
            gdzie gracz wprowadza sw�j nick. Inicjalnie, pole tekstowe jest puste (input_text = "") oraz zmienna nick przechowuje warto�� nicku.

            W p�tli while, program oczekuje na wprowadzenie poprawnego nicku przez gracza. W ka�dej iteracji p�tli, 
            odczytywane s� zdarzenia od u�ytkownika. Je�li gracz naci�nie klawisz BACKSPACE, ostatni znak w polu tekstowym zostaje usuni�ty. 
            Je�li gracz naci�nie klawisz RETURN, wprowadzony nick zostaje zatwierdzony i przypisany do zmiennej nick. 
            W przeciwnym razie, je�li gracz wprowadzi inny klawisz, jego znak jest dodawany do pola tekstowego input_text.

            W ka�dej iteracji p�tli, ekran gry jest czyszczony i rysowany na nowo. 
            Pole tekstowe jest renderowane jako powierzchnia tekstu za pomoc� czcionki self.font.render(), 
            a nast�pnie umieszczane na ekranie. R�wnie� rysowany jest prostok�t wok� pola tekstowego, aby wskaza�, �e jest aktywne.

            P�tla wykonuje si�, dop�ki wprowadzony nick nie zostanie uznany za poprawny przez obiekt n klasy biblioteka.Nick() z modu�u c++. 
            Po spe�nieniu tego warunku, zostaje utworzony obiekt Game z przekazanym nickiem, co oznacza rozpocz�cie w�a�ciwej gry.

        """
        pygame.display.set_caption("Nick")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)
        input_rect = pygame.Rect(520, 300, 200, 50)
        input_text = ""
        nick = ""
        n = biblioteka.Nick()
        while not n.czyPoprawnyNick(nick):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]  # Usu� ostatni znak
                    elif event.key == pygame.K_RETURN:
                        #print("Wprowadzony tekst:", input_text)
                        nick = input_text
                        input_text = ""
                        
                    else:
                        input_text += event.unicode

            self.screen.blit(self.tlo, (0, 0))
            
            input_surface = self.font.render(input_text, True, (255, 255, 255))
            self.screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

            self.draw_title()
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 2)
            pygame.display.flip()
            clock.tick(60)
        Game(nick)

    def top10(self):
        """
            Metoda top10() s�u�y do wy�wietlenia i obs�ugi tabeli wynik�w poprzez tworzenie obiektu tabeli, 
            rysowanie tabeli na ekranie oraz uruchomienie p�tli obs�uguj�cej tabel� wynik�w.

            Metoda top10() odpowiada za wy�wietlenie i obs�ug� tabeli wynik�w.

            Najpierw tworzony jest obiekt tabela klasy TabelaWynikow, 
            kt�ry reprezentuje tabel� wynik�w. Nast�pnie wywo�ywana jest metoda draw_table() tego obiektu, 
            kt�ra rysuje tabel� wynik�w na ekranie.

            Po narysowaniu tabeli, uruchamiana jest metoda run_table(), 
            kt�ra inicjuje g��wn� p�tl� odpowiedzialn� za obs�ug� tabeli wynik�w. 
            W tej p�tli oczekuje si� na zdarzenia od u�ytkownika, takie jak wci�ni�cie przycisku zamykania okna. 
            Wy�wietlanie i obs�uga tabeli wynik�w odbywa si� w tej p�tli, umo�liwiaj�c interakcj� u�ytkownika z tabel�.
        """
        tabela = TabelaWynikow()
        tabela.draw_table()
        tabela.run_table()

    



