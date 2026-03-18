import qiskit
import numpy as np
import networkx as nx
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

from instance_generator import ProblemInstance, Graph
import instance_generator


n = 4

G = instance_generator.random_graph(n, 0.5)

instance = ProblemInstance(G, 2)

qaoa = qiskit.circuit.library.QAOAAnsatz(cost_operator=instance.hamiltonian.bicolor_cost_hamiltonian(), reps=1)
params = [0.1] * qaoa.num_parameters
bound_qaoa = qaoa.assign_parameters(params)
bound_qaoa.measure_all()
sim = AerSimulator()
transpiled = qiskit.transpile(bound_qaoa, sim)
counts = AerSimulator().run(transpiled, shots=1024).result().get_counts()

# Plot the counts as a bar chart
def plot_counts(counts):
    plt.figure(figsize=(8, 4))
    plt.bar(counts.keys(), counts.values(), color='skyblue')
    plt.xlabel('Bitstring')
    plt.ylabel('Counts')
    plt.title('Measurement Results')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

max_bitstring = max(counts, key=counts.get)
x_best = [int(bit) for bit in max_bitstring]
print(f"solution : {x_best}")

plot_counts(counts)
G.draw()
