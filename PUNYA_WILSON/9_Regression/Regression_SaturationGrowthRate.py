import numpy as np
import pandas as pd
import math

# ==============================================================================
#  BAGIAN 1: INPUT DATA (BAGIAN INI YANG BISA DIUBAH SESUAI SOAL)
# ==============================================================================
print("=== SATURATION GROWTH RATE REGRESSION (y = alpha * x / (beta + x)) ===\n")

# 1. Masukkan Data X dan Y di sini:
# ##############################################################################
x_i = np.array([2, 4, 6, 8, 10])           # <--- UBAH DATA X DI SINI
y_i = np.array([4, 5.71, 6.67, 7.27, 7.69]) # <--- UBAH DATA Y DI SINI
# ##############################################################################

# ==============================================================================
#  BAGIAN 2: LINEARISASI DATA (Transformasi ke 1/y dan 1/x)
# ==============================================================================
# Model Saturation: y = (alpha * x) / (beta + x)
# Dilinear-kan menjadi: 1/y = (beta/alpha) * (1/x) + (1/alpha)
# Persamaan Linear: Y_baru = a1 * X_baru + a0
# Dimana: Y_baru = 1/y, X_baru = 1/x
#         a1 (Slope)     = beta / alpha
#         a0 (Intercept) = 1 / alpha

x_inv = 1 / x_i  # Mengubah x menjadi 1/x
y_inv = 1 / y_i  # Mengubah y menjadi 1/y

# Membentuk Matriks Z untuk Linear Regression
z_0 = np.ones_like(x_i)
z_1 = x_inv  # Variabel bebasnya adalah 1/x

Z = np.stack([z_0, z_1], axis=1)
Y_matrix = y_inv.reshape(-1, 1) # Targetnya adalah 1/y

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

a_linear = A.flatten() 

# ==============================================================================
#  BAGIAN 4: KONVERSI KEMBALI KE BENTUK ASLI
# ==============================================================================
# Dari linearisasi: 
# a0 = 1/alpha      --> alpha = 1 / a0
# a1 = beta/alpha   --> beta = a1 * alpha

intercept_val = a_linear[0] # a0
slope_val = a_linear[1]     # a1

alpha = 1 / intercept_val
beta = slope_val * alpha

# ==============================================================================
#  BAGIAN 5: ANALISIS ERROR (Menggunakan Y ASLI vs Y PREDIKSI)
# ==============================================================================
# Prediksi menggunakan model saturation akhir: y = (alpha * x) / (beta + x)
y_pred = (alpha * x_i) / (beta + x_i)

n = len(y_i)
y_bar = np.mean(y_i)

# Hitung komponen tabel detail
xinv_yinv = x_inv * y_inv
xinv_sq = x_inv ** 2
yi_ybar_sq = (y_i - y_bar)**2      # (yi - y_rata)^2
yi_model_sq = (y_i - y_pred)**2    # (yi - y_prediksi_asli)^2

# St (Total Sum of Squares)
St = np.sum(yi_ybar_sq)

# Sr (Sum of Squares of Residuals)
Sr = np.sum(yi_model_sq)

# Standar Deviasi (Sy)
Sy = math.sqrt(St / (n - 1))

# Standar Error Estimasi (Sy/x)
# Variabel bebas = 2 (alpha dan beta)
Sy_x = math.sqrt(Sr / (n - 2))

# Koefisien Determinasi (r^2)
r2 = (St - Sr) / St
r = math.sqrt(r2)

# ==============================================================================
#  BAGIAN 6: MENAMPILKAN TABEL DAN HASIL
# ==============================================================================
# Tabel 1: Perhitungan Linearisasi (1/x vs 1/y)
df_linear = pd.DataFrame({
    'xi': x_i,
    'yi': y_i,
    '1/xi': x_inv,
    '1/yi': y_inv,
    '(1/xi).(1/yi)': xinv_yinv,
    '(1/xi)^2': xinv_sq
})
sum_lin = df_linear.sum()
sum_lin.name = 'SUM'
df_linear = pd.concat([df_linear, sum_lin.to_frame().T])

# Tabel 2: Perhitungan Error (Model Asli)
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
print(f"Intercept Linear (1/alpha)  = {intercept_val:.7f}")
print(f"Slope Linear (beta/alpha)   = {slope_val:.7f}")
print("-" * 30)
print(f"NILAI ALPHA (1/intercept)   = {alpha:.7f}")
print(f"NILAI BETA (slope * alpha)  = {beta:.7f}")
print(f"PERSAMAAN AKHIR             : y = ({alpha:.4f} * x) / ({beta:.4f} + x)")
print("-" * 60)

print("\n[TABEL 1] PERHITUNGAN LINEARISASI (1/x vs 1/y):")
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