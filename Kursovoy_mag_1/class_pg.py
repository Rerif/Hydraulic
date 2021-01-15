import math
import matplotlib.pyplot as plt

class Pgemod():
	def __init__(self, delta_1, delta_2, pn_n, pn_k, \
		pvs_n=100000, pvs_k=100000, dpn_k=0, dpvs_k=0, dpn_n=0, dpvs_n=0,\
		n=1000):
		'''Создание объекта по требуемым данным'''
		self.delta_1 = delta_1
		self.delta_2 = delta_2

		# зазор со стороны компрессорной полости
		#delta_1 = delta_1
		# зазор со стороны насосной полости
		#delta_2 = delta_2
		self.delta_1_in_3 = delta_1**3
		self.delta_2_in_3 = delta_2**3
		self.pn_nasosa = pn_n
		self.pvs_nasosa = pvs_n
		self.pn_kompressora = pn_k
		self.pvs_kompressora = pvs_k
		self.dpn_kompressora = dpn_k
		self.dpvs_kompressora = dpvs_k
		self.dpn_nasosa = dpn_n
		self.dpvs_nasosa = dpn_n

		self.rho = 1000
		self.muw =  0.001004

		self.n = n
		self.T = (1/self.n*60)
		self.omega = math.pi*self.n/30

		self.k = 1.4

		self.Sh = 0.045
		self.dc = 0.04


		self.l1_0 = self.Sh
		self.l2_0 = self.Sh
		self.lyambda = 0.25
		self.l1_0 = self.Sh
		self.l2_0 = 0
		self.lp = self.Sh
		# площади полости
		self.A = math.pi * self.dc * self.dc / 4
		self.full_pfi = 360
		# метод расчета
		self.dpfi = 0.5
		self.number_of_iterations = self.full_pfi//self.dpfi
		self.dt = self.T / self.number_of_iterations

		# рабочий объем полости
		self.Vh = self.A*self.Sh
		self.Vm = self.Vh*0.05
		self.V0 = self.Vh + self.Vm
		self.l1_0 = self.Sh
		self.l2_0 = 0
		self.M1 = 0
		self.M2 = 0
		# для графиков
		self.list_pfi_i = []
		self.list_M1 = [[]]
		self.list_M2 = [[]]
		self.list_M10 = [[]]
		self.list_M20 = [[]]

		self.list_pump_pressure = []
		self.list_komp_pressure = []
		self.list_komp_obem = []
		self.list_pump_obem = []
		self.V_n = 0
		self.V_k = 0
		self.pfi_i_kompressora = 0
		self.pfi_i_nasosa = 0





	def pump_cycle(self, pfi_i_rad, diag=False):
		'''расчет цикла насосной секции, рассчитывает и возвращает dM
		diag - параметр для построения индикаторной диаграммы'''
		p2 = self.pn_nasosa + self.dpn_nasosa
		p1 = self.pvs_kompressora + self.dpvs_kompressora
		l1 = self.l1_0 - (self.Sh/2)*((1-math.cos(pfi_i_rad)) + (self.lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		l2 = self.l2_0 + (self.Sh/2)*((1-math.cos(pfi_i_rad)) + (self.lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		if l1==0.0:
			l1=0.00001
		if l2==0.0:
			l2=0.00001
		p3 = (((self.delta_1_in_3/l1)*p1) + ((self.delta_2_in_3/l2)*p2))/((self.delta_1_in_3/l1)+(self.delta_2_in_3/l2))

		M2 = (p2 - p3)/(l2)*self.rho * ((math.pi * self.dc * self.delta_2_in_3)/(12*self.muw*self.omega))
		M20 = ((p2-p1)/self.lp)* self.rho * ((math.pi * self.dc * self.delta_1_in_3)/(12*self.muw*self.omega))
		if diag:
			self.list_komp_pressure.append(p1)
			self.list_pump_pressure.append(p2)
			self.V_k += self.d_obem(pfi_i_rad)
			self.V_n += self.d_obem(pfi_i_rad)
			self.list_komp_obem.append(self.V_k)
			self.list_pump_obem.append(self.V_n)
		return M2, M20

	def compressor_cycle(self, pfi_i_rad, diag=False):
		'''расчет цикла компрессорной секции, рассчитывает и возвращает dM
		diag - параметр для построения индикаторной диаграммы'''
		p2 = self.pvs_nasosa + self.dpn_nasosa
		V1 = (self.Vh/2)*((1-math.cos(pfi_i_rad)) + (self.lyambda/4)*(1-math.cos(2*pfi_i_rad))) + self.Vm
		p1 = self.pvs_kompressora * ((self.V0/V1)**self.k)
		if p1 >= self.pn_kompressora:	
			p1 = self.pn_kompressora + self.dpn_kompressora
		l1 = self.l1_0 - (self.Sh/2)*((1-math.cos(pfi_i_rad)) + (self.lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		l2 = self.l2_0 + (self.Sh/2)*((1-math.cos(pfi_i_rad)) + (self.lyambda/4) * (1-math.cos(2*pfi_i_rad)))
		if l1==0.0:
			l1=0.00001
		if l2==0.0:
			l2=0.00001
		p3 = (((self.delta_1_in_3/l1)*p1) + ((self.delta_2_in_3/l2)*p2))/((self.delta_1_in_3/l1)+(self.delta_2_in_3/l2))
		M1 = (p1 - p3)/(l1)*self.rho * ((math.pi * self.dc * self.delta_1_in_3)/(12*self.muw*self.omega))
		M10 = ((p1 - p2)/self.lp) * self.rho * ((math.pi * self.dc * self.delta_1_in_3)/(12*self.muw*self.omega))
		if diag:
			self.list_komp_pressure.append(p1)
			self.list_pump_pressure.append(p2)
			self.V_k += self.d_obem(pfi_i_rad)
			self.V_n += self.d_obem(pfi_i_rad)
			self.list_komp_obem.append(self.V_k)
			self.list_pump_obem.append(self.V_n)
		return M1, M10

	def cycles_mass(self, number_of_cycles=1, diag=False):
		'''Расчет массы по кол-ву заданных циклов, по-умолчанию 1'''
		self.list_pfi_i = []
		self.list_pump_pressure = []
		self.list_komp_pressure = []
		self.list_komp_obem = []
		self.list_pump_obem = []
		self.list_M2 = [[] for i in range(number_of_cycles)]
		self.list_M1 = [[] for i in range(number_of_cycles)]

		self.list_M20 = [[] for i in range(number_of_cycles)]
		self.list_M10 = [[] for i in range(number_of_cycles)]
		self.full_M1 = 0
		self.full_M2 = 0
		self.full_M10 = 0
		self.full_M20 = 0
		for i in range(1, number_of_cycles+1):
			pfi_i = 0
			self.M1 = 0
			self.M2 = 0
			self.M20 = 0
			self.M10 = 0
			while pfi_i< self.full_pfi:
				pfi_i_rad = (pfi_i)*math.pi/180
				self.pfi_i_kompressora = (pfi_i)*math.pi/180
				self.pfi_i_nasosa = (pfi_i + 180)*math.pi/180
				if 0 <= pfi_i < 180:
					dM, dM0 = self.pump_cycle(pfi_i_rad, diag=diag)
					self.M2 += dM
					self.M20 += dM0
					self.list_M2[i-1].append(self.M2)
					self.list_M20[i-1].append(self.M20)
					self.full_M2 += dM
					self.full_M20 += dM0
				else:
					dM, dM0 = self.compressor_cycle(pfi_i_rad, diag=diag)
					self.M1 += dM
					self.M10 += dM0
					self.list_M1[i-1].append(self.M1)
					self.list_M10[i-1].append(self.M10)
					self.full_M1 += dM
					self.full_M10 += dM0
				if self.list_pfi_i == []:
					self.list_pfi_i.append(0)
				else:
					self.list_pfi_i.append(self.list_pfi_i[-1]+self.dpfi)
				pfi_i += self.dpfi
		return self.full_M1, self.full_M2


	def get_functions(self):
		f2 = self.full_M2/self.full_M1
		return f2


	def draw_graphics(self):
		'''Рисует график изменения массы жидкости в комп секции'''
		y = []
		y1 = [0]
		yy = []
		y2 = [0]
		M = 0
		MM = 0
		for i in range(len(self.list_M2)):
			y.append(self.list_M2[i])
			y.append(self.list_M1[i])
		c = 2
		for i in range(0, len(y)):
			M = y1[-1]
			for j in y[i]:
				if c%2==0:
					y1.append(M + j)
				else:
					y1.append(M - j)
			c+=1
		del(y1[0])

		for i in range(len(self.list_M20)):
			yy.append(self.list_M20[i])
			yy.append(self.list_M10[i])
		c = 2
		for i in range(0, len(yy)):
			MM = y2[-1]
			for j in yy[i]:
				if c%2==0:
					y2.append(MM + j)
				else:
					y2.append(MM - j)
			c+=1
		del(y2[0])




		plt.plot(self.list_pfi_i, y1)
		plt.plot(self.list_pfi_i, y2)
		plt.show()

	def draw_indicator_diagram(self):
		'''Построение индикаторной диаграммы данной ПГЭМОД'''
		self.cycles_mass(1, diag=True)
		self.list_komp_pressure.append(self.pvs_kompressora)
		self.list_pump_pressure.append(self.pn_nasosa)

		self.list_komp_obem.append(0)
		self.list_pump_obem.append(0)

		x2 = [i+self.Vm for i in self.list_pump_obem]
		y2 = self.list_pump_pressure

		x1 = [i+self.Vm for i in self.list_komp_obem]
		y1 = self.list_komp_pressure

		
		plt.figure(figsize=(7, 7))
		plt.subplot(2, 1, 1)
		plt.plot(x2, y2, linewidth=3.3)               # построение графика
		#plt.title("Зависимости давления от объема") # заголовок
		plt.xlabel("Объем камеры насоса, м3", fontsize=14)
		plt.ylabel("давление P2(насоса), Па", fontsize=14) # ось ординат

		   # шаг по оси х

		#plt.xticks(xx)
		plt.grid(True)                # включение отображение сетки
		plt.subplot(2, 1, 2)
		plt.plot(x1, y1, linewidth=3.3)               # построение графика
		plt.xlabel("Объем камеры компрессора, м3", fontsize=14)  # ось абсцисс
		plt.ylabel("Давление P1(компрессора), Па", fontsize=14) # ось ординат
		plt.grid(True)
		plt.subplots_adjust(wspace=0, hspace=0.5)
		plt.show()


		
	def d_obem(self, pfi_i):
		v = self.omega * (self.Sh/2) * math.sin(pfi_i)
		dV = self.A*self.dt*v
		return dV