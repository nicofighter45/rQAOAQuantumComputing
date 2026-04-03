import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "solvers"))
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "struct"))
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "tools"))
)

from recursive_quantum_solver import RecursiveQAOASolver
from graph import random_graph, Graph
from visualization import plot_counts


G = random_graph(10, 0.5)
rQAOA = RecursiveQAOASolver(G, depth=1, number_of_color=2)
G, counts = rQAOA.generate_solution()

plot_counts(counts)

print(counts)

G.draw()

