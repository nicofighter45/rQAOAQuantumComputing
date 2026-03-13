import abc

class Graph:
    """A simple non oriented graph class to represent the problem instance."""

    def __init__(self, num_verticles: int):
        self.verticles = list(range(num_verticles))
        self.edges = {i: set() for i in range(num_verticles)}

    def number_of_edges(self) -> int:
        """
        Returns the number of edges in the graph.
        """
        return sum(len(edges) for edges in self.edges.values())

    def number_of_verticles(self) -> int:
        """
        Returns the number of vertices in the graph.
        """
        return len(self.verticles)

    def add_edge(self, i: int, j: int) -> None:
        """
        Add the edge i-j to the graph
        """
        if not 0 <= i < self.number_of_verticles() or not 0 <= j < self.number_of_verticles():
            raise ValueError("Node indices must be within the range of the graph's vertices.")
        
        i, j = min(i, j), max(i, j)

        if not j in self.edges[i]:
            self.edges[i].add(j)
    
    def __str__(self) -> str:
        return f"Graph with {len(self.verticles)} vertices and edges: {self.edges}"


class ColoredGraph(Graph):
    """A simple non oriented colored graph class to represent the problem instance."""

    def __init__(self, num_verticles: int, number_of_color: int):
        super().__init__(num_verticles)
        self.max_color = number_of_color - 1
        self.coloration = [0 for _ in range(self.num_verticles)]
    
    def set_color(self, color: int) -> None:
        if color < 0 or color > self.max_color:
            raise ValueError(f"Color must be between 0 and {self.max_color}.")
        self.color = color
    
    def set_coloration(self, coloration: list[int]) -> None:
        if len(coloration) != self.num_verticles():
            raise ValueError("Coloration length must be equal to the number of vertices.")
        if any(c >= self.max_color or c < 0 for c in coloration):
            raise ValueError(f"Color values must be between 0 and {self.max_color}.")
        self.coloration = coloration



class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph, k):
        self.graph = graph
        self.k = k
    
    @abc.abstractmethod
    def generate_solution(self):
        pass
