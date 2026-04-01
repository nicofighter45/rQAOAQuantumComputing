from quantum_solver import QAOASolver
from graph import Graph
import numpy as np
from copy import deepcopy

class RecursiveQAOASolver(QAOASolver):
    def __init__(self, graph: Graph, number_of_color=2, depth=1, measurement_shots=1024, number_of_recursive_steps=lambda n: int(n/2)):
        self.__number_of_recursive_steps = number_of_recursive_steps
        super().__init__(graph, number_of_color, depth, measurement_shots)
        

    def generate_solution(self):

        initial_n = len(self.graph)

        graph = Graph()
        graph.add_nodes_from(deepcopy(self.graph.nodes(data=True)))
        graph.add_edges_from(deepcopy(self.graph.edges(data=True)))
        binded_nodes = []

        for i in range(self.__number_of_recursive_steps(len(self.graph))):
            
            n = initial_n - i
            print(f"Recursive step {i+1}/{self.__number_of_recursive_steps(len(self.graph))}, nodes {graph.nodes}, edges {graph.edges(data=True)}, binded_nodes {binded_nodes}")
            graph.draw()
            qaoa_solver = QAOASolver(graph, self.number_of_color, self.depth, self.measurement_shots)
            _, counts = qaoa_solver.generate_solution()

            sign_acc = np.zeros((n, n), dtype=np.float64)
            acc = np.zeros((n, n), dtype=np.float64)
            for (i, j) in graph.edges:
                for bitstring in counts.keys():
                    proba = counts[bitstring]
                    acc[i, j] += proba * (int(bitstring[i])*2-1) * (int(bitstring[j])*2-1)
            for x in range(n):
                for y in range(n):
                    acc[x, y] = abs(acc[x, y])
                    sign_acc[x, y] = np.sign(acc[x, y])
            i, j = np.unravel_index(acc.argmax(), acc.shape)
            s = np.sign(acc[i, j])
            print(f"Collapsing nodes {i} and {j} with sign {s}, acc {acc[i, j]}\n\n{acc}")
            
            for neighbor in graph.neighbors(i):
                if neighbor != j:
                    if graph.has_edge(j, neighbor):
                        graph.add_weight(j, neighbor, graph.get_weight(i, neighbor))
                    else:
                        graph.set_weight(j, neighbor, (graph.get_weight(i, neighbor)+graph.get_weight(i, j))/2)
                    graph.set_weight(j, neighbor, s*graph.get_weight(j, neighbor))
            

            self.graph.set_binded_color(self.graph.get_super_node(i), self.graph.get_super_node(j), s)
            binded_nodes.append(self.graph.get_super_node(i))
            super_nodes = [graph.get_super_node(u) for u in graph.nodes]
            graph.remove_node(i)
            relabeling = {u: u for u in graph.nodes}
            for k in range(i+1, len(graph.nodes)+1):
                relabeling[k] = k-1
            print("relabeling", relabeling)
            graph.relabel_nodes(relabeling)
            for k in range(i, len(graph.nodes)):
                graph.set_super_node(k, super_nodes[k+1])
    
        
        print(f"Last step, nodes {graph.nodes}, edges {graph.edges(data=True)}, binded_nodes {binded_nodes}")
        graph.draw()
        qaoa_solver = QAOASolver(graph, self.number_of_color, self.depth, self.measurement_shots)
        _, counts = qaoa_solver.generate_solution()

        for i, c in enumerate(graph.get_colors()):
            print(f"Color of node {i}, {graph.get_super_node(i)} is {c}")
            self.graph.set_color(self.graph.get_super_node(i), c)
        for u in binded_nodes[::-1]:
            v, s = self.graph.get_binded_color(u)
            if s == 1:
                self.graph.set_color(u, self.graph.get_color(v))
            else:
                self.graph.set_color(u, 1-self.graph.get_color(v))
        

        return self.graph, counts
