#include <iostream>
using namespace std;

// sprawdza czy NWD liczb a,b wynosi 1
bool ifgcd1(int a, int b){
    for(int i = 2; i <= a; i++){
        if((a % i == 0) && (b % i == 0)){
            return false;
        }
    }
    return true;
}

//funcja eulera 
int eulerf(int n){
    int count = 0;
    for(int i = 1; i <= n; i++){
        if(ifgcd1(i,n)){
            count = count + 1;
        }
    }
    return count;
}

//funkcja F
int F(int n){
    int count = 0;
    for(int i = 1; i <=n; i++){
        if(n % i == 0){
            count = count + eulerf(i);
        }
    }
    return count;
}

//ostatecznie F(n) = n

int main(){
    int n ;
    cin >> n;
    cout << F(n);
    return 0;
}