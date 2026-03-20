from src.struct.hamiltonian_builder import Hamiltonian
import abc
import networkx as nx
import matplotlib.pyplot as plt

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    return G

class Graph(nx.Graph):
    """A simple non oriented graph class to represent the problem instance."""

    def __init__(self):
        super().__init__()

    def draw(self) -> None:
            G = nx.Graph()
            G.add_nodes_from(range(len(self)))
            G.add_edges_from(self.edges)

            plt.figure(figsize=(3, 3))
            
            pos = nx.spring_layout(G, seed=42)

            nx.draw_networkx_nodes(G, pos, node_size=800, node_color="#b3d9ff", edgecolors="black")
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, pos)
            
            plt.title(f"Graph |V|={len(self)}, |E|={len(self.edges)}")
            plt.axis("off")
            plt.tight_layout()
            plt.show()

    
    def __str__(self) -> str:
        return f"Graph with {len(self.verticles)} vertices and edges: {self.edges}"


class ProblemInstance:
    """Instance of a graph coloring problem"""
    def __init__(self, graph, k):
        self.graph = graph
        self.k = k
        self.hamiltonian = Hamiltonian(graph)

class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph, number_of_color):
        self.graph = graph
        self.number_of_color = number_of_color

    @abc.abstractmethod
    def generate_solution(self):
        pass


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
