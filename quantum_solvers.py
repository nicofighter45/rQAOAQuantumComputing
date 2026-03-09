import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import ParameterVector
import numpy as np


def QAOA(problem, p):

    n = problem.graph.E
    qr = QuantumRegister(n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Initial superposition
    for i in range(n):
        qc.h(qr[i])
    
    # Parameters: p angles for problem Hamiltonian, p angles for mixer Hamiltonian
    params = ParameterVector('θ', 2 * p)
    
    # QAOA layers
    for layer in range(p):
        # Problem Hamiltonian (cost) unitary
        gamma = params[layer]
        qc.barrier()
        U(qc, qr, gamma, problem.graph)
        
        # Mixer Hamiltonian unitary
        beta = params[p + layer]
        qc.barrier()
        V(qc, qr, beta)
    
    # Measurement
    qc.measure(qr, cr)
    
    return qc


def U(qc, qr, gamma, graph):
    def cr(i, j):
        qc.cx(qr[i],qr[j])
        qc.rz(np.angle,qr[j])
        qc.cx(qr[i],qr[j])

    for i in range(graph.E):
        for j in graph.edges[i]:
            cr(i, j)
    
    for i in range(len(qr)):
        qc.rz(2 * gamma, qr[i])


def V(qc, qr, beta):
    

    for i in range(len(qr)):
        qc.rx(2 * beta, qr[i])
