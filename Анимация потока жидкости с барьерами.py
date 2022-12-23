import numpy, matplotlib.pyplot, matplotlib.animation, PIL

# Параметры симуляции
height = 80				                # экран
width = 200
viscosity = 0.005					# вязкость
u0 = 0.12						# скорость потока
k4to9 = 4.0/9.0					# Веса сетки
k1to9   = 1.0/9.0
k1to36  = 1.0/36.0

# Регулируем поток
n0 = k4to9 * (numpy.ones((height,width)) - 1.5*u0**2)	# центральная клетка сетки
nN = k1to9 * (numpy.ones((height,width)) - 1.5*u0**2)          # остальные клетки по направлениям
nS = k1to9 * (numpy.ones((height,width)) - 1.5*u0**2)
nE = k1to9 * (numpy.ones((height,width)) + 3*u0 + 4.5*u0**2 - 1.5*u0**2)
nW = k1to9 * (numpy.ones((height,width)) - 3*u0 + 4.5*u0**2 - 1.5*u0**2)
nNE = k1to36 * (numpy.ones((height,width)) + 3*u0 + 4.5*u0**2 - 1.5*u0**2)
nSE = k1to36 * (numpy.ones((height,width)) + 3*u0 + 4.5*u0**2 - 1.5*u0**2)
nNW = k1to36 * (numpy.ones((height,width)) - 3*u0 + 4.5*u0**2 - 1.5*u0**2)
nSW = k1to36 * (numpy.ones((height,width)) - 3*u0 + 4.5*u0**2 - 1.5*u0**2)
rho = n0 + nN + nS + nE + nW + nNE + nSE + nNW + nSW		# плотность
ux = (nE + nNE + nSE - nW - nNW - nSW) / rho			# скорости по осям
uy = (nN + nNE + nNW - nS - nSE - nSW) / rho

# Обозначаем барьеры
barrier = numpy.zeros((height,width), bool)
barrier[(height // 2) - 8:(height // 2) + 8, height // 2] = True
barrierN = numpy.roll(barrier,  1, axis=0)
barrierS = numpy.roll(barrier, -1, axis=0)
barrierE = numpy.roll(barrier,  1, axis=1)
barrierW = numpy.roll(barrier, -1, axis=1)
barrierNE = numpy.roll(barrierN,  1, axis=1)
barrierNW = numpy.roll(barrierN, -1, axis=1)
barrierSE = numpy.roll(barrierS,  1, axis=1)
barrierSW = numpy.roll(barrierS, -1, axis=1)


# Продвижение жидкости за шаг
def stream():
	global nN, nS, nE, nW, nNE, nNW, nSE, nSW
	nN  = numpy.roll(nN,   1, axis=0)
	nNE = numpy.roll(nNE,  1, axis=0)
	nNW = numpy.roll(nNW,  1, axis=0)
	nS  = numpy.roll(nS,  -1, axis=0)
	nSE = numpy.roll(nSE, -1, axis=0)
	nSW = numpy.roll(nSW, -1, axis=0)
	nE  = numpy.roll(nE,   1, axis=1)
	nNE = numpy.roll(nNE,  1, axis=1)
	nSE = numpy.roll(nSE,  1, axis=1)
	nW  = numpy.roll(nW,  -1, axis=1)
	nNW = numpy.roll(nNW, -1, axis=1)
	nSW = numpy.roll(nSW, -1, axis=1)
	# Маркеры столкновения с барьерами
	nN[barrierN] = nS[barrier]
	nS[barrierS] = nN[barrier]
	nE[barrierE] = nW[barrier]
	nW[barrierW] = nE[barrier]
	nNE[barrierNE] = nSW[barrier]
	nNW[barrierNW] = nSE[barrier]
	nSE[barrierSE] = nNW[barrier]
	nSW[barrierSW] = nNE[barrier]

	
# Столкновения с барьерами
def collide():
	global rho, ux, uy, n0, nN, nS, nE, nW, nNE, nNW, nSE, nSW
	rho = n0 + nN + nS + nE + nW + nNE + nSE + nNW + nSW
	ux = (nE + nNE + nSE - nW - nNW - nSW) / rho
	uy = (nN + nNE + nNW - nS - nSE - nSW) / rho
	ux2 = ux * ux
	uy2 = uy * uy
	u2 = ux2 + uy2
	omu215 = 1 - 1.5*u2
	uxuy = ux * uy
	omega = 1 / (3*viscosity + 0.5)
	n0 = (1-omega)*n0 + omega * k4to9 * rho * omu215
	nN = (1-omega)*nN + omega * k1to9 * rho * (omu215 + 3*uy + 4.5*uy2)
	nS = (1-omega)*nS + omega * k1to9 * rho * (omu215 - 3*uy + 4.5*uy2)
	nE = (1-omega)*nE + omega * k1to9 * rho * (omu215 + 3*ux + 4.5*ux2)
	nW = (1-omega)*nW + omega * k1to9 * rho * (omu215 - 3*ux + 4.5*ux2)
	nNE = (1-omega)*nNE + omega * k1to36 * rho * (omu215 + 3*(ux+uy) + 4.5*(u2+2*uxuy))
	nNW = (1-omega)*nNW + omega * k1to36 * rho * (omu215 + 3*(-ux+uy) + 4.5*(u2-2*uxuy))
	nSE = (1-omega)*nSE + omega * k1to36 * rho * (omu215 + 3*(ux-uy) + 4.5*(u2-2*uxuy))
	nSW = (1-omega)*nSW + omega * k1to36 * rho * (omu215 + 3*(-ux-uy) + 4.5*(u2+2*uxuy))
	# Краевые условия
	nE[:,0] = k1to9 * (1 + 3*u0 + 4.5*u0**2 - 1.5*u0**2)
	nW[:,0] = k1to9 * (1 - 3*u0 + 4.5*u0**2 - 1.5*u0**2)
	nNE[:,0] = k1to36 * (1 + 3*u0 + 4.5*u0**2 - 1.5*u0**2)
	nSE[:,0] = k1to36 * (1 + 3*u0 + 4.5*u0**2 - 1.5*u0**2)
	nNW[:,0] = k1to36 * (1 - 3*u0 + 4.5*u0**2 - 1.5*u0**2)
	nSW[:,0] = k1to36 * (1 - 3*u0 + 4.5*u0**2 - 1.5*u0**2)


# Вычисление скручивания жидкости по разности скоростей
def curl(ux, uy):
	return numpy.roll(uy,-1,axis=1) - numpy.roll(uy,1,axis=1) - numpy.roll(ux,-1,axis=0) + numpy.roll(ux,1,axis=0)


# Создаем график
theFig = matplotlib.pyplot.figure(figsize=(10,7))
fluidImage = matplotlib.pyplot.imshow(curl(ux, uy), origin='lower', norm=matplotlib.pyplot.Normalize(-0.1, 0.1), 
									cmap=matplotlib.pyplot.get_cmap('jet'), interpolation='none')
# Выделяем барьеры
bImageArray = numpy.zeros((height, width, 4), numpy.uint8)
bImageArray[barrier,3] = 255
barrierImage = matplotlib.pyplot.imshow(bImageArray, origin='lower', interpolation='none')


def nextFrame(frame):					# Тело анимации (аргумент не нужен)
	for step in range(20):
		stream()
		collide()
	fluidImage.set_array(curl(ux, uy))
	return (fluidImage, barrierImage)

animate = matplotlib.animation.FuncAnimation(theFig, nextFrame, interval=0.5, blit=True)
matplotlib.pyplot.show()
# animate.save('Abobus.gif', fps=60)                    # Можно сохранить результат в формате .gif






