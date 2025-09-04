# Clase 06 — Modulación AM (AM-DSB) 🎙️📻

> **Ejercicio 12 — Multiplicación de señales: modulación de amplitud simple (DSB con portadora)**  
> Implementar una AM básica multiplicando una señal de mensaje por una portadora y analizarla en tiempo y frecuencia.

---

## 🎯 Objetivo
- Generar una **señal de mensaje** \(m(t)\) y una **portadora** \(c(t)\).
- Construir la **señal modulada**:
  \[
  y(t)=\big(1+m\,m(t)\big)\,c(t)
  \]
  donde \(m\) es el **índice de modulación**.
- Visualizar en la PC: **tiempo (zoom)**, **envolvente** y **espectro** (FFT hasta 8 kHz).
- Probar distintos **índices de modulación** y observar **sobremodulación** (\(m>1\)).

---

## 🧭 Pasos

1) **Definir señales**  
   - **Mensaje**: \(m(t)=\sin(2\pi f_m t)\) con \(f_m=200\ \text{Hz}\), amplitud 1.  
   - **Portadora**: \(c(t)=\sin(2\pi f_c t)\) con \(f_c=5\ \text{kHz}\), amplitud 1.

2) **Modulación AM (DSB-FC)**  
   - \( y(t)=\big(1+m\,m(t)\big)\,c(t) \)  
   - Probar \(m \in \{0.2,\ 0.8,\ 1.2\}\).

3) **Gráficos**  
   - **Mensaje** en el tiempo.  
   - **Portadora** (zoom corto).  
   - **Señal modulada** con **zoom ~20 ms**.  
   - **FFT** de la modulada hasta **8 kHz**.

4) **Análisis**  
   - Identificar **bandas laterales** en \(f_c\pm f_m\).  
   - Comparar amplitudes para distintos \(m\).  
   - Discutir **sobremodulación** cuando \(m>1\) (cambio de signo de la envolvente).

---

## ⚙️ Parámetros sugeridos
- Frecuencia de muestreo: `fs = 44100 Hz`  
- Duración: `dur = 0.05–0.1 s` (para ver bien el zoom)  
- Mensaje: `fm = 200 Hz`, amplitud `A_m = 1`  
- Portadora: `fc = 5000 Hz`, amplitud `A_c = 1`  
- Índice de modulación: `m = 0.2, 0.8, 1.2`

---

## 🔎 Resultados esperados
- Para **m < 1**: envolvente **no** se invierte; en el espectro aparecen picos en **fc**, **fc±fm**.  
- Para **m = 1**: envolvente toca cero.  
- Para **m > 1**: **sobremodulación** (inversión de envolvente) y distorsión; el espectro muestra mayor contenido fuera de las laterales ideales.

---

## ✨ Extras (opcionales)
- **AM DSB-SC (sin portadora)**: \(y(t)=m(t)\,c(t)\).  
- **SSB (banda lateral única)** con transformada de Hilbert:
  \[
  y_{\text{USB}}=m(t)\cos(2\pi f_c t)-\hat m(t)\sin(2\pi f_c t)
  \]
- Comparar espectros **DSB-FC**, **DSB-SC** y **SSB**.

---