#include <iostream>
using namespace std;


// zamienia wartości zmiennych a i b 
void swap(int& a, int& b){
    int c = a;
    a = b;
    b = c;
}


// wyświetla tablicę
void p_arr(int arr[],int len){
    int i = 0;
    while (i < len){
        cout << arr[i] << " ";
        i++;
    }
    cout << endl;
}


// scala i sortuje dwie "podtablice"
// first to indeks początku pierwszej tablicy, mid to indeks początku drugiej tablicy, last indeks końca drugiej tablicy
// funkcja działa "w miejscu", jednak pierwsza tablica musi być większa równa drugiej (nie ma znaczenia dla działania programu)
void merge(int arr[],int first, int last, int mid){
    while(mid <= last && last - first != 0){
        if (arr[first] > arr[mid]){
            for(int i = mid; i > first; i--){
                swap(arr[i],arr[i-1]);
            }
            mid++;
        }
        first++;
    }
}

//właściwa funcja sortująca
void m_sort(int arr[], int len){
    int n = 2;
    while(n <= len){
        int i = 0;
        while(i + n - 1 < len){
            merge(arr, i, i + n - 1, (i + (i + n - 1)) / 2 + 1);
            i = i + n; 
        }
        if(i + n/2 < len){
            merge(arr,i , len - 1, i + n/2);
        }
        n = n * 2;
    }
    merge(arr,0,len-1,n/2);
}   

int main(){
    int len;
    cout << "ile liczb? ";
    cin >> len;
    int arr[len];
    cout << "podaj liczby ";
    for(int i = 0; i < len; i++){
        cin >> arr[i];
    }
    m_sort(arr,len);
    p_arr(arr,len);
    return 0;
} 