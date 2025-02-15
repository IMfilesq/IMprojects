#include <iostream>
using namespace std;


class node{
  public:
  node* left;
  int data;
  node* right;

  node(int val){
    left = nullptr;
    data = val;
    right = nullptr;
  }

  void add(int val){
    if(val >= data){
      if(right == nullptr){
        right = new node(val);
      }
      else{
        right->add(val);
      }
    }
    else{
      if(left == nullptr){
        left = new node(val);
      }
      else{
        left->add(val);
      }
    }
  }

  void print(){
    if(left != nullptr){
      left->print();
    }
    cout << data << endl;
    if(right != nullptr){
      right->print();
    }
  }
};


int main(){
  int n;
  cout << "podaj n" << endl;
  cin >> n;
  
  cout << "oczekuje " << n << " liczb" << endl;
  int first;
  cin >> first;
  node root = node(first);

  for(int i = 2; i <= n; i++){
    int val;
    cin >> val;
    root.add(val);
  }
  
  cout << "posortowane: " << endl;
  root.print();
  return 0;
}
