import numpy as np
import pandas as pd
import math

# ==============================================================================
#  BAGIAN 1: INPUT DATA (BAGIAN INI YANG BISA DIUBAH SESUAI SOAL)
# ==============================================================================
print("=== REGRESI EKSPONENSIAL (y = alpha * e^(beta * x)) ===\n")

# 1. Masukkan Data X dan Y di sini:
# ##############################################################################
x_i = np.array([2, 3, 4, 5, 6])          # <--- UBAH DATA X DI SINI
y_i = np.array([2.47, 3.18, 4.08, 5.24, 6.72]) # <--- UBAH DATA Y DI SINI
# ##############################################################################

# ==============================================================================
#  BAGIAN 2: LINEARISASI DATA (Transformasi ke ln(y))
# ==============================================================================
# Model Eksponensial: y = alpha * e^(beta * x)
# Dilinear-kan menjadi: ln(y) = ln(alpha) + beta * x
# Jadi: Y_baru = a0 + a1 * x
# Dimana: Y_baru = ln(y), a0 = ln(alpha), a1 = beta

y_log = np.log(y_i)  # Mengubah y menjadi ln(y)

# Membentuk Matriks Z untuk Linear Regression (menggunakan data yang sudah di-log)
z_0 = np.ones_like(x_i)
z_1 = x_i

Z = np.stack([z_0, z_1], axis=1)
Y_matrix = y_log.reshape(-1, 1) # Targetnya adalah ln(y), bukan y asli

# ==============================================================================
#  BAGIAN 3: PERHITUNGAN MATRIKS (Mencari Koefisien)
# ==============================================================================
# Rumus: {A} = ([Z]T [Z])^-1 * [Z]T {Y}
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y_matrix

try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
except np.linalg.LinAlgError:
    print("Error: Matriks Singular.")
    A = np.zeros((2, 1))

a_linear = A.flatten() # a0 (intercept linear) dan a1 (slope linear)

# ==============================================================================
#  BAGIAN 4: KONVERSI KEMBALI KE BENTUK EKSPONENSIAL
# ==============================================================================
# Dari linearisasi: a0 = ln(alpha)  --> alpha = e^a0
#                   a1 = beta       --> beta = a1

ln_alpha = a_linear[0]
beta = a_linear[1]
alpha = np.exp(ln_alpha)

# ==============================================================================
#  BAGIAN 5: ANALISIS ERROR (Menggunakan Y ASLI vs Y PREDIKSI)
# ==============================================================================
# Prediksi menggunakan model eksponensial akhir
y_pred = alpha * np.exp(beta * x_i)

n = len(y_i)
y_bar = np.mean(y_i)

# Hitung komponen tabel detail
xi_sq = x_i ** 2
xi_lny = x_i * y_log
yi_ybar_sq = (y_i - y_bar)**2      # (yi - y_rata)^2
yi_model_sq = (y_i - y_pred)**2    # (yi - y_prediksi_asli)^2 (Residual Kuadrat)

# St (Total Sum of Squares)
St = np.sum(yi_ybar_sq)

# Sr (Sum of Squares of Residuals)
Sr = np.sum(yi_model_sq)

# Standar Deviasi (Sy)
Sy = math.sqrt(St / (n - 1))

# Standar Error Estimasi (Sy/x)
# Variabel bebas = 2 (alpha dan beta), jadi pembagi n - 2
Sy_x = math.sqrt(Sr / (n - 2))

# Koefisien Determinasi (r^2)
r2 = (St - Sr) / St
r = math.sqrt(r2)

# ==============================================================================
#  BAGIAN 6: MENAMPILKAN TABEL DAN HASIL
# ==============================================================================
# Tabel 1: Perhitungan Linearisasi (Untuk mencari koefisien)
df_linear = pd.DataFrame({
    'xi': x_i,
    'yi': y_i,
    'ln(yi)': y_log,
    'xi.ln(yi)': xi_lny,
    'xi^2': xi_sq
})
sum_lin = df_linear.sum()
sum_lin.name = 'SUM'
df_linear = pd.concat([df_linear, sum_lin.to_frame().T])

# Tabel 2: Perhitungan Error (Berdasarkan model akhir)
df_error = pd.DataFrame({
    'xi': x_i,
    'yi': y_i,
    'y_pred': y_pred,
    '(yi-ybar)^2': yi_ybar_sq,
    '(yi-y_pred)^2': yi_model_sq
})
sum_err = df_error.sum()
sum_err.name = 'SUM'
df_error = pd.concat([df_error, sum_err.to_frame().T])

print("-" * 60)
print("HASIL KOEFISIEN:")
print(f"Intercept Linear (ln alpha) = {ln_alpha:.7f}")
print(f"Slope Linear (beta)         = {beta:.7f}")
print("-" * 30)
print(f"NILAI ALPHA (e^intercept)   = {alpha:.7f}")
print(f"NILAI BETA                  = {beta:.7f}")
print(f"PERSAMAAN AKHIR             : y = {alpha:.4f} * e^({beta:.4f} * x)")
print("-" * 60)

print("\n[TABEL 1] PERHITUNGAN LINEARISASI (Untuk mencari a & b):")
print(df_linear.round(5).to_string())

print("\n[TABEL 2] ANALISIS ERROR (Menggunakan Y asli):")
print(df_error.round(5).to_string())

print("-" * 60)
print("STATISTIK ERROR:")
print(f"Sy (Standard Deviation)   = {Sy:.7f}")
print(f"Sy/x (Std Error Est)      = {Sy_x:.7f}")
print(f"r^2 (Determinasi)         = {r2:.7f} ({r2*100:.4f}%)")
print(f"r (Korelasi)              = {r:.7f}")
print("-" * 60)