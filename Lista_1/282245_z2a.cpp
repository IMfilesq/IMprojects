#include <iostream>
#include <string>
#include <cmath>
using namespace std;

bool ifgcd1(int a, int b){
    for(int i = 2; i <= a; i++){
        if((a % i == 0) && (b % i == 0)){
            return false;
        }
    }
    return true;
}

int eulerf(int n){
    int count = 0;
    for(int i = 1; i <= n; i++){
        if(ifgcd1(i,n)){
            count = count + 1;
        }
    }
    return count;
}

int main(){
    int n;
    cin >> n;
    cout << eulerf(n);
    return 0;
}