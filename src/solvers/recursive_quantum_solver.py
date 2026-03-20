from src.solvers.quantum_solvers import QAOASolver
from src.struct.instance_generator import AbstractSolverInstance

class rQAOASolver(AbstractSolverInstance):
    def __init__(self, graph, number_of_color=2, depth=1, measurement_shots=1024):
        super().__init__(graph, number_of_color, depth, measurement_shots)
    
    def generate_solution(self):
        qaoa_solver = QAOASolver(self.graph, self.number_of_color, self.depth, self.measurement_shots)
        solution, counts = qaoa_solver.generate_solution()
        
        return solution, counts
