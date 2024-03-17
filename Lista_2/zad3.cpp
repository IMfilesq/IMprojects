#include <iostream>
using namespace std;

// zwraca długoś stringa
int len(const char* str){
    int length = 1;
    while (str[length] != '\0'){
        length++;
    }
    return length;
}


int main(int argc, char* argv[]){
    int len1 = len(argv[1]);
    int len2 = len(argv[2]);
    if(len1 != len2){
        cout << "Nie";
        return 0;
    }
    for(int i = 0; i <= len1 - 1; i++){
        if(argv[1][i] != argv[2][len1-i-1]){
            cout << "NIE";
            return 0;
        }
    }
    cout << "TAK";
    return 0;
}