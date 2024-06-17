#include <iostream>
#include <cmath>
using namespace std;


class pojazd{
    public:

    string model;
    int rok_produkcji;
    float przebieg;

    pojazd(string model, int rok_produkcji, float przebieg = 0){
        this->model = model;
        this->rok_produkcji = rok_produkcji;
        this->przebieg = przebieg;
    }

    void info(){
        cout << "model: " << this->model << "\n" << "rok_produkcji: " << this->rok_produkcji << "\n" << "przebieg: " << this->przebieg << "\n";
    }

    virtual void przejazd(float kilometry){
        this->przebieg += kilometry;
    }


};

class pojazd_spalinowy : public pojazd{
    public:
    int następne_tankowanie;
    pojazd_spalinowy(string model, int rok_produkcji, float przebieg = 0) : pojazd(model,rok_produkcji,przebieg) {
        this->następne_tankowanie =  przebieg + 300;
    }
    void przejazd(float kilometry) override{
        pojazd::przejazd(kilometry);
        if(następne_tankowanie <= przebieg){
            cout<< "rozwaz tankowanie" << "\n";
            this->następne_tankowanie += 300;
        }
    }
};

class pojazd_elektryczny : public pojazd{
    public:
    int następne_ładowanie;
    pojazd_elektryczny(string model, int rok_produkcji, float przebieg = 0) : pojazd(model,rok_produkcji,przebieg) {
        this->następne_ładowanie =  przebieg + 100;
    }
    void przejazd(float kilometry) override{
        pojazd::przejazd(kilometry);
        if(następne_ładowanie <= przebieg){
            cout<< "rozwaz ladowanie" << "\n";
            this->następne_ładowanie += 100;
        }
    }
};

int main(){
    string m1;
    string m2;
    int r1;
    int r2;
    int p1;
    int p2;

    cin >> m1;
    cin >> r1;
    cin >> m2;
    cin >> r2; 
    cin >> p1;
    cin >> p2;

    pojazd_spalinowy car1(m1,r1);
    pojazd_elektryczny car2(m2,r2);

    cout << "\n";
    car1.przejazd(p1);
    car1.info();


    cout << "\n";
    car2.przejazd(p2);
    car2.info();

    return 0;
}
