#pragma once
#include "tabela_wynikow.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // Dodane dla obs³ugi konwersji std::string
#include <regex>
#include <string>

namespace py = pybind11;
/*!
    Klasa nick s³u¿y do sprawdzania poprawnoœci nicku gracza na podstawie wzorca wyra¿enia regularnego.
*/
class nick {
    
public:
    /*!
     Metoda czyPoprawnyNick przyjmuje jako argument string nick i sprawdza, czy spe³nia on wzorzec wyra¿enia regularnego,
     który wymaga, aby nick zaczyna³ siê od wielkiej litery i 
     sk³ada³ siê z co najmniej 8 znaków, zawieraj¹cych litery (zarówno wielkie jak i ma³e) oraz cyfry. 
     Metoda zwraca wartoœæ logiczn¹ w zale¿noœci od wyniku dopasowania wzorca do nicku gracza.
    */
    bool czyPoprawnyNick(const std::string& nick) {
        // wzorzec wyra¿enia regularnego dla nicku gracza
        std::regex wzorzec("[A-Z][a-za-z0-9]{7,}");

        // sprawdzenie dopasowania wzorca do nicku gracza
        return std::regex_match(nick, wzorzec);
    }
};
/*.def("Wyswietanie", &TW::Wyswietanie)*/
/*!
    Klasa Nick jest eksponowana do Pythona i posiada metodê czyPoprawnyNick.
    Klasa TW jest eksponowana do Pythona i posiada metody Wyswietanie, DodajWynik, getNazwa, getCzas_G, getCzas_M, getCzas_S oraz getPPK.
    Klasa Struktura jest eksponowana do Pythona i posiada konstruktor oraz metody dostêpowe 
    (getGodziny, getMinuty, getSekundy, getNazwa, getPunktyZdrowia) oraz metody ustawCzasINick i __lt__.
    Funkcje globalne Czy_Plik_TW_Istnieje i Czy_Plik_XYZ_Istnieje s¹ eksponowane do Pythona.
    Kod ten umo¿liwia wywo³ywanie tych funkcji i korzystanie z tych klas w kodzie Pythona.
*/
PYBIND11_MODULE(biblioteka, m) {
    py::class_<nick>(m, "Nick")
        .def(py::init<>())
        .def("czyPoprawnyNick", &nick::czyPoprawnyNick);

    py::class_<TW>(m, "TW")
        .def(py::init<>())
        .def("Wyswietanie", &TW::Wyswietanie)
        .def("DodajWynik", &TW::DodajWynik).def("getNazwa", &TW::getNazwa)
        .def("getCzas_G", &TW::getCzas_G)
        .def("getCzas_M", &TW::getCzas_M)
        .def("getCzas_S", &TW::getCzas_S)
        .def("getPPK", &TW::getPPK);

    py::class_<Struktura>(m, "Struktura")
        .def(py::init<int, int, int, const std::string&, int>())
        .def("getGodziny", &Struktura::getGodziny)
        .def("getMinuty", &Struktura::getMinuty)
        .def("getSekundy", &Struktura::getSekundy)
        .def("getNazwa", &Struktura::getNazwa)
        .def("getPunktyZdrowia", &Struktura::getPunktyZdrowia)
        .def("ustawCzasINick", &Struktura::ustawCzasINick)
        .def("__lt__", [](const Struktura& self, const Struktura& other) {
        return self < other;
            });

    m.def("Czy_Plik_TW_Istnieje", &TW::Czy_Plik_TW_Istnieje);
    m.def("Czy_Plik_XYZ_Istnieje", &TW::Czy_Plik_XYZ_Istnieje);
}
