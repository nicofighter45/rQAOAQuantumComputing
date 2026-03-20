import json

def approximation_ratio(solution_value: float, optimal_value: float) -> float:
    """
    Compute the approximation ratio of a solution.
    """
    if optimal_value == 0:
        return 1.0 if solution_value == 0 else 0.0
    return solution_value / optimal_value


def compare_solutions(solutions_dict: dict) -> dict:
    """
    Compare solutions and store the comparison in a json file.
    """
    values = {method: val for method, (sol, val) in solutions_dict.items()}
    best_method = max(values, key=values.get)
    best_value = values[best_method]

    with open('comparison_results.json', 'w') as f:
        json.dump(values, f, indent=4)
    
    return {
        'best_method': best_method,
        'best_value': best_value,
        'all_values': values
    }
