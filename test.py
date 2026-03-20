from quantum_solvers import QAOASolver
from src.struct.instance_generator import random_graph

QAOASolver(graph=random_graph(4, 0.5)).generate_solution()
