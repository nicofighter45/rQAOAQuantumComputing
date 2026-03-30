from struct.hamiltonian import Hamiltonian
from src.struct.graph import Graph


class ProblemInstance:
    """Instance of a graph coloring problem"""
    def __init__(self, graph: Graph, k: int):
        self.graph = graph
        self.k = k
        self.hamiltonian = Hamiltonian(graph)


def create_test_graphs() -> dict[str, Graph]:
    """
    Create a dictionary of test graphs for benchmarking solvers.
    
    Returns:
        dict: Dictionary with graph names as keys and Graph objects as values
    """
    test_graphs = {}
    
    # Test 1: Triangle (K3)
    g1 = Graph(E=3)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 0)
    test_graphs["Triangle K3"] = g1
    
    # Test 2: Square (C4)
    g2 = Graph(E=4)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 0)
    test_graphs["Square C4"] = g2
    
    # Test 3: Star (S4)
    g3 = Graph(E=5)
    g3.add_edge(0, 1)
    g3.add_edge(0, 2)
    g3.add_edge(0, 3)
    g3.add_edge(0, 4)
    test_graphs["Star S4"] = g3
    
    # Test 4: Butterfly
    g4 = Graph(E=5)
    g4.add_edge(0, 1)
    g4.add_edge(1, 2)
    g4.add_edge(2, 0)  # Triangle 1
    g4.add_edge(2, 3)
    g4.add_edge(3, 4)
    g4.add_edge(4, 2)  # Triangle 2
    test_graphs["Butterfly"] = g4
    
    # Test 5: Path (P6)
    g5 = Graph(E=6)
    g5.add_edge(0, 1)
    g5.add_edge(1, 2)
    g5.add_edge(2, 3)
    g5.add_edge(3, 4)
    g5.add_edge(4, 5)
    test_graphs["Path P6"] = g5
    
    return test_graphs
