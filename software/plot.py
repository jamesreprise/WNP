# Plot class for plotting 2D node optimisation spaces and outputs.
# 
#
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from bound import Bound
from fspl import fspl_min
from search.bayesian_search import BayesianSearch

class Plot():
    def __init__(self, nodes, bound):
        self.nodes = nodes
        self.bound = bound
        # More colour maps can be found at https://matplotlib.org/stable/tutorials/colors/colormaps.html
        self.cmap = "magma_r"
        self.function = fspl_min

    def objective(self, nodes):
            if self.bound.valid(nodes):
                return self.function(nodes, self.bound.points)
            else:
                return 100 if self.bound.minimising else -100

    def plot_space(self):
        """
        Plots the space given by self.bound and self.function.
        
        Returns: matplotlib.pyplot
        """
        plt.clf()
        theta_1 = np.linspace(0, self.bound.area[1][0], 250)
        theta_2 = np.linspace(0, self.bound.area[1][1], 250)
        Xp, Yp = np.meshgrid(theta_1, theta_2)
        Z = np.zeros(Xp.shape)
        for (i,j),v in np.ndenumerate(Xp):
            Z[i,j] = self.objective([[Xp[i,j], Yp[i,j]]])
        
        plt.contourf(Xp, Yp, Z, np.linspace(np.min(Z), 100, 40), cmap=matplotlib.cm.get_cmap(self.cmap))
        plt.colorbar()
        plt.xlabel("X")
        plt.ylabel("Y")
        for point in self.bound.points:
            plt.scatter(point[0], point[1], marker=".", s=80, color="purple")
        for node in self.nodes:
            plt.scatter(node[0], node[1], marker="*", s=80, color="red")
        return plt