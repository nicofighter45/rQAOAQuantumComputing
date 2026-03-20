from math import log, floor

from src.tools.utils import *
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

class Hamiltonian:
    def __init__(self, graph, number_of_color=2):
        self.graph = graph
        self.number_of_color = number_of_color


    def cost(self, x):
        acc = 0
        for i in range(len(self.graph)):
            for j in range(i+1, len(self.graph)):
                acc += delta_function(x[i], x[j])
        return acc
    
    def bicolor_cost_hamiltonian(self) -> SparsePauliOp:
        n = len(self.graph)  # Number of qubits
        diagonal = [] # diagonal of the Hamiltonian matrix

        for i in range(2**n):
            bitstring = format(i, f'0{n}b')  # Convert index to binary string
            value = 0
            for (i, j) in self.graph.edges:
                if bitstring[n-1-i] != bitstring[n-1-j]: # if the edges are connectd and different color
                    value += 1
            diagonal.append(value)

        # Create a list of Pauli terms for each state
        pauli_terms = [('I'*n, diagonal[i]) for i in range(2**n)]

        # Convert the list of Pauli terms to a SparsePauliOp
        return SparsePauliOp.from_list(pauli_terms)

    def cost_hamiltonian(self) -> SparsePauliOp:
        if self.number_of_color == 2:
            return self.bicolor_cost_hamiltonian()
        n = len(self.graph)
        k = self.number_of_color
        m = log(k, 2) # number of qubits needed to encode k colors
        if int(m) != m:
            m = int(m) + 1
        else:
            m = int(m)
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
            for (i, j) in self.graph.edges:
                if knary[n-1-i] != knary[n-1-j]: # if the edges are connectd and different color
                    value += 1
            diagonal.append(value)

        # Create a list of Pauli terms for each state
        pauli_terms = [('I'*n*m, diagonal[i]) for i in range(k**n)]

        # Convert the list of Pauli terms to a SparsePauliOp
        return SparsePauliOp.from_list(pauli_terms)
            

    """

    def cost_hamiltonian(self):
        cost_hamiltonian = PauliSumOp.from_list([])
        for (i, j) in self.graph.edges:
            for b in range(self.graph.k):
                for a in range(self.graph.k):
                    cost_hamiltonian += self.__projector(i, j, a, b)
        return cost_hamiltonian
    
    def __projector(self, i, j, a, b):
        # For k=2, a and b can be 0 or 1
        # The projector is |a, a XOR b><a, a XOR b|
        a_xor_b = a ^ b

        # Create a quantum circuit for the projector |a, a_xor_b><a, a_xor_b|
        qc = QuantumCircuit(2)

        # Prepare the state |a, a_xor_b>
        if a == 1:
            qc.x(0)
        if a_xor_b == 1:
            qc.x(1)

        # Create the projector |a, a_xor_b><a, a_xor_b|
        state = Statevector.from_instruction(qc)
        projector = state.to_operator()

        return projector
    
    """
    
    
