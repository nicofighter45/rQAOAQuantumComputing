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
from quantum_solver import QAOASolver
from graph import random_graph
from visualization import plot_counts


colors = 2
G = random_graph(5, 0.5)
QAOA = RecursiveQAOASolver(G, depth=1)
G, counts = QAOA.generate_solution()

plot_counts(counts)

print(counts)

G.draw()

