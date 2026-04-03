import qiskit
from qiskit.circuit.library import QAOAAnsatz
from qiskit_aer import AerSimulator
import hamiltonian
from abstract_solver_instance import AbstractSolverInstance
import numpy as np
from scipy.optimize import minimize


def clean_counts(counts: dict[str, int], colors: int = 2) -> dict[str, int]:
    if colors <= 1:
        return dict(counts)

    def shift_key(key: str, shift: int) -> str:
        return "".join(str((int(ch) + shift) % colors) for ch in key)

    merged: dict[str, int] = {}
    for key, count in counts.items():
        # Canonicalize by taking the lexicographically smallest key in the
        # orbit obtained by adding a global color shift modulo `colors`.
        orbit = [shift_key(key, shift) for shift in range(colors)]
        representative = min(orbit)
        merged[representative] = merged.get(representative, 0) + count

    return merged


class QAOASolver(AbstractSolverInstance):
    def __init__(self, graph, number_of_color=2, depth=1, measurement_shots=1024):
        super().__init__(graph, number_of_color)
        self.depth = depth
        self.measurement_shots = measurement_shots

    def generate_solution(self):

        cost_operator = hamiltonian.cost_hamiltonian(len(self.graph.nodes), self.number_of_color, self.encoding_bit_number, self.graph.edges, self.graph.get_weight)
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
                # Qiskit returns bitstrings in little-endian order for measured qubits.
                x = self.from_bistring_to_color(bitstring)                
                exp += hamiltonian.cost(self.graph.edges, lambda u: x[u], self.graph.get_weight) * count
            return -exp
        
        # Initial parameters
        params_init = np.random.uniform(0, 2 * np.pi, qaoa.num_parameters)
        res = minimize(get_expectation, params_init, method='COBYLA')
        best_params = res.x

        # Final circuit and solution
        bound_qaoa = qaoa.assign_parameters(best_params)
        bound_qaoa.measure_all()
        transpiled = qiskit.transpile(bound_qaoa, sim)
        counts = sim.run(transpiled, shots=self.measurement_shots).result().get_counts()
        max_bitstring = max(counts, key=counts.get)
        x_best = self.from_bistring_to_color(max_bitstring)
        for u, color in enumerate(x_best):
            self.graph.set_color(u, color)
        return self.graph, clean_counts(counts)
