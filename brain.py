import numpy as np
import copy

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class NeuralNet:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.W1 = np.random.randn(hidden_nodes, input_nodes)
        self.b1 = np.random.randn(hidden_nodes, 1)
        self.W2 = np.random.randn(output_nodes, hidden_nodes)
        self.b2 = np.random.randn(output_nodes, 1)

    def predict(self, inputs):
        x = np.array(inputs, ndmin=2).T
        a1 = sigmoid(np.dot(self.W1,x) + self.b1)
        return sigmoid(np.dot(self.W2,a1)+self.b2)
    
    def clone(self):
        return copy.deepcopy(self)
    
    def mutate(self, mutation_rate = 0.1):
        self.W1 += np.random.randn(*self.W1.shape) * mutation_rate
        self.b1 += np.random.randn(*self.b1.shape) * mutation_rate
        self.W2 += np.random.randn(*self.W2.shape) * mutation_rate
        self.b2 += np.random.randn(*self.b2.shape) * mutation_rate