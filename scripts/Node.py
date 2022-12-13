import numpy as np


class Node:
    def __init__(self):
        self.sigma = np.zeros((), dtype=[('xx', np.float64), ('xy', np.float64), ('xz', np.float64),
                                         ('yy', np.float64), ('yz', np.float64), ('zz', np.float64)])
        self.V = np.zeros((), dtype=[('x', np.float64), ('y', np.float64), ('z', np.float64)])
        self.mu = 0.5
        self.rho = 1000
        self.lmd = 0.5