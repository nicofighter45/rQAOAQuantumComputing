from hamiltonian_builder import Hamiltonian
import abc
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, E):
        self.E = E
        self.edges = set()

    def add_edge(self, i, j):
        if i != j:
            self.edges.add((min(i, j), max(i, j)))

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

    
    def __str__(self):
        return f"Graph with {len(self.E)} vertices and edges: {self.edges}"

class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph, k):
        self.graph = graph
        self.k = k
    
    @abc.abstractmethod
    def generate_solution(self):
        pass
