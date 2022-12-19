import numpy as np


class Node:
    def __init__(self, rh, nu, E):  # Параметры среды считываются из файла
        self.sigma = np.zeros(6, dtype=np.float64)
        self.V = np.zeros(3, dtype=np.float64)
        self.mu = E / (2 * (1 + nu))
        self.rho = rh
        self.lmd = nu * E / ((1 + nu) * (1 - 2 * nu))