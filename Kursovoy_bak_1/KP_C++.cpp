#include <iostream>
#include <cmath>

using namespace std;

double P0, P01, P02, P1, P2;
double T0, T01, T02, T1, T2;
double w1, w2;
double d, l, k, D1, D2;
double p, te;
double n1, n2, ksi, ksi1, ksi2, ksi11, ksi12, ksi21, ksi22;
double eps1, eps2, M1, M2, dM1, dM2, v, v2, dt, t;
double mu, Re, lyam;

double speed(double ksi, double T);

int main()
{
	P0 = 100000.0;
	T0 = 273.0;
	P01 = 98000.0;
	P02 = 50000.0;
	T01 = 20.0;
	T02 = 80.0;
	w1 = 70.0;
	w2 = 100.0;
	d = 0.3;
	l = 0.2;
	k = 0.001;
	D1 = 0.6;
	D2 = 0.9;
	p = 1000.0;
	te = 0.5;

	n1 = (d*d)/(D1*D1);
	eps1 = 0.57+(0.043/(1.1-n1));
	ksi11 = pow((1-eps1)/eps1, 2);
	ksi21 = pow((((d*d)/(D2*D2))-1),2);
	
	n2 = (d*d)/(D2*D2);
	eps2 = 0.57+(0.043/(1.1-n2));
	ksi12 = pow((1-eps2)/eps2, 2);
	ksi22 = pow((((d*d)/(D1*D1))-1),2);

	ksi1 = ksi11 + ksi21;
	ksi2 = ksi12 + ksi22;

	t = 0.0;
	dt = (te - 0)/10000.0;
	M1 = 0.0;
	M2 = 0.0;
	while (t <= te){
		P1 = P01*cos(w1*t)+P0;
		T1 = T01*cos(w1*t)+T0;
		P2 = P02*cos(w2*t)+P0;
		T2 = T02*cos(w2*t)+T0;
		if (P1 > P2){
			v = speed(ksi1, T1);
			dM1 = M_PI*d*d*v*dt*p/4;
			M1 = M1 + dM1;
		}
		else if (P2 > P1){
			v = speed(ksi2, T2);
			dM2 = M_PI*d*d*v*dt*p/4;
			M2 = M2 + dM2;
		}
		t = t + dt;
	}
	cout.setf(ios_base::fixed, ios_base::floatfield);
	cout << "t = " << t << endl;
	cout << "M1 = " <<  M1 << endl;
	cout << "M2 = " << M2 << endl;
	cout << "dM = " << fabs(M1 - M2) << endl;
	return 0;
}

double speed (double ksi, double T){
	double v = 0.1;
	double v2 = 0.0;
	mu = (0.0179)/(1+0.0368*T+0.000221*T*T);
	while ((fabs(v-v2)/v) >= 0.01){
		v = (v + v2)/2;
		Re = v*d*p/mu;
		if (Re < 2320)
			lyam = 64/Re;
		else if (3000 <= Re && Re<=20*d/k)
			lyam = 0.3164/(pow(Re, 0.25));
		else if (20*k/d<=Re && Re<=500*k/d)
			lyam = 0.11*pow(((k/d)+(68/Re)),0.25);
		else 
			lyam = 0.11*pow(k/d, 0.25);
		v2 = sqrt((2*fabs(P1-P2))/(p*(lyam*l/d+ksi)));
	}
	return v;
}