import unittest
from bound import Bound
from fspl import fspl_min
from search.random_search import RandomSearch
from search.simulated_annealing import SimulatedAnnealing
from search.genetic_search import GeneticSearch
from search.bayesian_search import BayesianSearch

class BoundTests(unittest.TestCase):
    def setUp(self):
        self.bound = Bound.from_file("template.bounds")
    
    def test_name(self):
        assert self.bound.name == "MONA"
        
    def test_count(self):
        assert self.bound.node_count == 5
    
    def test_iterations(self):
        assert self.bound.iterations == 500
    
    def test_minimising(self):
        assert self.bound.minimising == True
    
    def test_constraint_length(self):
        assert len(self.bound.constraints) == 10
    
    def test_constraint_rect(self):
        assert self.bound.constraints[0][0] == "RECT"
    
    def test_constraint_circ(self):
        assert self.bound.constraints[9][0] == "CIRC"
    
    def test_constraint_content(self):
        for constraint in self.bound.constraints:
            if constraint[0] == "RECT":
                assert len(constraint[1]) == 2
                assert len(constraint[1][0]) == 2
                assert len(constraint[1][1]) == 2
            elif constraint[0] == "CIRC":
                assert len(constraint[1]) == 3
    
    def test_points_length(self):
        assert len(self.bound.points) == 9
    
    def test_points_content(self):
        assert self.bound.points[0][0] == 12
        assert self.bound.points[0][1] == 23

class SearchTests(unittest.TestCase):
    def setUp(self):
        self.bound = Bound.from_file("template.bounds")
        self.function = fspl_min
    
    def test_random_search(self):
        result = RandomSearch(self.function, self.bound).search()
        assert len(result[0]) == self.bound.node_count
        assert result[1]
        
    
    def test_genetic_search(self):
        result = GeneticSearch(self.function, self.bound).search()
        assert len(result[0]) == self.bound.node_count
        assert result[1]
    
    def test_simulated_annealing(self):
        result = SimulatedAnnealing(self.function, self.bound).search()
        assert len(result[0]) == self.bound.node_count
        assert result[1]
    
    def test_bayesian_search(self):
        result = BayesianSearch(self.function, self.bound).search()
        assert len(result[0]) == self.bound.node_count
        assert result[1]

if __name__ == "__main__":
    unittest.main()