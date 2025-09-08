# Clase 02 — Señales discretas, AM, muestreo y audio 🎧📈

> **Objetivo:** practicar generación y manipulación de señales en Python (NumPy + Matplotlib), modulación AM, muestreo y cuantificación, y un primer contacto con audio digital.

---

## 📦 Contenidos
- Portadora senoidal y **AM** (DSB con portadora).
- **Secuencias**: `cos(n)` con negativos en 0 y seno discreto con M muestras/ciclo.
- **Muestreo** y **cuantificación** (ADC de 12 bits).
- **Audio**: escala pentatónica menor de **La**.

---

## 🗂️ Estructura sugerida
clase02/
├─ README.md

├─ modulacion/

│ ├─ init.py

│ ├─ portadora.py # generar_portadora(), graficar()

│ └─ am.py # modulacion_am(), graficar()

├─ ejercicios/

│ ├─ ej1_am.py

│ ├─ ej2_secuencias.py

│ └─ ej3_muestreo_cuant.py

└─ audio/

└─ escala_pentatonica.py

---

## ⚙️ Requisitos e instalación

- Python **3.9+**
- Paquetes: `numpy`, `matplotlib` (y opcional `ipython`/`jupyter` para reproducir audio en notebooks).

```bash
# (opcional) entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install numpy matplotlib ipython
```

## 🟢 Actividad 1 — Portadora y AM
- **Consigna:** crear un módulo que grafique una **portadora** y otra que **module en amplitud**.
- **Modelo:**  
  $$x_{AM}(t)=(1+m\cos 2\pi f_m t)\,A\cos 2\pi f_c t$$
- **Parámetros usados:** `fs=44100`, `fc=2000`, `fm=100`, `A=1.0`, `m=0.7`.



```python
import numpy as np
import matplotlib.pyplot as plt

def generar_portadora(fc, fs, dur, A=1.0):
    t = np.arange(0, dur, 1/fs)
    c = A*np.cos(2*np.pi*fc*t)
    return t, c

def graficar(t, x, titulo):
    plt.figure(); plt.plot(t, x)
    plt.title(titulo); plt.xlabel('t [s]'); plt.ylabel('amplitud')
    plt.grid(True); plt.show()



clase02-2.py
import numpy as np
import matplotlib.pyplot as plt

def modulacion_am(t, c, fm, m):
    mod = (1 + m*np.cos(2*np.pi*fm*t))
    return t, mod*c

def graficar(t, x, titulo):
    plt.figure(); plt.plot(t, x)
    plt.title(titulo); plt.xlabel('t [s]'); plt.ylabel('amplitud')
    plt.grid(True); plt.show()


ejercicios/ej1_am.py

from modulacion.portadora import generar_portadora, graficar as gport
from modulacion.am import modulacion_am, graficar as gam

fs, dur, fc, fm, A, m = 44100, 0.01, 2000, 100, 1.0, 0.7
t, c = generar_portadora(fc, fs, dur, A); gport(t, c, "Portadora 2 kHz")
t, xam = modulacion_am(t, c, fm, m);      gam(t, xam, "AM (fm=100 Hz, m=0.7)")
```


## 🟢Actividad 2 — Secuencias

- **Consigna:**
A) Mostrar los primeros 50 valores de y = cos(n) reemplazando con 0 los negativos.
B) Graficar una senoide discreta con 12 muestras por ciclo.

- **Parámetros usados:**
`N=50`, `M=12`, `ciclos=3.`


clase02-1.py
```python 
import numpy as np
import matplotlib.pyplot as plt

# Parte 1: cos(n) con negativos a 0
n = np.arange(50)
y = np.cos(n)                 # n en radianes
y_trunc = np.clip(y, 0, None) # reemplaza y<0 por 0

plt.figure()
plt.stem(n, y, basefmt='r-', label='cos(n)')
plt.stem(n, y_trunc, basefmt='r-', label='cos(n) truncado')
plt.title("cos(n) y cos(n) truncado (negativos→0)")
plt.xlabel("n"); plt.grid(True); plt.legend()

# Parte 2: seno discreto con 12 muestras/ciclo
M, ciclos = 12, 3
k = np.arange(M*ciclos)
x = np.sin(2*np.pi*k/M)

plt.figure()
plt.stem(k, x, basefmt='r-')
plt.title(f"Seno discreto con {M} muestras/ciclo — {ciclos} ciclos")
plt.xlabel("k (muestras)"); plt.grid(True)
plt.show()
```

## 🟢Ejercicio 3 — Muestreo y cuantificación

- **Consigna:** Generar una senoidal continua de 1 kHz, amplitud ±5, duración 10 ms.
Muestrear a 50 kHz y mostrar las primeras 50 muestras.
Cuantificar esas 50 a 12 bits (ADC) y graficar las 3 curvas juntas.
#Señal continua: senoidal 1 kHz, ±5, 10 ms.


clase02-3.py
```python 
import numpy as np
import matplotlib.pyplot as plt

A, f, dur = 5.0, 1000.0, 0.01
Fs = 50000.0
Nadc = 12
xmin, xmax = -A, +A

# Señal continua
t = np.linspace(0, dur, 5000, endpoint=False)
x = A*np.sin(2*np.pi*f*t)

# Muestreo
n = np.arange(int(Fs*dur))
tm = n/Fs
xm = A*np.sin(2*np.pi*f*tm)

# Primeras 50 sin cuantificar
tm50, xm50 = tm[:50], xm[:50]

# Cuantificación uniforme a 12 bits en rango [-A, A]
L = 2**Nadc
codes = np.round((xm50 - xmin) / (xmax - xmin) * (L-1))
codes = np.clip(codes, 0, L-1)
xm50_q = codes/(L-1)*(xmax - xmin) + xmin

# Gráficos
fig, ax = plt.subplots(3,1,figsize=(10,8))
ax[0].plot(t, x);                  ax[0].set_title("Señal continua 1 kHz (±5)")
ax[1].stem(tm50, xm50, basefmt='r-');   ax[1].set_title("50 muestras (sin cuantificar)")
ax[2].stem(tm50, xm50_q, basefmt='r-'); ax[2].set_title("50 muestras cuantificadas (ADC 12 bits)")
for a in ax: a.grid(True); a.set_xlabel("tiempo [s]")
plt.tight_layout(); plt.show()

LSB (12 bits, rango ±5): LSB = 10 / (2^12 - 1) ≈ 2.44 mV.
```

## 🟢🔊 Ejercicio 4 — Escala pentatónica menor de La

- **Consigna:** reproducir la escala pentatónica menor de La (A, C, D, E, G, A).
#Rango audible aprox. 20 Hz–20 kHz.


clase02-4.py
```python
import numpy as np
Fs = 44100

def tono(f, dur, A=0.8):
    t = np.linspace(0, dur, int(Fs*dur), endpoint=False)
    return (A*np.sin(2*np.pi*f*t)).astype(np.float32)

# Pentatónica menor de La (A, C, D, E, G, A)
A4 = 440.0
ratios = [1, 6/5, 4/3, 3/2, 6/4, 2]
freqs = [A4*r for r in ratios]

audio = np.concatenate([tono(f, 0.35) for f in freqs])

# Guardar a WAV (16 bits little-endian)
from pathlib import Path
Path("escala_la_pent.wav").write_bytes((audio*32767).astype("<i2").tobytes())
```

✅ Checklist rápido

 Portadora y AM graficadas (Ej1).

 cos(n) (50) con negativos→0 + seno con 12 muestras/ciclo (Ej2).

 3 gráficas: continua, 50 muestras, 50 cuantificadas (Ej3).

 WAV de la escala pentatónica (Ej4).

 Scripts corriendo desde la raíz del proyecto.

🆘 Problemas comunes

No aparece la ventana de gráficos → agregá plt.show() y/o matplotlib.use("TkAgg").

Valores “raros” al cuantificar → verificá xmin/xmax y aplica np.clip.

ImportError de módulos → ejecutá desde la raíz del repo o ajustá PYTHONPATH.