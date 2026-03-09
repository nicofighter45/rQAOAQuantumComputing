from utils import *

class Hamiltonian:
    def __init__(self, graph):
        self.graph = graph

    def C(self, x):
        acc = 0
        for i in range(self.graph.E):
            for j in range(i+1, self.graph.E):
                acc += 1 - delta_function(x[i], x[j])
        return acc

def J(i, j, b, graph):
    if i in graph.E and j in graph.E:
        return 1 - delta_function(b, 0)
    return 0

def PI(i, j, b, graph):
    acc = 0

