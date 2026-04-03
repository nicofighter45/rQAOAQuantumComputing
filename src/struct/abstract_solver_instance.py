import abc

from math import log
from graph import Graph

class AbstractSolverInstance(abc.ABC):
    def __init__(self, graph: Graph, number_of_color: int):
        self.graph = graph
        self.number_of_color = number_of_color
        self.encoding_bit_number = log(self.number_of_color, 2)
        if int(self.encoding_bit_number) != self.encoding_bit_number:
            self.encoding_bit_number = int(self.encoding_bit_number) + 1
        else:
            self.encoding_bit_number = int(self.encoding_bit_number)

    @abc.abstractmethod
    def generate_solution(self):
        pass

    def from_bistring_to_color(self, bitstring: str) -> list[int]:
        bitstring = bitstring[::-1]
        color_assignment = []
        for i in range(0, len(bitstring), self.encoding_bit_number):
            color_bits = bitstring[i:i+self.encoding_bit_number]
            color = int(color_bits, 2)
            color_assignment.append(color)
        return color_assignment
