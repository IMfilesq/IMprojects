 #include <iostream>
using namespace std;

class Zwierz{
    public:
    string imie;
    string rasa;
    Zwierz(string na_imie, string jaka_rasa){
        imie = na_imie;
        rasa = jaka_rasa;
    }
    virtual void sound() const = 0 ;

    friend ostream & operator << (ostream &output, const Zwierz &obj) { 
      output << "imie: " << obj.imie << endl << "rasa: " << obj.rasa << endl << "dzwiek: ";
      obj.sound();
      return output;            
    }

    friend istream & operator >> (istream &input, Zwierz &obj) { 
       input >> obj.imie >> obj.rasa;
       return input;
    }

};

class Kot : public Zwierz{
    public:
    Kot(string na_imie = "", string jaka_rasa = "") :  Zwierz(na_imie,jaka_rasa) {}
    void sound() const override{
        cout << "miau" << endl;
    }
};


class Pies : public Zwierz{
    public:
    Pies(string na_imie = "", string jaka_rasa = "") : Zwierz(na_imie,jaka_rasa) {}
    void sound() const override{
        cout << "hau" << endl;
    }
};


int main(){
    Kot mruczek = Kot();
    cout << "oczekuje na imie i rase kota" << endl;
    cin >> mruczek;

    Pies fafik = Pies();
    cout << "oczekuje na imie i rase psa" << endl; 
    cin >> fafik;

    cout << "wypisuje kota" << endl;
    cout << mruczek << endl;

    cout << "wypisuje psa" << endl;
    cout << fafik ;
    
    return 0;
}
