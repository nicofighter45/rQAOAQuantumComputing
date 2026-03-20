from utils import *
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

class Hamiltonian:
    def __init__(self, graph):
        self.graph = graph


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
            print(i, bitstring)
            value = 0
            for (i, j) in self.graph.edges:
                if bitstring[n-1-i] != bitstring[n-1-j]: # if the edges are connectd and different color
                    value += 1
            diagonal.append(value)

        # Create a list of Pauli terms for each state
        pauli_terms = [('I'*n, diagonal[i]) for i in range(2**n)]

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
    
    
