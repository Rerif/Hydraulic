import math


delta_1 = 50*10**(-6)
delta_2 = 70*10**(-6)
pn_nasosa = 0.4 * 10**6
pvs_nasosa = 100000
pn_kompressora = 0.4 * 10**6
pvs_kompressora = 100000

n = 1000
rho = 1000
n = 1000
muw =  8.90*10**(-4)
omega = math.pi*n/30
k = 1.4
a = 0
dpn_kompressora = 0

dpvs_kompressora = 0
dpn_nasosa = 0
dpvs_nasosa = 0
Sh = 0.045
dc = 0.04

l1 = Sh
l2 = Sh
lp = Sh
l1_0 = Sh
l2_0 = Sh
lyambda = Sh/(2*l1)

A = math.pi * dc * dc / 4
full_pfi = 360
number_of_iterations = 720
dpfi = full_pfi / number_of_iterations

delta_1_in_3 = delta_1**3
delta_2_in_3 = delta_2**3

Vh = A*Sh
Vm = Vh*0.05
V0 = Vh + Vm

dM1 = 0
dM2 = 0
M1 = 0
M2 = 0


for i in range(number_of_iterations + 1):
	pfi_i = i*dpfi
	pfi_i_kompressora = (pfi_i)*math.pi/180
	pfi_i_nasosa = (pfi_i + 180)*math.pi/180
	# нагнетание жидкости в насосе, всасывание газа в компрессоре
	if pfi_i < 180:
		# процесс нагнетания жидкости
		p2 = pn_nasosa + dpn_nasosa
		# процесс всасывания газа
		p1 = pvs_kompressora + dpvs_kompressora
		# комп секция
		l1 = l1_0 + (Sh/2)*((1-math.cos(pfi_i_kompressora)) + (lyambda/4) * (1-math.cos(2*pfi_i_kompressora)))
		# насосная секция 
		l2 = l2_0 + (Sh/2)*((1-math.cos(pfi_i_nasosa)) + (lyambda/4) * (1-math.cos(2*pfi_i_nasosa)))
		# давление в щели
		p3 = (((delta_1_in_3/l1)*p1) + ((delta_2_in_3/l2)*p2))/((delta_1_in_3/l1)+(delta_2_in_3/l2))
		# масса жидкости из насоса в компрессор
		dM2 = rho * ((math.pi * dc * delta_2_in_3)/(12*muw*omega))*((p2 - p3)/l2)*dpfi
		M2 += dM2
	# всасывание жидкости в насосе, нагнетание или сжатие газа в компрессоре
	else:
		# давление в насосе
		p2 = pvs_nasosa + dpn_nasosa
		# давление в компрессоре
		V1 = (Vh/2)*((1-math.cos(pfi_i)) + (lyambda/4)*(1-math.cos(2*pfi_i))) + Vm
		p1 = pvs_kompressora * (V0/V1)**k
		if p1 >= pn_kompressora:	
			p1 = pn_kompressora + dpn_kompressora	
		# комп секция
		l1 = l1_0 + (Sh/2)*((1-math.cos(pfi_i_kompressora)) + (lyambda/4) * (1-math.cos(2*pfi_i_kompressora)))
		# насосная секция 
		l2 = l2_0 + (Sh/2)*((1-math.cos(pfi_i_nasosa)) + (lyambda/4) * (1-math.cos(2*pfi_i_nasosa)))
		p3 = (((delta_1_in_3/l1)*p1) + ((delta_2_in_3/l2)*p2))/((delta_1_in_3/l1)+(delta_2_in_3/l2))
		# масса жидкости из компрессора в насос
		dM1 = rho * ((math.pi * dc * delta_1_in_3)/(12*muw*omega))*((p1 - p3)/l1)*dpfi
		M1 += dM2


#print(pfi_i, dpfi)
print(M2/M1)
print(M2, M1)

