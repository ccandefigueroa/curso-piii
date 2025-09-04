# Clase 05 — Audio, cuantificación y suavizado 🔊📦

> **Objetivo general:** trabajar con archivos de audio (WAV/MP3), visualizar **tiempo + frecuencia + espectrograma**, implementar un **cuantificador** uniforme y un **filtro EMA** (media móvil exponencial).  

---

## 📦 Contenidos
- **Ej. 9:** Cargar audio propio (WAV/MP3), obtener **fs**, **duración**, **canales** y **bits por muestra**; graficar **tiempo–frecuencia–espectrograma**.
- **Ej. 10:** **Cuantificación y distorsión**: cuantificador uniforme de `Nbits`, comparación en tiempo/espectro y **SNR** teórica vs. medida.
- **Ej. 11:** **Suavizado EMA** sobre audio grabado con micrófono; análisis de espectro y comparación visual.

---

### ✅ Ejercicio 9 — PASOS  (Audio WAV/MP3)
1) **Cargar** un archivo de audio propio (WAV o MP3).  
2) Publicar **fs**, **duración**, **canales** y **bits por muestra**.  
3) Graficar **tiempo**, **espectro** y **espectrograma** (`plot_tiempo_frecuencia_espectrograma`).  
4) Reproducir **WAV** y repetir con **MP3**; comentar diferencias.

---

### ✅ Ejercicio 10 — PASOS (Cuantificación y distorsión)
1) Generar seno **440 Hz**, **A=1**, **dur=2 s**, `fs=44100`.  
2) Implementar `cuantizar(x, Nbits, vmin, vmax)` para `Nbits ∈ {8, 4, 2}`.  
3) Graficar:  
   - **Zoom** a pocas ondas (original vs. cuantificada).  
   - **Error de cuantificación**.  
   - **Espectro** de la cuantificada.  
4) Calcular **SNR medida** y compararla con la **teórica**:  
   \(\mathrm{SNR}\approx 6.02\cdot Nbits + 1.76\ \mathrm{dB}\).

---

### ✅ Ejercicio 11 — PASOS (Suavizado EMA)
1) **Grabar** algunos segundos de audio.  
2) Aplicar **EMA** con \(\alpha = 0.6,\ 0.2,\ 0.05\).  
3) Graficar **original vs. filtrada** (zoom en tiempo) y **espectro**.  
4) Comentar efecto de \(\alpha\) en el **suavizado** (atenuación de altas y retardo)
