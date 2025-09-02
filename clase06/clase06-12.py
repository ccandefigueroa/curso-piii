# ============================================================
# Modulaciones AM: DSB-FC, DSB-SC y SSB (USB)
# Genera dos figuras:
#   - Lámina A (6 paneles, vertical)
#   - Lámina B (3x2) exactamente como tu maqueta
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ---------------- Parámetros ----------------
fs  = 100_000              # muestreo 100 kHz
dur = 0.025                # 25 ms (coincide con tus tiempos)
t   = np.arange(0, dur, 1/fs)

fm = 200.0                 # mensaje 200 Hz
fc = 5_000.0               # portadora 5 kHz
Am = 1.0                   # amplitud mensaje
Ac = 1.0                   # amplitud portadora

# -------------- Señales base ---------------
m = Am * np.sin(2*np.pi*fm*t)        # mensaje
c = Ac * np.sin(2*np.pi*fc*t)        # portadora
y = (1 + m) * c                      # AM-DSB (con portadora)
y_sc = m * c                         # DSB-SC (mensaje·portadora en tiempo)

# -------------- Utilidades -----------------
def analytic_signal_fft(x):
    """Señal analítica por método espectral (equiv. a Hilbert)."""
    N = len(x)
    X = np.fft.rfft(x)
    H = np.ones_like(X, dtype=complex)
    H[1:-1] *= 2.0                   # duplica positivas (salvo DC/Nyquist)
    Xa = X * H
    xa = np.fft.irfft(Xa, n=N)
    return xa                        # x + j x_hat

def fft_mag_norm(x, fs, fmax=8000):
    """Magnitud normalizada de la rFFT, con ventana Hann y recorte a fmax."""
    N = len(x)
    X = np.fft.rfft(x * np.hanning(N))
    f = np.fft.rfftfreq(N, 1/fs)
    mag = np.abs(X)
    mag = mag / (mag.max() + 1e-12)
    sel = f <= fmax
    return f[sel], mag[sel]

# -------------- Modulación SSB -------------
# SSB-SC banda superior (USB) vía señal analítica
ma = analytic_signal_fft(m)
y_ssb_sc_upper = np.real(ma * np.exp(1j*2*np.pi*fc*t))   # USB (sin portadora)
y_ssb_fc       = y_ssb_sc_upper + c                      # USB + portadora (con portadora)

# -------------- FFTs necesarias ------------
f_y,   M_y   = fft_mag_norm(y,   fs, 8000)               # FFT de y(t) (DSB-FC)
f_sc,  M_sc  = fft_mag_norm(y_sc, fs, 8000)              # FFT de m(t)·c(t) (DSB-SC)
f_dsb, M_dsb = fft_mag_norm(y_sc, fs, 8000)              # para la lámina 3x2
f_ssbfc, M_ssbfc = fft_mag_norm(y_ssb_fc, fs, 8000)
f_ssbsc, M_ssbsc = fft_mag_norm(y_ssb_sc_upper, fs, 8000)

# ============================================================
# LÁMINA A — 6 paneles (vertical)
# ============================================================
figA, axs = plt.subplots(6, 1, figsize=(12, 12))

# 1) m(t)
axs[0].plot(t, m, linewidth=1.0, label="m(t)")
axs[0].set_xlim(0.0, 0.025)
axs[0].set_ylim(-1.05, 1.05)
axs[0].grid(True, alpha=0.35)
axs[0].set_title("Mensaje en el tiempo m(t)")
axs[0].set_xlabel("Tiempo [s]")
axs[0].set_ylabel("Amplitud")
axs[0].legend(loc="upper right")

# 2) c(t) (zoom)
axs[1].plot(t, c, linewidth=1.0, label="c(t)")
axs[1].set_xlim(0.0, 0.001)   # 0–1 ms para ver ciclos de 5 kHz
axs[1].set_ylim(-1.05, 1.05)
axs[1].grid(True, alpha=0.35)
axs[1].set_title("Portadora en el tiempo c(t) (zoom)")
axs[1].set_xlabel("Tiempo [s]")
axs[1].set_ylabel("Amplitud")
axs[1].legend(loc="upper right")

# 3) m(t)·c(t) (DSB-SC tiempo)
axs[2].plot(t, y_sc, linewidth=1.0, label="m(t)·c(t)")
axs[2].set_xlim(0.0, 0.010)
axs[2].set_ylim(-1.05, 1.05)
axs[2].grid(True, alpha=0.35)
axs[2].set_title("Señal mensaje·portadora (DSB-SC) en el tiempo")
axs[2].set_xlabel("Tiempo [s]")
axs[2].set_ylabel("Amplitud")
axs[2].legend(loc="upper right")

# 4) y(t) = (1+m(t))·c(t) (DSB-FC tiempo)
axs[3].plot(t, y, linewidth=1.0, label="y(t) = (1+m(t))·c(t)")
axs[3].set_xlim(0.0, 0.010)
axs[3].set_ylim(-2.1, 2.1)
axs[3].grid(True, alpha=0.35)
axs[3].set_title("Señal modulada AM-DSB (con portadora) en el tiempo")
axs[3].set_xlabel("Tiempo [s]")
axs[3].set_ylabel("Amplitud")
axs[3].legend(loc="upper right")

# 5) FFT de y(t)
axs[4].plot(f_y, M_y, linewidth=1.0)
axs[4].set_xlim(0, 8000)
axs[4].set_ylim(0.0, 0.8)
axs[4].grid(True, alpha=0.35)
axs[4].set_title("Espectro de la señal modulada y(t) (FFT)")
axs[4].set_xlabel("Frecuencia [Hz]")
axs[4].set_ylabel("Magnitud (norm.)")

# 6) FFT de m(t)·c(t)
axs[5].plot(f_sc, M_sc, linewidth=1.0)
axs[5].set_xlim(0, 8000)
axs[5].set_ylim(0.0, 0.8)
axs[5].grid(True, alpha=0.35)
axs[5].set_title("Espectro de m(t)·c(t) (FFT)")
axs[5].set_xlabel("Frecuencia [Hz]")
axs[5].set_ylabel("Magnitud (norm.)")

plt.tight_layout()
plt.show()

# (Opcional) Guardar
# figA.savefig("lamina_AM_6paneles.png", dpi=200, bbox_inches="tight")


# ============================================================
# LÁMINA B — 3x2 como en tu captura
# ============================================================
figB, axs = plt.subplots(3, 2, figsize=(12, 7.5))

# Fila 1: AM-DSB-SC (tiempo | espectro)
axs[0,0].plot(t, y_sc, linewidth=1.0)
axs[0,0].set_xlim(0.0, 0.012)
axs[0,0].set_ylim(-1.05, 1.05)
axs[0,0].grid(True, alpha=0.35)
axs[0,0].set_title("AM-DSB-SC (sin portadora) - tiempo")
axs[0,0].set_xlabel("Tiempo [s]")
axs[0,0].set_ylabel("Amplitud")

axs[0,1].plot(f_dsb, M_dsb, linewidth=1.0)
axs[0,1].set_xlim(0, 8000)
axs[0,1].set_ylim(0, 0.8)
axs[0,1].grid(True, alpha=0.35)
axs[0,1].set_title("AM-DSB-SC (sin portadora) - espectro")
axs[0,1].set_xlabel("Frecuencia [Hz]")
axs[0,1].set_ylabel("|X(f)| (norm.)")

# Fila 2: AM-SSB (con portadora) (tiempo | espectro)
axs[1,0].plot(t, y_ssb_fc, linewidth=1.0)
axs[1,0].set_xlim(0.0, 0.012)
axs[1,0].set_ylim(-2.05, 2.05)
axs[1,0].grid(True, alpha=0.35)
axs[1,0].set_title("AM-SSB (con portadora) - tiempo")
axs[1,0].set_xlabel("Tiempo [s]")
axs[1,0].set_ylabel("Amplitud")

axs[1,1].plot(f_ssbfc, M_ssbfc, linewidth=1.0)
axs[1,1].set_xlim(0, 8000)
axs[1,1].set_ylim(0, 0.8)
axs[1,1].grid(True, alpha=0.35)
axs[1,1].set_title("AM-SSB (con portadora) - espectro")
axs[1,1].set_xlabel("Frecuencia [Hz]")
axs[1,1].set_ylabel("|X(f)| (norm.)")

# Fila 3: SSB-SC (tiempo | espectro)
axs[2,0].plot(t, y_ssb_sc_upper, linewidth=1.0)
axs[2,0].set_xlim(0.0, 0.010)
axs[2,0].set_ylim(-1.05, 1.05)
axs[2,0].grid(True, alpha=0.35)
axs[2,0].set_title("SSB-SC (portadora suprimida) - tiempo")
axs[2,0].set_xlabel("Tiempo [s]")
axs[2,0].set_ylabel("Amplitud")

axs[2,1].plot(f_ssbsc, M_ssbsc, linewidth=1.0)
axs[2,1].set_xlim(0, 8000)
axs[2,1].set_ylim(0, 0.8)
axs[2,1].grid(True, alpha=0.35)
axs[2,1].set_title("SSB-SC (portadora suprimida) - espectro")
axs[2,1].set_xlabel("Frecuencia [Hz]")
axs[2,1].set_ylabel("|X(f)| (norm.)")

plt.tight_layout()
plt.show()

# (Opcional) Guardar
# figB.savefig("modulaciones_AM_layout_3x2.png", dpi=200, bbox_inches="tight")
