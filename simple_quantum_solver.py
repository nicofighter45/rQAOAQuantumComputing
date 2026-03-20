from qiskit.quantum_info import Pauli, PauliList, SparsePauliOp
import numpy as np


edges = [(0, 1), (0, 2)]  # Example edges
n = 3  # Number of qubits
diagonal = [] # diagonal of the Hamiltonian matrix

for i in range(2**n):
    bitstring = format(i, f'0{n}b')  # Convert index to binary string
    print(i, bitstring)
    value = 0
    for (i, j) in edges:
        if bitstring[n-1-i] != bitstring[n-1-j]: # if the edges are connectd and different color
            value += 1
    diagonal.append(value)

# Create a list of Pauli terms for each state
pauli_terms = [('I'*n, diagonal[i]) for i in range(2**n)]

# Convert the list of Pauli terms to a SparsePauliOp
hamiltonian = SparsePauliOp.from_list(pauli_terms)

print(hamiltonian)

