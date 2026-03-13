from utils import *

class Hamiltonian:
    def __init__(self, graph):
        self.graph = graph

    def C(self, color_list: list) -> int:
        acc = 0
        for i in range(self.graph.E):
            for j in range(i+1, self.graph.E):
                acc += delta_function(color_list[i], color_list[j])
        return acc
