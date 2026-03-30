import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from colors import int_to_color

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    G.__init__(should_super=False)
    for u, v in G.edges():
        G.set_weight(u, v, np.random.rand())
    return G

class Graph(nx.Graph):
    """A simple non oriented graph class to represent the problem instance."""

    def __init__(self, should_super=True):
        if should_super:
            super().__init__()
        self.colors = np.zeros(self.__len__(), dtype=np.int8)
        self.weight_list = self.__weight_list
    
    def set_weight(self, u: int, v: int, weight: float) -> None:
        self[u][v]['weight'] = weight

    def _get_colors(self) -> np.array[int]:
        return np.array([int_to_color(self.colors[u]) for u in range(len(self.colors))])
    
    def set_color(self, u: int, color: int) -> None:
        self.colors[u] = color

    @property
    def __weight_list(self) -> np.array[float]:
        list = np.array([d['weight'] if 'weight' in d.keys() else 1 for _,_, d in self.edges(data=True)])
        return list/np.mean(list)

    def draw(self) -> None:

            plt.figure(figsize=(3, 3))
            
            pos = nx.spring_layout(self, seed=42)

            nx.draw_networkx_nodes(self, pos, node_size=800, node_color=self._get_colors(), edgecolors="black")
            
            nx.draw_networkx_edges(self, pos, width=self.weight_list)
            nx.draw_networkx_labels(self, pos)
            
            plt.title(f"Graph |V|={len(self)}, |E|={len(self.edges)}")
            plt.axis("off")
            plt.tight_layout()
            plt.show()

    
    def __str__(self) -> str:
        return f"Graph with {len(self)} vertices and edges: {self.edges}"

    def __copy__(self):
        G = Graph()
        G.add_nodes_from(self.nodes)
        G.add_edges_from(self.edges(data=True))
        G.colors = self.colors.copy()
        return G

class MergedGraph(Graph):
    def __init__(self):
        self.__removed_vertices = []
        self.colors = np.zeros(len(self), dtype=np.int8)
        self.__merged_nodes = []

    def _get_colors(self) -> np.array[int]:
        print(np.array([int_to_color(self.colors[u]) for u in range(len(self.colors)) if u not in self.__removed_vertices]))
        print(self.__removed_vertices)
        return np.array([int_to_color(self.colors[u]) for u in range(len(self.colors)) if u not in self.__removed_vertices])
    
    def get_merged_nodes(self) -> list[tuple[int, int]]:
        return self.__merged_nodes
    
    def get_removed_vertices(self) -> list[int]:
        return self.__removed_vertices

    def merge_vertices(self, original_node: int, merged_node: int) -> None:
        for neighbor in list(self.neighbors(original_node)):
            if neighbor != merged_node:
                self.add_edge(merged_node, neighbor)
                if self.has_edge(merged_node, neighbor):
                    self[merged_node][neighbor]['weight'] = self[merged_node][neighbor].get('weight', 1) + self[original_node][neighbor].get('weight', 1)
                else:
                    self.add_edge(merged_node, neighbor, weight=self[original_node][neighbor].get('weight', 1))
        self.remove_node(merged_node)
        self.__merged_nodes.append((original_node, merged_node))
        self.__removed_vertices.append(merged_node)
    
    def vertices(self) -> list[int]:
        #print("Calling verticles", self.__removed_vertices, self.nodes)
        return [u for u in self.nodes if u not in self.__removed_vertices]

    def set_color(self, u: int, color: int) -> None:
        self.colors[self.vertices()[u]] = color
