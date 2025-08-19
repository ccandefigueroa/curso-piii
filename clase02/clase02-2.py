import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# PARÁMETROS GENERALES
# =========================================================
N_MUESTRAS_COS = 50   # cantidad de muestras para cos(n)
M = 12                # muestras por período para la senoidal discreta
CICLOS = 3            # cuántos períodos mostrar en la senoidal

# =========================================================
# PARTE 1: y = cos(n) para n = 0..49, con negativos -> 0
# =========================================================
n = np.arange(N_MUESTRAS_COS)        # n = [0, 1, 2, ..., 49]
y = np.cos(n)                        # coseno en radianes evaluado en enteros
y_trunc = np.where(y < 0, 0.0, y)    # reemplazo vectorizado de negativos por 0

# (Opcional) métricas rápidas:
num_negativos = np.sum(y < 0)
porcentaje_negativos = 100.0 * num_negativos / N_MUESTRAS_COS

print("=== PARTE 1: cos(n) con negativos reemplazados por 0 ===")
print(f"Primeros {N_MUESTRAS_COS} n: {n.tolist()}")
print(f"Cantidad de negativos en cos(n): {num_negativos} ({porcentaje_negativos:.1f}%)")
print("Vector resultante (y_trunc):")
np.set_printoptions(precision=4, suppress=True)
print(y_trunc, "\n")

# =========================================================
# PARTE 2: Secuencia senoidal con 12 muestras por ciclo
# =========================================================
# Fórmula: x[k] = sin(2π * k / M)  -> exactamente M muestras por período
k = np.arange(0, M * CICLOS)         # índices de muestra para CICLOS períodos
x = np.sin(2 * np.pi * k / M)

print("=== PARTE 2: Seno discreto con 12 muestras por ciclo ===")
print(f"Muestras por ciclo (M): {M}")
print(f"Ciclos mostrados: {CICLOS}")
print(f"Longitud de la secuencia x: {len(x)}\n")

# =========================================================
# G R Á F I C A S
# =========================================================

# ----- Figura A: cos(n) vs cos(n) truncado -----
plt.figure(figsize=(12, 4))
# Graficamos ambas para comparar fácilmente:
plt.stem(n, y, linefmt='C0-', markerfmt='C0o', basefmt='r-', label='cos(n)', use_line_collection=True)
plt.stem(n, y_trunc, linefmt='C2-', markerfmt='C2s', basefmt='r-', label='cos(n) truncado (negativos→0)', use_line_collection=True)
plt.title(f"cos(n) para n=0..{N_MUESTRAS_COS-1} (comparación original vs truncado)")
plt.xlabel("n")
plt.ylabel("valor")
plt.grid(True, alpha=0.3)
plt.legend(loc="upper right")
plt.tight_layout()

# ----- Figura B: Senoidal con 12 muestras por ciclo -----
plt.figure(figsize=(12, 4))
plt.stem(k, x, linefmt='C1-', markerfmt='C1o', basefmt='r-', use_line_collection=True)
plt.title(f"Seno discreto con {M} muestras por ciclo — {CICLOS} ciclos (longitud = {len(x)})")
plt.xlabel("k (muestras)")
plt.ylabel("amplitud")
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ----- Figura C (resumen): dos subplots juntos -----
fig, axs = plt.subplots(2, 1, figsize=(12, 7), sharex=False)
# Subplot 1: cos(n) truncado
axs[0].stem(n, y_trunc, linefmt='C3-', markerfmt='C3o', basefmt='r-', use_line_collection=True)
axs[0].set_title(f"(Resumen) cos(n) truncado a 0 cuando es negativo — n=0..{N_MUESTRAS_COS-1}")
axs[0].set_xlabel("n")
axs[0].set_ylabel("valor")
axs[0].grid(True, alpha=0.3)

# Subplot 2: senoidal M-muestras/ciclo
axs[1].stem(k, x, linefmt='C4-', markerfmt='C4o', basefmt='r-', use_line_collection=True)
axs[1].set_title(f"(Resumen) Seno discreto con {M} muestras por ciclo — {CICLOS} ciclos")
axs[1].set_xlabel("k (muestras)")
axs[1].set_ylabel("amplitud")
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
