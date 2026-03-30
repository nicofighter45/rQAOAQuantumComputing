import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from src.tools.colors import int_to_color

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    for u, v in G.edges():
        G[u][v]['weight'] = 1
    return G

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
