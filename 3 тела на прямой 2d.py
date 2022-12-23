import matplotlib.pyplot as plt
import numpy as np

# параметры системы тел
m1 = 100
x1 = 10
v1 = 0
m2 = 100
x2 = 20
v2 = 0
m3 = 100
x3 = 0
v3 = 0
G = 1

# параметры симуляции
t0 = 0
t1 = 100
kt = 100000
dt = (t1 - t0) / kt

# данные по каждому телу в виде массива типа [координата, ускорение, скорость]
a1 = G * (m2 * ((x2 - x1) / (abs(x2 - x1) ** 3)) + m3 * ((x3 - x1) / (abs(x3 - x1) ** 3)))
data1 = [[x1, a1, v1]]

a2 = G * (m1 * ((x1 - x2) / (abs(x1 - x2) ** 3)) + m3 * ((x3 - x2) / (abs(x3 - x2) ** 3)))
data2 = [[x2, a2, v2]]

a3 = G * (m2 * ((x2 - x3) / (abs(x2 - x3) ** 3)) + m1 * ((x1 - x3) / (abs(x1 - x3) ** 3)))
data3 = [[x3, a3, v3]]
for i in range(1, kt):
    x1 = data1[i - 1][0] + data1[i - 1][2] * dt + (data1[i - 1][1] * (dt ** 2)) / 2
    x2 = data2[i - 1][0] + data2[i - 1][2] * dt + (data2[i - 1][1] * (dt ** 2)) / 2
    x3 = data3[i - 1][0] + data3[i - 1][2] * dt + (data3[i - 1][1] * (dt ** 2)) / 2
    
    v1 = data1[i - 1][2] + data1[i - 1][1] * dt
    v2 = data2[i - 1][2] + data2[i - 1][1] * dt
    v3 = data3[i - 1][2] + data3[i - 1][1] * dt
    
    a1 = G * (m2 * ((x2 - x1) / (abs(x2 - x1) ** 3)) + m3 * ((x3 - x1) / (abs(x3 - x1) ** 3)))
    a2 = G * (m1 * ((x1 - x2) / (abs(x1 - x2) ** 3)) + m3 * ((x3 - x2) / (abs(x3 - x2) ** 3)))
    a3 = G * (m2 * ((x2 - x3) / (abs(x2 - x3) ** 3)) + m1 * ((x1 - x3) / (abs(x1 - x3) ** 3)))
    
    data1 += [[x1, a1, v1]]
    data2 += [[x2, a2, v2]]
    data3 += [[x3, a3, v3]]

# координаты каждого тела
pos1 = []
pos2 = []
pos3 = []
for i in range(kt):
    pos1.append(data1[i][0])
    pos2.append(data2[i][0])
    pos3.append(data3[i][0])
t = np.arange(t0, t1, dt)


fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
plt.title("Задача 3 тел на прямой")
plt.xlabel('Время', fontsize=12)
plt.ylabel('Координата', fontsize=12)
plt.plot(t, pos1, 'b')
plt.plot(t, pos2, 'r')
plt.plot(t, pos3, 'g')
ax.set_ylim(min(min(pos1), min(pos2), min(pos3)), max(max(pos1), max(pos2), max(pos3)))
ax.set_xlim(t0, t1)

plt.show()

























