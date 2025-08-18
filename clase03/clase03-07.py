# ---- Forzar backend que abre ventanas en Windows ----
import matplotlib
try:
    matplotlib.use("TkAgg")  # suele funcionar en Windows
except Exception:
    pass  # si falla, igual guardaremos imágenes

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice as sd

WAV_FILE = "audio.wav"   # tu archivo

# ---- utils ----
def to_float(audio):
    if np.issubdtype(audio.dtype, np.integer):
        return audio.astype(np.float32) / np.iinfo(audio.dtype).max
    return audio.astype(np.float32)

def to_mono(x):
    return x.mean(axis=1) if x.ndim == 2 else x

def rfft_db(y, sr):
    n = len(y)
    nfft = 1 << max(12, int(np.ceil(np.log2(n))))
    win = np.hanning(n)
    yw = y * win
    if n < nfft:
        yw = np.pad(yw, (0, nfft - n))
    Y = np.fft.rfft(yw, n=nfft)
    f = np.fft.rfftfreq(nfft, 1/sr)
    mag_db = 20*np.log10(np.abs(Y)/(np.sum(win)/2) + 1e-12)
    return f, mag_db

# ---- carga y repro ----
sr, data = wavfile.read(WAV_FILE)
audio_f = to_float(data)       # conserva estéreo si existe
mono = to_mono(audio_f)        # mono para análisis

print(f"SR: {sr} Hz | canales: {1 if data.ndim==1 else data.shape[1]} | duración: {len(data)/sr:.2f} s")
print("Reproduciendo…")
sd.play(audio_f, sr); sd.wait()

# ---- GRAFICO 1: tiempo (0.1 s) ----
fig1 = plt.figure(figsize=(10,3))
n = int(min(len(mono), 0.1*sr))
t = np.arange(n)/sr
plt.plot(t, mono[:n])
plt.title("Señal en el tiempo (0.1 s)")
plt.xlabel("Tiempo [s]"); plt.ylabel("Amplitud"); plt.grid(True)
fig1.tight_layout()
fig1.savefig("wav_tiempo.png", dpi=150)
plt.show(block=True)

# ---- GRAFICO 2: espectro ----
fig2 = plt.figure(figsize=(10,3))
f, mag_db = rfft_db(mono, sr)
plt.plot(f, mag_db)
plt.xlim(0, 8000)
plt.title("Espectro (dB)")
plt.xlabel("Frecuencia [Hz]"); plt.ylabel("Magnitud [dB]"); plt.grid(True)
fig2.tight_layout()
fig2.savefig("wav_fft.png", dpi=150)
plt.show(block=True)

# ---- GRAFICO 3: espectrograma ----
fig3 = plt.figure(figsize=(10,4))
Pxx, freqs, bins, im = plt.specgram(mono, NFFT=2048, Fs=sr, noverlap=1024, cmap="jet")
plt.ylim(0, 8000)
plt.title("Espectrograma")
plt.xlabel("Tiempo [s]"); plt.ylabel("Frecuencia [Hz]")
cbar = plt.colorbar(im); cbar.set_label("dB")
fig3.tight_layout()
fig3.savefig("wav_spec.png", dpi=150)
plt.show(block=True)

print("Guardados: wav_tiempo.png, wav_fft.png, wav_spec.png")
