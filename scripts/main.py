from scripts.Node import Node
import numpy as np


#========= Только для 2у мерного пространства =========#
###   Инициализация ?объекта?    ###

with open('init_data.txt') as f:
    dims = np.array(f.readline().split(), dtype=int)
    print(dims)

# Можно написать свой класс
Body = [[Node() for i in range(dims[1])] for j in range(dims[0])]
print(Body)
print(Body[0][0].sigma)

# Здесь должно задаваться начальное напряжение
