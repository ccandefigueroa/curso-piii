# Clase 07 — Media móvil simple, Tonos de Shepard y Pulsación 🎚️🎶

> En esta clase trabajamos con el **filtro de media móvil simple (SMA)**, lo comparamos con la **media móvil exponencial (EMA)**, generamos y analizamos **Tonos de Shepard**, y exploramos la **pulsación (beats)**.

---

## 🧠 Recordatorio — Simple Moving Average (SMA)

Ecuación en diferencias para ventana deslizante de tamaño `W`:

\[
y[n] = y[n-1] + \frac{1}{W}\,\big(x[n] - x[n-W]\big)
\]

- `W`: tamaño de la ventana.  
- `y[n]`: salida actual.  
- `y[n-1]`: salida anterior.  
- `x[n]`: entrada actual.  
- `x[n-W]`: muestra que sale de la ventana.

> El SMA es **pasabajos**: suaviza promediando y atenúa cambios rápidos (altas frecuencias).

---

## 🎯 Objetivo
- Implementar el **SMA** con varios tamaños de ventana y **compararlo** con un **EMA**.
- Analizar **tiempo** y **frecuencia** para notar el suavizado.
- Crear **Tonos de Shepard** (ilusión auditiva) y **señales con pulsación (beats)**.
- Relacionar percepción auditiva con medidas en el dominio temporal/espectral.

---

## 🟩 Ejercicio 13 — SMA vs EMA

1) **Implementar SMA**  
   - Probar `W ∈ {5, 25, 100}` sobre una señal (p.ej., seno 440 Hz + ruido blanco).

2) **Comparar con EMA**  
   - Usar `α ∈ {0.6, 0.2, 0.05}`.  
   - Discutir: menor `α` ⇒ mayor **suavizado** (y más **retardo**).

3) **Analizar**  
   - **Tiempo**: superponer original y filtrada (zoom a pocas ondas).  
   - **Frecuencia**: FFT y observar atenuación de altas.

4) **Conclusión**  
   - ¿Qué combinación `W`/`α` funcionó mejor para tu señal?

---

## 🎼 Tonos de Shepard

**Idea:** combinación de senoidales separadas por octavas con envolventes que atenúan los extremos (graves y agudos). Al reproducir una secuencia, se crea la **ilusión** de un tono que **sube/baja indefinidamente**.

**Pasos**
1) Definir función `generate_shepard_tone(base_freq, num_tones, duration, sample_rate)` que sume componentes en octavas.  
2) Construir una **escala** (ascendente y/o descendente) con esos tonos.  
3) Visualizar **tiempo**, **espectro** y **espectrograma**.  
4) Reproducir y comentar la percepción (ilusión de altura sin cambio real dominante en frecuencia).

---

## 🟦 Ejercicio 14 — Variaciones de escala

- Modificar parámetros: `num_tones`, `base_freq`, `steps`, **fs**, **duración por tono**.  
- Implementar una **versión descendente**.  
- Graficar señal, **FFT** y **espectrograma**; anotar cómo cambian las sensaciones de continuidad/altura.

---

## 💓 Pulsación (Beats)

La **pulsación** ocurre al sumar dos senos de frecuencias cercanas:

\[
x(t)=\sin(2\pi f_1 t)+\sin(2\pi f_2 t)
\quad\Rightarrow\quad
\text{envolvente a } f_b=|f_2-f_1|
\]

**Pasos**
1) Generar beats con \(f_1=440\ \text{Hz}\) y \(f_2=442\ \text{Hz}\) (o variantes).  
2) Visualizar un **fragmento** en tiempo (zoom) y reproducir audio.  
3) Calcular/mostrar **FFT**; relacionar \(f_b\) con la oscilación de la amplitud (no un pico nuevo dominante).  
4) Probar con frecuencias más alejadas: los beats se **aceleran** y luego desaparecen perceptualmente.

---
