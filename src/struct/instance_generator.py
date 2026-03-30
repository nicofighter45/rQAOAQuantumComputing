from src.struct.hamiltonian_builder import Hamiltonian
import abc
import networkx as nx
import matplotlib.pyplot as plt

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    for u, v in G.edges():
        G[u][v]['weight'] = 1
        G[u][v]['color'] = 1
    return G

def int_to_color(i: int) -> str:
    colors = ["red", "blue", "green", "yellow", "cyan", "magenta", "orange", "purple"]
    return colors[i % len(colors)]


class Graph(nx.Graph):
    """A simple non oriented graph class to represent the problem instance."""

    def __init__(self):
        super().__init__()
        self.color_list = None
    
    def set_color(self, u: int, v: int, color: int) -> None:
        self[u][v]['color'] = color
    
    def set_weight(self, u: int, v: int, weight: float) -> None:
        self[u][v]['weight'] = weight

    @property
    def color_list(self) -> list[int]:
        return [int_to_color(self[u][v]['color']) for u, v in self.edges()]
    
    @property
    def weight_list(self) -> list[float]:
        return [self[u][v]['weight'] for u, v in self.edges()]

    def draw(self) -> None:

            plt.figure(figsize=(3, 3))
            
            pos = nx.spring_layout(self, seed=42)

            nx.draw_networkx_nodes(self, pos, node_size=800, node_color=self.color_list, edgecolors="black")
            nx.draw_networkx_edges(self, pos)
            nx.draw_networkx_labels(self, pos)
            
            plt.title(f"Graph |V|={len(self)}, |E|={len(self.edges)}")
            plt.axis("off")
            plt.tight_layout()
            plt.show()

    
    def __str__(self) -> str:
        return f"Graph with {len(self)} vertices and edges: {self.edges}"


class ProblemInstance:
    """Instance of a graph coloring problem"""
    def __init__(self, graph: Graph, k: int):
        self.graph = graph
        self.k = k
        self.hamiltonian = Hamiltonian(graph)

class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph: Graph, number_of_color: int):
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
