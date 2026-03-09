from hamiltonian_builder import Hamiltonian

class Graph:
    def __init__(self, E):
        self.E = E
        self.edges = set()

    def add_edge(self, i, j):
        if i != j:
            self.edges.add((min(i, j), max(i, j)))
    
    def __str__(self):
        return f"Graph with {len(self.E)} vertices and edges: {self.edges}"


class ProblemInstance:
    def __init__(self, graph, k):
        self.graph = graph
        self.k = k
        self.hamiltonian = Hamiltonian(self.graph)
