program MZHG;

var
  P0, T0, P01, P02, P1, P2, T01, T02, T1, T2, 
  w1, ksi1, ksi2, v,
  dM1, dM2,
  n1, n2, eps1, eps2, ksi11, ksi12, ksi21, ksi22,
  w2, d, l, k, d1, d2, p, te, t, dt, M1, M2: real;

function Speed(ksi: real; T: real): real;
var
  v, v2, mu, lyam, Re: real;
begin
  v := 0.1;
  v2 := 0.0;
  mu := (0.0179) / (1 + 0.0368 * T + 0.000221 * T * T);
  while ((abs(v - v2) / v) >= 0.01) do
  begin
    v := (v + v2) / 2.0;
    Re := v * d * p / mu;
    if (Re < 2320.0) then 
      lyam := 64.0 / Re
    else if (3000.0 <= Re) and (Re <= 20.0 * d / k) then
      lyam := 0.3164 / power(Re,0.25)
    else if (20 * k / d <= Re)  and (Re <= 500 * k / d) then
      lyam := 0.11 * power(((k / d) + (68 / Re)),0.25)
    else 
      lyam := 0.11 * power((k / d), 0.25);
    v2 := sqrt(((2.0*abs(P1-P2))/(p*(lyam*l/d+ksi))));
  end;
  Speed := v;
end;

begin
  P0 := 100000.0;
  T0 := 273.0;
  P01 := 98000.0;
  P02 := 50000.0;
  T01 := 20.0;
  T02 := 80.0;
  w1 := 70.0;
  w2 := 100.0;
  d := 0.3;
  l := 0.2;
  k := 0.001;
  D1 := 0.6;
  D2 := 0.9;
  p := 1000.0;
  te := 0.5;
  
  n1 := (d * d) / (D1 * D1);
  eps1 := 0.57 + (0.043 / (1.1 - n1));
  ksi11 := power(((1 - eps1) / eps1), 2);
  ksi21 := power((((d * d) / (D2 * D2)) - 1), 2);
  
  n2 := (d * d) / (D2 * D2);
  eps2 := 0.57 + (0.043 / (1.1 - n2));
  ksi12 := power(((1 - eps2) / eps2), 2);
  ksi22 := power((((d * d) / (D1 * D1)) - 1), 2);
  
  ksi1 := ksi11 + ksi21;
  ksi2 := ksi12 + ksi22;
  
  t := 0.0; 
  dt := te / 10000.0;
  M1 := 0.0;
  M2 := 0.0;
  while t <= te do
  begin
    P1 := P01 * cos(w1 * t) + P0;
    T1 := T01 * cos(w1 * t) + T0;
    P2 := P02 * cos(w2 * t) + P0;
    T2 := T02 * cos(w2 * t) + T0;
    if P1 > P2 then
      begin
        v := Speed(ksi1, T1);
        dM1 := Pi * d * d * v * dt * p / 4;
        M1 := M1 + dM1;
      end
    else if P2 > P1 then
      begin
        v := Speed(ksi2, T2);
        dM2 := Pi * d * d * v * dt * p / 4;
        M2 := M2 + dM2;
      end;
    t := t + dt;
  end;
  writeln('t = ', t:3:1);
  writeln('M1 = ', M1:7:3);
  writeln('M2 = ', M2:7:3);
  writeln('dM = ', abs(M1 - M2):7:3);
end.



