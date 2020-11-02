


class Yacheyka:
	def __init__(self, number, speed, pressure, rho, temp):
		self.number = number
		
		self.Wi_n = speed
		self.Wi_plus_05_n = speed
		self.Wi_minus_05_n = speed

		self.Wi_n_vec = speed
		self.Wi_plus_05_n_vec = speed
		self.Wi_minus_05_n_vec = speed

		self.Pi_n = pressure
		self.Pi_plus_05_n = pressure
		self.Pi_minus_05_n = pressure

		self.Mi_n = 1

		self.Ei_n = 0
		self.Ei_n_vec = 0
		self.dMi_plus_05_n = 0
		self.dMi_minus_05_n = 0
		self.rhoi_n = rho
		self.Ti_n = temp

	


