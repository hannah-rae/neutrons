file_text = '''LunaH-Map CLYC detector
C cells
 1 1 -3.3        -1     $ CLYC detector
11 2 -2.7        -11 1
12 3 -8.65       -12 11 $ Cd
c 12 4 -7.31       -12 11 $ Sn
 2 0             1 11 12 -2  $ Sphere
 3 0             2     $ Void

 1 rpp -1.250 1.250   0.000 2.0 -1.250 1.250  $
11 rpp -1.350 1.350  -0.100 2.0 -1.350 1.350
12 rpp -1.413 1.413  -0.163 2.0 -1.413 1.413
 2 sph 0 0 0 10               $ Sphere

m1    55133  -0.46234  $ Cs
      39089  -0.15469  $ Y
       3006  -0.00991  $ Li
       3007  -0.00061
      17035  -0.27740  $ Cl
      17037  -0.09261
      58140  -0.00217  $ Ce
      58142  -0.00027
c
m2    13027  -1.00000  $ Al
m3    48000  -1.00000  $ Cd
m4    50000  -1.00000  $ Sn
c
c sdef pos=0 -5 0 DIR=1 VEC= 0 1 0 ERG=1e-9 par=n AXS=0 1 0 EXT=0
sdef pos=0 -5 0 DIR=1 VEC= 0 1 0 ERG=d1 par=n AXS=0 1 0 EXT=0
si1 h 0.00
      1.00E-09
      1.58E-09
      2.51E-09
      3.98E-09
      6.31E-09
      1.00E-08
      1.58E-08
      2.51E-08
      3.98E-08
      6.31E-08
      1.00E-07
      1.58E-07
      2.51E-07
      3.98E-07
      6.31E-07
      1.00E-06
      1.58E-06
      2.51E-06
      3.98E-06
      6.31E-06
      1.00E-05
      1.58E-05
      2.51E-05
      3.98E-05
      6.31E-05
      1.00E-04
      1.58E-04
      2.51E-04
      3.98E-04
      6.31E-04
      1.00E-03
      1.58E-03
      2.51E-03
      3.98E-03
      6.31E-03
      1.00E-02
      1.58E-02
      2.51E-02
      3.98E-02
      6.31E-02
      1.00E-01
      1.58E-01
      2.51E-01
      3.98E-01
      6.31E-01
      1.00E+00
c
sp1   %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
      %s
c
c _______________tallies_____________________________
c
fc14 Reaction Number (107)
f14:n 1
sd14 1
fm14 -1 1 107
e14     4e-7  1e-5  1e-4  1e-3 1e-2 1e-1 1 1e1 1e2 1e3 1e4
c
c f4:n 1
c e4     4e-7  1e-5  1e-4  1e-3 20
c
f6:a 1
sd6 1
c ft6 geb 0.025 0 0
c
f16:t 1
sd16 1
c
fc8 Alphas
e8  0 1e-8 0.05 198i 10. 1e9
f8:a 1
ft8 phl 1 6 1 0
c
fc18 Tritons
e18 0 1e-8 0.05 198i 10. 1e9
f18:t 1
ft18 phl 1 16 1 0
c
fc28 Spectrum (a t)
e28 0 1e-8 0.05 198i 10. 1e9
f28:a 1
ft28 phl 2 6 1 16 1 0
c
e38 0 1e-8 0.05 198i 10. 1e9
f38:t 1
ft38 phl 2 6 1 16 1 0
c
c ______________parameters___________________________
imp:n,a,t 1 1 1 1 0
mode n a t
phys:n 1000 5j 2
c phys:h 1e5
c mphys on
cut:n 2j 0 0
cut:a,t j 0
nps 1e7
c print'''