import math


delta_1 = 50
delta_2 = 70
pnn = 0.4
pnk = 0.4
nob = 1000
a = 0
dpnk = 0
dpvsk = 0
dpnn = 0
dpbsn = 0
Sh = 0.045
dc = 0.04
lyambda = 0.25
l1 = Sh
l2 = Sh
lp = Sh

delta_1_in_3 = delta_1**3
delta_2_in_3 = delta_2**3

#Q1 = (math.pi * dc * delta_1_in_3*(p1-p3)) / (12*muw*l1)
#Q2 = (math.pi * dc * delta_1_in_3*(p3-p2)) / (12*muw*l2)
p1 = pvsk*(Vvs/V1)**k
p3 = ((delta_1_in_3/l1)*p1 + (delta_2_in_3/l2)*p2)/(delta_1_in_3/l1 + delta_2_in_3/l2)
M1 = pw * (math.pi*dc*delta_1_in_3/(12*muw*omega))*integral(p1, p3, l1)

#1.Процесс сжатия

Vvs = Vh + Vmk
V1 = (Vh/2)*((1-math.cos(fi)) + (lyambda_1/4)*(1-math.cos(2*fi)))*Vm
lyambda = Sh/(2*l)
#2.Процесс нагнетания
p1 = pnk + dpnk
#3.Процесс всасывания
p1 = pvsk + dpvsk
l1 = l10 + Sh/2*((1-math.cos(fi))+lyambda_1/4*(1-math.cos(2*fi)))

#Опредлим значение давлений в насосной секции
#1.Процес нагнетания
p2 = pnn + dpnn
#2. Процесс всасывания
p2 = pbsn + dpvsn
l2 = l20 + Sh/2*((1-math.cos(fi))+lyambda_1/4*(1-math.cos(2*fi)))
M1 = pw * (math.pi*dc*delta_2_in_3/(12*muw*omega))*integral(p2, p3, l2)







