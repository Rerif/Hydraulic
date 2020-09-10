import math

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
rho1 = 1000
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
# для второго способа
M1 = 0
M2 = 0
M = 0
dM = 0
dx = l/10

# Main cycle.                            
while t<=te:                                 
    P1 = P01*math.cos(w1*t)+P0
    T1 = T01*math.cos(w1*t)+T0
    P2 = P02*math.cos(w2*t)+P0
    T2 = T02*math.cos(w2*t)+T0
    t+=dt



# начальные условия
u = 0
p = (P01+P02) / 2
T = (T01+T02) / 2
rho = rho1

    # первый этап

    # параметры газа относящиеся к границам ячеек
    Pi_plus_05 = (Pi+Pi_plus_1)/2
    Pi_minus_05 = (Pi+Pi_minus_1)/2
    Wi_plus_05 = (Wi + Wi_plus_1)/2
    Wi_minus_05 = (Wi + Wi_minus_1)/2


    Wi_n_plus_1 = Wi_n - ((Pi_plus_05-Pi_minus_05)/dx)*(dt/rho)
    ei_n_plus_1 = ei_n - ((Pi_plus_05*Wi_plus_05-Pi_minus_05*Wi_minus_05)/dx)*(dt/rho)


    # второй этап
    # потоки массы газа за dt через границы ячейки
    # масса газа прошедшая через правую границу i-ячейки при площади A
    
    if wi_n_plus_1+wi_plus_1_n_plus_1 > 0:
        dMi_plus_05 = (rho*(wi_n_plus_1+wi_plus_1_n_plus_1)*A*dt)/2
    else:
        dMi_plus_05 = (rho*(wi_n_plus_1+wi_plus_1_n_plus_1)*A*dt)/2
    
    # масса газа проходящая через левую границу i-й ячейки
    if wi_n_plus_1+wi_minus_1_n_plus_1 > 0:
        dMi_minus_05 = (rho*(wi_n_plus_1+wi_plus_1_n_plus_1)*A*dt)/2
    else:
        dMi_minus_05 = (rho*(wi_n_plus_1+wi_minus_1_n_plus_1)*A*dt)/2
    
    # третий этап
    
    rhoi_n_plus_1 = rhoi + (dMi_minus_05 - dMi_plus_05)/(A*dx)
    wi_n_plus_1 = rhoi_n * Wi_n / rhoi_n_plus_1 + (abs(dMi_minus_05_n)*Wi_minus_05_n_minus_1 - abs(dMi_plus_05_n) * Wi_plus_05_n_plus_1)/(rhoi_n_plus_1*A*dx)
    ei_n_plus_1 = rhoi_n * ei_n / rhoi_n_plus_1 + (dMi_minus_05_n * ei_minus_05_n_plus_1 - dMi_plus_05_n * ei_plus_05_n_plus_1)/(rhoi_n_plus_1 * A * dx)

    if wi_n_plus_1+wi_plus_1_n_plus_1 > 0:
        wi_plus_05_n_plus_1 = wi_n_plus_1
        ei_plus_1_n_plus_1 = ei_n_plus_1
    else:
        wi_plus_05_n_plus_1 = wi_plus_1_n_plus_1
        ei_plus_1_n_plus_1 = ei_plus_1_n_plus_1





