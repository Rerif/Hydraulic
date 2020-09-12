


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


	def change_speed(self, new_speed):
		self.W = new_speed

	def change_pressure(self, new_pressure):
		self.P = new_pressure


