from src.solvers.recursive_quantum_solver import RecursiveQAOASolver
from src.struct.graph import random_graph
from src.tools.visualization import plot_counts

G = random_graph(4, 0.5)
rQAOA = RecursiveQAOASolver(G)
solution, counts = rQAOA.generate_solution()
print(solution)
plot_counts(counts)
rQAOA.graph.draw()
G.draw
