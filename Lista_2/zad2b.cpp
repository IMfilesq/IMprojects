#include <iostream>
using namespace std;


//wystarcza jedno porównanie 

int main(){
    int nums[1001];
    for(int i = 0; i <= 1000 ; i++){
        cin >> nums[i];
    }
    if(nums[999] == nums[1000]){
        cout << "TAK";
        return 0;
    }
    cout << "NIE";
    return 0;
}