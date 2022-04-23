# Simulated Annealing for 2D space optimisation problems.
#
# See the simulated annealing section under traditional techniques in the document for more details.

import random
import math
from search.search import Search

class SimulatedAnnealing(Search):
    def __init__(self, function, bound):
        super().__init__(function, bound)
        self.name = "Simulated Annealing"
    
    def search(self):
        nodes = []
        for _ in range(self.bound.node_count):
            nodes.append([random.uniform(self.x_1, self.x_2), random.uniform(self.y_1, self.y_2)])
        x_best = nodes
        y_best = self.objective(x_best)
        x_c = x_best
        y_c = y_best
        
        for k in range(1, self.iterations + 1):
            x_p = self.neighbour(x_c)
            y_p = self.objective(x_p)
            y_d = y_p - y_c
            if y_d <= 0 or random.uniform(0, 1) < min(self.exp(-y_d/self.temp(k)), 1):
                x_c, y_c = x_p, y_p
            if self.minimising:
                if y_p < y_best:
                    x_best = x_p
                    y_best = y_p
            else:
                if y_p > y_best:
                    x_best = x_p
                    y_best = y_p
        return x_best, y_best

    def neighbour(self, nodes):
        neighbours = []
        for n in nodes:
            neighbours.append([random.uniform(
                max(n[0] - self.movement(0), self.x_1),
                min(n[0] + self.movement(0), self.x_2)
            ),
            random.uniform(
                max(n[1] - self.movement(1), self.y_1),
                min(n[1] + self.movement(1), self.y_2)
            )])
        return neighbours
    
    def movement(self, x):
        return ((self.bound.get_area()[1][x] - self.bound.get_area()[0][x]) * 0.2)
        
    def temp(self, k):
        return 100 * (math.log(2)/math.log(k + 1))
    
    def exp(self, x):
        return math.e ** x