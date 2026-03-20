from src.solvers.quantum_solvers import QAOASolver, plot_counts
from src.struct.instance_generator import random_graph

G = random_graph(4, 0.5)
solver = QAOASolver(G)
best_coloration, counts = solver.generate_solution()
print(best_coloration)
plot_counts(counts)
G.draw()
