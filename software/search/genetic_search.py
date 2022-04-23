# Genetic Search for 2D space optimisation problems.
#
# See the genetic algorithms section under traditional techniques in the document for more details.

import numpy as np
import random
from search.search import Search
# Gaussian mutation for continuous encoded genes.
from scipy.stats import multivariate_normal

class GeneticSearch(Search):
    def __init__(self, function, bound):
        super().__init__(function, bound)
        self.name = "Genetic Search"

    def search(self):
        result = self.ga(10, self.iterations, 0.8, 0.2)
        return (list(result[0]), self.objective(result[0]))

    def random_pop(self, size):
        population = []
        for _ in range(size):
            nodes = []
            for _ in range(self.bound.node_count):
                nodes.append([random.uniform(self.x_1, self.x_2), random.uniform(self.y_1, self.y_2)])
            population.append(nodes)
        return population
    
    def t_selection(self, population, k):
        evals = [(p, self.objective(p)) for p in population]
        evals = sorted(evals, key=lambda x: x[1], reverse=not self.bound.minimising)
        return [e[0] for e in evals[:k]]

    def crossover(self, a, b):
        point = random.choice(range(2, len(a), 2))
        return np.concatenate((a[point:], b[:point])), np.concatenate((a[:point], b[point:]))

    def mutate(self, c, k, prob=None):
        if prob is None:
            prob = 1 / len(c)
        for node in c:
            r = np.random.random()
            if r < prob:
                if random.choice([True, False]):
                    node[0] += multivariate_normal.pdf([node[0]], k)
                    node[1] += multivariate_normal.pdf([node[1]], k)
                else:
                    node[0] -= multivariate_normal.pdf([node[0]], k)
                    node[1] -= multivariate_normal.pdf([node[1]], k)
        return c

    def ga(self, size, generations, p_c, p_m):
        p = self.random_pop(size)
        for k in range(0, int(generations / size) + 1):
            a, b = np.random.choice(len(p), size=2, replace=False)
            a, b = p[a], p[b]
            r = np.random.random()
            if r < p_c:
                c1, c2 = self.crossover(a, b)
            else:
                c1, c2 = a, b
            if r < p_m:
                c1p, c2p = self.mutate(c1, k), self.mutate(c2, k)
            else:
                c1p, c2p = c1, c2
            p = p + [c1p, c2p]
            p = self.t_selection(p, size - 2)
        p = list(map(list, p))
        return p