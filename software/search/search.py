# Abstract search class for 2D space optimisation problems.
#
# This class defines a simple interface for a search.
#
# Every search needs:
# - a function to optimise,
# - the number of times it should call the function,
# - a `Bound` defining the area and constraints,
# - whether we are minimising or maximising the function
#   (we take minimising=False to mean that we are maximising.)
#
# Some searches may require extra parameters.
import math

class Search:
    def __init__(self, function, bound):
        self.function = function
        self.bound = bound
        self.iterations = bound.iterations
        self.minimising = bound.minimising
        self.x_1 = self.bound.get_area()[0][0]
        self.y_1 = self.bound.get_area()[0][1]
        self.x_2 = self.bound.get_area()[1][0]
        self.y_2 = self.bound.get_area()[1][1]
    
    def objective(self, nodes):
        if self.bound.valid(nodes):
            return self.function(nodes, self.bound.points)
        else:
            return self.function(nodes, self.bound.points) + 100 if self.minimising else self.function(nodes, self.bound.points) - 100
    
    def search(self):
        print("Search function not implemented.")
