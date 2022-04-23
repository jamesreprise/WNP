# CLI driver program for the optimisation library found in ./search.
#
# This interface is primarily string manipulation and pretty printing
# the imported bounds files and the results of the optimisations.

import sys
import matplotlib.pyplot as plt
from bound import Bound
from search.random_search import RandomSearch
from search.simulated_annealing import SimulatedAnnealing
from search.genetic_search import GeneticSearch
from search.bayesian_search import BayesianSearch
from fspl import fspl_min

FUNCTION = fspl_min

print("=" * 60)
print(f"Launched Node Placement Optimiser with Args: {sys.argv[1::]}")
print()
for arg in sys.argv[1::]:
    print("Loading bounds...")
    print()
    bound = Bound.from_file(arg)
    print(f"Bound {bound.name} loaded.")

    if bound.node_count >= len(bound.points):
        print("!" * 30)
        print(f"WARNING: You're trying to place {bound.node_count} nodes to cover {len(bound.points)} sensors. Are you sure you want to do this?")
        print("!" * 30)

    print(f"{bound.name} has following specifications: ")
    print(f"- # of Nodes: {bound.node_count}")
    print(f"- Constraints: ")
    for constraint in bound.constraints:
        print(f"    - {constraint}")
    print(f"- Points: ")
    for point in bound.points:
        print(f"    - {point}")
    print(f"- Iterations: {bound.iterations}")
    print(f"- Minimising: {bound.minimising}")
    print("=" * 60)
    print("Beginning optimisation...")

    optimisers = [
                RandomSearch(FUNCTION, bound), 
                SimulatedAnnealing(FUNCTION, bound),
                GeneticSearch(FUNCTION, bound),
                BayesianSearch(FUNCTION, bound)
                ]

    for optimiser in optimisers:
        result = optimiser.search()
        print(f"{optimiser.name} finished!")

        print(f"Lowest average free space path loss: {result[1]:.2f}")
        print(f"Best configuration found in {bound.iterations} evaluations was:")
        for node in zip(range(1, len(result[0]) + 1), result[0]):
            print(f"{node[0]} : [{node[1][0]:.2f}, {node[1][1]:.2f}]")
        print()
