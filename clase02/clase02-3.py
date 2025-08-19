import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Parámetros
# ----------------------------
f0   = 1_000        # Hz (señal senoidal)
A    = 5.0          # amplitud pico (rango -5 a +5)
fs   = 50_000       # Hz (frecuencia de muestreo)
dur  = 0.010        # 10 ms a mostrar en señal continua
N50  = 50           # primeras 50 muestras a graficar
bits = 12           # ADC de 12 bits
Vref_plus  = +5.0   # rango de cuantificación
Vref_minus = -5.0

# ----------------------------
# Señal continua (10 ms)
# ----------------------------
t_cont = np.linspace(0, dur, int(fs*dur*5), endpoint=False)  # densa para "continua"
x_cont = A * np.sin(2*np.pi*f0*t_cont)

# ----------------------------
# Muestreo (fs = 50 kHz)
# ----------------------------
Ts = 1/fs
n = np.arange(0, N50)         # índices de 0 a 49
t_s = n * Ts                  # instantes de muestreo
x_s = A * np.sin(2*np.pi*f0*t_s)

# ----------------------------
# Cuantización uniforme (12 bits, rango -5 a +5)
# ----------------------------
levels = 2**bits
delta  = (Vref_plus - Vref_minus) / levels   # paso
# mapea cada muestra al nivel más cercano dentro del rango
q_idx  = np.clip(np.floor((x_s - Vref_minus)/delta + 0.5), 0, levels-1)   # índice 0..4095
x_q    = Vref_minus + q_idx * delta

# (opcional) SNR de cuantización teórica
sqnr_db = 6.02*bits + 1.76

# ----------------------------
# Ploteo: 3 gráficos
# ----------------------------
plt.figure(figsize=(12, 8))

# 1) Señal continua (10 ms)
plt.subplot(3,1,1)
plt.plot(t_cont*1e3, x_cont, lw=1.2)
plt.title("Señal senoidal continua (1 kHz, A = ±5 V) — 10 ms")
plt.xlabel("Tiempo [ms]")
plt.ylabel("Amplitud [V]")
plt.grid(True)

# 2) Primeras 50 muestras sin cuantificar
plt.subplot(3,1,2)
plt.stem(n, x_s, basefmt='r-', use_line_collection=True)
plt.title(f"Primeras {N50} muestras muestreadas a {fs/1000:.0f} kHz (sin cuantificar)")
plt.xlabel("n (muestras)")
plt.ylabel("Amplitud [V]")
plt.grid(True)

# 3) Primeras 50 muestras cuantificadas (12 bits)
plt.subplot(3,1,3)
plt.stem(n, x_q, basefmt='r-', use_line_collection=True)
plt.title(f"Primeras {N50} muestras cuantificadas — ADC {bits} bits (Δ = {delta:.4f} V, SQNR≈{sqnr_db:.1f} dB)")
plt.xlabel("n (muestras)")
plt.ylabel("Amplitud cuantificada [V]")
plt.grid(True)

plt.tight_layout()
plt.show()
