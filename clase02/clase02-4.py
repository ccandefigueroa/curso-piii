import numpy as np
from scipy.io import wavfile

try:
    import sounddevice as sd   # opcional para reproducir
    HAS_SD = True
except Exception:
    HAS_SD = False

# -----------------------------
# Parámetros
# -----------------------------
fs = 44100        # frecuencia de muestreo
dur_note = 0.5    # duración de cada nota (s)
gap = 0.05        # silencio entre notas (s)
A = 0.8           # amplitud

# -----------------------------
# Utilidades
# -----------------------------
def tone(f, dur, fs, A=1.0):
    """Seno con pequeña envolvente para evitar clicks."""
    t = np.arange(0, dur, 1/fs)
    y = A * np.sin(2*np.pi*f*t)
    # Envolvente (fade in/out ~10 ms o 10% si la nota es muy corta)
    n = len(y)
    nfade = max(1, int(min(0.01, dur*0.1) * fs))
    fade = 0.5*(1 - np.cos(np.linspace(0, np.pi, nfade)))
    y[:nfade] *= fade
    y[-nfade:] *= fade[::-1]
    return y

def silence(dur, fs):
    return np.zeros(int(dur*fs), dtype=np.float32)

# -----------------------------
# Pentatónica menor de La
# Grados: 1, ♭3, 4, 5, ♭7, 1  → offsets en semitonos: 0, +3, +5, +7, +10, +12
# -----------------------------
A4 = 440.0
semitone = [0, 3, 5, 7, 10, 12]
note_names = ["A", "C", "D", "E", "G", "A'"]  # ' indica la octava superior

# Ascenso y descenso (como el ejemplo del .mid)
pattern = semitone + semitone[-2:0:-1] + [0]   # 0,3,5,7,10,12,10,7,5,3,0
pattern_names = note_names + note_names[-2:0:-1] + ["A"]

# Frecuencias de la secuencia
freqs = [A4 * 2**(n/12) for n in pattern]

print("Escala pentatónica menor de La (A minor pentatonic):")
for name, f in zip(pattern_names, freqs):
    print(f"  {name:>2}  →  {f:8.2f} Hz")

# -----------------------------
# Construcción del audio
# -----------------------------
audio = []
for f in freqs:
    audio.append(tone(f, dur_note, fs, A))
    audio.append(silence(gap, fs))

audio = np.concatenate(audio).astype(np.float32)

# -----------------------------
# Guardar y (opcional) reproducir
# -----------------------------
wavfile.write("la_pentatonica_menor.wav", fs, audio)
print("\nGuardado: la_pentatonica_menor.wav")

if HAS_SD:
    print("Reproduciendo…")
    sd.play(audio, fs); sd.wait()
else:
    print("sounddevice no está instalado; se guardó el WAV para reproducirlo con tu reproductor.")
