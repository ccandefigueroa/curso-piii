# Clase 04 — Muestreo, Nyquist y *aliasing* ⚡📉

> **Ejercicio 8 — Comparación de muestreo sub-Nyquist y sobre-Nyquist**  
> Generar una señal compuesta, muestrearla a distintas frecuencias y observar el **aliasing** en tiempo y frecuencia.

---

## 🎯 Objetivo
- Generar una **señal compuesta** por varias frecuencias.
- Muestrearla a tres **frecuencias de muestreo**:  
  una **inferior**, una **igual (≈)** y una **superior** a \(2\cdot f_{\max}\).
- Observar y **comparar visualmente** el **aliasing**.

---

## 🗂️ Estructura sugerida

## 🟢 Ejercicio 8 — Pasos

1) **Señal compuesta de 3 senoidales**  
   - Frecuencias bien separadas (ejemplo): **300 Hz**, **800 Hz**, **1500 Hz**.  
   - Duración: **1 s**.  
   - Frecuencia de muestreo de referencia (alta): `fs_ref = 44100 Hz`.

2) **Remuestrear a tres casos**  
   - `fs_bajo   < 2·f_max`  *(sub-Nyquist)*  
   - `fs_limite ≈ 2·f_max`  
   - `fs_alto   > 2·f_max`  *(sobre-Nyquist)*  

   Con `f_max = 1500 Hz` ⇒ `2·f_max = 3000 Hz`.  
   **Ejemplo de elección:** `fs_bajo = 2200 Hz`, `fs_limite = 3000 Hz`, `fs_alto = 8000 Hz`.

3) **Graficar para cada caso**  
   - Señal en **tiempo** (zoom a **20 ms**).  
   - **FFT** hasta **2 kHz**.

4) **Discutir aliasing**  
   - ¿Qué componentes se **pliegan**?  
   - ¿Cómo cambian los **picos** en el espectro?  
   - ¿Qué se ve en **tiempo** cuando hay aliasing?
