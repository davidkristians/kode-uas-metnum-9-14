import numpy as np
import pandas as pd
import math

# ==============================================================================
#  BAGIAN 1: INPUT DATA (BAGIAN INI YANG BISA DIUBAH SESUAI SOAL)
# ==============================================================================
print("=== REGRESI POWER / PANGKAT (y = alpha * x^beta) ===\n")

# 1. Masukkan Data X dan Y di sini:
# ##############################################################################
x_i = np.array([1, 2, 3, 4, 5])          # <--- UBAH DATA X DI SINI
y_i = np.array([0.5, 1.7, 3.4, 5.7, 8.4]) # <--- UBAH DATA Y DI SINI
# ##############################################################################

# ==============================================================================
#  BAGIAN 2: LINEARISASI DATA (Transformasi ke log10)
# ==============================================================================
# Model Power: y = alpha * x^beta
# Dilinear-kan menjadi: log(y) = beta * log(x) + log(alpha)
# Persamaan Linear: Y_baru = a1 * X_baru + a0
# Dimana: Y_baru = log10(y), X_baru = log10(x)
#         a1 (Slope) = beta
#         a0 (Intercept) = log10(alpha)

x_log = np.log10(x_i)  # Mengubah x menjadi log10(x)
y_log = np.log10(y_i)  # Mengubah y menjadi log10(y)

# Membentuk Matriks Z untuk Linear Regression
z_0 = np.ones_like(x_i)
z_1 = x_log  # Variabel bebasnya adalah log(x)

Z = np.stack([z_0, z_1], axis=1)
Y_matrix = y_log.reshape(-1, 1) # Targetnya adalah log(y)

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
#  BAGIAN 4: KONVERSI KEMBALI KE BENTUK POWER
# ==============================================================================
# Dari linearisasi: a0 = log10(alpha) --> alpha = 10^a0
#                   a1 = beta         --> beta = a1

log_alpha = a_linear[0]
beta = a_linear[1]
alpha = 10 ** log_alpha  # Gunakan basis 10 sesuai Excel

# ==============================================================================
#  BAGIAN 5: ANALISIS ERROR (Menggunakan Y ASLI vs Y PREDIKSI)
# ==============================================================================
# Prediksi menggunakan model power akhir: y = alpha * x^beta
y_pred = alpha * (x_i ** beta)

n = len(y_i)
y_bar = np.mean(y_i)

# Hitung komponen tabel detail
logx_logy = x_log * y_log
logx_sq = x_log ** 2
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
# Tabel 1: Perhitungan Linearisasi (Log-Log)
df_linear = pd.DataFrame({
    'xi': x_i,
    'yi': y_i,
    'log(xi)': x_log,
    'log(yi)': y_log,
    'logx.logy': logx_logy,
    '(logx)^2': logx_sq
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
print(f"Intercept Linear (log alpha) = {log_alpha:.7f}")
print(f"Slope Linear (beta)          = {beta:.7f}")
print("-" * 30)
print(f"NILAI ALPHA (10^intercept)   = {alpha:.7f}")
print(f"NILAI BETA                   = {beta:.7f}")
print(f"PERSAMAAN AKHIR              : y = {alpha:.4f} * x^({beta:.4f})")
print("-" * 60)

print("\n[TABEL 1] PERHITUNGAN LINEARISASI (LOG-LOG):")
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