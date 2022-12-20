from scripts.Body import Body
from scripts.visualization import init_visualize
import copy
import sys
from PIL import Image

c = 3500  # Примерная скорость звука в меди в метрах на секунду
A, B, C = 1, 1, 1  # Длина, ширина, высота образца в метрах
N = 100 # Количество итераций

# Сетка
Body = Body('init_data.txt', 'material_data.txt', A, B, C)

dt = 0.5 * Body.h[0] / c  # Шаг по времени в секундах
omega = c / Body.h[0] * 0.5  # Частота гармонического напряжения
Ampl = 10000  # Амлитуда гармонического напряжения в ньютонах на метр

for i in range(N):
    PrevStep = copy.deepcopy(Body.mp)
    Body.GarmonicBorderTension(Ampl, omega, i * dt)
    Body.Velocity(PrevStep, dt)
    Body.Tension(PrevStep, dt)
    # Сохраняем кадры для дальнейшей визуализации
    filename = f'C:\\Users\\vladi\Documents\\PyCharmProjects\\Python-3term\\3term_Project\\images\\step{i}.png'
    init_visualize(sys.argv, Body.dims, Body, filename)

# Создание гифки
frames = []
for n in range(N):
    frame = Image.open(f'C:\\Users\\vladi\Documents\\PyCharmProjects\\Python-3term\\3term_Project\\images\\step{n}.png')
    frames.append(frame)

frames[0].save(
    'result252525(1).gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=200,
    loop=1
)