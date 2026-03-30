import itertools
from struct.problem_instance import ProblemInstance


def brute_force_solver(problem_instance: ProblemInstance) -> tuple:
    """
    Find the optimal solution by exhaustively searching all possible configurations.
    We consider 2-coloring of a graph, which means we have 2^n possible configurations for n vertices.
    This method is computationally expensive and only suitable for small graphs (n <= 20).
    """
    n = problem_instance.graph.E
    best_solution = None
    best_score = -float('inf')
    
    # Iterate over all possible configurations
    for config in itertools.product([0, 1], repeat=n):
        score = problem_instance.hamiltonian.C(list(config))
        if score > best_score:
            best_score = score
            best_solution = list(config)
    
    return best_solution, best_score


def greedy_solver(problem_instance: ProblemInstance) -> tuple:
    """
    This method iteratively builds a solution by making the locally optimal choice at each step.
    """
    n = problem_instance.graph.E
    solution = [0] * n
    
    # We evaluate the score for both assignments (0 and 1) and pick the one that yields a higher score.
    for i in range(n):
        solution[i] = 0
        score_0 = problem_instance.hamiltonian.C(solution)
        
        solution[i] = 1
        score_1 = problem_instance.hamiltonian.C(solution)
        
        solution[i] = 1 if score_1 >= score_0 else 0
    
    return solution, problem_instance.hamiltonian.C(solution)
