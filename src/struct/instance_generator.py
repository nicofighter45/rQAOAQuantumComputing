from src.struct.hamiltonian_builder import Hamiltonian
import abc
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    for u, v in G.edges():
        G[u][v]['weight'] = 1
    return G

def int_to_color(i: int) -> str:
    colors = ["red", "blue", "green", "yellow", "cyan", "magenta", "orange", "purple"]
    return colors[i % len(colors)]


class Graph(nx.Graph):
    """A simple non oriented graph class to represent the problem instance."""

    def __init__(self):
        super().__init__()
        self.colors = np.zeros(len(self.nodes))
        self.weight_list = self.__weight_list  
    
    def set_weight(self, u: int, v: int, weight: float) -> None:
        self[u][v]['weight'] = weight

    def __get_colors(self) -> np.array[int]:
        return np.array([int_to_color(self.colors[u]) for u in range(len(self))])
    
    def set_color(self, u: int, color: int) -> None:
        self.colors[u] = color

    @property
    def __weight_list(self) -> np.array[float]:
        list = np.array([self[u][v]['weight'] for u, v in self.edges()])
        return list/np.mean(list)

    def draw(self) -> None:

            plt.figure(figsize=(3, 3))
            
            pos = nx.spring_layout(self, seed=42)

            nx.draw_networkx_nodes(self, pos, node_size=800, node_color=self.__get_colors(), edgecolors="black")
            
            nx.draw_networkx_edges(self, pos, width=self.weight_list)
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

class MergedGraph(Graph):
    def __init__(self, graph: Graph, merged_nodes: list[tuple[int, int]]):
        super().__init__()
        self.__removed_vertices = []
        self.__merged_nodes = []
        self.vertices = self.__vertices
    
    def __len__(self):
        return super().__len__()-len(self.__removed_vertices)

    def original_len(self):
        return super().__len__()
    
    def get_merged_nodes(self) -> list[tuple[int, int]]:
        return self.__merged_nodes

    def merge_vertices(self, original_node: int, merged_node: int) -> None:
        for neighbor in list(self.graph.neighbors(original_node)):
                if neighbor != merged_node:
                    self.graph.add_edge(merged_node, neighbor)
        self.graph.remove_node(merged_node)
        self.__merged_nodes.append((original_node, merged_node))
        self.__removed_vertices.append(merged_node)
    
    @property
    def __vertices(self):
        return [u for u in self.nodes if u not in self.__remove_vertices]
    
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
