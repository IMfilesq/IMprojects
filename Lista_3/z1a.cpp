#include <iostream>
using namespace std;

int main(){
    int zap;
    cout << "Podaj liczbe zapalek" << endl;
    cin >> zap;
    int ile;
    while(zap >= 1){
        cout << "Liczba zapalek: " << zap << " Ile zabiera gracz A? " << endl;
        cin >> ile;
        zap = zap - ile;
        if(zap == 1){
            cout << "gracz B przegral" << endl;
            return 0;
        }
        if(zap <= 1){
            cout << "gracz A przegral" << endl;
            return 0;
        }
        cout << "Liczba zapalek: " << zap << " Ile zabiera gracz B? " << endl;
        cin >> ile;
        zap = zap - ile;
        if(zap == 1){
            cout << "gracz A przegral" << endl;
            return 0;
        }
        if(zap <= 1){
            cout << "gracz B przegral" << endl;
            return 0;
        }
    }
    return 0;
}