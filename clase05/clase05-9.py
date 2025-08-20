import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
from scipy.fft import fft
from scipy.io import wavfile
import librosa
from IPython.display import Audio, display

# ------------------- FFT + Plots -------------------
def fourier_calculation(y, sample_rate=44100):
    """FFT unilateral con magnitud lineal."""
    N = len(y)
    w = np.hanning(N)
    Y = fft(y * w)
    Y = 2.0 / N * np.abs(Y[:N // 2])
    f = np.linspace(0.0, sample_rate/2, N // 2, endpoint=False)
    return Y, f

def plot_tiempo_frecuencia_espectrograma(
        y, sample_rate=44100, tiempo_max=-1,
        f_max_fft=5000, f_max_espectrograma=5000, titulo=""):

    y = np.asarray(y)
    # si es estéreo, graficar canal 0
    y_plot = y[:, 0] if y.ndim == 2 else y
    x = np.arange(len(y_plot))/sample_rate

    plt.figure(figsize=(14, 12))

    # Tiempo
    ax1 = plt.subplot(3, 1, 1)
    if tiempo_max != -1:
        mask = x <= tiempo_max
        ax1.plot(x[mask], y_plot[mask])
        ax1.set_xlim(0, tiempo_max)
    else:
        ax1.plot(x, y_plot)
    ax1.set_title(f"{titulo} - Tiempo")
    ax1.set_xlabel("Tiempo [s]")
    ax1.set_ylabel("Amplitud")
    ax1.grid(True, alpha=0.3)

    # FFT
    ax2 = plt.subplot(3, 1, 2)
    mag, f = fourier_calculation(y_plot, sample_rate)
    ax2.plot(f, mag)
    ax2.set_xlim(0, f_max_fft)
    ax2.set_title(f"{titulo} - Espectro")
    ax2.set_xlabel("Frecuencia [Hz]")
    ax2.set_ylabel("|Y(f)|")
    ax2.grid(True, alpha=0.3)

    # Espectrograma
    ax3 = plt.subplot(3, 1, 3)
    Pxx, freqs, bins, im = ax3.specgram(
        y_plot, NFFT=1024, Fs=sample_rate, noverlap=512, cmap='jet')
    ax3.set_ylim(0, f_max_espectrograma)
    ax3.set_title(f"{titulo} - Espectrograma")
    ax3.set_xlabel("Tiempo [s]")
    ax3.set_ylabel("Frecuencia [Hz]")
    plt.colorbar(im, ax=ax3, label="dB (rel)")

    plt.tight_layout()
    plt.show()

# ------------------- Utilidades -------------------
def describe_audio(y, sr, source_name=""):
    """Imprime fs, canales y duración."""
    y = np.asarray(y)
    if y.ndim == 1:
        ch, n = 1, y.shape[0]
    else:
        n, ch = y.shape[0], y.shape[1]
    dur = n / sr
    print(f"[{source_name}] Frecuencia de muestreo: {sr} Hz")
    print(f"[{source_name}] Canales: {ch}")
    print(f"[{source_name}] Duración: {dur:.3f} s")
    return ch, dur

def infer_wav_bit_depth_from_dtype(data):
    """Estima bits por muestra del WAV PCM por su dtype."""
    dt = data.dtype
    if np.issubdtype(dt, np.integer):
        bits = np.iinfo(dt).bits
        if bits == 32:
            maxabs = np.max(np.abs(data))
            full24 = 2**23 - 1
            return 24 if maxabs <= full24 else 32
        return bits
    elif np.issubdtype(dt, np.floating):
        return "float (no aplica bit ADC)"
    else:
        return "desconocido"

def load_wav(path):
    """Devuelve y(float en [-1,1]), sr, bits."""
    sr, data = wavfile.read(path)  # (N,) o (N,C)
    if data.dtype == np.int16:
        y = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        y = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.uint8:
        y = (data.astype(np.float32) - 128.0) / 128.0
    else:  # float32/64
        y = data.astype(np.float32)
    bits = infer_wav_bit_depth_from_dtype(data)
    return y, sr, bits

def load_mp3(path, target_sr=None):
    """Carga MP3 con librosa (decodifica a PCM float)."""
    # mono=False -> librosa retorna (C, N) o (N,) si mono
    y, sr = librosa.load(path, sr=target_sr, mono=False)
    if y.ndim == 1:
        y = y.astype(np.float32)                 # (N,)
    else:
        y = y.T.astype(np.float32)               # (N, C)
    return y, sr

def play_audio(y, sr, label="Audio"):
    """Reproduce en notebooks. En terminal, podés comentar esta función."""
    y = np.asarray(y)
    y_disp = y.T if y.ndim == 2 else y
    print(f"▶ Reproduciendo: {label}")
    display(Audio(y_disp, rate=sr))

# ------------------- WAV -------------------
ruta_wav = r"ruta_wav.wav"   # <-- CAMBIAR

try:
    y_wav, sr_wav, bits_wav = load_wav(ruta_wav)
    describe_audio(y_wav, sr_wav, "WAV")
    print(f"[WAV] Bits por muestra (ADC): {bits_wav}\n")
    # play_audio(y_wav, sr_wav, "WAV")  # comentar si estás en terminal
    plot_tiempo_frecuencia_espectrograma(
        y_wav, sample_rate=sr_wav, tiempo_max=0.06,
        f_max_fft=8000, f_max_espectrograma=8000, titulo="WAV")
except FileNotFoundError:
    print("No se encontró el WAV. Cambiá 'ruta_wav' por un archivo existente.")

# ------------------- MP3 -------------------
ruta_mp3 = r"ruta_mp3.mp3"   # <-- CAMBIAR

try:
    y_mp3, sr_mp3 = load_mp3(ruta_mp3, target_sr=None)
    describe_audio(y_mp3, sr_mp3, "MP3")
    print("[MP3] Bits por muestra: no aplica (formato comprimido con pérdida)\n")
    # play_audio(y_mp3, sr_mp3, "MP3")  # comentar si estás en terminal
    plot_tiempo_frecuencia_espectrograma(
        y_mp3, sample_rate=sr_mp3, tiempo_max=0.06,
        f_max_fft=8000, f_max_espectrograma=8000, titulo="MP3")
except FileNotFoundError:
    print("No se encontró el MP3. Cambiá 'ruta_mp3' por un archivo existente.")
