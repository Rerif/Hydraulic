import math
from method_k_ya import *


# кол-во ячеек 
cell_count = 100
# кол-во временных отрезков
n = 10
P0 = 100000
T0 = 273
P01 = 98000
P02 = 50000
T01 = 20
T02 = 80
Rg = 8.31
w1 = 70
w2 = 100
d = 0.3
l = 0.2
rhoi = 1000
te = 0.1
# площадь канала
A = math.pi * d * d / 4
# Coefficients of local resistance calculation.
t = 0
dt = te/n
# для второго способа
M1 = 0
M2 = 0
dx = l/cell_count

pole = [Yacheyka(i, 0, (P01+P02)/2, rhoi, (T01+T02)/2) for i in range(cell_count)]

# начальные условия
ei_n = 0
# Main cycle.                            
while t<=te:                                 
	P1 = P01*math.cos(w1*t)+P0
	T1 = T01*math.cos(w1*t)+T0
	P2 = P02*math.cos(w2*t)+P0
	T2 = T02*math.cos(w2*t)+T0
	pole[0].change_pressure(P1)
	pole[cell_count-1].change_pressure(P2)

	# первый этап
	for j in range(cell_count):
		# первый этап
		yacheyka = pole[j]
		# параметры газа относящиеся к границам ячеек
		# Pi_plus_05_n = (Pi_n+Pi_plus_1_n)/2
		Pi_n = yacheyka.Pi_n
		Wi_n = yacheyka.Wi_n
		# граничные условия 1
		if j == 0:
			Pi_minus_1_n = Pi_n
			Wi_minus_1_n = Wi_n
			Pi_plus_1_n = pole[j+1].Pi_n
			Wi_plus_1_n = pole[j+1].Wi_n
			prev_yacheyka = pole[j]

		elif j == cell_count-1:
			Pi_plus_1_n = Pi_n
			Wi_plus_1_n = Wi_n
			Pi_minus_1_n = pole[j-1].Pi_n
			Wi_minus_1_n = pole[j-1].Wi_n
			next_yacheyka = pole[j]

		else:
			prev_yacheyka = pole[j-1]
			next_yacheyka = pole[j+1]
			Pi_plus_1_n = pole[j+1].Pi_n
			Pi_minus_1_n = pole[j-1].Pi_n
			Wi_plus_1_n = pole[j+1].Wi_n
			Wi_minus_1_n = pole[j-1].Wi_n

		Pi_minus_05_n = (Pi_n+Pi_minus_1_n)/2
		Pi_plus_05_n = (Pi_n+Pi_plus_1_n)/2

		Wi_plus_05_n = (Wi_n + Wi_plus_1_n)/2
		Wi_minus_05_n = (Wi_n + Wi_minus_1_n)/2

		# промежуточные значения (значения на первом этапе) скорости и энергии газа
		# на временном слое n+1
		Wi_n_plus_1_vector = Wi_n - ((Pi_plus_05_n-Pi_minus_05_n)/dx)*(dt/rhoi)
		#ei_n_plus_1 = ei_n - ((Pi_plus_05_n*Wi_plus_05_n-Pi_minus_05_n*Wi_minus_05_n)/dx)*(dt/rhoi)

		yacheyka.Wi_n_vector = Wi_n_plus_1_vector
		yacheyka.Wi_plus_05_n = Wi_plus_05_n
		yacheyka.Wi_minus_05_n = Wi_minus_05_n
		yacheyka.Pi_plus_05_n = Pi_plus_05_n
		yacheyka.Pi_minus_05_n = Pi_minus_05_n
		yacheyka.Ti_n = (T1+T2)/2
		#yacheyka.change_energy(ei_n_plus_1)


	# второй этап
	for j in range(cell_count):
		yacheyka = pole[j]
		if j == 0:
			prev_yacheyka = pole[j]

		elif j == cell_count-1:
			next_yacheyka = pole[j]

		else:
			prev_yacheyka = pole[j-1]
			next_yacheyka = pole[j+1]

		Wi_n_plus_1_vector = yacheyka.Wi_n_vector
		Wi_plus_1_n_plus_1_vector = next_yacheyka.Wi_n_vector
		Wi_minus_1_n_plus_1_vector = prev_yacheyka.Wi_n_vector
		
		# потоки массы газа за dt через границы ячейки

		# масса газа прошедшая через правую границу i-ячейки при площади A    
		if Wi_n_plus_1_vector+Wi_plus_1_n_plus_1_vector > 0:
			yacheyka.change_dMi_plus_05_n((yacheyka.rhoi_n*(Wi_n_plus_1_vector+Wi_plus_1_n_plus_1_vector)*A*dt)/2)
		else:
			yacheyka.change_dMi_plus_05_n((yacheyka.rhoi_n*(Wi_n_plus_1_vector+Wi_plus_1_n_plus_1_vector)*A*dt)/2)

		# масса газа проходящая через левую границу i-й ячейки
		if Wi_n_plus_1_vector+Wi_minus_1_n_plus_1_vector > 0:
			yacheyka.change_dMi_minus_05_n((yacheyka.rhoi_n*(Wi_n_plus_1_vector+Wi_plus_1_n_plus_1_vector)*A*dt)/2)
		else:
			yacheyka.change_dMi_minus_05_n((yacheyka.rhoi_n*(Wi_n_plus_1_vector+Wi_minus_1_n_plus_1_vector)*A*dt)/2)
		    
		if j == 0:
			if yacheyka.dMi_minus_05_n < 0:
				M1 += abs(yacheyka.dMi_minus_05_n)
			if t<dt:
				print(yacheyka.dMi_minus_05_n)
		elif j == cell_count-1:
			if yacheyka.dMi_plus_05_n > 0:
				M2 += yacheyka.dMi_plus_05_n

	# третий этап
	for j in range(cell_count):
		yacheyka = pole[j]
		if j == 0:
			prev_yacheyka = pole[j]
		elif j == cell_count - 1:
			next_yacheyka = pole[j]
		else:
			prev_yacheyka = pole[j-1]
			next_yacheyka = pole[j+1]
		
		Wi_n_plus_1_vector = yacheyka.Wi_n_vector
		Wi_plus_1_n_plus_1_vector = next_yacheyka.Wi_n_vector
		
		if Wi_n_plus_1_vector+Wi_plus_1_n_plus_1_vector > 0:
			Wi_plus_05_n_plus_1_vector = Wi_n_plus_1_vector
			#ei_plus_1_n_plus_1_vector = ei_n_plus_1_vector
		else:
			Wi_plus_05_n_plus_1_vector = Wi_plus_1_n_plus_1_vector
			#ei_plus_1_n_plus_1_vector = ei_plus_1_n_plus_1_vector

		yacheyka.Wi_plus_05_n_vector = Wi_plus_05_n_plus_1_vector

		rhoi_n_plus_1 = yacheyka.rhoi_n + (yacheyka.dMi_minus_05_n - yacheyka.dMi_plus_05_n)/(A*dx)
		Wi_n_plus_1 = yacheyka.rhoi_n * yacheyka.Wi_n / rhoi_n_plus_1 + (abs(yacheyka.dMi_minus_05_n)*yacheyka.Wi_minus_05_n_vector - abs(yacheyka.dMi_plus_05_n) * yacheyka.Wi_plus_05_n_vector)/(rhoi_n_plus_1*A*dx)
		#ei_n_plus_1 = yacheyka.rhoi_n * yacheyka.ei_n / rhoi_n_plus_1 + (yacheyka.dMi_minus_05_n * ei_minus_05_n_plus_1 - dMi_plus_05_n * ei_plus_05_n_plus_1)/(rhoi_n_plus_1 * A * dx)
		
		yacheyka.change_density(rhoi_n_plus_1)
		yacheyka.Wi_n = Wi_n_plus_1
		
		yacheyka.Pi_n = yacheyka.rhoi_n*Rg*yacheyka.Ti_n
		rhoi

		

	t+=dt

#for i in range(cell_count):
	#print(pole[i].Pi_n)
	#print(pole[i].Pi_plus_05_n)
	#print(pole[i].Pi_minus_05_n)
	#print(pole[i].Wi_n_vector)
	#print(pole[i].Wi_n)
	#print(pole[i].dMi_plus_05_n)
	#print(pole[i].dMi_minus_05_n)
print(M1, M2)
