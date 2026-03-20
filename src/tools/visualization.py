import matplotlib.pyplot as plt
import numpy as np


_test_results = {}


def store_test_results(graph_name: str, results: dict) -> None:
    _test_results[graph_name] = results

def plot_results_summary() -> None:
    """
    Creates two subplots:
    - Left: Execution times per solver
    - Right: Solution quality (scores) per solver
    """
    if not _test_results:
        print("No results to plot yet. Run tests first.")
        return
    
    graph_names = list(_test_results.keys())
    methods = list(_test_results[graph_names[0]].keys())
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Execution times
    ax1 = axes[0]
    times_by_method = {method: [] for method in methods}
    
    for graph_name in graph_names:
        for method in methods:
            _, _, exec_time = _test_results[graph_name][method]
            times_by_method[method].append(exec_time * 1000)  # Convert to ms
    
    x = np.arange(len(graph_names))
    width = 0.35
    for i, method in enumerate(methods):
        offset = width * (i - len(methods)/2 + 0.5)
        ax1.bar(x + offset, times_by_method[method], width, label=method.upper())
    
    ax1.set_xlabel('Graph')
    ax1.set_ylabel('Execution Time (ms)')
    ax1.set_title('Solver Performance - Execution Times')
    ax1.set_xticks(x)
    ax1.set_xticklabels(graph_names, rotation=45)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Solution quality (scores)
    ax2 = axes[1]
    scores_by_method = {method: [] for method in methods}
    
    for graph_name in graph_names:
        for method in methods:
            _, score, _ = _test_results[graph_name][method]
            scores_by_method[method].append(score)
    
    for i, method in enumerate(methods):
        offset = width * (i - len(methods)/2 + 0.5)
        ax2.bar(x + offset, scores_by_method[method], width, label=method.upper())
    
    ax2.set_xlabel('Graph')
    ax2.set_ylabel('Score')
    ax2.set_title('Solver Performance - Solution Quality')
    ax2.set_xticks(x)
    ax2.set_xticklabels(graph_names, rotation=45)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
