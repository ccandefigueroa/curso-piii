import numpy as np
import matplotlib.pyplot as plt

# ---------------- Parámetros de la señal ----------------
fs  = 44100            # Hz
dur = 2.0              # s
f0  = 440              # Hz
A   = 1.0              # amplitud pico
t = np.arange(0, dur, 1/fs)
x = A*np.sin(2*np.pi*f0*t)

# ---------------- Cuantificador uniforme (mid-tread) ----------------
def cuantificar(x, Nbits, xmax=1.0):
    """
    Cuantificador uniforme simétrico (mid-tread: incluye 0)
    Rango: [-xmax, xmax]
    Paso:  Δ = 2*xmax / (2^N - 1)
    """
    L = 2**Nbits
    Delta = 2*xmax/(L - 1)
    x_clip = np.clip(x, -xmax, xmax)
    xq = np.round(x_clip/Delta)*Delta
    return xq, Delta

# ---------------- SNR (tiempo) ----------------
def snr_db(x, e):
    Ps = np.mean(x**2)
    Pe = np.mean(e**2)
    return 10*np.log10(Ps/(Pe + 1e-20))

# ---------------- Config de gráficos ----------------
zoom_ini = 0.0
zoom_fin = 0.005     # 5 ms como en tus fotos

def plot_tiempo(x, xq, t, Nbits):
    plt.figure()
    plt.plot(t, x,  '--', linewidth=1.2, label='Original')
    plt.plot(t, xq, '-',  linewidth=1.5, label='Cuantificada')
    plt.xlim(zoom_ini, zoom_fin)
    plt.title(f'Señal original vs. cuantificada (Nbits = {Nbits})')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='lower left')

def plot_error(e, t, Nbits):
    plt.figure()
    plt.plot(t, e, '-', linewidth=1.2, color='tab:red')
    plt.xlim(zoom_ini, zoom_fin)
    plt.title(f'Error de cuantificación (Nbits = {Nbits})')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Error')
    plt.grid(True, alpha=0.3)

# ---------------- Experimento ----------------
for Nbits in [8, 4, 2]:
    xq, Delta = cuantificar(x, Nbits, xmax=A)
    e = xq - x

    snr_teo  = 6.02*Nbits + 1.76
    snr_real = snr_db(x, e)

    print(f'Nbits = {Nbits}')
    print(f'  SNR teórico: {snr_teo:5.2f} dB')
    print(f'  SNR real:    {snr_real:5.2f} dB')

    plot_tiempo(x, xq, t, Nbits)
    plot_error(e, t, Nbits)

plt.show()
