import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. INPUT DATA & MODEL (SATURATION GROWTH: y = alpha*x / (beta + x))
# =========================================================================
# Data Contoh (Gunakan data dari Pertemuan 9.xlsx - Saturation Growth Rate.csv Anda)
# Pastikan tidak ada nilai x=0 atau y=0
# x_i = np.array([1, 2, 3, 4, 5, 6, 7]) 
# y_i = np.array([0.5, 0.8, 1.0, 1.1, 1.2, 1.25, 1.28]) # Data Y asli (contoh)

x_i = np.array([2, 4, 6, 8, 10])
y_i = np.array([4, 5.71, 6.67, 7.27, 7.69])
n = len(y_i)

# --- TAHAP LINEARISASI (Transformasi x dan y) ---
# X = 1/x  ;  Y = 1/y
# Model Linear: Y = A0 + A1 * X
try:
    X_i = 1 / x_i 
    Y_i = 1 / y_i 
except ZeroDivisionError:
    print("Error: Terdapat nilai x=0 atau y=0 dalam data yang akan menyebabkan pembagian nol.")
    exit()

# --- DEFINISI FUNGSI BASIS (Matriks [Z]) ---
# z0 = 1 (untuk koefisien A0)
# z1 = X = 1/x (untuk koefisien A1)
z_0 = np.ones_like(X_i)
z_1 = X_i
Z = np.stack([z_0, z_1], axis=1)  # Matriks Z (n x 2)

# Vektor Y (sudah ditransformasi)
Y_vec = Y_i.reshape(-1, 1)

# =========================================================================
# 2. PERHITUNGAN KOEFISIEN LINEAR MENGGUNAKAN LEAST SQUARES (G-LS)
# =========================================================================
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y_vec

try:
    A = np.linalg.inv(Z_T_Z) @ Z_T_Y
except np.linalg.LinAlgError:
    print("Error: Matriks Singular.")
    exit()

# Ambil hasil koefisien Linear [A0, A1]
A_linear = A.flatten()
A0 = A_linear[0] # A0 = 1/alpha
A1 = A_linear[1] # A1 = beta/alpha

# =========================================================================
# 3. TRANSFORMASI KOEFISIEN KEMBALI KE BENTUK NON-LINEAR
# =========================================================================
# alpha = 1 / A0
# beta = A1 * alpha
alpha = 1 / A0
beta = A1 * alpha 

# Nilai prediksi model pada y ASLI: y_model = alpha * x / (beta + x)
y_model = (alpha * x_i) / (beta + x_i)

# =========================================================================
# 4. ANALISIS KUALITAS REGRESI LENGKAP (Diukur pada data ASLI y_i)
# =========================================================================
m_vars = Z.shape[1] 

# --- METRIK BERDASARKAN DATA ASLI (y_i) ---
y_bar = np.mean(y_i)
St_y = np.sum((y_i - y_bar)**2) 
Sr_y = np.sum((y_i - y_model)**2) 

# Koefisien Determinasi ASLI (r^2)
r2_asli = (St_y - Sr_y) / St_y
r_asli = np.sqrt(r2_asli)

# Standar Error Estimasi ASLI (Sy/x)
Sy_x_asli = np.sqrt(Sr_y / (n - m_vars))

# Standar Deviasi ASLI (Sy)
Sy_asli = np.sqrt(St_y / (n - 1))

# =========================================================================
# 5. HASIL OUTPUT & TABEL DETAIL
# =========================================================================
print("-" * 75)
print("HASIL REGRESI SATURATION GROWTH (y = alpha*x / (beta + x))")
print("-" * 75)

print(f"Koefisien Linear: A0 = {A0:.7f}, A1 = {A1:.7f}")
print(f"Koefisien Non-Linear: alpha = {alpha:.7f}, beta = {beta:.7f}")
print(f"\nPersamaan Regresi Final: y = {alpha:.4f} * x / ({beta:.4f} + x)")

print("-" * 75)
print("METRIK KUALITAS MODEL (Dihitung pada data ASLI 'y'):")
print(f"Sy (Standard Deviation Asli)    = {Sy_asli:.7f}")
print(f"Sy/x (Std Error Estimasi Asli)  = {Sy_x_asli:.7f}")
print(f"r^2 (Koef. Determinasi Asli)    = {r2_asli:.7f} ({r2_asli*100:.2f}%)")
print(f"r (Koef. Korelasi Asli)         = {r_asli:.7f}")

print("-" * 75)
# Membuat Tabel Menggunakan Pandas
df = pd.DataFrame({
    'xi_asli': x_i,
    'yi_asli': y_i,
    'Xi=1/xi': X_i,
    'Yi=1/yi': Y_i, 
    'y_pred_model': y_model,
    '(yi-ybar)^2': (y_i - y_bar)**2,
    '(yi-model)^2': (y_i - y_model)**2
})
sum_row = df.sum(numeric_only=True)
sum_row.name = 'Σ'
df_final = pd.concat([df, sum_row.to_frame().T])

print("TABEL DETAIL PERHITUNGAN:")
print(df_final.round(7).to_string())
print("-" * 75)