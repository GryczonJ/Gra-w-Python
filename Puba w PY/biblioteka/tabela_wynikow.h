#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <fstream>
#include <filesystem>
#include <list>

using std::cout;
using std::string;
using std::list;
using std::string;
using std::ifstream;
using std::ofstream;

namespace py = pybind11;
namespace fs = std::filesystem;

class Struktura {
    /*!
        Zadaniem klasy struktura jest przechowywanie struktury tabeli. 
        Dzieki temu że wszyskie dane są w takiej struktuże łatwo będize nam je stabilnie posortować.
    */
private:
    int godziny;
    int minuty;
    int sekundy;
    string nazwa;
    int punktyZdrowia;

public:
    // Konstruktory
    Struktura() {}

    Struktura(int g, int m, int s, const string& n, int pz)
        : godziny(g), minuty(m), sekundy(s), nazwa(n), punktyZdrowia(pz)
    {
    }

    // Gettery
     /*! Zwraca godzine */
    int getGodziny() const {
        return godziny;
    }

    /*! Zwraca minute */
    int getMinuty() const {
        return minuty;
    }

    /*! Zwraca sekundy */
    int getSekundy() const {
        return sekundy;
    }
    /*! Zwraca nazwe */
    string getNazwa() const {
        return nazwa;
    }

    /*! Zwraca Ilość trafień */
    int getPunktyZdrowia() const {
        return punktyZdrowia;
    }

    /*! Funkcja ustawiająca czas, nick i punkty zdrowia */
    void ustawCzasINick(int czasMS, const string& nick, int pz);

    /*!
      Ta metoda definiuje operator < dla klasy Struktura, który porównuje obiekty tej klasy na podstawie ich czasu (godziny, minuty, sekundy), zwracając wartość logiczną czy jeden obiekt jest mniejszy od drugiego.
    */
    bool operator<(const Struktura& other) const {
        // Sortowanie po czasie (godziny, minuty, sekundy)
        if (godziny != other.godziny){
            return godziny < other.godziny;
        }
        if (minuty != other.minuty){
            return minuty < other.minuty;
        }
        if (sekundy != other.sekundy){
            return sekundy < other.sekundy;
        }
        return false;
    }
};


class TW
{
    /*!
    * Zadaniem tej klasy jest reprezentowanie Tabeli Wyników.
    */
    // list<string> nicki;
    // list<int> godziny, minuty, skundy;
    py::list PNazwa;
    py::list PCzas_G;
    py::list PCzas_M;
    py::list PCzas_S;
    py::list PPK;
public:
    /*!
        Konstruktor
        Sprawdza czy istnieje poprawna struktira plików
    */
	TW() {
		if (!Czy_Plik_TW_Istnieje()) {
            fs::create_directory("TW");
		}
        if (!Czy_Plik_XYZ_Istnieje()) {
			fs::path sciezka = fs::current_path() / "TW" / "XYZ.txt";
            ofstream plik(sciezka);
            plik.is_open();
            plik.close();
        }
	}

    /*! Zwraca liztę nick - ów gracza */
    py::list getNazwa() {
        return PNazwa;
    }
    /*! Zwraca liztę godzin */
    py::list getCzas_G() {
        return PCzas_G;
    }
    /*! Zwraca liztę minut */
    py::list getCzas_M() {
        return PCzas_M;
    }
    /*! Zwraca liztę sekund */
    py::list getCzas_S() {
        return PCzas_S;
    }
    /*! Zwraca listę ilości trafień */
    py::list getPPK() {
        return PPK;
    }

    // Sprawdzenie
    /*! Sprzwadza czy ścieszka do folderu istnieję */
	bool Czy_Plik_TW_Istnieje()
	{
		fs::path sciezka = fs::current_path() / "TW";
		return fs::exists(sciezka);
	}

    /*! Sprzwadza czy ścieszka do pliku tekstowego zawierającego tabelkę istnieję */
	bool Czy_Plik_XYZ_Istnieje()
	{
		fs::path sciezka = fs::current_path() / "TW" / "XYZ.txt";
		return fs::exists(sciezka);
	}

    // Wycztawanie
    // void Wyswietanie(py::list& Nazwa, py::list& Czas_G, py::list& Czas_M, py::list& Czas_S, py::list& PK);
    // list<string>& Nazwa, list<int>& Czas_G, list<int>& Czas_M, list<int>& Czas_S, list<int>& PK
    /*!
        Metoda "TW::Wyswietanie()" odczytuje dane z pliku tekstowego "XYZ.txt" znajdującego się w katalogu "TW". 
        Jeśli plik istnieje i jest otwarty poprawnie, odczytuje dane w formacie: nick, godzina, minuta, sekunda i ilość trafień (nazywana punkty zdrowia). 
        Następnie dodaje odczytane wartości do odpowiednich list: PNazwa, PCzas_G, PCzas_M, PCzas_S i PPK. 
        Jeśli plik jest pusty, do listy PNazwa zostaje dodany specjalny tekst "Pusty_Plik1". 
        Jeśli plik nie istnieje lub wystąpił błąd podczas otwierania pliku, do listy PNazwa zostaje dodany specjalny tekst "Pusty_Plik2". 
        Na końcu plik jest zamykany.
    */
	void Wyswietanie();

    /*!
        Metoda "TW::wczytajDoKlasy()" odczytuje dane z pliku tekstowego "XYZ.txt" znajdującego się w katalogu "TW" i 
        wczytuje je do listy przekazanej jako argument.

        Najpierw tworzona jest ścieżka do pliku "XYZ.txt", a następnie tworzony jest strumień wejściowy do odczytu pliku. 
        Jeśli plik nie może zostać otwarty, wypisywany jest odpowiedni komunikat o błędzie, a funkcja kończy działanie.

        Następnie, w pętli, odczytywane są wartości z pliku, takie jak nazwa, godzina, minuta, sekunda i ilość trafień (nazywana punkty zdrowia). 
        Te wartości są używane do utworzenia nowej struktury, która jest dodawana do listy za pomocą metody emplace_back().

        Po zakończeniu odczytu, plik jest zamykany.
        W rezultacie, metoda wczytuje dane z pliku "XYZ.txt" i tworzy obiekty struktur, które są dodawane do przekazanej listy.
    */
    void wczytajDoKlasy(list<Struktura>& lista);

    /*!
        Metoda "TW::DodajWynik()" dodaje nowy wynik do pliku tekstowego "XYZ.txt" w katalogu "TW". 
        Najpierw wczytuje istniejące wyniki do listy pomocniczej Zpomocnicza poprzez wywołanie funkcji wczytajDoKlasy(). 
        Następnie tworzy nową strukturę pomocniczą i ustawia jej wartości czasu, nazwy i ilości trafien( nazwane punktami zdrowia ) na podstawie przekazanych argumentów. 
        Nowa struktura jest dodawana na koniec listy Zpomocnicza.
        Po tym sortuje listę Zpomocnicza i usuwa nadmiarowe wyniki przy użyciu funkcji sortujOrazUsun().

        Następnie tworzona jest ścieżka do pliku "XYZ.txt" i tworzony jest strumień wyjściowy do zapisu. 
        Jeśli plik otwiera się poprawnie, pętla iteruje po elementach listy Zpomocnicza i zapisuje je do pliku, 
        oddzielając poszczególne wartości spacjami i kończąc każdą linię znakiem nowej linii. Na koniec plik jest zamykany. 
        Jeśli wystąpił błąd podczas otwierania pliku, zostaje wypisany odpowiedni komunikat na standardowym wyjściu.
    */
    void DodajWynik(const int& czas, const string& nazwa, const int& pnktyZrowia);

    /*! Organiezacja zmiennych */
    void sortujOrazUsun(list<Struktura>& lista);
    
};

