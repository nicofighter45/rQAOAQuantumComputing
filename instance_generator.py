from hamiltonian_builder import Hamiltonian
import abc
import networkx as nx
import matplotlib.pyplot as plt

class Graph(nx.Graph):
    """A simple non oriented graph class to represent the problem instance."""

    def __init__(self, num_verticles: int):
        self.verticles = list(range(num_verticles))
        self.edges = {i: set() for i in range(num_verticles)}

    def number_of_edges(self) -> int:
        """
        Returns the number of edges in the graph.
        """
        return sum(len(edges) for edges in self.edges.values())

    def number_of_verticles(self) -> int:
        """
        Returns the number of vertices in the graph.
        """
        return len(self.verticles)

    def add_edge(self, i: int, j: int) -> None:
        """
        Add the edge i-j to the graph
        """
        if not 0 <= i < self.number_of_verticles() or not 0 <= j < self.number_of_verticles():
            raise ValueError("Node indices must be within the range of the graph's vertices.")
        
        i, j = min(i, j), max(i, j)

        if not j in self.edges[i]:
            self.edges[i].add(j)

    def draw(self) -> None:
            G = nx.Graph()
            G.add_nodes_from(range(self.E))
            G.add_edges_from(self.edges)

            plt.figure(figsize=(3, 3))
            
            pos = nx.spring_layout(G, seed=42)

            nx.draw_networkx_nodes(G, pos, node_size=800, node_color="#b3d9ff", edgecolors="black")
            nx.draw_networkx_edges(G, pos)
            nx.draw_networkx_labels(G, pos)
            
            plt.title(f"Graph |V|={self.E}, |E|={len(self.edges)}")
            plt.axis("off")
            plt.tight_layout()
            plt.show()

    
    def __str__(self) -> str:
        return f"Graph with {len(self.verticles)} vertices and edges: {self.edges}"


class ColoredGraph(Graph):
    """A simple non oriented colored graph class to represent the problem instance."""

    def __init__(self, num_verticles: int, number_of_color: int):
        super().__init__(num_verticles)
        self.max_color = number_of_color - 1
        self.coloration = [0 for _ in range(self.num_verticles)]
    
    def set_color(self, color: int) -> None:
        if color < 0 or color > self.max_color:
            raise ValueError(f"Color must be between 0 and {self.max_color}.")
        self.color = color
    
    def set_coloration(self, coloration: list[int]) -> None:
        if len(coloration) != self.num_verticles():
            raise ValueError("Coloration length must be equal to the number of vertices.")
        if any(c >= self.max_color or c < 0 for c in coloration):
            raise ValueError(f"Color values must be between 0 and {self.max_color}.")
        self.coloration = coloration



class ProblemInstance:
    """Instance of a graph coloring problem"""
    def __init__(self, graph, k):
        self.graph = graph
        self.k = k
        self.hamiltonian = Hamiltonian(graph)

class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph, k):
        self.graph = graph
        self.k = k
    
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
