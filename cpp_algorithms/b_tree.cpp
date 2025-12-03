#include <iostream>
#include <cmath>

using namespace std;

struct T_Node {
  int data;
  T_Node * left;
  T_Node * right;

  T_Node(int val) {
      data = val;
      left = nullptr;
      right = nullptr;
    }

    ~T_Node() {
      cout << "Deleting node with value " << data << "\n";
      delete left;
      delete right;
    }
};

struct node {
  T_Node * data;
  node * next;

  node(T_Node * val): data(val), next(nullptr) {}
};

struct Queue {
  node * front;
  node * back;

  Queue(): front(nullptr), back(nullptr) {}

    ~Queue() {
      while (!is_empty()) {
        dequeue();
      }
    }

  bool is_empty() {
    return (front == nullptr);
  }

  void enqueue(T_Node * val) {
    node * new_el = new node(val);
    if (is_empty()) {
      front = new_el;
      back = new_el;
    } else {
      back -> next = new_el;
      back = new_el;
    }
  }
  T_Node * dequeue() {
    if (is_empty()) {
      return nullptr;
    } else {
      T_Node * val = front -> data;
      node * temp = front;
      front = front -> next;
      delete temp;
      return val;
    }
  }
  void print() {
    node * temp_back = back;
    while (temp_back != nullptr) {
      cout << temp_back -> data << " ";
      temp_back = temp_back -> next;
    }
    cout << endl;
  }
};

void ch_sign(T_Node* root){
  root->data = -(root->data);
  if (root->left){
    ch_sign(root->left);
  }
  if (root->right){
    ch_sign(root->right);
  }
}

int nodes(T_Node * root) {
  if (root == nullptr) {
    return 0;
  }
  if (root -> left == nullptr && root -> right == nullptr) {
    return 1;
  }
  return nodes(root -> left) + nodes(root -> right) + 1;
}

//konwetruje tablice intów na drzewo, korzysta z kolejki, zwraca wskaźnik do korzenia drzewa
T_Node * arr_to_tree(int arr[], int len) {
  Queue kolejka;
  T_Node * root = new T_Node(arr[0]);
  kolejka.enqueue(root);
  int i = 1;
  T_Node * temp;
  while (i < len) {
    temp = kolejka.dequeue();
    temp -> left = new T_Node(arr[i]);
    i++;
    if (i >= len) break;
    temp -> right = new T_Node(arr[i]);
    kolejka.enqueue(temp -> left);
    kolejka.enqueue(temp -> right);
    i++;
  }
  return root;
}


//printuje drzewo
void print_tree(T_Node * root, int dist = 0, int count = 10) {
  if (root != nullptr) {
    dist += count;
    print_tree(root -> right, dist);
    cout << endl;
    for (int i = count; i < dist; i++) {
      cout << " ";
    }
    cout << root -> data << "\n";
    print_tree(root -> left, dist);
  }
}

void t_copy(T_Node* root, T_Node*& new_root){
  new_root = new T_Node(root->data);
  if(root->left != nullptr){
    t_copy(root->left, new_root->left);
  }
  if(root->right != nullptr){
    t_copy(root->right, new_root->right);
  }
}

void add(T_Node*& new_tree, T_Node* tree2){
  if(tree2 != nullptr){
    if(new_tree != nullptr){
      new_tree->data += tree2->data;
      add(new_tree->left, tree2->left);
      add(new_tree->right, tree2->right);
    }
    else{
      t_copy(tree2,new_tree);
    }
  }
}

int row(int num, int count = 0){
  if (pow(2,count) > num){
    return count;
  }
  return row(num, count + 1);
}

void printBinary(int n) {
    for (int i = row(n) - 2; i >= 0; i--) {
        cout << ((n >> i) & 1);
    }
    cout << endl;
}

int get_val(int n, T_Node* root){
  for (int i = row(n) - 2; i >= 0; i--) {
    int bit = ((n >> i) & 1);
    if (bit == 0) root = root->left;
    else if (bit == 1) root = root->right;
  }
  return root->data;
}

class tree {
  public:
  T_Node* root;
  

  // inicjalizacja drzewa z node'a
  tree(T_Node* new_tree){
    root = new_tree;
  }

  //inicjalizacja drzewa z tablicy
  tree(int* arr, int len){
    root = arr_to_tree(arr, len);
  }


  // tworzy kopię, zmienia jej znak, następnie są zwraca
  tree operator -(){
    T_Node* new_root;
    t_copy(root, new_root);
    ch_sign(new_root);
    return tree(new_root);
  }


  void print(){
    print_tree(root);
  }

  //tworzy kopię drzewa 1, dodaje do niej drzewo 2, następnie zwraca
  tree operator + (tree tree2){
    T_Node* new_tree;
    t_copy(root, new_tree);
    add(new_tree, tree2.root);
    return tree(new_tree);
  }

  //dodaje do samego siebie odwrotność drzewa 2
  tree operator - (tree tree2){
    return *this + (-tree2);
  }


  /*drzewa przetwarzam zapełniając kolejne rzędy node'ami, za pomocą kolejki.
  Tak też indeksuje node'y, n - ty element inputu zajmuje n - ty indeks w drzewie (indeksuje zaczynając od 1).
  Korzystam z tego, że przetwarzając taki indeks na zapis binarny (i ignorując ostatnią cyfrę) otrzymujmy ścieżkę dostępu do node'a.
  W takiej ścieżce 0 oznacza idź w lewo, 1 oznacza idź w prawo.
  */

  int operator [] (int n){
    if (n <= nodes(root) && n > 0){
      return get_val(n, root);
    }
    else{
      cout << "drzewo nie ma elementu pod inedeksem n, zwracam 0: " << endl;
      return 0;
    }
  }
};

int main() {
  int n;
  cout << "podaj n " << "\n";
  cin >> n;
  int * arr_n = new int[n];

  int k;
  cout << "podaj k " << "\n";
  cin >> k;
  int * arr_k = new int[k];

  cout << "podaj " << n << "(n) elementow" << "\n";
  for (int i = 0; i < n; i++) {
    cin >> arr_n[i];
  }

  cout << "podaj " << k << "(k) elementow" << "\n";
  for (int i = 0; i < k; i++) {
    cin >> arr_k[i];
  }

  tree drzewo1 = tree(arr_n,n);
  tree drzewo2 = tree(arr_k,k);

  cout << "-t1: " << endl;
  (-drzewo1).print();
  cout << "t1 + t2:" << endl;
  (drzewo1 + drzewo2).print();
  cout << "t2 - t1:" << endl;
  (drzewo2 - drzewo1).print();

  cout << "warotsci drzewa t1 za pomoca []: " << endl;
  for(int i = 1; i <= nodes(drzewo1.root); i++){
    cout << drzewo1[i] << " ";
  }

  return 0;
}
