import math
def speed(ksi, T):
    """ Speed search function."""
    v=0.1
    v2=0
    mu = (0.0179)/(1+0.0368*T+0.000221*T*T)
    while abs(v-v2)/v>=0.01:
        v = (v+v2)/2
        Re = v*d*p/mu
        if Re<2320:
            lyam = 64/Re
        elif 3000<=Re<20*d/k:
            lyam = 0.3164/(Re**0.25)
        elif 20*k/d<=Re<=500*k/d:
            lyam = 0.11*(((k/d)+(68/Re))**0.25)
        else:
            lyam = 0.11*((k/d)**0.25)
        v2 = math.sqrt((2*(abs(P1-P2)))/(p*(lyam*l/d+ksi)))
    return v

# Enumeration of constants.

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
p = 1000
te = 0.5
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
dt = te/10000
M1 = 0
M2 = 0
# Main cycle.                            
while t<=te:                                 
    P1 = P01*math.cos(w1*t)+P0
    T1 = T01*math.cos(w1*t)+T0
    P2 = P02*math.cos(w2*t)+P0
    T2 = T02*math.cos(w2*t)+T0
    if P1>P2:
        v = speed(ksi1, T1)
        #  First mass calculation.                                          
        dM1 = math.pi*d*d*v*dt*p/4                           
        M1 = M1+dM1
    else:                                                  
        v = speed(ksi2, T2)
        # Second mass calculation.
        dM2 = math.pi*d*d*v*dt*p/4
        M2 = M2+dM2
    t = t + dt
# Output of the results.
print('Общее время процесса:','{0:.1}'.format(t), 'c')     
print('Из левого бака перетекло:','{0:.6}'.format(M1), 'кг')
print('Из правого бака перетекло:','{0:.6}'.format(M2), 'кг')
if M1>M2:
    print('Жидкость течет из левого бака в правый')
else:
    print('Жидкость течет из правого бака в левый')
print('Всего перетекло:', '{0:.5}'.format(abs(M1-M2)), 'кг')
