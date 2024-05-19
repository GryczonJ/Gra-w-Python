#include "tabela_wynikow.h"
//list<string>& Nazwa, list<int>& Czas_G, list<int>& Czas_M, list<int>& Czas_S, list<int>& PK
void TW::Wyswietanie() {
    //void Wyswietanie(py::list& Nazwa, py::list& Czas_G, py::list& Czas_M, py::list& Czas_S, py::list& PK){
fs::path sciezka = fs::current_path() / "TW" / "XYZ.txt";
    ifstream plik(sciezka);
    if (plik.is_open())
    {
        if (plik.peek() == ifstream::traits_type::eof())
        {
            PNazwa.append("Pusty_Plik1");
        }
        else{
            int godzina, minuta, sekunda, PunktyZdrowia;
            string nick;
                while (plik >> nick >> godzina >> minuta >> sekunda >> PunktyZdrowia)
                {
                    PNazwa.append(nick);
                    PCzas_G.append(godzina);
                    PCzas_M.append(minuta);
                    PCzas_S.append(sekunda);
                    PPK.append(PunktyZdrowia);
                }
        }
    }
    else
    {
        PNazwa.append("Pusty_Plik2");
        //plik.is_open();
        //std::cout << "Nie mo¿na otworzyæ pliku Z tabela wynikow." << std::endl;
    }
    plik.close();
}

void TW::DodajWynik(const int& czas, const string& nazwa,const int& pnktyZrowia)
{
    list<Struktura> Zpomocnicza;
    wczytajDoKlasy(Zpomocnicza);
    Struktura pomocnicza;

    pomocnicza.ustawCzasINick(czas, nazwa, pnktyZrowia);
    Zpomocnicza.push_back(pomocnicza);
    sortujOrazUsun(Zpomocnicza);

    fs::path sciezka = fs::current_path() / "TW" / "XYZ.txt";

    ofstream plik(sciezka, std::ios::trunc); // Nadpisanie
    if (plik.is_open())
    {
        for (const auto& element : Zpomocnicza) {
            plik << element.getNazwa() << " " << element.getGodziny() << " "
                << element.getMinuty() << " " << element.getSekundy() << " "
                << element.getPunktyZdrowia() << '\n';
        }
        plik.close();
    }
    else {
        cout << "\n Blond krytyczny, ale spokojnie ogarne!!!\n";
    }
}

void TW::sortujOrazUsun(list<Struktura>& lista) {

    // Sortowanie po punktach zdrowia [Z-A]
    lista.sort([](const Struktura& a, const Struktura& b) {
        return a.getPunktyZdrowia() > b.getPunktyZdrowia();
        });

    // Sortowanie stabilne po czasie [A-Z]
    lista.sort([](const Struktura& a, const Struktura& b) {
        return a < b;
        });

    while (lista.size() > 10)
    {
        lista.pop_back();
    }
}

void TW::wczytajDoKlasy(list<Struktura>& lista) {
    fs::path sciezka = fs::current_path() / "TW" / "XYZ.txt";
    ifstream plik(sciezka);
    if (!plik) {
        cout << "B³¹d: Nie mo¿na otworzyæ pliku " << sciezka << '\n';
        return;
    }

    int g, m, s, pz;
    string n;
    while (plik >> n >> g >> m >> s >> pz) {
        lista.emplace_back(g, m, s, n, pz);
    }
    plik.close();
}

// Funkcja ustawiaj¹ca czas, nick i punkty zdrowia

void Struktura::ustawCzasINick(int czasS, const string& nick, int pz) {
    godziny = czasS / 3600;
    minuty = (czasS % 3600) / 60;
    sekundy = (czasS % 3600) % 60;
    nazwa = nick;
    punktyZdrowia = pz;
}

