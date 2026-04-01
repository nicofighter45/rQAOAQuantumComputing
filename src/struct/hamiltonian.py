from math import log

from qiskit.quantum_info import SparsePauliOp


def cost(edges: list[tuple[int, int]], color: function, weight: function) -> float:
    acc = 0
    for (i, j) in edges:
        if color(i) != color(j):
            acc += weight(i, j)
    return acc


def bicolor_cost_hamiltonian(n: int, edges: list[tuple[int, int]], weight: function) -> SparsePauliOp:
    diagonal = [] # diagonal of the Hamiltonian matrix

    for i in range(2**n):
        bitstring = format(i, f'0{n}b')  # Convert index to binary string
        value = 0
        for (i, j) in edges:
            if bitstring[i] != bitstring[j]: # if the edges are connectd and different color
                value += weight(i, j)
        diagonal.append(value)

    # Create a list of Pauli terms for each state
    pauli_terms = [('I'*n, diagonal[i]) for i in range(2**n)]

    # Convert the list of Pauli terms to a SparsePauliOp
    return SparsePauliOp.from_list(pauli_terms)

"""
m = log(k, 2) # number of qubits needed to encode k colors
if int(m) != m:
    m = int(m) + 1
else:
    m = int(m)
"""

def cost_hamiltonian(n: int, k: int, m: int, edges: list[tuple[int, int]], weight: function) -> SparsePauliOp:
        if k == 2:
            return bicolor_cost_hamiltonian(n, edges, weight)

        color_encoding = {j: format(j, f'0{m}b') for j in range(k)} # map color index to binary string
        diagonal = []

        for i in range(k**n):
            ni = i
            knary = ""
            while ni > 0:
                knary += str(ni % k)
                ni //= k
            knary = knary[::-1] # k-nary string encoding the colors
            binary = ""
            for c in knary:
                binary += color_encoding[int(c)]
            knary = knary.zfill(n)
            binary = binary.zfill(n*m) # pad with zeros to get the full binary string
            value = 0
            for (i, j) in edges:
                if knary[i] != knary[j]: # if the edges are connectd and different color
                    value += weight(i, j)
            diagonal.append(value)

        # Create a list of Pauli terms for each state
        pauli_terms = [('I'*n*m, diagonal[i]) for i in range(k**n)]

        # Convert the list of Pauli terms to a SparsePauliOp
        return SparsePauliOp.from_list(pauli_terms)
