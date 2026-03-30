from src.solvers.quantum_solvers import QAOASolver
from src.struct.instance_generator import AbstractSolverInstance, MergedGraph, Graph
import numpy as np

class RecursiveQAOASolver(QAOASolver):
    def __init__(self, graph: Graph, number_of_color=2, depth=1, measurement_shots=1024, number_of_recursive_steps=lambda n: int(n/2)):
        self.__number_of_recursive_steps = number_of_recursive_steps
        self.__original_graph = graph.copy()
        graph.__class__ = MergedGraph
        self.__merged_nodes = {n: [] for n in range(len(graph))}
        super().__init__(graph, number_of_color, depth, measurement_shots)
        

    def generate_solution(self):

        for _ in range(self.__number_of_recursive_steps(len(self.__original_graph))):
            qaoa_solver = QAOASolver(self.graph, self.number_of_color, self.depth, self.measurement_shots)
            solution, counts = qaoa_solver.generate_solution()

            n = len(self.graph)

            acc = np.zeros((len(self.graph), len(self.graph)))
            for (i, j) in self.graph.edges:
                for bitstring in counts.keys():
                    proba = counts[bitstring] / self.measurement_shots
                    acc[self.graph.vertices.index(i), self.graph.vertices.index(j)] += proba * (int(bitstring[n-1-i])*2-1) * (int(bitstring[n-1-j])*2-1)
            i, j = np.unravel_index(np.argmax(acc), acc.shape)
            
            self.graph.merge_vertices(i, j)

        return solution, counts

    def __paint_original_graph(self) -> Graph:
        self.__original_graph.colors = self.graph.colors
        for i, j in self.graph.get_merged_nodes()[::-1]:
            self.__original_graph.set_color(j, self.__original_graph.colors[i])
        return self.__original_graph
