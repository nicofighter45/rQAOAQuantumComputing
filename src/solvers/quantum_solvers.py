import qiskit
from qiskit.circuit.library import QAOAAnsatz
from qiskit_aer import AerSimulator
from src.struct.hamiltonian_builder import Hamiltonian
from src.struct.instance_generator import AbstractSolverInstance
import numpy as np
from scipy.optimize import maximize


class QAOASolver(AbstractSolverInstance):
    def __init__(self, graph, number_of_color=2, depth=1, measurement_shots=1024):
        super().__init__(graph, number_of_color)
        self.hamiltonian = Hamiltonian(self.graph, number_of_color)
        self.depth = depth
        self.measurement_shots = measurement_shots

    def generate_solution(self):

        cost_operator = -self.hamiltonian.bicolor_cost_hamiltonian()
        qaoa = QAOAAnsatz(cost_operator=cost_operator, reps=self.depth)
        sim = AerSimulator()

        def get_expectation(params):
            bound_qaoa = qaoa.assign_parameters(params)
            bound_qaoa.measure_all()
            transpiled = qiskit.transpile(bound_qaoa, sim)
            result = sim.run(transpiled, shots=self.measurement_shots).result()
            counts = result.get_counts()
            # Compute expectation value
            exp = 0
            for bitstring, count in counts.items():
                x = [int(bit) for bit in bitstring[::-1]]
                exp += self.hamiltonian.cost(x) * count
            exp /= self.measurement_shots
            return exp
        
        # Initial parameters
        params_init = np.random.uniform(0, 2 * np.pi, qaoa.num_parameters)
        res = maximize(get_expectation, params_init, method='COBYLA')
        best_params = res.x

        # Final circuit and solution
        bound_qaoa = qaoa.assign_parameters(best_params)
        bound_qaoa.measure_all()
        transpiled = qiskit.transpile(bound_qaoa, sim)
        counts = sim.run(transpiled, shots=self.measurement_shots).result().get_counts()
        max_bitstring = max(counts, key=counts.get)
        x_best = [int(bit) for bit in max_bitstring[::-1]]
        return x_best, counts


class quditQAOASolver(AbstractSolverInstance):
    def __init__(self, graph, k):
        super().__init__(graph, k)
        self.hamiltonian = Hamiltonian(self.graph)
    
    def generate_solution(self):
        # https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CXGate
        pass



"""

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
"""