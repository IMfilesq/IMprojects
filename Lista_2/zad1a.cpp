#include <iostream>
using namespace std;

int fib_iter(int n){
    if (n <= 1) return n;
    int prev = 0;
    int curr = 1;
    for (int i = 1; i <= n - 1; i++){
        int old_curr = curr;
        curr = prev + old_curr;
        prev = old_curr;
    }
    return curr;
}

int main(){
    int n;
    cin >> n;
    cout << fib_iter(n);
    return 0;
}