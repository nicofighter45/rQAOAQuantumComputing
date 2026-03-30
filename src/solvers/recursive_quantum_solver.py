from quantum_solvers import QAOASolver
from graph import MergedGraph, Graph
import numpy as np
from copy import deepcopy

class RecursiveQAOASolver(QAOASolver):
    def __init__(self, graph: Graph, number_of_color=2, depth=1, measurement_shots=1024, number_of_recursive_steps=lambda n: int(n/2)):
        self.__number_of_recursive_steps = number_of_recursive_steps
        self.__original_graph = deepcopy(graph)
        graph.__class__ = MergedGraph
        graph.__init__()
        super().__init__(graph, number_of_color, depth, measurement_shots)
        

    def generate_solution(self):

        initial_n = len(self.graph)

        for i in range(self.__number_of_recursive_steps(len(self.__original_graph))):
            n = initial_n - i
            print(f"Recursive step {i+1}/{self.__number_of_recursive_steps(len(self.__original_graph))}, colors {self.graph.colors}, vertices {self.graph.vertices()}, removed vertices {self.graph.get_removed_vertices()}")
            #self.graph.draw()
            qaoa_solver = QAOASolver(self.graph, self.number_of_color, self.depth, self.measurement_shots)
            _, counts = qaoa_solver.generate_solution()

            

            acc = np.zeros((n, n))
            for (i, j) in self.graph.edges:
                for bitstring in counts.keys():
                    proba = counts[bitstring] / self.measurement_shots
                    acc[self.graph.vertices().index(i), self.graph.vertices().index(j)] += proba * (int(bitstring[n-1-i])*2-1) * (int(bitstring[n-1-j])*2-1)
            i, j = np.unravel_index(np.argmax(acc), acc.shape)
            
            self.graph.merge_vertices(i, j)
        
        qaoa_solver = QAOASolver(self.graph, self.number_of_color, self.depth, self.measurement_shots)
        _, counts = qaoa_solver.generate_solution()

        return self.__paint_original_graph(), counts

    def __paint_original_graph(self) -> Graph:
        self.__original_graph.colors = self.graph.colors.copy()
        for i, j in self.graph.get_merged_nodes()[::-1]:
            self.__original_graph.set_color(j, self.__original_graph.colors[i])
        return self.__original_graph
