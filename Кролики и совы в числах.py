import matplotlib.pyplot as plt

x0 = 10
x1 = 10
y0 = 100

t0 = 0
t1 = 100
kt = 10000


dt = (t1 - t0) / kt
t = [t0 + i * dt for i in range(kt)]
x = [x0, x1]
y = [y0, y0 / (1 - (x[1] / 2 - 1) * dt)]
for i in range(2, kt):
    a = 1 - 2 / dt
    b = 2 * x[i - 1] / dt + 4 / dt - 2
    c = 4 * x[i - 2] / (dt ** 2) - 4 * x[i - 1] / dt
    d = -4 * (x[i - 1] / dt) ** 2

    p = c / a - b ** 2 / (3 * a ** 2)
    q = d / a - b * c / (3 * a ** 2) + 2 * (b / 3 / a) ** 3

    z = abs((-q / 2 + ((q / 2) ** 2 + (p / 3) ** 3) ** 0.5) ** (1 / 3) + (-q / 2 - ((q / 2) ** 2 + (p / 3) ** 3) ** 0.5) ** (1 / 3))

    if z - b / 3 / a > 0:
        x += [z - b / 3 / a]
    else:
        x += [0]
    if y[i - 1] / (1 - dt * (x[i] / 2 - 1)) > 0:
        y += [y[i - 1] / (1 - dt * (x[i] / 2 - 1))]
    else:
        y += [0]


fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, x, label='добыча')
plt.plot(t, y, label='хищник')
plt.xlabel('Время', fontsize=12)
plt.ylabel('Количество', fontsize=12)
plt.title("Система добыча - хищник")
plt.legend()

plt.show()
