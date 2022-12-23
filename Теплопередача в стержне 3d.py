import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.colors as mcolors
import time

def noizo_1D(x, t):
    u = ((u2 - u1) / l) * x + u1
    for n in range(1, 150):
        u += ((2 / np.pi) / n) * (u0 - u1 + ((-1) ** n) * (u2 - u0)) * (np.e ** (-((np.pi * n * a / l) ** 2) * t)) * (np.sin(np.pi * n * x / l))
    return u


def izo_1D(x, t):
    u = x * 0
    for i in range(len(u[0])):
        u[0][i] = u1
    for i in range(len(u)):
        u[i][0] = u0
    for j in range(1, len(u[0])):
        for i in range(1, len(u) - 1):
            u[i][j] = (a ** 2) * ((u[i + 1][j - 1] - 2 * u[i][j - 1] + u[i - 1][j - 1]) / (dx ** 2)) * dt + u[i][j - 1]
#        u[-1][j] = u[-2][j] # с изоляцией на конце
        u[-1][j] = u2 # без изоляции на конце
    return u

# прараметры стержня
u0 = 20 #Температура стержня
u1 = 100 #Температура на левом конце
u2 = 50 #Температура на правом конце
l = 10 #Длина стержня
a = 0.2 #Коэффициент теплопроводности стержня

# параметры запуска
x0 = 0
x1 = l
dx = 1
t0 = 0
t1 = 1000
dt = 0.01 * (dx / a) ** 2


# создание массивов
kx = (x1 - x0) // dx # это надо подставить сюда (да, руками)
kt = (t1 - t0) // dt #!kx           !kt
x, t = np.mgrid[x0:x1:10j, t0:t1:4000j]

start_time = time.time()
u = izo_1D(x, t)
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.plot_surface(x, t, u, cmap="inferno")
plt.title(label='Численное решение')
plt.xlabel('Координата стержня', fontsize=12)
plt.ylabel('Время', fontsize=12)
ax.set_zlabel('Температура')
ax.set_zlim(min(u0, u1), max(u0, u1))
ax.set_ylim(0, t1)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
u = noizo_1D(x, t)
ax = fig.add_subplot(122, projection='3d')
ax.plot_surface(x, t, u, cmap="inferno")
plt.title(label='Общее решение')
plt.xlabel('Координата стержня', fontsize=12)
plt.ylabel('Время', fontsize=12)
ax.set_zlabel('Температура')
ax.set_zlim(min(u0,u1), max(u0, u1))
ax.set_ylim(0, t1)
print("--- %s seconds ---" % (time.time() - start_time))

plt.show()



