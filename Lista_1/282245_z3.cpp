#include <iostream>
using namespace std;

//funcja fives liczy potęge liczby 5 w rozkładzie liczby n na czynniki pierwsze
int fives(int n){
    int count = 0;
    while(n % 5 == 0){
        n = n / 5;
        count = count +1;
    }
    return count;
}

//fzeros liczy potęgę liczby 5 w rozkładzie n! na czynniki pierwsze (jest ona również liczbą zer na końcu n!)
int fzeros(int n){
    int count = 0;
    for(int i = 1; i <= n; i++){
        count = count + fives(i);
    }
    return count;
}

int main(){
    int n;
    cin >> n;
    cout << fzeros(n);
    return 0;
}