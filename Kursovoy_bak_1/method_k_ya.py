


class Yacheyka:
	def __init__(self, number, speed, pressure, rho, temp):
		self.number = number
		
		self.Wi_n = speed
		self.Wi_plus_05_n = speed
		self.Wi_minus_05_n = speed

		self.Wi_n_vector = speed
		self.Wi_plus_05_n_vector = speed
		self.Wi_minus_05_n_vector = speed

		self.Pi_n = pressure
		self.Pi_plus_05_n = pressure
		self.Pi_minus_05_n = pressure

		self.ei_n = 0
		self.dMi_plus_05_n = 0
		self.dMi_minus_05_n = 0
		self.rhoi_n = rho
		self.Ti_n = temp

	def change_speed(self, new_speed):
		self.Wi_n_vector = new_speed

	def change_Wi_plus_05_n(self, new_Wi_plus_05_n):
		self.Wi_plus_05_n_vector = new_Wi_plus_05_n

	def change_Wi_minus_05_n(self, new_Wi_minus_05_n):
		self.Wi_minus_05_n_vector = new_Wi_minus_05_n

	def change_pressure(self, new_pressure):
		self.Pi_n = new_pressure

	def change_Pi_plus_05_n(self, new_Pi_plus_05_n):
		self.Pi_plus_05_n = new_Pi_plus_05_n

	def change_Pi_minus_05_n(self, new_Pi_minus_05_n):
		self.Pi_minus_05_n = new_Pi_minus_05_n

	def change_energy(self, new_energy):
		self.ei_n = new_energy

	def change_dMi_plus_05_n(self, new_dM):
		self.dMi_plus_05_n = new_dM

	def change_dMi_minus_05_n(self, new_dM):
		self.dMi_minus_05_n = new_dM

	def change_density(self, new_density):
		self.rhoi_n = new_density