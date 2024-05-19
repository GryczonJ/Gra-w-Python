
import pygame
from pygame.math import Vector2
from Dziedziczenie import NaEkranie
pygame.init()
class Health(NaEkranie):
    """
        Obiekt klasy Health, za zadanie ma reprezentowa� na ekranie za pomoc� serduszek stan zdrowia gracza. 
        Ilo� �ycia jaka opzosta�a do zako�czenia rozgrywki.
    """
    def __init__(self, game):
        """
            Knstruktor inicjalizuje obiekt Health ustawiaj�c liczb� �y�,
            wczytuj�c obrazek serca oraz ustalaj�c pocz�tkowe pozycje serc na ekranie.

            Metoda __init__() klasy Health s�u�y do inicjalizacji obiektu reprezentuj�cego zdrowie w grze.
            Parametr game to obiekt gry, kt�ry przekazuje referencj� do aktualnej gry.
            Atrybut zliczaj inicjalizowany jest warto�ci� 5 i reprezentuje liczb� �y� dost�pnych dla gracza.
            Atrybut bochater to obrazek serca wczytany z pliku "serce1.png". Ten obrazek b�dzie u�ywany do reprezentowania zdrowia na ekranie.
            Atrybut pos (position/pozycja) to lista obiekt�w typu Vector2, kt�re przechowuj� pozycje serc na ekranie.
            Ka�dy Vector2 reprezentuje pozycj� (x, y) serca na ekranie, gdzie (40, 40) to pozycja pierwszego serca, 
            (60, 40) to pozycja drugiego serca, itd. Ta lista zawiera pocz�tkowe pozycje serc na ekranie.
 
        """
        self.game = game
        self.zliczaj = 5
        self.bochater = pygame.image.load("serce1.png")
        self.pos = [Vector2 (40,40),Vector2 (60,40),Vector2 (80,40)] # pozition / pozycja 1280,720
          
    def add_health(self, zniszczone):
        """
            Metoda add_health() klasy Health s�u�y do dodawania zdrowia dla gracza w zale�no�ci od liczby zniszczonych obiekt�w.

            Parametr zniszczone to liczba zniszczonych obiekt�w, kt�ra jest przekazywana do metody.

            Metoda sprawdza, czy r�nica mi�dzy zniszczone a aktualn� warto�ci� zliczaj (liczb� �y�) jest wi�ksza lub r�wna zero. 
            Je�li tak, oznacza to, �e gracz zdoby� wystarczaj�c� ilo�� punkt�w, aby otrzyma� dodatkowe �ycie.

            Nast�pnie sprawdzane jest, czy lista pos (przechowuj�ca pozycje serc) jest pusta. Je�li tak, oznacza to, 
            �e gracz straci� wszystkie �ycia i teraz otrzymuje pierwsze serce.

            Je�li lista pos nie jest pusta, to pobierana jest ostatnia pozycja serca z listy, 
            a nast�pnie obliczana jest nowa pozycja serca o przesuni�cie o 20 jednostek w osi x. 
            Ta nowa pozycja jest dodawana do listy pos.

            Dodatkowo, warto�� zliczaj (liczba �y�) jest mno�ona przez 2, 
            co oznacza �e musimy zdoby� kolejne punkty by znowu dosta� punkt zdrowia.
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
            Metoda del_health() usuwa ostatnie serce z listy pos, je�li lista nie jest pusta, i zwraca warto�� 1, 
            je�li lista jest pusta (brak dost�pnych �y�).

            Metoda sprawdza, czy lista pos nie jest pusta. 
            Je�li lista nie jest pusta, to usuwa ostatni element z listy poprzez wywo�anie metody pop(). 
            Oznacza to, �e gracz straci� jedno �ycie i ostatnie serce jest usuwane z listy.

            Je�li lista pos jest pusta, oznacza to, 
            �e gracz nie ma ju� �adnych �y� do usuni�cia. 
            W takim przypadku metoda zwraca warto�� 1, 
            co mo�e by� wykorzystane jako sygna� informuj�cy o braku dost�pnych �y�.
        """
        if len(self.pos) != 0:
            self.pos.pop()
        else:
            return 1

    def draw1(self):
        """
            Metoda draw1() klasy Health s�u�y do rysowania serc na ekranie gry.

            Metoda iteruje przez wszystkie pozycje serc przechowywane w li�cie pos. 
            Dla ka�dej pozycji, metoda u�ywa funkcji blit() obiektu screen gry, 
            aby narysowa� obraz serca na odpowiednich wsp�rz�dnych x i y na ekranie.
        """
        for p in self.pos:
            self.game.screen.blit(self.bochater,(p[0],p[1]))

        



        
