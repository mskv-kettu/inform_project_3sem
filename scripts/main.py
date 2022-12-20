from scripts.Body import Body
from scripts.visualization import init_visualize
import copy
import sys
from PIL import Image

c = 3500  # Примерная скорость звука в меди в метрах на секунду
A, B, C = 1, 1, 1  # Длина, ширина, высота образца в метрах
N = 50  # Количество итераций

# Сетка
Body = Body('init_data.txt', 'material_data.txt', A, B, C)

dt = 0.5 * Body.h[0] / c  # Шаг по времени в секундах
omega = c / Body.h[0] * 0.5  # Частота гармонического напряжения
Ampl = 10000  # Амлитуда гармонического напряжения в ньютонах на метр
V = 1e-3  # Константа скорости для отрисовки в зависимости от модуля

for i in range(N):
    PrevStep = copy.deepcopy(Body.mp)
    print(Body.mp[1, 1, 1].V[0], Body.mp[1, 1, 1].V[1], Body.mp[1, 1, 1].V[2])
    Body.GarmonicBorderTension(Ampl, omega, i * dt)
    Body.Velocity(PrevStep, dt)
    Body.Tension(PrevStep, dt)
    # Сохраняем кадры для дальнейшей визуализации
    filename = r'C:\Users\vladi\Documents\PyCharmProjects\Python-3term\3term_Project\images\step%d.png' % i
    init_visualize(sys.argv, Body.dims, Body, filename, V)

# Создание гифки
frames = []
for n in range(N):
    frame = Image.open(r'C:\Users\vladi\Documents\PyCharmProjects\Python-3term\3term_Project\images\step%d.png' % n)
    frames.append(frame)

frames[0].save(
    r'C:\Users\vladi\Documents\PyCharmProjects\Python-3term\3term_Project\result.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=200,
    loop=1
)