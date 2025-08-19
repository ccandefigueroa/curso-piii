import matplotlib
matplotlib.use("TkAgg")  # si ya te funciona, podés omitir esta línea

from modulacion.portadora import generar_portadora, graficar as graf_port
from modulacion.am import modulacion_am, graficar as graf_am

fs = 44100
dur = 0.01
fc = 2000
fm = 100
A  = 1.0
m  = 0.7

t, c   = generar_portadora(fc, fs, dur, A)
graf_port(t, c, "Portadora 2 kHz")

t, xam = modulacion_am(t, c, fm, m)
graf_am(t, xam, "AM (fm=100 Hz, m=0.7)")
