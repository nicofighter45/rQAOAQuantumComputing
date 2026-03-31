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

        mapper = [u for u in self.graph.nodes]
        color_bind = []

        graph = Graph()
        graph.add_nodes_from(deepcopy(self.graph.nodes(data=True)))
        graph.add_edges_from(deepcopy(self.graph.edges(data=True)))

        for i in range(self.__number_of_recursive_steps(len(self.graph))):
            
            n = initial_n - i
            print(f"Recursive step {i+1}/{self.__number_of_recursive_steps(len(self.graph))}, nodes {graph.nodes}, edges {graph.edges}, mapper {mapper}")
            graph.draw()
            qaoa_solver = QAOASolver(graph, self.number_of_color, self.depth, self.measurement_shots)
            _, counts = qaoa_solver.generate_solution(node_remapper=lambda x: mapper.index(x))

            acc = np.zeros((n, n), dtype=np.float64)
            for (u, v) in graph.edges:
                i, j = mapper[u], mapper[v]
                for bitstring in counts.keys():
                    proba = counts[bitstring] / self.measurement_shots
                    acc[i, j] += proba * (int(bitstring[n-1-i])*2-1) * (int(bitstring[n-1-j])*2-1)
            max_value, max_x, max_y = 0, 0, 0
            for x in range(n):
                for y in range(n):
                    if acc[x, y] > max_value:
                        max_value = acc[x, y]
                        max_x, max_y = x, y
            i, j = mapper.index(max_x), mapper.index(max_y)
            
            for neighbor in graph.neighbors(i):
                if neighbor != j:
                    graph.add_weight(j, neighbor, graph[i][neighbor]['weight'])
            graph.remove_node(i)
            mapper[i] = -1
            color_bind.append((i, j))
            for k in range(i+1, initial_n):
                mapper[k] -= 1
        
        print(f"Last step, nodes {graph.nodes}, edges {graph.edges}, mapper {mapper}, color_bind {color_bind}")
        graph.draw()
        qaoa_solver = QAOASolver(graph, self.number_of_color, self.depth, self.measurement_shots)
        _, counts = qaoa_solver.generate_solution(node_remapper=lambda x: mapper.index(x))

        for u, d in graph.nodes(data=True):
            self.graph.set_color(u, d['color'])
        for u, v in color_bind[::-1]:
            self.graph.set_color(u, self.graph.get_color(v))
        

        return self.graph, counts
