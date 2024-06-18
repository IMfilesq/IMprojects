#include <iostream>
#include <cmath>
using namespace std;


class wektor{
    public:
    float* coefficients;
    const static int dim = 10;

    wektor(){
        this->coefficients = new float[dim]();
    }
    wektor(float arr[],int len){
        if(len <= dim -1){
            this->coefficients = new float[dim]();
            for(int i =0; i < len; i++){
                this->coefficients[i] = arr[i];
            }
        }
    }

    void print(){
        for(int i = 0; i<dim ;i++ ){
            cout << this->coefficients[i] << " ";
        }
        cout << "\n";
    }

    wektor operator + (wektor wektor_2){
        wektor nowy_wektor = wektor();
        for(int i = 0; i < dim; i++){
            nowy_wektor.coefficients[i] += wektor_2.coefficients[i];
            nowy_wektor.coefficients[i] += this->coefficients[i];
        }
    }
    wektor operator - (wektor wektor_2){
        wektor nowy_wektor = wektor();
        for(int i = 0; i < dim; i++){
            nowy_wektor.coefficients[i] -= wektor_2.coefficients[i];
            nowy_wektor.coefficients[i] -= this->coefficients[i];
        }
    }

    wektor scalar(float x){
        wektor nowy_wektor = wektor();
        for(int i = 0; i < dim; i++){
            nowy_wektor.coefficients[i] *= x;
        }       
    }

    float product (wektor wektor_2){
        wektor nowy_wektor = wektor();
        int result = 0;
        for(int i = 0; i < dim; i++){
            result += this->coefficients[i]*wektor_2.coefficients[i];
        }
    }

    
};

int main(){
    cout << "niestety nie zdąrzyłem dokończyć zadania";
    return 0;
}
