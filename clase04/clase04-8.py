import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
from numpy.fft import rfft, rfftfreq

# ==================================================
# Parámetros base
# ==================================================
fs_ref = 44100          # Muestreo de referencia (alto) [Hz]
dur = 1.0               # Duración [s]
t_ref = np.arange(0, dur, 1/fs_ref)

# Señal compuesta por 3 senoidales
f1, f2, f3 = 300, 800, 1500          # [Hz]
x_ref = (np.sin(2*np.pi*f1*t_ref) +
         np.sin(2*np.pi*f2*t_ref) +
         np.sin(2*np.pi*f3*t_ref))

# Frecuencias de muestreo a comparar
f_max = max(f1, f2, f3)
fs_bajo   = 2000                      # Sub-Nyquist: fs < 2*f_max (=3000)
fs_limite = 3000                      # Límite Nyquist: fs = 2*f_max
fs_alto   = 8000                      # Sobre-Nyquist: fs > 2*f_max

# ==================================================
# Funciones auxiliares
# ==================================================
def remuestrear(x_high, fs_high, fs_target, dur):
    """Remuestrea x_high (a fs_high) a un nuevo fs_target usando scipy.signal.resample"""
    n_new = int(round(dur * fs_target))
    x_new = resample(x_high, n_new)
    t_new = np.arange(n_new) / fs_target
    return t_new, x_new

def espectro_db(x, fs):
    """Magnitud en dB del espectro unilateral"""
    X = rfft(x) / len(x)
    f = rfftfreq(len(x), 1/fs)
    mag = 20*np.log10(np.abs(X) + 1e-12)  # evitar log(0)
    return f, mag

def dibujar_caso(nombre, fs_target, color_tiempo=None):
    # --- Remuestreo ---
    t, x = remuestrear(x_ref, fs_ref, fs_target, dur)

    # --- Espectros ---
    f_ref, mag_ref = espectro_db(x_ref, fs_ref)
    f_new, mag_new = espectro_db(x, fs_target)

    # ================================
    # Ventana: TIEMPO (zoom a 0–20 ms)
    # ================================
    plt.figure(f"{nombre} - Tiempo")
    # Señal original (referencia) punteada
    plt.plot(t_ref*1000, x_ref, linestyle='--', linewidth=1, label=f"Original (fs={fs_ref} Hz)")
    # Señal remuestreada (línea continua)
    plt.plot(t*1000, x, linewidth=1.5, label=f"Remuestreada (fs={fs_target} Hz)")
    plt.xlim(0, 20)                        # zoom 0–20 ms
    plt.xlabel("Tiempo [ms]")
    plt.ylabel("Amplitud")
    plt.title(f"Comparación en el tiempo - {nombre}")
    plt.grid(True, alpha=0.3)
    plt.legend(loc="upper right")

    # ================================
    # Ventana: ESPECTRO (hasta 2 kHz)
    # ================================
    plt.figure(f"{nombre} - Espectro")
    plt.plot(f_new, mag_new, linewidth=1.5, label=f"Remuestreada (fs={fs_target} Hz)")
    plt.xlim(0, 2000)                      # hasta 2 kHz
    # opcional: mostrar una línea tenue de referencia del espectro original
    plt.plot(f_ref, mag_ref, linestyle='--', linewidth=1, label=f"Original (fs={fs_ref} Hz)")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud [dB]")
    plt.title(f"{nombre} - espectro")
    plt.grid(True, alpha=0.3)
    plt.legend(loc="upper right")

# ==================================================
# Dibujar los 3 casos (3 ventanas *dobles*: tiempo + espectro)
# ==================================================
dibujar_caso("Sub-Nyquist (2000 Hz)", fs_bajo)
dibujar_caso("Límite Nyquist (3000 Hz)", fs_limite)
dibujar_caso("Muestreo alto (8000 Hz)", fs_alto)

plt.show()
