#include <iostream>
#include <cmath>
using namespace std;


bool pierwotne(int a, int b , int c){
    int najwieksza = max(max(a,b),c);
    for(int i = 2; i <= najwieksza; i++){
        if(i <= a && i <= b && i <=c){
            if(a%i == 0 && b%i == 0 && c%i == 0 ){
                return false;
            }
        }
    }
    return true;
}

void triples(int n){
    for(int i = 1; i <= n-2; i++){
        for(int j = 2; j <= n-1;j++){
            for(int k = 3; k <= n; k++){
                if(pow(i,2) + pow(j,2) == pow(k,2) && i < j && j < k && pierwotne(i,j,k)){
                    cout << "(" << i << ", " << j << ", "<< k << ")" << "\n";
                }
            }
        }
    }

}

int main(){
    int n;
    cin >> n;
    triples(n);
    return 0;
}
