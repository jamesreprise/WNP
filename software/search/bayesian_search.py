# Bayesian Search for 2D space optimisation problems.
#
# See the Bayesian Optimisation section in the document for more details.

import math
import random
import lhsmdu
import warnings
import numpy as np
from scipy.stats import norm
from scipy.special import erf
from sklearn.gaussian_process import GaussianProcessRegressor
from search.sa_for_bayes import SABayes
from search.search import Search

class BayesianSearch(Search):
    def __init__(self, function, bound):
        super().__init__(function, bound)
        self.name = "Bayesian Search"

    def search(self):
        samples = []
        results = []
        # Latin hypercube sampling.
        lhs = lhsmdu.sample(self.bound.iterations // 4, self.bound.node_count * 2)
        # LHS gives us values between 0 and 1, so we adjust these for our upper bounds.
        lhs[::2] *= self.bound.area[1][0]
        lhs[1::2] *= self.bound.area[1][1]
        for s in lhs:
            result = self.objective(s.reshape(self.bound.node_count, 2).tolist())
            samples.append(s.tolist()[0])
            results.append(result)

        gpr = GaussianProcessRegressor()
        # Fit the GPR for our initial samples.
        gpr.fit(samples, results)

        for _ in range(self.bound.iterations - (self.bound.iterations // 4)):
            # We optimise our next query point using the surrogate function.
            prediction = self.predict(results, gpr)
            result = self.objective(prediction)

            samples.append(np.array(prediction).flatten())
            results.append(result)
            
            # Then re-fit our GPR to update our values.
            gpr.fit(samples, results)
            
        # Return the best result.
        i = np.argmin(results)
        return (np.array(samples[i]).reshape(self.bound.node_count, 2), results[i])
    
    def predict(self, results, gpr):
        """
        We use our expected improvement function to find the best next query point, using gpr.predict() to access the surrogate function.
        """
        def expected_improvement(X):
            # Expected improvement function adapted from https://bitbucket.org/arahat/gecco-2017/src/master/ in IscaOpt/surrogate.py
            X = np.array(X).reshape(1, -1)
            y, std_dev = gpr.predict(X, return_std=True)
            if std_dev != 0:
                best = -1 * np.max(-1 * np.array(results))
                s = -1 * (y - best) / std_dev
                # https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.erf.html
                # The cumulative of the unit normal distribution is given by Phi(z) = 1/2[1 + erf(z/sqrt(2))].
                norm_cdf = (0.5 * erf(s / np.sqrt(2.0))) + 0.5 
                # normal probability density function
                norm_pdf = 1 / np.sqrt(2.0 * np.pi) * np.exp(-s**2 / 2.0) 
                ei =  std_dev * ((s * norm_cdf) + (norm_pdf)) 
                return ei
            else:
                return -math.inf
        # We use a special simulated annealing algorithm designed for optimising the surrogate function.
        sa = SABayes(expected_improvement, self.bound)
        result = sa.search()
        return result[0]