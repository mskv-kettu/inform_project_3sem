import numpy as np
from scripts.Node import Node


class Body:
    def __init__(self, initdata, hx, hy, hz):
        with open(initdata) as f:  # Считывание размера сетки из файла
            dims = np.array(f.readline().split(), dtype=int)
        self.mp = np.array([[[Node() for i in range(dims[2])] for j in range(dims[1])] for k in range(dims[0])])  # Трёхмерная Сетка
        self.M, self.N, self.K = np.shape(self.mp)[2], np.shape(self.mp)[1], np.shape(self.mp)[0]  # Размеры сетки
        self.h = np.array([hx, hy, hz], dtype=[('x', int), ('y', int), ('z', int)])  # Размеры ячеек

    def Velocity(self, PrevStep, dt):  # Функция вычисления скоростей, передаём в неё карту на предыдущей итерации
        for k in range(1, self.K - 1):  # Только внутренние точки
            for j in range(1, self.N - 1):
                for i in range(1, self.M - 1):
                    # Вычисляем новое значение Vx
                    self.mp[k, j, i].V['x'] += dt / self.mp[k, j, i].rho * \
                            ((PrevStep[k, j, i + 1].sigma['xx'] - PrevStep[k, j, i - 1].sigma['xx']) / (2 * self.h['x']) +
                            (PrevStep[k, j + 1, i].sigma['xy'] - PrevStep[k, j - 1, i].sigma['xy']) / (2 * self.h['y']) +
                            (PrevStep[k + 1, j, i].sigma['xz'] - PrevStep[k - 1, j, i].sigma['xz']) / (2 * self.h['z']))
                    # Вычисляем новое значение Vy
                    self.mp[k, j, i].V['y'] += dt / self.mp[k, j, i].rho * \
                            ((PrevStep[k, j, i + 1].sigma['xy'] - PrevStep[k, j, i - 1].sigma['xy']) / (2 * self.h['x']) +
                            (PrevStep[k, j + 1, i].sigma['yy'] - PrevStep[k, j - 1, i].sigma['yy']) / (2 * self.h['y']) +
                            (PrevStep[k + 1, j, i].sigma['zy'] - PrevStep[k - 1, j, i].sigma['zy']) / (2 * self.h['z']))
                    # Вычисляем новое значение Vz
                    self.mp[k, j, i].V['z'] += dt / self.mp[k, j, i].rho * \
                            ((PrevStep[k, j, i + 1].sigma['xz'] - PrevStep[k, j, i - 1].sigma['xz']) / (2 * self.h['x']) +
                            (PrevStep[k, j + 1, i].sigma['yz'] - PrevStep[k, j - 1, i].sigma['yz']) / (2 * self.h['y']) +
                            (PrevStep[k + 1, j, i].sigma['zz'] - PrevStep[k - 1, j, i].sigma['zz']) / (2 * self.h['z']))

    def Tension(self, PrevStep, dt):  # Функция вычисления напряжений, передаём в неё карту на предыдущей итерации
        for k in range(self.K - 1):  # Только внутренние точки
            for j in range(self.N - 1):
                for i in range(self.M - 1):
                    # Вычисляем новое значение напряжения xx
                    self.mp[k, j, i].sigma['xx'] += dt * ((self.mp[k, j, i].lmd + 2 * self.mp[k, j, i].mu) *
                        (PrevStep[k, j, i + 1].V['x'] - PrevStep[k, j, i - 1].V['x']) / (2 * self.h['x']) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j + 1, i].V['y'] - PrevStep[k, j - 1, i].V['y']) / (2 * self.h['y']) +
                        self.mp[k, j, i].lmd * (PrevStep[k + 1, j, i].V['z'] - PrevStep[k - 1, j, i].V['z']) / (2 * self.h['z']))
                    # Вычисляем новое значение напряжения yy
                    self.mp[k, j, i].sigma['yy'] += dt * ((self.mp[k, j, i].lmd + 2 * self.mp[k, j, i].mu) *
                        (PrevStep[k, j + 1, i].V['y'] - PrevStep[k, j - 1, i].V['y']) / (2 * self.h['y']) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j, i + 1].V['x'] - PrevStep[k, j, i - 1].V['x']) / (2 * self.h['x']) +
                        self.mp[k, j, i].lmd * (PrevStep[k + 1, j, i].V['z'] - PrevStep[k - 1, j, i].V['z']) / (2 * self.h['z']))
                    # Вычисляем новое значение напряжения yy
                    self.mp[k, j, i].sigma['zz'] += dt * ((self.mp[k, j, i].lmd + 2 * self.mp[k, j, i].mu) *
                        (PrevStep[k + 1, j, i].V['z'] - PrevStep[k - 1, j, i].V['z']) / (2 * self.h['z']) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j + 1, i].V['y'] - PrevStep[k, j - 1, i].V['y']) / (2 * self.h['y']) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j, i + 1].V['z'] - PrevStep[k, j, i - 1].V['x']) / (2 * self.h['x']))
                    # Вычисляем новое значение напряжения xy
                    self.mp[k, j, i].sigma['xy'] += dt * ((PrevStep[k, j, i + 1].V['y'] - PrevStep[k, j, i - 1].V['y']) / (2 * self.h['x'])
                                                          + (PrevStep[k, j + 1, i].V['x'] - PrevStep[k, j - 1, i].V['x']) / (2 * self.h['y'])) * \
                                                    self.mp[k, j, i].mu
                    # Вычисляем новое значение напряжения xz
                    self.mp[k, j, i].sigma['xz'] += dt * ((PrevStep[k, j, i + 1].V['z'] - PrevStep[k, j, i - 1].V['z']) / (2 * self.h['x'])
                                                          + (PrevStep[k + 1, j, i].V['x'] - PrevStep[k - 1, j, i].V['x']) / (2 * self.h['z'])) * \
                                                    self.mp[k, j, i].mu

                    # Вычисляем новое значение напряжения yz
                    self.mp[k, j, i].sigma['yz'] += dt * ((PrevStep[k + 1, j, i].V['y'] - PrevStep[k - 1, j, i].V['y']) / (2 * self.h['z'])
                                                          + (PrevStep[k, j + 1, i].V['z'] - PrevStep[k, j - 1, i].V['z']) / (2 * self.h['y'])) * \
                                                    self.mp[k, j, i].mu

