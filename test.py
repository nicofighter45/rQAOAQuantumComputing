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


colors = 2
G = Graph()
G.add_nodes_from([0, 1, 2, 3, 4])
G.add_edge(0, 1)
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(0, 2)
rQAOA = RecursiveQAOASolver(G, depth=1)
G, counts = rQAOA.generate_solution()

plot_counts(counts)

print(counts)

G.draw()

