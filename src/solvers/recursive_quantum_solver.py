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

        for step in range(self.__number_of_recursive_steps(len(self.graph))):

            n = initial_n - step
            print(f"Recursive step {step+1}/{self.__number_of_recursive_steps(len(self.graph))}, nodes {graph.nodes}, edges {graph.edges(data=True)}, binded_nodes {binded_nodes}")
            graph.draw()
            qaoa_solver = QAOASolver(graph, self.number_of_color, self.depth, self.measurement_shots)
            _, counts = qaoa_solver.generate_solution()

            if len(graph.edges) == 0:
                break

            corr = np.zeros((n, n), dtype=np.float64)
            for (u, v) in graph.edges:
                value = 0.0
                for bitstring, sample_count in counts.items():
                    # Qiskit bitstrings are little-endian; map qubit q -> bitstring[-q-1].
                    su = int(bitstring[-u - 1]) * 2 - 1
                    sv = int(bitstring[-v - 1]) * 2 - 1
                    value += sample_count * su * sv
                corr[u, v] = value
                corr[v, u] = value

            # Collapse only along existing edges using maximum absolute correlation.
            collapse_u, collapse_v = max(
                graph.edges,
                key=lambda edge: abs(corr[edge[0], edge[1]]),
            )
            raw_corr = corr[collapse_u, collapse_v]
            s = 1 if raw_corr >= 0 else -1
            print(f"Collapsing nodes {collapse_u} and {collapse_v} with sign {s}, corr {raw_corr}\n\n{corr}")

            for neighbor in list(graph.neighbors(collapse_u)):
                if neighbor != collapse_v:
                    graph.add_weight(collapse_v, neighbor, s*graph.get_weight(collapse_u, neighbor))

            self.graph.set_binded_color(
                self.graph.get_super_node(collapse_u),
                self.graph.get_super_node(collapse_v),
                s,
            )
            binded_nodes.append(self.graph.get_super_node(collapse_u))
            super_nodes = [graph.get_super_node(u) for u in graph.nodes]
            graph.remove_node(collapse_u)
            relabeling = {u: u for u in graph.nodes}
            for k in range(collapse_u + 1, len(graph.nodes) + 1):
                relabeling[k] = k - 1
            print("relabeling", relabeling)
            graph.relabel_nodes(relabeling)
            for k in range(collapse_u, len(graph.nodes)):
                graph.set_super_node(k, super_nodes[k + 1])
    
        
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
