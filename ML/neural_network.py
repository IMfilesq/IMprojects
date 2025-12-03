import numpy as np
import gzip
import pickle
import random

def load_data():
    """Return the MNIST data as a tuple containing the training data,
    the validation data, and the test data.
    The ``training_data`` is returned as a tuple with two entries.
    The first entry contains the actual training images.  This is a
    numpy ndarray with 50,000 entries.  Each entry is, in turn, a
    numpy ndarray with 784 values, representing the 28 * 28 = 784
    pixels in a single MNIST image.
    The second entry in the ``training_data`` tuple is a numpy ndarray
    containing 50,000 entries.  Those entries are just the digit
    values (0...9) for the corresponding images contained in the first
    entry of the tuple.
    The ``validation_data`` and ``test_data`` are similar, except
    each contains only 10,000 images.
    This is a nice data format, but for use in neural networks it's
    helpful to modify the format of the ``training_data`` a little.
    That's done in the wrapper function ``load_data_wrapper()``, see
    below.
    """
    f = gzip.open('mnist.pkl.gz', 'rb')
    training_data, validation_data, test_data = pickle.load(f, encoding="latin1")
    f.close()
    return (training_data, validation_data, test_data)

def load_data_wrapper():
    """Return a tuple containing ``(training_data, validation_data,
    test_data)``. Based on ``load_data``, but the format is more
    convenient for use in our implementation of neural networks.
    In particular, ``training_data`` is a list containing 50,000
    2-tuples ``(x, y)``.  ``x`` is a 784-dimensional numpy.ndarray
    containing the input image.  ``y`` is a 10-dimensional
    numpy.ndarray representing the unit vector corresponding to the
    correct digit for ``x``.
    ``validation_data`` and ``test_data`` are lists containing 10,000
    2-tuples ``(x, y)``.  In each case, ``x`` is a 784-dimensional
    numpy.ndarry containing the input image, and ``y`` is the
    corresponding classification, i.e., the digit values (integers)
    corresponding to ``x``.
    Obviously, this means we're using slightly different formats for
    the training data and the validation / test data.  These formats
    turn out to be the most convenient for use in our neural network
    code."""
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)

def vectorized_result(j):
    """Return a 10-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere.  This is used to convert a digit
    (0...9) into a corresponding desired output from the neural
    network."""
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

class class_network:

    def __init__(self, layer_sizes, hidden_function, hidden_derivative):
        # liczba wartsw
        self.n_layers = len(layer_sizes)

        #inicjalizacja warstw
        self.layers = [np.random.randn(layer_sizes[i+1], layer_sizes[i]+1) * np.sqrt(2/(layer_sizes[i])) for i in range(self.n_layers - 1)]

        #funkcja aktywaji dla warstw ukrytych
        self.hidden_function = hidden_function

        #pochodna funkcji aktywacji dla warstw ukrytych
        self.hidden_derivative = hidden_derivative
    
    def softmax(self, x):
        #dodatkowo stosuję centrowanie do średniej, np max liczy średnią po kolumnach (axis = 0)
        x -= np.max(x, axis = 0)
        x = np.exp(x)
        return x / np.sum(x, axis = 0)

    def outputs(self, data):
        #wiersz jedynek
        row_of_ones = np.ones((1, data.shape[1]))

        #dodaję wiersz jedynek do wejścia
        current = np.vstack((row_of_ones, data))
        
        #tworzę listy na przyszłe wyniki z warstw
        unactivated = []
        activated = [current]

        for i in range(self.n_layers - 2):
            #przepuszczem przez kolejną warstwę
            z = self.layers[i] @ current

            #nakładam funkcje na warstwy ukryte
            a = self.hidden_function(z)

            #znów dodaję wektor jedynek
            current = np.vstack((row_of_ones, a))

            #zapisuje kolejne wyjścia
            unactivated.append(z)
            activated.append(current)

        #obliczam wyjście z ostatniej warstwy 
        z = self.layers[-1] @ current
        a = self.softmax(z)

        #dodaję wyniki z ostatniej warstwy
        unactivated.append(z)
        activated.append(a)

        #zwracam listy z wynikami
        return unactivated, activated
    
    def predict(self, data):
        #to samo co output, ale bez zapisywania wartości po drodze, zwraca tylko ostateczny wynik
        row_of_ones = np.ones((1, data.shape[1]))
        current = np.vstack((row_of_ones, data))

        for i in range(self.n_layers - 2):
            z = self.layers[i] @ current
            a = self.hidden_function(z)
            current = np.vstack((row_of_ones, a))

        z = self.layers[-1] @ current
        a = self.softmax(z)

        return a

    
    def fit(self, X, Y, step, n_iter):
        for _ in range(n_iter):
            #permutuję dane
            combined = list(zip(X, Y))
            random.shuffle(combined)
            X_perm, Y_perm = zip(*combined)
            X_perm = list(X_perm)
            Y_perm = list(Y_perm)
            
            #tworzę batche, u mnie mają mają po 50 obrazów
            X_batches = [np.hstack(X_perm[i:i+50]) for i in range(1000)]
            Y_batches = [np.hstack(Y_perm[i:i+50]) for i in range(1000)]

            for X_batch , Y_batch in zip(X_batches, Y_batches):
                batch_size = X_batch.shape[1]
                z_vals, a_vals = self.outputs(X_batch)

                #warstwa wyjściowa
                Y_hat = a_vals[-1]
                delta = (Y_hat - Y_batch)
                self.layers[-1] -= (step / batch_size) * delta @ a_vals[-2].T

                #warstwy ukryte
                for i in reversed(range(self.n_layers - 2)):
                    delta = (self.layers[i+1][:, 1:].T @ delta) * self.hidden_derivative(z_vals[i])
                    self.layers[i] -= (step / batch_size) * delta @ a_vals[i].T
    
    def test(self, X, Y):
        Y_hat = self.predict(X)
        correct = np.sum(np.argmax(Y_hat, axis = 0) == Y, axis = 0)
        return correct / len(Y)
    
def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    t = np.tanh(x)
    return 1 - t**2
    
def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_derivative(x, alpha=0.01):
    dx = np.ones_like(x)
    dx[x < 0] = alpha
    return dx
        
def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

net = class_network(layer_sizes = (784, 250, 100, 10),
                    hidden_function = relu,
                    hidden_derivative = relu_derivative)

X = [i[0] for i in load_data_wrapper()[0]]

Y = [i[1] for i in load_data_wrapper()[0]]

X_test = [i[0] for i in load_data_wrapper()[1]]
X_test = np.hstack(X_test)

Y_test = [i[1] for i in load_data_wrapper()[1]]
Y_test = np.hstack(Y_test)

for epoch in range(15): 
    net.fit(X, Y, step=0.01, n_iter=1)
    acc = net.test(X_test,Y_test)
    print(f"Epoch {epoch+1}, accuracy: {acc:.4f}")

for epoch in range(15):  # 15 epochs
    net.fit(X, Y, step=0.001, n_iter=1)
    acc = net.test(X_test,Y_test)
    print(f"Epoch {epoch+1}, accuracy: {acc:.4f}")

for epoch in range(15):  # 15 epochs
    net.fit(X, Y, step=0.0001, n_iter=1)
    acc = net.test(X_test,Y_test)
    print(f"Epoch {epoch+1}, accuracy: {acc:.4f}")

net.test(X_test,Y_test)



