#include <iostream>
using namespace std;


int main(){
    int nums[5];
    for(int i = 0; i <= 4 ; i++){
        cin >> nums[i];
    }
    int last = nums[4];
    for(int i = 0; i <= 3; i++){
        if (nums[i] == last){
            cout << "TAK";
            return 0;
        }
    }
    cout << "NIE";
    return 0;
}