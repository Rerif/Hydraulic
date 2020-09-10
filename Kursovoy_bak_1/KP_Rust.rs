

fn speed (ksi:&f64, temp:&f64, p_1:&f64, p_2:&f64) -> f64 {
	let d:f64 = 0.3;
	let l:f64 = 0.2;
	let k:f64 = 0.001;
	let p:f64 = 1000.0;
	let mut v:f64 = 0.1;
	let mut v2:f64 = 0.0;
	let mu:f64 = (0.0179)/(1.0+0.0368*temp+0.000221*temp*temp);
	let mut lyam:f64;
	let mut re:f64;
	while ((v - v2) / v).abs() >= 0.01 {
			v = (v + v2) / 2.0;
			re = v * d * p / mu;
			if re < 2320.0 {
				lyam = 64.0 / re;
			}
			else if 3000.0 <= re && re <= 20.0 * d * k {
				lyam = 0.3164 / (re).powf(0.25);
			}
			else if 20.0 *k / d <= re && re <= 500.0 * k / d {
				lyam = 0.11 * ((k/d) + (68.0/re)).powf(0.25);
			}
			else {
				lyam = 0.11 * (k/d).powf(0.25);
			};
			v2 = (2.0*(p_1 - p_2).abs() / (p * (lyam*l/d + ksi))).powf(0.5);
		};
	v
}

fn main() {
	let p_0:f64 = 100000.0;
	let t_0:f64 = 273.0;
	let p_01:f64 = 98000.0;
	let p_02:f64 = 50000.0;
	let t_01:f64 = 20.0;
	let t_02:f64 = 80.0;
	let w1:f64 = 70.0;
	let w2:f64 = 100.0;
	let d:f64 = 0.3;
	let d1:f64 = 0.6;
	let d2:f64 = 0.9;
	let p:f64 = 1000.0;
	let te:f64 = 0.5;       
	let dt:f64 = te / 10000.0;
	// Coefficients of local resistance calculation.
	// From left to right.
	let n1 = (d*d)/(d1*d1);
	let eps1 = 0.57+(0.043/(1.1-n1));
	let ksi11 = ((1.0-eps1)/(eps1)).powf(2.0);
	let ksi21 = ((d*d)/(d2*d2)-1.0).powf(2.0);
	// From right to left.
	let n2 = (d*d)/(d2*d2);
	let eps2 = 0.57+(0.043/(1.1-n2));
	let ksi12 = ((1.0-eps2)/eps2).powf(2.0);
	let ksi22 = ((d*d)/(d1*d1)-1.0).powf(2.0);
	// Full resistance.
	let ksi1 = ksi11 + ksi21;
	let ksi2 = ksi12 + ksi22;

	let mut t:f64 = 0.0;
	let mut p_1:f64;
	let mut t_1:f64;
	let mut p_2:f64;
	let mut t_2:f64;
	let mut dm_1:f64;
	let mut dm_2:f64;
	let mut m_1:f64 = 0.0;
	let mut m_2:f64 = 0.0;
	let mut v:f64;

	while t < te {

		p_1 = p_01 * (w1 * t).cos() + p_0;
		t_1 = t_01 * (w1 * t).cos() + t_0;
		p_2 = p_02 * (w2 * t).cos() + p_0;
		t_2 = t_02 * (w2 * t).cos() + t_0;
		if p_1 > p_2 {
			v = speed(&ksi1, &t_1, &p_1, &p_2);
			dm_1 = std::f64::consts::PI * d * d * v * dt * p/4.0;
			m_1 = m_1 + dm_1;
		}
		else {
			v = speed(&ksi2, &t_2, &p_1, &p_2);
			dm_2 = std::f64::consts::PI * d * d * v * dt * p/4.0;
			m_2 = m_2 + dm_2;
		}
		t = t + dt;
	}
	println!("M1 = {:.3}", m_1);
	println!("M2 = {:.3}", m_2);
	println!("dM = {:.3}", (m_1 - m_2).abs());
}

