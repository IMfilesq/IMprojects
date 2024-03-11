#include <iostream>
#include <string>
#include <cmath>
using namespace std;

//do tej pory nie udało się rozstrzygnąć czy wszystkie trajektorie wpadają w jedynkę

int func(int n){
    if (n % 2 == 0){
        return n / 2;
    }
    else{
        return 3 * n + 1;
    }
}

int main(){
    int n;
    int i = 0;
    cin >> n;
    while(func(n) != 1){
        cout << func(n) << " ";
        n = func(n);
        i = i+1;
    }
    cout << 1 << "," << " " << i + 1;
    return 0;
}