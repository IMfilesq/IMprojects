#include <iostream>
using namespace std;

class R3{
  public:
  float first;
  float second;
  float third;

  R3(float one, float two, float three){
    first = one;
    second = two;
    third = three;
  }

  R3 add(R3 vect){
    R3 new_vect = R3(first + vect.first, second + vect.second, third +  vect.third);
    return new_vect;
  }

  R3 scal_mult(float scal){
    R3 new_vect = R3(first * scal, second * scal, third * scal);
    return new_vect;
  }
  
  float dot_prod(R3 vect){
    return first * vect.first + second * vect.second + third * vect.third;
  }

  bool is_ortogonal(R3 vect){
    if(dot_prod(vect) == 0){
      return true;
    }
    else{
      return false;
    }
  }

  R3 cross_prod(R3 vect){
    R3 new_vect = R3(second * vect.third - third * vect.second, third * vect.first - first * vect.third, first * vect.second - second * vect.first);
    return new_vect;
  }

  bool is_pararel(R3 vect){
    R3 new_vect = cross_prod(vect);
    if ( new_vect.first == 0 && new_vect.second == 0 && new_vect.third == 0){
      return true;
    }
    else{
      return false;
    }
  }

  void display(){
    cout << "(" << first << ", " << second << ", " << third << ")" << endl;
  }
};

int main(){
  float arr[7];
  cout << "oczekuje wspolrzednych wektorow oraz skalara a" << endl;
  for(int i = 0 ; i <= 6; i++){
    cin >> arr[i];
  }

  R3 v = R3(arr[0], arr[1], arr[2]);
  R3 w = R3(arr[3], arr[4], arr[5]);
  float a = arr[6];

  cout << "wektor v: ";
  v.display();

  cout << "wektor w: ";
  w.display();

  cout << "a = " << a << endl;

  cout << "av = ";
  (v.scal_mult(a)).display();

  cout << "v + w = ";
  (v.add(w)).display();

  cout << "v dot w = " << v.dot_prod(w) << endl;

  cout << "rownolegle: ";
  if(v.is_pararel(w)){
    cout << "tak" << endl;
  }
  else{
    cout << "nie" <<endl;
  }

  cout << "prostopadle: ";
  if(v.is_ortogonal(w)){
    cout << "tak" << endl;
  }
  else{
    cout << "nie" << endl;
  }
  
  return 0;
}
