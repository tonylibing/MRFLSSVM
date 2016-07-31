# -*- coding: utf-8 -*-
__author__ = 'spacegoing'

from Utils.ReadMat import loadCheckboard
import numpy as np
from pprint import pprint as pp
from linEnvLearn import linEnvLearn

# initialize random number generator
np.random.seed(0)


# Generate checkboard data
def checkboardHelper(H, W):
    cliques = np.zeros([H, W])  # mapping of variables to cliques
    y = np.zeros([H, W])  # ground-truth labels

    # create checkboard data
    _black = True  # indicate _black True or white False
    _cliqueID = 1.0
    for _rowIndx in range(0, H, Options.gridStep):
        for _colIndx in range(0, W, Options.gridStep):
            cliques[_rowIndx:_rowIndx + Options.gridStep,
            _colIndx:_colIndx + Options.gridStep] = _cliqueID
            _cliqueID += 1.0

            y[_rowIndx:_rowIndx + Options.gridStep,
            _colIndx:_colIndx + Options.gridStep] = 0.0 if _black else 1.0
            _black = not _black

        _black = not _black

    return cliques.flatten('F'), y.flatten('F')


class Options:
    K = 10  # number of lower linear functions
    gridStep = 16  # grid size for defining cliques
    maxIters = 100  # maximum learning iterations
    eps = 1.0e-16  # constraint violation threshold
    learningQP = 1  # encoding for learning QP (1, 2, or 3)
    figWnd = 0  # figure for showing results


class Instance:
    W = 128  # image width
    H = 128  # image height
    numCliques = (W / Options.gridStep) ** 2  # number of cliques

    N = W * H  # number of variables

    def __init__(self):
        # flatten arrays
        self.cliques, self.y = checkboardHelper(self.H, self.W)

        # # create noisy observations
        # _eta = [0.1, 0.1]
        # self.unary = np.zeros([self.N, 2])
        # self.unary[:, 1] = 2 * (np.random.rand(self.N, 1).flatten() - 0.5) + \
        #               (_eta[0] * (1 - self.y) - _eta[1] * self.y)
        self.unary = loadCheckboard().astype(np.float64)

        # no pairwise edges
        self.pairwise = np.array([])


# # U+H experiments --------------------------------------------
instance = Instance()
options = Options()
history, y_hat = linEnvLearn(instance, options)

