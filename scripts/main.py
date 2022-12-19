from scripts.Body import Body
from scripts.visualization import visualize
import copy
import sys

c = 3500  # Примерная скорость звука в меди в метрах на секунду
A, B, C = 1, 1, 1  # Длина, ширина, высота образца в метрах
N = 200  # Количество итераций

# Сетка
Body = Body('init_data.txt', 'material_data.txt', A, B, C)

dt = 0.5 * Body.h[0] / c  # Шаг по времени в секундах
omega = c / Body.h[0] * 0.5  # Частота гармонического напряжения
Ampl = 1000  # Амлитуда гармонического напряжения в ньютонах на метр

for i in range(N):
    PrevStep = copy.deepcopy(Body.mp)
    Body.GarmonicBorderTension(Ampl, omega, i * dt)
    Body.Velocity(PrevStep, dt)
    Body.Tension(PrevStep, dt)
    # Смотрим за значениями в клетках
    visualize(sys.argv, Body.dims, Body)
    print(Body.mp[10, 10, 10].V[0], Body.mp[10, 10, 10].V[1], Body.mp[10, 10, 10].V[2])
    for u in Body.mp[10, 10, 10].sigma:
        print(u, end=' ')
    print()
    for u in Body.mp[11, 10, 10].sigma:
        print(u, end=' ')
    print()