
import pygame
from pygame.math import Vector2
from Dziedziczenie import NaEkranie
pygame.init()
class Health(NaEkranie):
    """
        Obiekt klasy Health, za zadanie ma reprezentowaæ na ekranie za pomoc¹ serduszek stan zdrowia gracza. 
        Iloæ ¿ycia jaka opzosta³a do zakoñczenia rozgrywki.
    """
    def __init__(self, game):
        """
            Knstruktor inicjalizuje obiekt Health ustawiaj¹c liczbê ¿yæ,
            wczytuj¹c obrazek serca oraz ustalaj¹c pocz¹tkowe pozycje serc na ekranie.

            Metoda __init__() klasy Health s³u¿y do inicjalizacji obiektu reprezentuj¹cego zdrowie w grze.
            Parametr game to obiekt gry, który przekazuje referencjê do aktualnej gry.
            Atrybut zliczaj inicjalizowany jest wartoœci¹ 5 i reprezentuje liczbê ¿yæ dostêpnych dla gracza.
            Atrybut bochater to obrazek serca wczytany z pliku "serce1.png". Ten obrazek bêdzie u¿ywany do reprezentowania zdrowia na ekranie.
            Atrybut pos (position/pozycja) to lista obiektów typu Vector2, które przechowuj¹ pozycje serc na ekranie.
            Ka¿dy Vector2 reprezentuje pozycjê (x, y) serca na ekranie, gdzie (40, 40) to pozycja pierwszego serca, 
            (60, 40) to pozycja drugiego serca, itd. Ta lista zawiera pocz¹tkowe pozycje serc na ekranie.
 
        """
        self.game = game
        self.zliczaj = 5
        self.bochater = pygame.image.load("serce1.png")
        self.pos = [Vector2 (40,40),Vector2 (60,40),Vector2 (80,40)] # pozition / pozycja 1280,720
          
    def add_health(self, zniszczone):
        """
            Metoda add_health() klasy Health s³u¿y do dodawania zdrowia dla gracza w zale¿noœci od liczby zniszczonych obiektów.

            Parametr zniszczone to liczba zniszczonych obiektów, która jest przekazywana do metody.

            Metoda sprawdza, czy ró¿nica miêdzy zniszczone a aktualn¹ wartoœci¹ zliczaj (liczb¹ ¿yæ) jest wiêksza lub równa zero. 
            Jeœli tak, oznacza to, ¿e gracz zdoby³ wystarczaj¹c¹ iloœæ punktów, aby otrzymaæ dodatkowe ¿ycie.

            Nastêpnie sprawdzane jest, czy lista pos (przechowuj¹ca pozycje serc) jest pusta. Jeœli tak, oznacza to, 
            ¿e gracz straci³ wszystkie ¿ycia i teraz otrzymuje pierwsze serce.

            Jeœli lista pos nie jest pusta, to pobierana jest ostatnia pozycja serca z listy, 
            a nastêpnie obliczana jest nowa pozycja serca o przesuniêcie o 20 jednostek w osi x. 
            Ta nowa pozycja jest dodawana do listy pos.

            Dodatkowo, wartoœæ zliczaj (liczba ¿yæ) jest mno¿ona przez 2, 
            co oznacza ¿e musimy zdobyæ kolejne punkty by znowu dostaæ punkt zdrowia.
        """
        if zniszczone - self.zliczaj >= 0:
            if(len(self.pos) == 0):
                self.pos.append(Vector2 (40,40))
            else:
                pom = self.pos[-1] 
                x = pom[0]
                self.pos.append( Vector2 (x+20,40) )
                self.zliczaj *= 2

    def del_health(self):
        """
            Metoda del_health() usuwa ostatnie serce z listy pos, jeœli lista nie jest pusta, i zwraca wartoœæ 1, 
            jeœli lista jest pusta (brak dostêpnych ¿yæ).

            Metoda sprawdza, czy lista pos nie jest pusta. 
            Jeœli lista nie jest pusta, to usuwa ostatni element z listy poprzez wywo³anie metody pop(). 
            Oznacza to, ¿e gracz straci³ jedno ¿ycie i ostatnie serce jest usuwane z listy.

            Jeœli lista pos jest pusta, oznacza to, 
            ¿e gracz nie ma ju¿ ¿adnych ¿yæ do usuniêcia. 
            W takim przypadku metoda zwraca wartoœæ 1, 
            co mo¿e byæ wykorzystane jako sygna³ informuj¹cy o braku dostêpnych ¿yæ.
        """
        if len(self.pos) != 0:
            self.pos.pop()
        else:
            return 1

    def draw1(self):
        """
            Metoda draw1() klasy Health s³u¿y do rysowania serc na ekranie gry.

            Metoda iteruje przez wszystkie pozycje serc przechowywane w liœcie pos. 
            Dla ka¿dej pozycji, metoda u¿ywa funkcji blit() obiektu screen gry, 
            aby narysowaæ obraz serca na odpowiednich wspó³rzêdnych x i y na ekranie.
        """
        for p in self.pos:
            self.game.screen.blit(self.bochater,(p[0],p[1]))

        



        
