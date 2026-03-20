from src.solvers.quantum_solvers import QAOASolver
from src.solvers.recursive_quantum_solver import RecursiveQAOASolver
from src.struct.instance_generator import random_graph
from src.struct.hamiltonian_builder import Hamiltonian

RecursiveQAOASolver(random_graph(4, 0.5)).generate_solution()