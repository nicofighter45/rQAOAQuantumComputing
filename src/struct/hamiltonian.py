from math import log

import numpy as np
from typing import Callable
from qiskit.quantum_info import Operator, SparsePauliOp


def cost(edges: list[tuple[int, int]], color: Callable[[int], int], weight: Callable[[int, int], float]) -> float:
    acc = 0
    for (i, j) in edges:
        if color(i) != color(j):
            acc += weight(i, j)
    return acc


def bicolor_cost_hamiltonian(
    n: int,
    edges: list[tuple[int, int]],
    weight: Callable[[int, int], float],
) -> SparsePauliOp:
    # MaxCut cost operator: sum_(i,j) w_ij/2 * (I - Z_i Z_j)
    identity = "I" * n
    pauli_terms: list[tuple[str, float]] = [(identity, 0.0)]

    for (i, j) in edges:
        wij = float(weight(i, j))
        zz = ["I"] * n
        zz[i] = "Z"
        zz[j] = "Z"
        pauli_terms.append((identity, wij / 2.0))
        pauli_terms.append(("".join(zz), -wij / 2.0))

    return SparsePauliOp.from_list(pauli_terms).simplify()


def old_bicolor_cost_hamiltonian(
    n: int,
    edges: list[tuple[int, int]],
    weight: Callable[[int, int], float],
) -> SparsePauliOp:
    # Legacy implementation kept for debugging/comparison with the fixed operator.
    diagonal = []

    for state_idx in range(2**n):
        bitstring = format(state_idx, f"0{n}b")
        value = 0.0
        for (i, j) in edges:
            if bitstring[i] != bitstring[j]:
                value += float(weight(i, j))
        diagonal.append(value)

    pauli_terms = [("I" * n, diagonal[state_idx]) for state_idx in range(2**n)]
    return SparsePauliOp.from_list(pauli_terms)

"""
m = log(k, 2) # number of qubits needed to encode k colors
if int(m) != m:
    m = int(m) + 1
else:
    m = int(m)
"""

def old_cost_hamiltonian(
    n: int,
    k: int,
    m: int,
    edges: list[tuple[int, int]],
    weight: Callable[[int, int], float],
) -> SparsePauliOp:
    if k == 2:
        return old_bicolor_cost_hamiltonian(n, edges, weight)

    color_encoding = {j: format(j, f"0{m}b") for j in range(k)}
    diagonal = []

    for i in range(k**n):
        ni = i
        knary = ""
        while ni > 0:
            knary += str(ni % k)
            ni //= k
        knary = knary[::-1]
        binary = ""
        for c in knary:
            binary += color_encoding[int(c)]
        knary = knary.zfill(n)
        binary = binary.zfill(n * m)
        value = 0.0
        for (u, v) in edges:
            if knary[u] != knary[v]:
                value += float(weight(u, v))
        diagonal.append(value)

    pauli_terms = [("I" * (n * m), diagonal[i]) for i in range(k**n)]
    return SparsePauliOp.from_list(pauli_terms)


def cost_hamiltonian(
    n: int,
    k: int,
    m: int,
    edges: list[tuple[int, int]],
    weight: Callable[[int, int], float],
) -> SparsePauliOp:
    if k == 2:
        return bicolor_cost_hamiltonian(n, edges, weight)
    if m <= 0:
        raise ValueError("m must be a strictly positive number of qubits per vertex.")

    num_qubits = n * m
    dim = 2**num_qubits
    diagonal = np.zeros(dim, dtype=np.float64)

    # States that decode to colors outside [0, k-1] are invalid for the chosen
    # encoding. Push them below any feasible score so QAOA avoids them.
    #max_abs_cost = sum(abs(float(weight(u, v))) for (u, v) in edges)
    #invalid_state_penalty = -(max_abs_cost + 1.0) # not working

    # Build the true diagonal in the full 2^(n*m) Hilbert space.
    for state_idx in range(dim):
        bits = format(state_idx, f"0{num_qubits}b")
        colors = []
        valid_encoding = True

        for node in range(n):
            color = int(bits[node * m : (node + 1) * m], 2)
            if color >= k:
                valid_encoding = False
                break
            colors.append(color)

        if not valid_encoding:
            #diagonal[state_idx] = invalid_state_penalty # not working
            continue

        value = 0.0
        for (u, v) in edges:
            if colors[u] != colors[v]:
                value += float(weight(u, v))
        diagonal[state_idx] = value

    pauli_terms = [("I" * num_qubits, diagonal[i]) for i in range(dim) if diagonal[i] != 0.0]
    return SparsePauliOp.from_list(pauli_terms).simplify()
