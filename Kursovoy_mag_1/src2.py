import math
import matplotlib.pyplot as plt



def obem(pfi):
	v = omega * (Sh/2) * math.sin(pfi)
	dV = A*dt*v
	return dV


def dM_delta_const(isPump):
	if isPump:
		return p2 - p1
	else:
		return p1 - p2


# зазор со стороны компрессорной полости
delta_1 = 50*10**(-6)
# зазор со стороны насосной полости
delta_2 = 70*10**(-6)
delta_1_in_3 = delta_1**3
delta_2_in_3 = delta_2**3
pn_nasosa = 0.4 * 10**6
pvs_nasosa = 100000
pn_kompressora = 0.4 * 10**6
pvs_kompressora = 100000
dpn_kompressora = 0
dpvs_kompressora = 0
dpn_nasosa = 0
dpvs_nasosa = 0

rho = 1000
muw =  8.90*10**(-4)

n = 1000
T = (1/n*60)
omega = math.pi*n/30

k = 1.4
a = 0

Sh = 0.045
dc = 0.04


l1_0 = Sh
l2_0 = Sh
lyambda = 0.25

# площади полости
A = math.pi * dc * dc / 4
full_pfi = 360
# метод расчета
dpfi = 0.5
number_of_iterations = full_pfi//dpfi
dt = T / number_of_iterations

# рабочий объем полости
Vh = A*Sh
Vm = Vh*0.05
V0 = Vh + Vm
Vnasosa_i = 0
Vkompressora_i = 0

M1 = 0
M2 = 0

M10 = 0
M20 = 0


davlenie_nasosa = []
davlenie_kompressora = []
obem_nasosa = []
obem_kompressora = []
pfi_i = 0
pfi_i_k = []
pfi_i_n = []
list_pfi_i = []
list_l1 = []
list_l2 = []
list_lp = []
while pfi_i<= full_pfi:
	# угол поворота в радианах
	pfi_i_rad = (pfi_i)*math.pi/180
	pfi_i_kompressora = (pfi_i)*math.pi/180
	pfi_i_nasosa = (pfi_i + 180)*math.pi/180
	list_pfi_i.append(pfi_i)
	# нагнетание жидкости в насосе, всасывание газа в компрессоре
	if 0 <= pfi_i < 180:
		pump = True
		# процесс нагнетания жидкости
		p2 = pn_nasosa + dpn_nasosa
		davlenie_nasosa.append(p2)
		# процесс всасывания газа
		p1 = pvs_kompressora + dpvs_kompressora
		davlenie_kompressora.append(p1)
		# комп секция
		
		l1 = l1_0 + (Sh/2)*((1-math.cos(pfi_i_rad)) + (lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		# насосная секция
		l2 = Sh - l1
		l2 = l2_0 - (Sh/2)*((1-math.cos(pfi_i_rad)) + (lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		
		if l1==0.0:
			l1=0.00001
		if l2==0.0:
			l2=0.00001
		# давление в щели
		p3 = (((delta_1_in_3/l1)*p1) + ((delta_2_in_3/l2)*p2))/((delta_1_in_3/l1)+(delta_2_in_3/l2))
		# масса жидкости из насоса в компрессор при ступенчатой щели
		M2 += ((p2 - p3)/l2)
		M20 += dM_delta_const(pump)

	# всасывание жидкости в насосе, нагнетание или сжатие газа в компрессоре
	else:
		pump = False
		# давление в насосе
		p2 = pvs_nasosa + dpn_nasosa
		davlenie_nasosa.append(p2)
		# давление в компрессоре
		V1 = (Vh/2)*((1-math.cos(pfi_i_kompressora)) + (lyambda/4)*(1-math.cos(2*pfi_i_kompressora))) + Vm
		p1 = pvs_kompressora * ((V0/V1)**k)
		# если происходит нагнетание
		if p1 >= pn_kompressora:	
			p1 = pn_kompressora + dpn_kompressora
		davlenie_kompressora.append(p1)	
		# комп секция
		
		l1 = l1_0 + (Sh/2)*((1-math.cos(pfi_i_rad)) + (lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		# насосная секция
		l2 = Sh - l1
		l2 = l2_0 - (Sh/2)*((1-math.cos(pfi_i_rad)) + (lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		
		if l1==0.0:
			l1=0.00001
		if l2==0.0:
			l2=0.00001
		p3 = (((delta_1_in_3/l1)*p1) + ((delta_2_in_3/l2)*p2))/((delta_1_in_3/l1)+(delta_2_in_3/l2))
		# масса жидкости из компрессора в насос
		M1 += ((p1 - p3)/l1)
		M10 += dM_delta_const(pump)
		

	'''if pfi_i<2:
		print(pfi_i)
		print(l1)
		print(l2)
		print()'''
		
	list_l1.append(l1)
	list_l2.append(l2)
	list_lp.append(l1+l2)
	Vnasosa_i += obem(pfi_i_nasosa)
	Vkompressora_i += obem(pfi_i_kompressora)
	obem_nasosa.append(Vnasosa_i)
	obem_kompressora.append(Vkompressora_i)
	pfi_i += dpfi
M1 *= rho * ((math.pi * dc * delta_1_in_3)/(12*muw*omega))
M2 *= rho * ((math.pi * dc * delta_2_in_3)/(12*muw*omega))

f1 = M20/M10
f2 = M2/M1
f3 = f2/f1

#print("M20 = ", M20, "M10 = ", M10)
print("f1 = M20/M10 =", f1)
print("M2 = ", str(M2)+",", "M1 = ", M1)
print("f2 = M2/M1 = ", f2)

print("f3 = f2/f1 = ", f3)



davlenie_nasosa.append(pn_nasosa)
davlenie_kompressora.append(pvs_kompressora)
obem_nasosa.append(obem_nasosa[-1])
obem_kompressora.append(obem_kompressora[0])


y1 = davlenie_nasosa
y2 = davlenie_kompressora
x1 = obem_nasosa
x2 = obem_kompressora



plt.figure(figsize=(7, 7))
plt.subplot(2, 1, 1)
plt.plot(x1, y1, linewidth=3.3)               # построение графика
#plt.title("Зависимости давления от объема") # заголовок
plt.xlabel("Объем камеры насоса, м3", fontsize=14)
plt.ylabel("давление P2(насоса), Па", fontsize=14) # ось ординат
plt.grid(True)                # включение отображение сетки
plt.subplot(2, 1, 2)
plt.plot(x2, y2, linewidth=3.3)               # построение графика
plt.xlabel("Объем камеры компрессора, м3", fontsize=14)  # ось абсцисс
plt.ylabel("Давление P1(компрессора), Па", fontsize=14) # ось ординат
plt.grid(True)
plt.subplots_adjust(wspace=0, hspace=0.5)
plt.show()

y1.pop()
y2.pop()
plt.plot(list_pfi_i, y1, label='P2', linewidth=3.3)
plt.plot(list_pfi_i, y2, '--', label='P1', linewidth=3.3)
plt.legend()
plt.xlabel("угол поворота вала, градусы", fontsize=14)
plt.ylabel("Давления P1 и P2, Па", fontsize=14)
plt.grid(True)
plt.show()


plt.plot(list_pfi_i, list_l2)
plt.plot(list_pfi_i, list_l1)
plt.plot(list_pfi_i,list_lp)
plt.show()
