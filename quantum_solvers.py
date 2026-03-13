from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, providers
from qiskit.circuit import ParameterVector
from qiskit_aer import AerSimulator
import numpy as np
from hamiltonian_builder import Hamiltonian
from instance_generator import AbstractSolverInstance
from scipy.optimize import minimize
from instance_generator import Graph


class QAOASolver(AbstractSolverInstance):
    def __init__(self, graph, k):
        super().__init__(graph, k)
        self.hamiltonian = Hamiltonian(self.graph)
        self.p = 1
    
    def generate_solution(self):

        def qaoa_expectation(params):
            qc = self.__generate_quantum_circuit_with_params(params)
            counts = AerSimulator().run(qc, shots=512).result().get_counts()
            max_bitstring = max(counts, key=counts.get)
            # Convert bitstring to integer array
            x = [int(bit) for bit in max_bitstring]
            return self.hamiltonian.cost(x)
        
        params_init = np.random.uniform(0, 2 * np.pi, 2 * self.p)
        res = minimize(qaoa_expectation, params_init, method='COBYLA')

        best_params = res.x
        qc_best = self.__generate_quantum_circuit_with_params(best_params)
        counts = AerSimulator().run(qc_best, shots=512).result().get_counts()
        max_bitstring = max(counts, key=counts.get)
        x_best = [int(bit) for bit in max_bitstring]
        best_cost = self.hamiltonian.cost(x_best)
        return {'solution': x_best, 'cost': best_cost, 'params': best_params}

    def __generate_quantum_circuit_with_params(self, params):
        n = self.graph.number_of_edges()
        qr = QuantumRegister(n, 'q')
        cr = ClassicalRegister(n, 'c')
        qc = QuantumCircuit(qr, cr)
        # tower of hadamard gates
        for i in range(n):
            qc.h(qr[i])
        for layer in range(self.p):
            gamma = params[layer]
            qc.barrier()
            self.__U(qc, qr, gamma, self.graph)
            beta = params[self.p + layer]
            qc.barrier()
            self.__V(qc, qr, beta)
        qc.barrier()
        qc.measure(qr, cr)
        
        return qc

    def __U(self, qc, qr, gamma, graph):
        for i in graph.edges:
            for j in graph.edges[i]:
                qc.rzz(2 * gamma, i, j)          

    def __V(self, qc, qr, beta):
        for i in range(len(qr)):
            qc.rx(2 * beta, qr[i])


class quditQAOASolver(AbstractSolverInstance):
    def __init__(self, graph, k):
        super().__init__(graph, k)
        self.hamiltonian = Hamiltonian(self.graph)
    
    def generate_solution(self):
        # https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CXGate
        pass



import random
num_nodes = 3
num_edges = 2  # arbitrary number of edges for testing
graph = Graph(num_nodes)
while graph.number_of_edges() < num_edges:
    i, j = random.sample(range(num_nodes), 2)
    graph.add_edge(i, j)
print(graph)
result = QAOASolver(graph, 2).generate_solution()
print("QAOA Result:", result)