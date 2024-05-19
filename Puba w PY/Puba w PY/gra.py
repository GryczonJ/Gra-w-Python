# class gra

from gracz import Gracz
from zrowie import Health
from Clock import Zegar
from przeciwnik import Kometa, Skala, Boss
import pygame, sys, random, pybind11
import biblioteka
class Game(object):
    """
        Klasa Game jest odpowiedzialna z przeprowadznie rozgrywki, wyœwietanie i zmianê obiektów na ekranie gry.
        A takrze za obs³ugê zda¿ñ.
    """
    def __init__(self, nick):
        """
        Konstruktor tej klasy inicjalizuje ró¿ne parametry i obiekty potrzebne do dzia³ania gry.
            - Przyjmuje argument nick, który jest nickiem gracza. Potrzebny do wpisania do tabeli po przegranej
            - Inicjalizuje zmienn¹ self.faza na wartoœæ 0. fazy zmieniaj¹ siê w czasie gry.
            - Ustawia maksymaln¹ wartoœæ self.tps_max na 100.0, która kontroluje prêdkoœæ odœwie¿ania gry.
            - Przypisuje wartoœæ argumentu nick do zmiennej self.imie.
            - Inicjalizuje modu³ Pygame za pomoc¹ pygame.init().
            - Ustawia tytu³ gry na "Wojna w Kosmosie" przy u¿yciu pygame.display.set_caption().
            - £aduje ikonê gry z pliku "3.png" i ustawia j¹ jako ikonê okna gry. Logo.
            - Tworzy ekran gry o rozmiarze 1280x720 pikseli za pomoc¹ pygame.display.set_mode().
            - Inicjalizuje zegar self.tps_clock i zmienn¹ self.tps_delta do œledzenia czasu odœwie¿ania gry.
            - Ustala punkt odniesienia czasu dodania kamieni i komet na aktualny czas w milisekundach pygame.time.get_ticks().
            - Inicjalizuje obiekty gracza (self.player), zdrowia (self.zdrowie), zegara (self.zegarek).
            - Tworzy pust¹ listê kamieni i komet (self.kamienie, self.komety).
            - Inicjalizuje zmienn¹ self.zniszczone na 0.
            - Ustala wartoœæ self.Koniec na 1.
            - £aduje t³o gry z pliku "tlo1.png".
            - Rozpoczyna pêtlê obs³ugi zdarzeñ while self.Koniec == 1.
            - W pêtli obs³ugi zdarzeñ sprawdza zdarzenia takie jak zamykanie okna gry (pygame.QUIT).
            - Sprawdza równie¿ naciœniêcie klawisza ESC, co powoduje wyjœcie z pêtli i przechodzi do kolejnej fazy gry.
            - Jeœli faza gry jest równa 0, sprawdza czy czas od ostatniego wydarzenia jest wiêkszy lub równy losowej wartoœci miêdzy 30000 a 40000 milisekund.
            - Jeœli tak, tworzy obiekt Szefa (self.Szef) i zwiêksza wartoœæ self.faza o 1.
            - Wywo³uje metodê czas_na_kamienie().
            - Oblicza czas trwania programu i odmierza czas (self.tps_delta) z dok³adnoœci¹ do 1/self.tps_max.
            - Wywo³uje metody tick(), uwuwa_kamienie(), uwuwa_komete(), kolizje().
            - Wyœwietla t³o na ekranie gry self.screen.blit(tlo, (0, 0)).
            - Wywo³uje metody self.draw().
            - Odœwie¿a ekran pygame.display.flip().
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
            Ta metoda tick() aktualizuje stan ró¿nych elementów gry w ka¿dym kroku gry.
                - Wywo³uje metodê tick() dla obiektu gracza (self.player), co pozwala na aktualizacjê jego stanu.
                - Wywo³uje metodê add_health() dla obiektu zdrowia (self.zdrowie), przekazuj¹c iloœæ zniszczonych obiektów jako argument, aby zwiêkszyæ poziom zdrowia gracza.
                - Wywo³uje metodê tick() dla ka¿dego obiektu kamienia w liœcie self.kamienie, co pozwala na ich aktualizacjê.
                - Wywo³uje metodê tick() dla ka¿dego obiektu komety w liœcie self.komety, co pozwala na ich aktualizacjê.
                - Jeœli faza gry jest równa 1, wykonuje odpowiednie operacje dla bossa (self.Szef), takie jak animacja wjazdu.
                - Jeœli faza gry jest równa 2, wykonuje operacje zwi¹zane z kolizjami z bossem (self.kolizjeBOS()) i aktualizuje stan bossa (self.Szef.tick()).
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
            Ta metoda sprawdza czas trwania gry i decyduje, czy dodawaæ kamienie i komety na ekran.

            - Sprawdza aktualny czas za pomoc¹ pygame.time.get_ticks().
            - Jeœli czas od ostatniego dodania kamienia przekracza 500 milisekund, 
            wywo³uje metodê dodaj_kamienie() w celu dodania nowych kamieni na ekran.

            - Aktualizuje czas ostatniego dodania kamienia na bie¿¹cy czas.
            - Jeœli czas od ostatniego dodania komety przekracza losow¹ wartoœæ miêdzy 8000 a 10000 milisekund, 
            wywo³uje metodê dodaj_komete() w celu dodania nowych komet na ekran.

            - Aktualizuje czas ostatniego dodania komety na bie¿¹cy czas.
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
            Ta metoda usuwa kamienie, które wypad³y poza obszar ekranu gry.

                - Przechodzi przez ka¿dy kamieñ (k) w liœcie self.kamienie.
                - Dla ka¿dego kamienia, pobiera indeks kamienia (index) w liœcie self.kamienie.
                - Przypisuje kamieñ (zmienna) na podstawie indeksu.
                - Sprawdza, czy pozycja Y kamienia (zmienna.pos[1]) przekracza wartoœæ 720 (wysokoœæ ekranu).
                - Jeœli tak, usuwa kamieñ z listy self.kamienie za pomoc¹ del self.kamienie[index].
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
            Ta metoda usuwa komety, które wysz³y poza obszar ekranu gry.

                - Przechodzi przez ka¿d¹ kometê (k) w liœcie self.komety.
                - Dla ka¿dej komety, pobiera indeks komety (index) w liœcie self.komety.
                - Przypisuje kometê (zmienna) na podstawie indeksu.
                - Sprawdza, czy pozycja X komety (zmienna.pos[0]) przekracza wartoœæ 1300 (szerokoœæ ekranu). ( Poza ekranem )
                - Jeœli tak, usuwa kometê z listy self.komety za pomoc¹ del self.komety[index].
                - Sprawdza równie¿, czy pozycja X komety (zmienna.pos[0]) jest mniejsza ni¿ -10. ( Poza ekranem )
                - Jeœli tak, równie¿ usuwa kometê z listy self.komety.
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
            Ta metoda obs³uguje kolizje miêdzy obiektami w grze:
                - Dla ka¿dego kamienia (k) w liœcie self.kamienie:
                    - Sprawdza kolizjê miêdzy pozycj¹ strza³u gracza (self.player.strzal.pos) a kamieniem, tworz¹c prostok¹ty dla obu obiektów i u¿ywaj¹c colliderect() do sprawdzenia kolizji.
                        - Jeœli jest kolizja, usuwa kamieñ z listy self.kamienie, wywo³uje efekt trafienia strza³u (self.player.strzal.efekt(p)) i zwiêksza licznik zniszczonych obiektów (self.zniszczone).
                    - Sprawdza równie¿ kolizjê miêdzy pozycj¹ gracza (self.player.pos) a kamieniem.
                        - Jeœli jest kolizja, usuwa kamieñ z listy self.kamienie.
                        - Jeœli zdrowie gracza (self.zdrowie.del_health()) wynosi 1, wywo³uje metodê przegrana().

                - Dla ka¿dej komety (k) w liœcie self.komety:
                    - Sprawdza kolizjê miêdzy pozycj¹ strza³u gracza (self.player.strzal.pos) a komet¹, tworz¹c prostok¹ty dla obu obiektów i u¿ywaj¹c colliderect() do sprawdzenia kolizji.
                        - Jeœli jest kolizja, usuwa kometê z listy self.komety, wywo³uje efekt trafienia strza³u (self.player.strzal.efekt(p)) i zwiêksza licznik zniszczonych obiektów (self.zniszczone).
                    - Sprawdza równie¿ kolizjê miêdzy pozycj¹ gracza (self.player.pos) a kometa.
                        - Jeœli jest kolizja, usuwa kometê z listy self.komety.
                        - Jeœli zdrowie gracza (self.zdrowie.del_health()) wynosi 1, wywo³uje metodê przegrana()
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
            Metoda kolizjeBOS() obs³uguje kolizje zwi¹zane z bossem:
                - Sprawdza kolizjê miêdzy pozycj¹ strza³u gracza (self.player.strzal.pos) a atakiem bossa (self.Szef.atak.pos).
                    - Jeœli jest kolizja, wywo³uje efekt trafienia ataku bossa (self.Szef.atak.efekt(k)) oraz efekt trafienia strza³u gracza (self.player.strzal.efekt(p)) i zwiêksza licznik zniszczonych obiektów (self.zniszczone).
                - Sprawdza równie¿ kolizjê miêdzy pozycj¹ gracza (self.player.pos) a bossem (self.Szef.pos).
                    - Jeœli jest kolizja, wywo³uje efekt trafienia ataku bossa (self.Szef.atak.efekt(k)).
                    - Jeœli liczba trafieñ bossa (self.Szef.trafienia) wynosi 0 lub mniej, zmienia fazê gry na 0, usuwa obiekt bossa (self.Szef).
                - Sprawdza kolizjê miêdzy pozycj¹ gracza (self.player.pos) a atakiem bossa (self.Szef.atak.pos).
                    - Jeœli jest kolizja, wywo³uje efekt trafienia ataku bossa (self.Szef.atak.efekt(k)).
                    - Jeœli zdrowie gracza (self.zdrowie.del_health()) wynosi 1, wywo³uje metodê przegrana().
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
            Ta metoda obs³uguje sytuacjê przegranej w grze:
                - Tworzona jest instancja klasy TW z biblioteki biblioteka, która jest interfejsem do obs³ugi tabeli wyników.
                - Wywo³ywana jest metoda DodajWynik() na obiekcie TW, przekazuj¹c aktualny czas gry (self.zegarek.get_elapsed_time()), 
                  nick gracza (self.imie) i liczbê zniszczonych obiektów (self.zniszczone) jako parametry.
                - Nastêpnie zmienna self.Koniec jest ustawiana na 0, co koñczy g³ówn¹ pêtlê gry i zamyka program.
        """
        TW = biblioteka.TW()
        TW.DodajWynik(self.zegarek.get_elapsed_time(),self.imie, self.zniszczone)
        self.Koniec = 0
  
 #================================================================================================================================

class TabelaWynikow:
        """
        Klasa TabelaWynikow jest odpowiedzialna z wyœwietlanie i aktualizacjê danych tabel 10 nalepszych wyników graczy.
        """
        def __init__(self):
            """
                Ten konstruktor inicjalizuje obiekt TabeliWynikow:
                    - Ustala kolory t³a, czcionki i nag³ówka.
                    - Okreœla szerokoœæ, wysokoœæ tabeli oraz odstêpy miêdzy komórkami.
                    - Definiuje rozmiar czcionki i kolor tekstu.
                    - Okreœla nazwê nag³ówka tabeli oraz nazwy kolumn.
                    - Inicjalizuje zmienn¹ DATA jako pust¹ listê.
                    - Wywo³uje metodê update_data() w celu zaktualizowania danych w tabeli.
                    - Inicjalizuje bibliotekê Pygame.
                    - Tworzy okno Pygame o okreœlonej szerokoœci i wysokoœci.
                    - Utworzenie czcionki za pomoc¹ pygame.font.SysFont.
            """
            self.BACKGROUND_COLOR = (255, 255, 255)  # Bia³y
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
                Zadaniem tej metoda aktualizuje dane w tabeli wyników:
                    - Tworzona jest instancja klasy TW z biblioteki biblioteka modu³u C++.
                    - Tworzone s¹ puste listy nazwy, czasy_g, czasy_m, czasy_s i pks.
                    - Wywo³ywana jest metoda Wyswietanie() na obiekcie TW, która pobiera dane z tabeli wyników.
                    - Przypisywane s¹ odpowiednie wartoœci zwrócone przez metody getNazwa(), getCzas_G(), getCzas_M(), getCzas_S() i getPPK() do odpowiednich list.
                    - Nastêpnie w pêtli for dla ka¿dego indeksu w zakresie d³ugoœci listy nazwy:
                        - Przypisywane s¹ wartoœci z poszczególnych list do zmiennych nazwa, czas_g, czas_m, czas_s i pk.
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
                Ta metoda rysuje tabelê wyników na ekranie:
                    - Najpierw ustawiane jest t³o okna na kolor okreœlony przez BACKGROUND_COLOR.
                    - Nastêpnie rysowany jest nag³ówek tabeli, który sk³ada siê z tekstu HEADER_TEXT. 
                    Tekst ten jest renderowany na powierzchni za pomoc¹ czcionki font i umieszczany w odpowiednim prostok¹cie header_rect.
                    Pod tym nag³ówkiem rysowany jest prostok¹t w kolorze HEADER_COLOR.
                    - Kolejnym krokiem jest rysowanie kolumn. Szerokoœæ ka¿dej kolumny jest obliczana na podstawie liczby kolumn i szerokoœci tabeli.
                   Dla ka¿dej nazwy kolumny w COLUMN_NAMES tworzona jest powierzchnia tekstowa column_surface, która jest renderowana w odpowiednim prostok¹cie column_rect.
                   Pod ka¿d¹ kolumn¹ rysowany jest prostok¹t w kolorze HEADER_COLOR.
                    - Nastêpnie rysowane s¹ dane w tabeli. W pêtli for dla ka¿dego wiersza w DATA:
                        - Dla ka¿dej wartoœci w wierszu tworzona jest powierzchnia tekstowa data_surface, która jest renderowana w odpowiednim prostok¹cie data_rect.
                        Pod ka¿d¹ wartoœci¹ rysowany jest prostok¹t w kolorze BACKGROUND_COLOR.
                    - Na koniec aktualizowane jest okno Pygame za pomoc¹ pygame.display.update(),
                   co powoduje wyœwietlenie narysowanej tabeli na ekranie.
            """
            # Ustawienie t³a
            self.window.fill(self.BACKGROUND_COLOR)

            # Rysowanie nag³ówka tabeli
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
                Ta metoda jest g³ówn¹ pêtl¹ programu tabeli wyników. 
                Wykonuje siê w niej pêtla while, która dzia³a dopóki zmienna running ma wartoœæ True. 
                Wewn¹trz pêtli nastêpuje nas³uchiwanie zdarzeñ Pygame za pomoc¹ pygame.event.get(). 
                Dla ka¿dego zdarzenia sprawdzane jest jego typ, 
                a jeœli jest to zdarzenie pygame.QUIT (np. zamkniêcie okna), 
                to wartoœæ running ustawiana jest na False, co powoduje wyjœcie z pêtli i 
                zakoñczenie dzia³ania programu tabeli wyników
            """
            # G³ówna pêtla Tabeli
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Zamkniêcie Pygame
            #pygame.quit()

 #================================================================================================================================

class MainMenu(object):
    """
        Zadaniem tej klasy MainMenu jest wyœwielenie manu, obs³uga zda¿en a takrze wyborów gracza. 
        A takrze pobranie nick-u od gracza. 
    """
    def __init__(self):
        """
            W konstruktorze tej klasy inicjalizowane s¹ ró¿ne elementy gry. 
            £aduje siê obrazek t³a za pomoc¹ pygame.image.load(), 
            tworzone jest okno o rozmiarze 1280x720 pikseli za pomoc¹ pygame.display.set_mode(), 
            ustawiany jest tytu³ okna za pomoc¹ pygame.display.set_caption(), 
            tworzony jest obiekt zegara gry za pomoc¹ pygame.time.Clock(), 
            a tak¿e ustawiana jest czcionka tekstu za pomoc¹ pygame.font.Font(). 
            Tworzone s¹ równie¿ przyciski "Start" i "High Scores" jako prostok¹tne obszary pygame.Rect(), 
            a obrazek t³a wczytywany jest ponownie do zmiennej self.tlo.
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
            Metoda run() to g³ówna pêtla menu, która dzia³a w nieskoñczonoœæ. 
            Wewn¹trz pêtli sprawdzane s¹ zdarzenia generowane przez Pygame, takie jak naciœniêcie przycisku zamykania okna lub klikniêcie mysz¹. 
            Jeœli zostanie naciœniêty przycisk zamykania, to gra zostaje zakoñczona poprzez wywo³anie funkcji sys.exit(). 
            Jeœli zostanie wykonane klikniêcie mysz¹, sprawdzane jest, 
            czy naciœniêty przycisk to lewy przycisk myszy, 
            a nastêpnie sprawdzane s¹ kolizje z przyciskami "Start" i "High Scores" za pomoc¹ metody collidepoint(). 
            Jeœli klikniêcie nast¹pi³o na przycisku "Start", wywo³ywana jest metoda start_game(), 
            a jeœli na przycisku "High Scores", wywo³ywana jest metoda top10().

            Nastêpnie odœwie¿ane jest t³o ekranu gry przy u¿yciu metody blit() wraz z obrazkiem t³a, 
            a nastêpnie rysowany jest tytu³ gry i przyciski za pomoc¹ odpowiednich metod. 
            Na koniec aktualizowane jest okno Pygame przy u¿yciu metody flip(), 
            a ograniczenie liczby klatek na sekundê jest ustawione na 60 za pomoc¹ clock.tick(60).
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
            Metoda draw_buttons() s³u¿y do rysowania przycisków na ekranie gry. 
            Wykorzystuje funkcjê pygame.draw.rect() do narysowania prostok¹tnych kszta³tów przycisków, 
            gdzie pierwszy argument to powierzchnia, na której maj¹ byæ rysowane (w tym przypadku self.screen), 
            drugi argument to kolor przycisku, a trzeci argument to prostok¹t definiuj¹cy po³o¿enie i 
            rozmiar przycisku.

            Nastêpnie, za pomoc¹ metody self.font.render() generowane s¹ powierzchnie z tekstem przycisków. 
            Tekst przycisku "Rozpocznij gre" jest renderowany z bia³ym kolorem, 
            a tekst przycisku "Tabela wynikow" jest równie¿ renderowany z bia³ym kolorem. 
            Ka¿da powierzchnia tekstu ma przypisane wspó³rzêdne, tak aby by³y wyœrodkowane.

            Na koniec, powierzchnie tekstu s¹ umieszczane na ekranie gry przy u¿yciu metody blit(), 
            która kopiuje zawartoœæ jednej powierzchni na drug¹.
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
            Metoda draw_title() s³u¿y do rysowania tytu³u gry na ekranie. 
            Wykorzystuje funkcjê self.font.render() do wygenerowania powierzchni z tekstem tytu³u. 
            Tekst tytu³u "Wojna w Kosmosie" jest renderowany z bia³ym kolorem.

            Nastêpnie, metoda get_rect() jest u¿ywana na powierzchni tekstu, 
            aby uzyskaæ prostok¹t okreœlaj¹cy po³o¿enie i rozmiar tekstu. 
            W tym przypadku, prostok¹t jest wyœrodkowany wzd³u¿ osi x na wartoœci 620, 
            a wysokoœæ tekstu jest ustalona na wartoœæ 50.

            Na koñcu, powierzchnia tekstu tytu³u jest umieszczana na ekranie gry przy u¿yciu metody blit(), 
            która kopiuje zawartoœæ jednej powierzchni na drug¹.
        """
        title_text = self.font.render("Wojna w Kosmosie", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center = (620, 50))
        self.screen.blit(title_text, title_text_rect)

    def start_game(self):
        """
            Metoda start_game() umo¿liwia graczowi wprowadzenie swojego nicku przed rozpoczêciem gry, 
            a¿ do wprowadzenia poprawnego nicku.

            Metoda start_game() odpowiada za rozpoczêcie gry poprzez pobranie nicku od gracza. Na pocz¹tku, 
            tytu³ okna gry jest ustawiany na "Nick". Tworzony jest równie¿ zegar (clock) oraz czcionka (font).

            Nastêpnie, tworzony jest prostok¹t (input_rect), który s³u¿y do przechowywania pola tekstowego, 
            gdzie gracz wprowadza swój nick. Inicjalnie, pole tekstowe jest puste (input_text = "") oraz zmienna nick przechowuje wartoœæ nicku.

            W pêtli while, program oczekuje na wprowadzenie poprawnego nicku przez gracza. W ka¿dej iteracji pêtli, 
            odczytywane s¹ zdarzenia od u¿ytkownika. Jeœli gracz naciœnie klawisz BACKSPACE, ostatni znak w polu tekstowym zostaje usuniêty. 
            Jeœli gracz naciœnie klawisz RETURN, wprowadzony nick zostaje zatwierdzony i przypisany do zmiennej nick. 
            W przeciwnym razie, jeœli gracz wprowadzi inny klawisz, jego znak jest dodawany do pola tekstowego input_text.

            W ka¿dej iteracji pêtli, ekran gry jest czyszczony i rysowany na nowo. 
            Pole tekstowe jest renderowane jako powierzchnia tekstu za pomoc¹ czcionki self.font.render(), 
            a nastêpnie umieszczane na ekranie. Równie¿ rysowany jest prostok¹t wokó³ pola tekstowego, aby wskazaæ, ¿e jest aktywne.

            Pêtla wykonuje siê, dopóki wprowadzony nick nie zostanie uznany za poprawny przez obiekt n klasy biblioteka.Nick() z modu³u c++. 
            Po spe³nieniu tego warunku, zostaje utworzony obiekt Game z przekazanym nickiem, co oznacza rozpoczêcie w³aœciwej gry.

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
                        input_text = input_text[:-1]  # Usuñ ostatni znak
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
            Metoda top10() s³u¿y do wyœwietlenia i obs³ugi tabeli wyników poprzez tworzenie obiektu tabeli, 
            rysowanie tabeli na ekranie oraz uruchomienie pêtli obs³uguj¹cej tabelê wyników.

            Metoda top10() odpowiada za wyœwietlenie i obs³ugê tabeli wyników.

            Najpierw tworzony jest obiekt tabela klasy TabelaWynikow, 
            który reprezentuje tabelê wyników. Nastêpnie wywo³ywana jest metoda draw_table() tego obiektu, 
            która rysuje tabelê wyników na ekranie.

            Po narysowaniu tabeli, uruchamiana jest metoda run_table(), 
            która inicjuje g³ówn¹ pêtlê odpowiedzialn¹ za obs³ugê tabeli wyników. 
            W tej pêtli oczekuje siê na zdarzenia od u¿ytkownika, takie jak wciœniêcie przycisku zamykania okna. 
            Wyœwietlanie i obs³uga tabeli wyników odbywa siê w tej pêtli, umo¿liwiaj¹c interakcjê u¿ytkownika z tabel¹.
        """
        tabela = TabelaWynikow()
        tabela.draw_table()
        tabela.run_table()

    



