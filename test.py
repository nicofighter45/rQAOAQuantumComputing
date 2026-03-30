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

from src.solvers.recursive_quantum_solver import RecursiveQAOASolver
from src.struct.graph import random_graph
from src.tools.visualization import plot_counts

G = random_graph(8, 0.5)
rQAOA = RecursiveQAOASolver(G)
G, counts = rQAOA.generate_solution()
plot_counts(counts)
G.draw()
