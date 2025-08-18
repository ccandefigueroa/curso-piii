import numpy as np
import matplotlib.pyplot as plt

# --- parámetros ---
A     = 8.0     # amplitud del pico central
M     = 8       # ceros de la sinc en n = ±8, ±16, ...
NMAX  = 32      # rango de muestras a graficar

# eje discreto y señal
n = np.arange(-NMAX, NMAX + 1, 1)
x = A * np.sinc(n / M)   # np.sinc(x) = sin(pi*x)/(pi*x)

# --- gráfico tipo stem + línea base roja ---
plt.figure(figsize=(9, 5))
markerline, stemlines, baseline = plt.stem(n, x, use_line_collection=True)
plt.setp(baseline, color='r', linewidth=1)     # línea y=0 en rojo
plt.setp(markerline, markersize=6)

# estilo para que se vea como en la consigna
plt.xlim(-NMAX, NMAX)
plt.ylim(-2, 8.3)
plt.xticks(np.arange(-32, 33, 4))
plt.yticks(np.arange(-2, 9, 1))
plt.grid(False)               # sin grilla
plt.xlabel("")                # sin etiquetas extra
plt.ylabel("")

plt.show()
