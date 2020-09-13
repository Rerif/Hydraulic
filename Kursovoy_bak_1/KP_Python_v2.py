import math
from method_k_ya import *


# кол-во ячеек 
cell_count = 10
# кол-во временных отрезков
n = 100
P0 = 100000
T0 = 273
P01 = 98000
P02 = 50000
T01 = 20
T02 = 80
w1 = 70
w2 = 100
d = 0.3
l = 0.2
k = 0.001
D1 = 0.6
D2 = 0.9 
rho = 1000
te = 0.5
# площадь канала
A = math.pi * d * d / 4
# Coefficients of local resistance calculation.
# From left to right.
n1 = (d**2)/(D1**2)                
eps1 = 0.57+(0.043/(1.1-n1))
ksi11 = ((1-eps1)/(eps1))**2
ksi21 = ((d**2)/(D2**2)-1)**2
# From right to left.
n2 = (d**2)/(D2**2)               
eps2 = 0.57+(0.043/(1.1-n2))
ksi12 = ((1-eps2)/eps2)**2
ksi22 = ((d**2)/(D1**2)-1)**2
# Full resistance.
ksi1 = ksi11+ksi21                 
ksi2 = ksi12+ksi22
# First conditions.                 
t = 0
dt = te/n
# для второго способа
M1 = 0
M2 = 0
M = 0
dM = 0
dx = l/cell_count

pole = [Yacheyka(i, 0, (P01+P02)/2, rho) for i in range(cell_count)]

# начальные условия
ei_n = 0
# Main cycle.                            
while t<=te:                                 
	P1 = P01*math.cos(w1*t)+P0
	#T1 = T01*math.cos(w1*t)+T0
	P2 = P02*math.cos(w2*t)+P0
	#T2 = T02*math.cos(w2*t)+T0
	pole[0].change_pressure(P1)
	pole[cell_count-1].change_pressure(P2)




	



	for j in range(cell_count):
		# первый этап
		yacheyka = pole[j]
		# параметры газа относящиеся к границам ячеек
		# Pi_plus_05_n = (Pi_n+Pi_plus_1_n)/2
		Pi_n = pole[j].P
		Wi_n = pole[j].W
		# граничные условия 1
		if j == 0:
			Pi_minus_1_n = Pi_n
			Wi_minus_1_n = Wi_n
			Pi_plus_1_n = pole[j+1].P
			Wi_plus_1_n = pole[j+1].W
			prev_yacheyka = pole[j]

		elif j == cell_count-1:
			Pi_plus_1_n = Pi_n
			Wi_plus_1_n = Wi_n
			Pi_minus_1_n = pole[j-1].P
			Wi_minus_1_n = pole[j-1].W
			next_yacheyka = pole[j]

		else:
			prev_yacheyka = pole[j-1]
			next_yacheyka = pole[j+1]
			Pi_plus_1_n = pole[j+1].P 
			Pi_minus_1_n = pole[j-1].P
			Wi_plus_1_n = pole[j+1].W
			Wi_minus_1_n = pole[j-1].W

		Pi_minus_05_n = (Pi_n+Pi_minus_1_n)/2
		Pi_plus_05_n = (Pi_n+Pi_plus_1_n)/2

		Wi_plus_05_n = (Wi_n + Wi_plus_1_n)/2
		Wi_minus_05_n = (Wi_n + Wi_minus_1_n)/2

		# промежуточные значения (значения на первом этапе) скорости и энергии газа
		# на временном слое n+1
		Wi_n_plus_1 = Wi_n - ((Pi_plus_05_n-Pi_minus_05_n)/dx)*(dt/rho)
		ei_n_plus_1 = ei_n - ((Pi_plus_05_n*Wi_plus_05_n-Pi_minus_05_n*Wi_minus_05_n)/dx)*(dt/rho)

		yacheyka.change_speed(Wi_plus_1_n)
		yacheyka.change_energy(ei_n_plus_1)
		


	for j in range(cell_count):
		yacheyka = pole[j]
		if j == 0:
			prev_yacheyka = pole[j]

		elif j == cell_count-1:
			next_yacheyka = pole[j]

		else:
			prev_yacheyka = pole[j-1]
			next_yacheyka = pole[j+1]

		Wi_n_plus_1 = yacheyka.W
		Wi_plus_1_n_plus_1 = next_yacheyka.W
		Wi_minus_1_n_plus_1 = prev_yacheyka.W
		# второй этап
		# потоки массы газа за dt через границы ячейки

		# масса газа прошедшая через правую границу i-ячейки при площади A    
		if Wi_n_plus_1+Wi_plus_1_n_plus_1 > 0:
			yacheyka.change_dM_plus((rho*(Wi_n_plus_1+Wi_plus_1_n_plus_1)*A*dt)/2)
		else:
			yacheyka.change_dM_plus((rho*(Wi_n_plus_1+Wi_plus_1_n_plus_1)*A*dt)/2)

		# масса газа проходящая через левую границу i-й ячейки
		if Wi_n_plus_1+Wi_minus_1_n_plus_1 > 0:
			yacheyka.change_dM_minus((rho*(Wi_n_plus_1+Wi_plus_1_n_plus_1)*A*dt)/2)
		else:
			yacheyka.change_dM_minus((rho*(Wi_n_plus_1+Wi_minus_1_n_plus_1)*A*dt)/2)
		    
	

	# третий этап
	for i in range(cell_count-1):	    
		rhoi_n_plus_1 = rhoi + (dMi_minus_05 - dMi_plus_05)/(A*dx)
		Wi_n_plus_1 = rhoi_n * Wi_n / rhoi_n_plus_1 + (abs(dMi_minus_05_n)*Wi_minus_05_n_minus_1 - abs(dMi_plus_05_n) * Wi_plus_05_n_plus_1)/(rhoi_n_plus_1*A*dx)
		ei_n_plus_1 = rhoi_n * ei_n / rhoi_n_plus_1 + (dMi_minus_05_n * ei_minus_05_n_plus_1 - dMi_plus_05_n * ei_plus_05_n_plus_1)/(rhoi_n_plus_1 * A * dx)

		if Wi_n_plus_1+Wi_plus_1_n_plus_1 > 0:
			Wi_plus_05_n_plus_1 = Wi_n_plus_1
			ei_plus_1_n_plus_1 = ei_n_plus_1
		else:
			Wi_plus_05_n_plus_1 = Wi_plus_1_n_plus_1
			ei_plus_1_n_plus_1 = ei_plus_1_n_plus_1




	t+=dt
