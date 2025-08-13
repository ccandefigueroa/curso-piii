import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from IPython.display import Audio, display

# ===== Parámetros base =====
fs  = 44_100     # frecuencia de muestreo [Hz]
dur = 3.0        # duración [s]
t   = np.arange(int(fs*dur)) / fs

A       = 0.8    # amplitud común (igual para ambas)
f_sq    = 400    # cuadrada (audible)
f_tri   = 800    # triangular (audible y distinta)
t_short = t[t <= 0.01]  # ventana de 10 ms para ver detalles

# ===== Señales =====
square   = A * signal.square(2*np.pi*f_sq*t)
triangle = A * signal.sawtooth(2*np.pi*f_tri*t, width=0.5)  # width=0.5 -> triangular pura
mix      = square + triangle

# Normalizamos la mezcla para evitar clip al escuchar
mix = 0.9 * mix / np.max(np.abs(mix))

# ===== Gráficos (una figura por señal) =====
plt.figure(); plt.title("Onda cuadrada (400 Hz)")
plt.plot(t_short, square[:len(t_short)]); plt.xlabel("Tiempo [s]"); plt.ylabel("Amplitud"); plt.show()

plt.figure(); plt.title("Onda triangular (800 Hz)")
plt.plot(t_short, triangle[:len(t_short)]); plt.xlabel("Tiempo [s]"); plt.ylabel("Amplitud"); plt.show()

plt.figure(); plt.title("Mezcla: cuadrada + triangular")
plt.plot(t_short, mix[:len(t_short)]); plt.xlabel("Tiempo [s]"); plt.ylabel("Amplitud"); plt.show()

print("► Audio: cuadrada");   display(Audio(square,   rate=fs))
print("► Audio: triangular"); display(Audio(triangle, rate=fs))
print("► Audio: mezcla");     display(Audio(mix,      rate=fs))

# ===== Cuantizador uniforme =====
def uniform_quantize(x, bits, vref_plus, vref_minus, mid_tread=True):
    """
    Cuantizador uniforme.
      - bits: cantidad de bits (niveles = 2**bits)
      - vref_plus/vref_minus: rango de cuantización [VRef-, VRef+)
      - mid_tread=True: niveles centrados en 0 (centro de celda)
    Devuelve: (señal cuantizada, códigos, Δ, SQNR_dB)
    """
    assert vref_plus > vref_minus, "VRef+ debe ser mayor que VRef-"
    L = 2**bits
    vmin, vmax = vref_minus, vref_plus
    delta = (vmax - vmin) / L

    # recorte al rango
    x_clip = np.clip(x, vmin, vmax - 1e-12)
    indices = np.floor((x_clip - vmin) / delta).astype(int)
    q = vmin + (indices + 0.5) * delta  # centro de celda

    # métrica SQNR
    noise = x - q
    sig_pow = np.mean(x**2)
    noise_pow = np.mean(noise**2)
    sqnr_db = np.inf if noise_pow == 0 else 10*np.log10(sig_pow / noise_pow)
    return q, indices, delta, sqnr_db

# ===== Demo de cuantización =====
bits = 8
Vref_plus, Vref_minus = 1.0, -1.0

q_mix, codes, delta, sqnr_db = uniform_quantize(mix, bits, Vref_plus, Vref_minus)
print(f"Bits={bits} | Niveles={2**bits} | Δ={delta:.6f} | SQNR≈{sqnr_db:.2f} dB")

plt.figure(); plt.title("Original vs Cuantizada (10 ms)")
plt.plot(t_short, mix[:len(t_short)], label="Original")
plt.plot(t_short, q_mix[:len(t_short)], "--", label="Cuantizada")
plt.xlabel("Tiempo [s]"); plt.ylabel("Amplitud"); plt.legend(); plt.show()

print("► Audio: mezcla cuantizada")
display(Audio(q_mix, rate=fs))
