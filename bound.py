# Bound class for 2D space optimisation problems.
#
# A 'Bound' is the total area of the environment
# i.e. the area in which evaluations generally
# take place AND the constraints for points in 
# the space that are not allowed.
#
# For example, take a Bound X as shown below, 
# which represents a room with 4 supporting
# columns.
#
# X:
# ##########
# #        #
# #  C  C  #
# #        #
# #  C  C  #
# #        #
# ##########
#
# We would define the above Bound X with the area
# coordinates (0, 0) and (9, 6) and the 
# constraints `C` (2,3), (2,6), (4,3), (4,6). 
#
# All measurements are in meters.
#
# Constraints can be single points as well as
# larger areas themselves.
# 
# We can use this Bound class to determine if a 
# placement of a point in space is valid for this
# area.

import math
import json

import numpy as np

class Bound:
    def __init__(self, name, node_count, area, constraints, points, iterations, minimising):
        # Area is a 2D array shaped like [[0, 0], [1, 1]].
        self.name = name
        self.node_count = node_count
        self.area = area
        self.constraints = constraints
        self.points = points
        self.iterations = iterations
        self.minimising = minimising
    
    def __str__(self):
        return f"Bound {self.name} with node_count {self.node_count}, area {self.area}, constraints {self.constraints}, points {self.points}, {self.iterations} iterations and minimising set to {self.minimising}."

    def _in_area(self, point, area):
        return area[0][0] <= point[0] <= area[1][0] and area[0][1] <= point[1] <= area[1][1]
    
    def _obeys_constraints(self, point):
        for constraint in self.constraints:
            c_type = constraint[0]
            c_bounds = constraint[1]
            if c_type == "RECT":
                if self._in_area(point, c_bounds):
                    return False
            elif c_type == "CIRC":
                if math.sqrt((point[0] - c_bounds[0])**2 + (point[1] - c_bounds[1])**2) < c_bounds[2]:
                    return False
        return True

    def valid(self, points):
        for point in points:
            if not self.point_valid(point):
                return False

        return True

    def point_valid(self, point):
        return self._in_area(point, self.area) and self._obeys_constraints(point)

    def get_area(self):
        return self.area

    def to_json(self):
        j = {"name": self.name,
                "node_count": self.node_count,
                "area": self.area,
                "constraints": self.constraints,
                "points": self.points,
                "iterations": self.iterations,
                "minimising": self.minimising}
        return j
    
    @staticmethod
    def from_json(j):
        bound = Bound(j["name"],
                      j["node_count"], 
                      j["area"],
                      j["constraints"],
                      j["points"],
                      j["iterations"],
                      j["minimising"])
        return bound

    @staticmethod
    def from_file(file):
        try:
            file = open(file)
            return Bound.from_json(json.load(file))
        except Exception as e:
            print(e)
            file.close()
            print("Bounds.from_file: Error in file parsing. File may not exist or an argument was invalid.")
    
    @staticmethod
    def random():
        name = "Random"
        point_count = np.random.randint(10, 20)
        area_limit = np.random.randint(10, 35)
        area = [[0, 0], [area_limit, area_limit]]
        points = np.random.randint(0, area_limit, (point_count, 2))
        node_count = point_count - np.random.randint(3, 5)
        minimising = True
        iterations = np.random.randint(100, 200)
        constraint_count = np.random.randint(5, 10)
        constraints = []
        for _ in range(constraint_count):
            shape = np.random.choice(["RECT", "CIRC"])
            if shape == "RECT":
                properties = list(np.random.randint(0, area_limit, [2, 2]))
            if shape == "CIRC":
                properties = list(np.random.randint(0, area_limit, 2)) + [np.random.randint(0, 5)]
            constraints.append([shape, properties])
        return Bound(name, node_count, area, constraints, points, iterations, minimising)