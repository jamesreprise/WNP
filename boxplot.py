import sys
import matplotlib.pyplot as plt
import numpy as np
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
print("Loading bounds...")
print()
bound = np.random.choice([Bound.random(), Bound.random(), Bound.random()])
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
            BayesianSearch(FUNCTION, bound)]

color_dict = {"Bayesian Search": 'red',
            "Genetic Search": 'blue',
            "Simulated Annealing": 'green',
            "Random Search": 'orange'}

outputs = {"Bayesian Search": [],
            "Genetic Search": [],
            "Simulated Annealing": [],
            "Random Search": []}


for x in range(25):
    for optimiser in optimisers:
        result = optimiser.search()
        outputs[optimiser.name].append(result[1])
    print(x)

fig, ax = plt.subplots()
ax.boxplot(outputs.values())
ax.set_xticklabels(["Bayesian Search",
            "Genetic Search",
            "Simulated Annealing",
            "Random Search"])
plt.show()