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
    
    def add_node(self, node_for_adding, **attr):
        if "color" not in attr.keys():
            attr["color"] = 0
        if "weight" not in attr.keys():
            attr["weight"] = 1
        super().add_node(node_for_adding, **attr)
    
    def add_nodes_from(self, nodes_for_adding, **attr):
        if "color" not in attr.keys():
            attr["color"] = 0
        if "weight" not in attr.keys():
            attr["weight"] = 1
        return super().add_nodes_from(nodes_for_adding, **attr)
    
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

    def _get_colors(self) -> np.array[int]:
        return np.array([int_to_color(d['color']) for u, d in self.nodes(data=True)])
    
    def _get_weights(self) -> np.array[float]:
        list = np.array([d['weight'] if 'weight' in d.keys() else 1 for _,_, d in self.edges(data=True)])
        return list/np.mean(list)

    def draw(self) -> None:

        plt.figure(figsize=(3, 3))
            
        pos = nx.spring_layout(self, seed=42)

        nx.draw_networkx_nodes(self, pos, node_size=800, node_color=self._get_colors(), edgecolors="black")
            
        nx.draw_networkx_edges(self, pos, width=self._get_weights())
        nx.draw_networkx_labels(self, pos)
            
        plt.title(f"Graph |V|={len(self)}, |E|={len(self.edges)}")
        plt.axis("off")
        plt.tight_layout()
        plt.show()
