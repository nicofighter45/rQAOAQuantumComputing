from src.solvers.quantum_solvers import QAOASolver
from src.struct.instance_generator import AbstractSolverInstance
import numpy as np

class RecursiveQAOASolver(QAOASolver):
    def __init__(self, graph, number_of_color=2, depth=1, measurement_shots=1024):
        super().__init__(graph, number_of_color, depth, measurement_shots)
    
    def generate_solution(self):
        
        for _ in range(int(len(self.graph)/2)):
            qaoa_solver = QAOASolver(self.graph, self.number_of_color, self.depth, self.measurement_shots)
            solution, counts = qaoa_solver.generate_solution()

            n = len(self.graph)

            acc = np.zeros((len(self.graph), len(self.graph)))
            for (i, j) in self.graph.edges:
                for bitstring in counts.keys():
                    proba = counts[bitstring] / self.measurement_shots
                    acc[i, j] += proba * (int(bitstring[n-1-i])*2-1) * (int(bitstring[n-1-j])*2-1)
            i, j = np.unravel_index(np.argmax(acc), acc.shape)
            
            for neighbor in list(self.graph.neighbors(i)):
                if neighbor != j:
                    self.graph.add_edge(j, neighbor)
            self.graph.remove_node(i)

        return solution, counts
