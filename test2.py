import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from src.tools.colors import int_to_color

def random_graph(n: int, p: float) -> Graph:
    G = nx.erdos_renyi_graph(n=n, p=p)
    G.__class__ = Graph
    G.__init__()
    return G





G = random_graph(8, 0.5)
G.draw()
