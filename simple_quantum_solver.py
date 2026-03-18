import qiskit
import numpy as np
import networkx as nx
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt


n = 4

G = nx.erdos_renyi_graph(n=n, p=0.5)

list = []
for i, j in G.edges():
    list.append(""*4, "")


HC = qiskit.quantum_info.SparsePauliOp(["I"*n, "Z"*n], np.array([1/2*c, -1/2*c]))


qaoa = qiskit.circuit.library.QAOAAnsatz(cost_operator=HC, reps=1)
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

plot_counts(counts)

max_bitstring = max(counts, key=counts.get)
x_best = [int(bit) for bit in max_bitstring]
print(f"solution : {x_best}")
