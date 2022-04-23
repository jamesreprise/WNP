import math
import random
import numpy as np
from search.search import Search

class SABayes(Search):
    def __init__(self, function, bound):
        super().__init__(function, bound)
        self.name = "Simulated Annealing for Bayesian Search"
    
    def search(self):
        nodes = []
        for _ in range(self.bound.node_count):
            nodes.append([random.uniform(self.x_1, self.x_2), random.uniform(self.y_1, self.y_2)])
        x_best = nodes
        y_best = self.function(np.array(x_best).flatten())
        x_c = x_best
        y_c = y_best
        
        for k in range(1, 100):
            x_p = self.neighbour(x_c)
            y_p = self.function(x_p)
            y_d = y_p - y_c
            if y_d >= 0 or random.uniform(0, 1) < min(self.exp(-y_d/self.temp(k)), 1):
                x_c, y_c = x_p, y_p
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
        return 5.5 / k
    
    def exp(self, x):
        return math.e ** x