#include <iostream>
#include <cmath>
using namespace std;



void triples(int n){
    for(int i = 1; i <= n-2; i++){
        for(int j = 2; j <= n-1;j++){
            for(int k = 3; k <= n; k++){
                if(pow(i,2) + pow(j,2) == pow(k,2) && i < j && j < k){
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
