from decimal import Decimal

# Резульаты вычисления
res = []
# Обороты двигателя об/мин
n = (300, 600, 750, 960, 1000, 1450, 1500, 3000)
# Эффективная подача
Qef = 12
# Количество цилиндров
z = (5, 7, 9)
# Объемный КПД
nob = 0.96
# Начальное значение s
s = Decimal(1)
# Все значения s
I = []
while s < 1.51:
    I.append(float(s))
    s += Decimal(0.01)
# Теоретическая подача
Qt = Qef / nob
for oborots in n:
    for cylinders in z:
        for k in I:
            q = Qt / (60 * oborots)
            d = ((4 * q) / (3.1415 * cylinders * k))**(1/3)
            if d > 0.025:
                d2 = 0.028
            elif d > 0.022:
                d2 = 0.025
            elif d > 0.020:
                d2 = 0.022
            elif d > 0.018:
                d2 = 0.020
            elif d > 0.016:
                d2 = 0.018

            h = k * d2
            if h > 0.032:
                h2 = 0.04
            elif h > 0.025:
                h2 = 0.032
            else:
                h2 = 0.025
            e = h2 / 2
            q22 = 3.1415 * d2**2 * h2 * cylinders / 4
            qC = q22 / cylinders
            res.append([abs((1 - q / q22) * 100), oborots, cylinders, k, d, d2, h, h2])
for r in res:
    if r[0] < 3:
        print("n = {}\nz = {}\nI = {}\nd = {}\nd2 = {}\nh = {}\nh2 = {}\n% = {}\n".format(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[0]))
        
