import abc
from graph import Graph

class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph: Graph, number_of_color: int):
        self.graph = graph
        self.number_of_color = number_of_color

    @abc.abstractmethod
    def generate_solution(self):
        pass
