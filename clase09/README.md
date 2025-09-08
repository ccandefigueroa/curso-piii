# Clase 09 — Transmisión PAM4 y diagrama de ojo 👁️📡

> **Ejercicio 16 — Secuencia extendida + Ojo PAM4 (normal y ampliado)**  
> Construir la señal transmitida para **PAM4** y obtener su **diagrama de ojo**, primero estándar y luego “ampliado” como la figura de referencia.

---

## 🎯 Objetivo
- Armar la **secuencia extendida** (tren de impulsos sobremuestreado).
- Transmitirla con un **pulso conformador** (raised-cosine).
- Graficar el **diagrama de ojo PAM4** (2 símbolos por traza).
- Hacer una versión **ampliada/zoom** (muchas trazas y baja opacidad) que se parezca a la imagen dada.

---

## ⚙️ Parámetros sugeridos
- **Baudios**: `fB = 32e9`  
- **Sobremuestreo**: `M = 8` (muestras por símbolo)  
- **Pulso TX (raised-cosine)**: `alpha = 0.1`, `L = 20` (longitud ±L símbolos)  
- **Símbolos**: `Nsym = 1000–3000`, **PAM4 niveles** = `{-3, -1, +1, +3}`  
- **Semilla**: fija si querés reproducibilidad

---

## 🧭 Pasos

### 1) Pulso del transmisor `g[n]` (raised-cosine)
- Generar \( g[n] \) a paso **T/M** sobre \(n\in[-L,\ L]\).
- Fórmula estándar:
  \[
  g(t)=\frac{\sin(\pi t/T)}{\pi t/T}\cdot \frac{\cos(\pi \alpha t/T)}{1-(2\alpha t/T)^2}
  \]
  y usar el **valor límite** en \(t/T=\pm\frac{1}{2\alpha}\) para evitar \(0/0\).
- **Normalizar** para que el pico sea 1 (opcional).  
- Verificar forma (lóbulo central y ceros en múltiplos de \(T\)).

---

### 2) Secuencia extendida (tren de impulsos)
- Crear un vector `xn` de longitud `Nsym * M` lleno de ceros.
- Cargar un símbolo cada **M** muestras: `xn[0::M] = symbols`.
- Comprobar con un **stem** de los primeros ~80 impulsos.

---

### 3) Transmisión
- Convolucionar: `yn = xn * g` (modo `"same"`).  
- Graficar **tiempo** (zoom ~**20 símbolos**) para ver la forma de onda.

---

### 4) Diagrama de ojo PAM4 (estándar)
- Ventana de **2 símbolos** por traza (`spans=2`, `Lseg = 2*M`).
- Saltar el transitorio: `start = L*M`.
- Tomar ventanas empezando en `start + k*M`, con `k = 0..K`.
- Superponer **~800–1000 trazas** con **alpha≈0.08–0.12**.
- Ejes sugeridos: `x ∈ [0, 2]` símbolos; `y ∈ [-3.5, 3.5]`.

---

### 5) Diagrama de ojo **ampliado**
- Aumentar **trazas** (1500–3000) y bajar **opacidad** (`alpha≈0.03–0.06`).
- Elegir **zoom** centrado: `xlim = (0.4, 1.6)` símbolos.
- Mantener `ylim = (-3.5, 3.5)` para ver los 4 niveles.
- Resultado esperado: ojo **denso/multicolor** similar a la imagen.

---
