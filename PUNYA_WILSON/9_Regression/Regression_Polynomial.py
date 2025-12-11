import numpy as np
import pandas as pd
import math

# ==============================================================================
#  BAGIAN 1: INPUT DATA & MODEL (BAGIAN INI YANG BISA DIUBAH)
# ==============================================================================
print("=== REGRESI POLINOMIAL (y = a0 + a1*x + a2*x^2 + ...) ===\n")

# 1. Masukkan Data X dan Y di sini:
# ##############################################################################
x_i = np.array([0, 1, 2, 3, 4, 5])           # <--- UBAH DATA X DI SINI
y_i = np.array([2.1, 7.7, 13.6, 27.2, 40.9, 61.1]) # <--- UBAH DATA Y DI SINI
# ##############################################################################

# 2. Tentukan Derajat Polinomial (Orde)
# ##############################################################################
orde = 2   # Ubah jadi 2 untuk Kuadrat, 3 untuk Kubik, dst.
# ##############################################################################

# Membentuk Matriks Z secara Otomatis sesuai orde
# Jika orde=2, kolomnya: [1, x, x^2]
# Jika orde=3, kolomnya: [1, x, x^2, x^3]
Z_list = [np.ones_like(x_i)] # Kolom pertama selalu 1 (untuk a0)
for i in range(1, orde + 1):
    Z_list.append(x_i ** i)

Z = np.stack(Z_list, axis=1)
Y_matrix = y_i.reshape(-1, 1)

# ==============================================================================
#  BAGIAN 2: PERHITUNGAN MATRIKS (Mencari Koefisien a0, a1, a2...)
# ==============================================================================
# Rumus: {A} = ([Z]T [Z])^-1 * [Z]T {Y}
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y_matrix

try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
except np.linalg.LinAlgError:
    print("Error: Matriks Singular.")
    A = np.zeros((orde + 1, 1))

a = A.flatten() # Berisi [a0, a1, a2, ...]

# ==============================================================================
#  BAGIAN 3: ANALISIS ERROR
# ==============================================================================
# Prediksi menggunakan model polinomial
y_pred = np.zeros_like(y_i, dtype=float)
for i in range(len(a)):
    y_pred += a[i] * (x_i ** i)

n = len(y_i)
y_bar = np.mean(y_i)

# Komponen Error
yi_ybar_sq = (y_i - y_bar)**2      # (yi - y_rata)^2
yi_model_sq = (y_i - y_pred)**2    # Residual Kuadrat

# St (Total Sum of Squares)
St = np.sum(yi_ybar_sq)

# Sr (Sum of Squares of Residuals)
Sr = np.sum(yi_model_sq)

# Standar Deviasi (Sy)
Sy = math.sqrt(St / (n - 1))

# Standar Error Estimasi (Sy/x)
# Pembagi adalah n - (m + 1), dimana m adalah orde polinomial
# Contoh: Orde 2 (kuadrat) punya 3 koefisien (a0, a1, a2), jadi n - 3
Sy_x = math.sqrt(Sr / (n - (orde + 1)))

# Koefisien Determinasi (r^2)
r2 = (St - Sr) / St
r = math.sqrt(r2)

# ==============================================================================
#  BAGIAN 4: MENAMPILKAN HASIL
# ==============================================================================
# Tabel Detail
data = {'xi': x_i, 'yi': y_i}
# Tambahkan kolom x^pangkat
for i in range(1, orde + 1):
    data[f'xi^{i}'] = x_i ** i
data['y_pred'] = y_pred
data['(yi-ybar)^2'] = yi_ybar_sq
data['(yi-model)^2'] = yi_model_sq

df = pd.DataFrame(data)
sum_row = df.sum()
sum_row.name = 'SUM'
df = pd.concat([df, sum_row.to_frame().T])

print("-" * 60)
print(f"HASIL KOEFISIEN (Polinomial Orde {orde}):")
for i in range(len(a)):
    print(f"a_{i} = {a[i]:.7f}")

print("-" * 30)
eq_str = f"y = {a[0]:.4f}"
for i in range(1, len(a)):
    sign = "+" if a[i] >= 0 else ""
    eq_str += f" {sign} {a[i]:.4f}x^{i}"
print("PERSAMAAN AKHIR:")
print(eq_str)
print("-" * 60)

print("\n[TABEL DETAIL PERHITUNGAN]:")
print(df.round(5).to_string())

print("-" * 60)
print("STATISTIK ERROR:")
print(f"Sy (Standard Deviation)   = {Sy:.7f}")
print(f"Sy/x (Std Error Est)      = {Sy_x:.7f}")
print(f"r^2 (Determinasi)         = {r2:.7f} ({r2*100:.4f}%)")
print(f"r (Korelasi)              = {r:.7f}")
print("-" * 60)