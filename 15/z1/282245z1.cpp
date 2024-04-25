#include <iostream>

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
  void show_tree() {
    cout << data << " ";
    if (left != nullptr) {
      ( * left).show_tree();
    }
    if (right != nullptr) {
      ( * right).show_tree();
    }
  };
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

//skleja dwa drzewa w jedno, tworząc nowy korzeń, jako argument należy podać wartość jaką będzie miał nowy korzeń
T_Node * glue(T_Node * l_tree, T_Node * r_tree, int new_root_value) {
  T_Node * new_root = new T_Node(new_root_value);
  new_root -> left = l_tree;
  new_root -> right = r_tree;
  return new_root;
}

//rekurencyjna implementacja wyszukiwania, zwraca 1 jeżeli znaleziono, 0 jeżeli nie znaleziono
bool search(T_Node * root, int element) {
  if (root -> data == element) {
    return true;
  }
  bool found_l = false;
  bool found_r = false;
  if (root -> left != nullptr) {
    found_l = search(root -> left, element);
  }
  if (root -> right != nullptr) {
    found_r = search(root -> right, element);
  }
  return found_l || found_r;
}

//zwraca wysokość drzewa
int height(T_Node * root) {
  if (root == nullptr) {
    return 0;
  }
  if (root -> left == nullptr && root -> right == nullptr) {
    return 0;
  }
  return max(height(root -> left), height(root -> right)) + 1;
}

//zwraca liczbę węzłów
int nodes(T_Node * root) {
  if (root == nullptr) {
    return 0;
  }
  if (root -> left == nullptr && root -> right == nullptr) {
    return 1;
  }
  return nodes(root -> left) + nodes(root -> right) + 1;
}

//zwraca liczbę liści
int leaves(T_Node * root) {
  if (root == nullptr) {
    return 0;
  }
  if (root -> left == nullptr && root -> right == nullptr) {
    return 1;
  }
  return leaves(root -> left) + leaves(root -> right);
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

int main() {
  int n;
  cout << "podaj liczbe elementow drzewa n" << "\n";
  cin >> n;
  int * arr = new int[n];

  int s;
  cout << "podaj wartosc szukana s" << "\n";
  cin >> s;

  cout << "podaj " << n << " elementow" << "\n";
  for (int i = 0; i < n; i++) {
    cin >> arr[i];
  }

  T_Node * tree = arr_to_tree(arr, n);
  cout << "drzewo: " << "\n";
  print_tree(tree);

  cout << "liczba wezlow: " << nodes(tree) << "\n";
  cout << "liczba lisci: " << leaves(tree) << "\n";
  cout << "wysokosc: " << height(tree) << "\n";

  if (search(tree, s)) {
    cout << "drzewo zawiera element " << s << "\n";
  } else {
    cout << "drzewo nie zawiera elementu " << s << "\n";
  }
  return 0;
}
