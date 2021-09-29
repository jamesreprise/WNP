# Random search for 2D space optimisation problems.
#
# An extremely naive and simple search algorithm.
#
# We take the number of nodes we have available `node_count`
# and attempt to minimise or maximise the function depending
# on the how the class is instantiated.

import random
import math
from search.search import Search

class RandomSearch(Search):
    def __init__(self, function, bound):
        super().__init__(function, bound)
        self.name = "Random Search"
    
    def search(self):
        if self.minimising:
            minimum = [], math.inf
            for i in range(self.iterations):
                result = self.random_sample()
                if result[1] < minimum[1]:
                    minimum = result
            return minimum
        else:
            maximum = [], -math.inf
            for i in range(self.iterations):
                result = self.random_sample()
                if result[1] > maximum[1]:
                    maximum = result
            return maximum

    
    def random_sample(self):
        nodes = []
        for _ in range(self.bound.node_count):
            nodes.append([random.uniform(self.x_1, self.x_2), random.uniform(self.y_1, self.y_2)])
        return nodes, self.objective(nodes)