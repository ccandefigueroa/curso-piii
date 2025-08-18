import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import get_window
import sounddevice as sd

# =============================
# Config: detectar FS real del dispositivo
# =============================
FS_DEFAULT = 44_100
try:
    dev_in = sd.query_devices(kind="input")
    FS = int(round(dev_in.get("default_samplerate", FS_DEFAULT)))
    print(f"[info] samplerate real de entrada: {FS} Hz")
except Exception:
    FS = FS_DEFAULT
    print(f"[aviso] no se pudo leer el samplerate del dispositivo. Uso {FS} Hz")

DUR = 5.0          # segundos cada toma
CH = 1             # mono
DTYPE = "float32"  # sounddevice dtype

# =============================
# Utilidades
# =============================
def trim_silence(x, fs, thr_db=-40.0, pad_ms=20.0):
    """Recorta inicio/fin con nivel < umbral relativo (thr_db)."""
    x = np.asarray(x, dtype=np.float32)
    thr = 10 ** (thr_db / 20.0) * (np.max(np.abs(x)) + 1e-12)
    idx = np.where(np.abs(x) > thr)[0]
    if idx.size == 0:
        return x
    pad = int((pad_ms / 1000.0) * fs)
    s = max(0, idx[0] - pad)
    e = min(len(x), idx[-1] + pad)
    return x[s:e]

def remove_dc_and_normalize(x, target_dbfs=-1.0):
    """Quita DC y normaliza SIEMPRE a -1 dBFS para comparación justa."""
    x = x.astype(np.float32)
    x -= np.mean(x)
    peak = np.max(np.abs(x)) + 1e-12
    target = 10 ** (target_dbfs / 20.0)
    return x * (target / peak)

def record_take(prompt, fs=FS, dur=DUR, ch=CH, dtype=DTYPE):
    input(f"\n{prompt}\n   > Prepará la fuente y presioná ENTER para grabar {dur:.1f} s...")
    print("Grabando…")
    x = sd.rec(int(dur * fs), samplerate=fs, channels=ch, dtype=dtype)
    sd.wait()
    print("Listo.")
    x = x.squeeze().astype(np.float32)

    if np.max(np.abs(x)) >= 0.999:
        print("⚠ Posible clipping (nivel muy alto). Bajá volumen o alejate un poco.")

    x = trim_silence(x, fs)
    x = remove_dc_and_normalize(x, target_dbfs=-1.0)
    return x

def rfft_db(x, fs, nfft=None, window="hann"):
    """FFT con ventana Hann y normalización aprox; devuelve f, |X|, dB."""
    if nfft is None:
        nfft = 1 << max(14, int(np.ceil(np.log2(len(x)))))
    w = get_window(window, len(x), fftbins=True).astype(np.float32)
    xw = x * w
    if len(xw) < nfft:
        xw = np.pad(xw, (0, nfft - len(xw)))
    X = np.fft.rfft(xw, n=nfft)
    f = np.fft.rfftfreq(nfft, d=1 / fs)
    mag = np.abs(X) / (np.sum(w) / 2 + 1e-12)
    mag_db = 20 * np.log10(mag + 1e-12)
    return f, mag, mag_db

def peak_interp_parabolic(f, mag, fmin=None, fmax=None):
    """Pico con búsqueda opcional en banda y ajuste parabólico sub-bin."""
    if fmin is not None or fmax is not None:
        mask = np.ones_like(f, dtype=bool)
        if fmin is not None: mask &= (f >= fmin)
        if fmax is not None: mask &= (f <= fmax)
        idx = np.where(mask)[0]
        if idx.size == 0:  # sin banda válida
            k = np.argmax(mag)
        else:
            k_local = np.argmax(mag[idx])
            k = idx[k_local]
    else:
        k = np.argmax(mag)

    if 1 <= k < len(mag) - 1:
        a, b, c = mag[k - 1], mag[k], mag[k + 1]
        p = 0.5 * (a - c) / (a - 2 * b + c + 1e-12)
        return f[k] + p * (f[1] - f[0])
    return f[k]

def annotate_harmonics(ax, f0, upto_hz=2000, color="tab:green"):
    h = 1
    while h * f0 <= upto_hz:
        ax.axvline(h * f0, color=color, linestyle=":", alpha=0.5)
        h += 1

def plot_take_all(x, fs, title, save_prefix=None):
    fig, axes = plt.subplots(3, 1, figsize=(11, 9))
    fig.suptitle(title)

    # Tiempo (50 ms)
    nmax = int(min(len(x), 0.05 * fs))
    t = np.arange(nmax) / fs
    axes[0].plot(t, x[:nmax], linewidth=1.0)
    axes[0].set_title("Tiempo (50 ms)")
    axes[0].set_xlabel("Tiempo [s]")
    axes[0].set_ylabel("Amplitud")
    axes[0].ticklabel_format(style="plain", axis="y")
    axes[0].grid(True, alpha=0.3)

    # Espectro (0–2 kHz) + pico
    f, mag, mag_db = rfft_db(x, fs)
    f_est = peak_interp_parabolic(f, mag, fmin=200, fmax=900)
    axes[1].plot(f, mag_db)
    axes[1].set_xlim(0, 2000)
    axes[1].set_ylim(mag_db.max() - 80, mag_db.max() + 3)
    axes[1].set_title(f"Espectro (0–2 kHz) — pico ≈ {f_est:.1f} Hz")
    axes[1].set_xlabel("Frecuencia [Hz]")
    axes[1].set_ylabel("Magnitud [dB]")
    axes[1].grid(True, alpha=0.3)
    axes[1].axvline(f_est, color="tab:red", linestyle="--", alpha=0.7)
    annotate_harmonics(axes[1], f_est, upto_hz=2000, color="tab:green")

    # Espectrograma
    Pxx, freqs, bins, im = axes[2].specgram(x, NFFT=2048, Fs=fs, noverlap=1024, cmap="jet")
    axes[2].set_ylim(0, 2000)
    axes[2].set_title("Espectrograma")
    axes[2].set_xlabel("Tiempo [s]")
    axes[2].set_ylabel("Frecuencia [Hz]")
    cbar = fig.colorbar(im, ax=axes[2]); cbar.set_label("dB")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    if save_prefix:
        fig.savefig(f"{save_prefix}.png", dpi=150)
    plt.show()
    return f_est

def save_wav(path, x, fs):
    write(path, fs, x.astype(np.float32))
    print(f"[ok] guardado: {path}")

def play_audio(x, fs):
    try:
        sd.play(x, fs); sd.wait()
    except Exception as e:
        print(f"[aviso] no se pudo reproducir: {e}")

# =============================
# Flujo principal
# =============================
if __name__ == "__main__":
    print("Ejercicio 6 — Grabación de 440 Hz y A4 (mejorado)")

    x_tone  = record_take("Toma 1: Generador ONLINE de 440 Hz.")
    x_piano = record_take("Toma 2: Piano virtual — nota A4 (440 Hz).")

    # Guardar WAV normalizados
    save_wav("toma_440Hz.wav",   x_tone,  FS)
    save_wav("toma_piano_A4.wav", x_piano, FS)

    # (opcional) escuchar
    # play_audio(x_tone, FS)
    # play_audio(x_piano, FS)

    f1 = plot_take_all(x_tone,  FS, "Toma 1 — 440 Hz (generador)", save_prefix="toma1")
    f2 = plot_take_all(x_piano, FS, "Toma 2 — Piano A4 (440 Hz)",  save_prefix="toma2")

    print("\n— Resumen —")
    print(f"Pico estimado Toma 1: {f1:.2f} Hz")
    print(f"Pico estimado Toma 2: {f2:.2f} Hz")
    print("Generador: espectro limpio y estable; Piano: armónicos visibles y decay en espectrograma.")
