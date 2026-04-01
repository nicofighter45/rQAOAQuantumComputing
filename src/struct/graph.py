import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from colors import int_to_color

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    G.__init__(should_super=False)
    return G

class Graph(nx.Graph):
    """
    A superclass of nx graph immplementation to force color for every node and weight for every edge in a graph.
    It also contains a method to draw the graph with colors and weights.
    """

    def __init__(self, should_super=True):
        if should_super:
            super().__init__()
        for u, d in self.nodes(data=True):
            if 'color' not in d.keys():
                self.nodes[u]['color'] = 0
        for u, v, d in self.edges(data=True):
            if 'weight' not in d.keys():
                self[u][v]['weight'] = 1
    
    def set_super_node(self, u: int, v: int) -> None:
        self.nodes[u]['super'] = v
    
    def get_super_node(self, u: int) -> int:
        if 'super' not in self.nodes[u].keys():
            return u
        return self.nodes[u]['super']

    def set_binded_color(self, u: int, v: int, s: int) -> None:
        self.nodes[u]['binded_color'] = (v, s)
    
    def get_binded_color(self, u: int) -> tuple[int, int]:
        if 'binded_color' not in self.nodes[u].keys():
            return None
        return self.nodes[u]['binded_color']
    
    def add_node(self, node_for_adding, **attr):
        if "color" not in attr.keys():
            attr["color"] = 0
        super().add_node(node_for_adding, **attr)
    
    def add_edge(self, u: int, v: int, **attr):
        if "weight" not in attr.keys():
            attr["weight"] = 1
        super().add_edge(u, v, **attr)
    
    def add_nodes_from(self, nodes_for_adding, **attr):
        if "color" not in attr.keys():
            attr["color"] = 0
        return super().add_nodes_from(nodes_for_adding, **attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        if "weight" not in attr.keys():
            attr["weight"] = 1
        super().add_edges_from(ebunch_to_add, **attr)
    
    def set_weight(self, u: int, v: int, weight: float) -> None:
        if self.has_edge(u, v):
            self[u][v]['weight'] = weight
        else:
            self.add_edge(u, v, weight=weight)
    
    def add_weight(self, u: int, v: int, weight: float) -> None:
        if self.has_edge(u, v):
            self[u][v]['weight'] += weight
        else:
            self.add_edge(u, v, weight=weight)
    
    def set_color(self, u: int, color: int) -> None:
        self.nodes[u]['color'] = color
    
    def get_color(self, u: int) -> int:
        return self.nodes[u]['color']
    
    def get_weight(self, u: int, v: int) -> float:
        return self[u][v]['weight']

    def get_colors(self) -> np.array[int]:
        return np.array([d['color'] for _, d in self.nodes(data=True)])

    def get_colors_string(self) -> np.array[int]:
        return np.array([int_to_color(d['color']) for _, d in self.nodes(data=True)])
    
    def get_weights(self) -> np.array[float]:
        return np.array([d['weight'] for _,_, d in self.edges(data=True)])

    def relabel_nodes(self, mapping: dict[int, int]) -> None:
        nx.relabel_nodes(self, mapping, copy=False)

    def draw(self) -> None:

        plt.figure(figsize=(3, 3))
            
        pos = nx.spring_layout(self, seed=42)

        nx.draw_networkx_nodes(self, pos, node_size=800, node_color=self.get_colors_string(), edgecolors="black")
            
        nx.draw_networkx_edges(self, pos, width=self.get_weights())
        nx.draw_networkx_labels(self, pos)
        
        edge_labels = {(u, v): d['weight'] for u, v, d in self.edges(data=True)}
        nx.draw_networkx_edge_labels(self, pos, edge_labels)
            
        plt.title(f"Graph |V|={len(self)}, |E|={len(self.edges)}")
        plt.axis("off")
        plt.tight_layout()
        plt.show()
