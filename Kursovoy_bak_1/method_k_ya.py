


class Yacheyka:
	def __init__(self, number, speed, pressure, rho):
		self.number = number
		self.W = speed
		self.P = pressure
		self.rho = rho
		self.P_i_plus_05 = pressure
		self.P_i_minus_05 = pressure
		self.W_i_plus_05 = speed
		self.W_i_minus_05 = speed
		self.e = 0
		self.dMi_plus_05 = 0
		self.dMi_minus_05 = 0

	def change_speed(self, new_speed):
		self.W = new_speed

	def change_pressure(self, new_pressure):
		self.P = new_pressure

	def change_energy(self, new_energy):
		self.e = new_energy

	def change_dM_plus(self, new_dM):
		self.dMi_plus_05 = new_dM

	def change_dM_minus(self, new_dM):
		self.dMi_minus_05 = new_dM

