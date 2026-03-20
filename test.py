from src.solvers.quantum_solvers import QAOASolver
from src.struct.instance_generator import random_graph
from src.struct.hamiltonian_builder import Hamiltonian

G = random_graph(3, 0.5)
hamiltonian = Hamiltonian(G, 3)
print(hamiltonian.cost_hamiltonian())
