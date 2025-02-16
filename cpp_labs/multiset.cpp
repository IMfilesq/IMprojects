#include <iostream>
using namespace std;

bool found = false;
bool exists = false;

template <typename T>
class Pair {
    public:
    T a;
    int n;

    Pair(){
        a = T();
        n = 0;
    }
    
    Pair(T element, int count = 1){
        a = element;
        n = count;
    }

    void add(int count = 1) {
        n += count;
    }

    bool in(Pair<T> pair_2){
        return (a == pair_2.a && n <= pair_2.n);
    }


};

template <typename U>
class multiset{
    public:
    int size;
    Pair<U> arr[100];

    int contains(U element){
        for(int i = 0; i < size; i++){
            if(arr[i].a == element){
                return i;
            }
        }
        return -1;
    }

    multiset(){
        size = 0;
    }

    multiset(const U input_arr[], const int& arr_len){
        size = 0;
        for(int i = 0; i < arr_len; i++){
            int index = contains(input_arr[i]);
            if(index != -1){
                arr[index].add();
            }
            else{
                arr[size] = Pair<U>(input_arr[i]);
                size += 1;
            }
        }
    }

    void print(){
        for(int i = 0; i < size; i++){
            if(arr[i].n != 0){
            cout << "(" << arr[i].a << ", " << arr[i].n << "), ";
            }
        }
        cout << endl;
    }

    multiset<U> copy(){
        multiset<U> new_set;
        new_set.size = size;
        for(int i = 0; i < size; i++){
            new_set.arr[i] = arr[i];
        }
        return new_set;
    }

    multiset<U> multiset_union(multiset<U> set_2){
        multiset<U> new_set = copy();
        for(int i = 0; i < new_set.size; i++){
            int index = set_2.contains(new_set.arr[i].a);
            if(index != -1){
                new_set.arr[i].n += set_2.arr[index].n;
            }
        }
        for(int j = 0; j < set_2.size; j++){
            if(new_set.contains(set_2.arr[j].a) == -1){
                new_set.arr[new_set.size] = set_2.arr[j];
                new_set.size += 1;
            }
        }
        return new_set;
        
    }

    multiset<U> multiset_intersection(multiset<U> set_2){
        multiset<U> new_set;
        for(int i = 0; i < size; i++){
            int index = set_2.contains(arr[i].a);
            if(index != -1){
                new_set.arr[new_set.size].a = arr[i].a;
                new_set.arr[new_set.size].n = min(arr[i].n, set_2.arr[index].n);
                new_set.size += 1;
            }
        }
        return new_set;
    }

    multiset<U> multiset_difference(multiset<U> set_2){
        multiset<U> new_set;
        for(int i = 0; i < size; i++){
            int index = set_2.contains(arr[i].a);
            if(index != -1){
                if(set_2.arr[index].n < arr[i].n){
                    new_set.arr[new_set.size] = arr[i];
                    new_set.arr[new_set.size].n -= set_2.arr[index].n;
                    new_set.size += 1;
                }
            }
            else{
                new_set.arr[new_set.size] = arr[i];
                new_set.size += 1;
            }
        }
        return new_set;
    }

    bool contained_in(multiset<U> set_2){
        if(multiset_difference(set_2).size == 0){
            return true;
        }
        return false;
    }

    multiset<U> operator == (multiset<U> set_2){
        if(contained_in(set_2) && set_2.contained_in(*this)){
            return true;
        }
        return false;
    }

    bool is_zero(){
        long result = 0;
        bool is_empty = true;
        for(int i = 0; i < this->size; i++){
            if(this->arr[i].n != 0){
                is_empty = false;
            }
            result += this->arr[i].n * this->arr[i].a;
        }
        if(is_empty || result != 0){
            return false;
        }
        return true;
    }
    

    void sub_multiset(multiset<int> set){
        if(set.is_zero()){
            set.print();
            found = true;
            exists = true;
            return;
        }
        else{
            for(int i = 0; i <= set.size; i++){
                if(set.arr[i].n > 0){
                    multiset<int> new_set = set.copy();
                    new_set.arr[i].n -= 1;
                    if(!found){
                        sub_multiset(new_set);
                    }
                    else{
                        found = true;
                    }
                }
            }
        }
    }
    
};



int main() {
    int n;
    int k;


    cout << "podaj n" << endl;
    cin >> n;
    cout << "podaj k" << endl;
    cin >> k;

    int* arr1 = new int[n];
    int* arr2 = new int[k];
    cout << "podaj n liczb" << endl;
    for(int i = 0; i < n; i++){
        cin >> arr1[i];
    }
    cout << "podaj k liczb" << endl;
    for(int i = 0; i < k; i++){
        cin >> arr2[i];
    }

    multiset<int> set1(arr1,n);
    multiset<int> set2(arr2,k);

    cout << "M1" << endl;
    set1.print();
    cout << "M2" << endl;
    set2.print();

    cout << "M1 suma M2" << endl;
    (set1.multiset_union(set2)).print();
    cout << "M1 czesc wspolna M2" << endl;
    set1.multiset_intersection(set2).print();
    cout << "M1 odjac M2" << endl;
    set1.multiset_difference(set2).print();
    cout << "M1 zawarte w M2" << endl;
    if(set1.contained_in(set2)){
        cout << "TAK" << endl;
    }
    else{
        cout << "NIE" << endl;
    }
   return 0;
}
