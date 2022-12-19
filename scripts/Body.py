import numpy as np
from scripts.Node import Node


class Body:
    def __init__(self, initdata, materialdata, X, Y, Z):  # X, Y, Z -- длина, ширина, высота образца
        with open(initdata) as f:  # Считывание размера сетки из файла
            dims = np.array(f.readline().split(), dtype=int)
        with open(materialdata) as f:  # Считывание модулей среды
            mods = np.array(f.readline().split(), dtype=float)
        self.mp = np.array([[[Node(*mods) for i in range(dims[2])] for j in range(dims[1])] for k in range(dims[0])])  # Трёхмерная Сетка
        self.M, self.N, self.K = np.shape(self.mp)[2], np.shape(self.mp)[1], np.shape(self.mp)[0]  # Размеры сетки
        self.h = np.array([X / self.M, Y / self.N, Z / self.K], dtype=np.float64)  # Размеры ячеек
        self.dims = dims

    def Velocity(self, PrevStep, dt):  # Функция вычисления скоростей, передаём в неё карту на предыдущей итерации
        for k in range(1, self.K - 1):  # Только внутренние точки
            for j in range(1, self.N - 1):
                for i in range(1, self.M - 1):
                    # Вычисляем новое значение Vx
                    self.mp[k, j, i].V[0] += dt / self.mp[k, j, i].rho * \
                            ((PrevStep[k, j, i + 1].sigma[0] - PrevStep[k, j, i - 1].sigma[0]) / (2 * self.h[0]) +
                            (PrevStep[k, j + 1, i].sigma[3] - PrevStep[k, j - 1, i].sigma[3]) / (2 * self.h[1]) +
                            (PrevStep[k + 1, j, i].sigma[4] - PrevStep[k - 1, j, i].sigma[4]) / (2 * self.h[2]))
                    # Вычисляем новое значение Vy
                    self.mp[k, j, i].V[1] += dt / self.mp[k, j, i].rho * \
                            ((PrevStep[k, j, i + 1].sigma[3] - PrevStep[k, j, i - 1].sigma[3]) / (2 * self.h[0]) +
                            (PrevStep[k, j + 1, i].sigma[1] - PrevStep[k, j - 1, i].sigma[1]) / (2 * self.h[1]) +
                            (PrevStep[k + 1, j, i].sigma[5] - PrevStep[k - 1, j, i].sigma[5]) / (2 * self.h[2]))
                    # Вычисляем новое значение Vz
                    self.mp[k, j, i].V[2] += dt / self.mp[k, j, i].rho * \
                            ((PrevStep[k, j, i + 1].sigma[4] - PrevStep[k, j, i - 1].sigma[4]) / (2 * self.h[0]) +
                            (PrevStep[k, j + 1, i].sigma[5] - PrevStep[k, j - 1, i].sigma[5]) / (2 * self.h[1]) +
                            (PrevStep[k + 1, j, i].sigma[2] - PrevStep[k - 1, j, i].sigma[2]) / (2 * self.h[2]))

    def Tension(self, PrevStep, dt):  # Функция вычисления напряжений, передаём в неё карту на предыдущей итерации
        for k in range(1, self.K - 1):  # Только внутренние точки
            for j in range(1, self.N - 1):
                for i in range(1, self.M - 1):
                    # Вычисляем новое значение напряжения xx
                    self.mp[k, j, i].sigma[0] += dt * ((self.mp[k, j, i].lmd + 2 * self.mp[k, j, i].mu) *
                        (PrevStep[k, j, i + 1].V[0] - PrevStep[k, j, i - 1].V[0]) / (2 * self.h[0]) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j + 1, i].V[1] - PrevStep[k, j - 1, i].V[1]) / (2 * self.h[1]) +
                        self.mp[k, j, i].lmd * (PrevStep[k + 1, j, i].V[2] - PrevStep[k - 1, j, i].V[2]) / (2 * self.h[2]))
                    # Вычисляем новое значение напряжения yy
                    self.mp[k, j, i].sigma[1] += dt * ((self.mp[k, j, i].lmd + 2 * self.mp[k, j, i].mu) *
                        (PrevStep[k, j + 1, i].V[1] - PrevStep[k, j - 1, i].V[1]) / (2 * self.h[1]) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j, i + 1].V[0] - PrevStep[k, j, i - 1].V[0]) / (2 * self.h[0]) +
                        self.mp[k, j, i].lmd * (PrevStep[k + 1, j, i].V[2] - PrevStep[k - 1, j, i].V[2]) / (2 * self.h[2]))
                    # Вычисляем новое значение напряжения zz
                    self.mp[k, j, i].sigma[2] += dt * ((self.mp[k, j, i].lmd + 2 * self.mp[k, j, i].mu) *
                        (PrevStep[k + 1, j, i].V[2] - PrevStep[k - 1, j, i].V[2]) / (2 * self.h[2]) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j + 1, i].V[1] - PrevStep[k, j - 1, i].V[1]) / (2 * self.h[1]) +
                        self.mp[k, j, i].lmd * (PrevStep[k, j, i + 1].V[0] - PrevStep[k, j, i - 1].V[0]) / (2 * self.h[0]))
                    # Вычисляем новое значение напряжения xy
                    self.mp[k, j, i].sigma[3] += dt * ((PrevStep[k, j, i + 1].V[1] - PrevStep[k, j, i - 1].V[1]) / (2 * self.h[0])
                                                          + (PrevStep[k, j + 1, i].V[0] - PrevStep[k, j - 1, i].V[0]) / (2 * self.h[1])) * \
                                                    self.mp[k, j, i].mu
                    # Вычисляем новое значение напряжения xz
                    self.mp[k, j, i].sigma[4] += dt * ((PrevStep[k, j, i + 1].V[2] - PrevStep[k, j, i - 1].V[2]) / (2 * self.h[0])
                                                          + (PrevStep[k + 1, j, i].V[0] - PrevStep[k - 1, j, i].V[0]) / (2 * self.h[2])) * \
                                                    self.mp[k, j, i].mu

                    # Вычисляем новое значение напряжения yz
                    self.mp[k, j, i].sigma[5] += dt * ((PrevStep[k + 1, j, i].V[1] - PrevStep[k - 1, j, i].V[1]) / (2 * self.h[2])
                                                          + (PrevStep[k, j + 1, i].V[2] - PrevStep[k, j - 1, i].V[2]) / (2 * self.h[1])) * \
                                                    self.mp[k, j, i].mu

    def GarmonicBorderTension(self, A, omega, t): # Случай изменения напряжений на одной из границ по гармоническому закону
        for j in range(1, self.N - 1):
            for i in range(1, self.M - 1):
                self.mp[0, j, i].sigma[2] = A * np.cos(omega * t)  # Задаём нормальное напряжение на одной грани, ортог oz