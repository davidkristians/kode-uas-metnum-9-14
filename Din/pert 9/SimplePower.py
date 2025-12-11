import numpy as np
import pandas as pd
import math

# Pilihan logaritma: Kita gunakan np.log10 (log basis 10) karena umum di Power Model.
LOG_BASE = np.log10 

# =========================================================================
# 1. INPUT DATA & MODEL (SIMPLE POWER: y = alpha * x^beta)
# =========================================================================
# Data Contoh (Gunakan data dari Pertemuan 9.xlsx - Simple Power.csv Anda)
# x_i = np.array([1, 2, 3, 4, 5, 6, 7]) 
# y_i = np.array([0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5]) # Data Y asli (contoh)
x_i = np.array([1, 2, 3, 4, 5])
y_i = np.array([0.5, 1.7, 3.4, 5.7, 8.4])
n = len(y_i)

# --- TAHAP LINEARISASI (Transformasi x dan y) ---
# X = log(x)  ;  Y = log(y)
# Model Linear: Y = A0 + A1 * X
try:
    X_i = LOG_BASE(x_i) 
    Y_i = LOG_BASE(y_i) 
except Exception as e:
    print(f"Error: Data x dan y harus positif untuk logaritma. ({e})")
    exit()

# --- DEFINISI FUNGSI BASIS (Matriks [Z]) ---
# z0 = 1 (untuk koefisien A0)
# z1 = X (untuk koefisien A1)
z_0 = np.ones_like(X_i)
z_1 = X_i
Z = np.stack([z_0, z_1], axis=1)  # Matriks Z (n x 2)

# Vektor Y (sudah ditransformasi)
Y_vec = Y_i.reshape(-1, 1)

# =========================================================================
# 2. PERHITUNGAN KOEFISIEN LINEAR MENGGUNAKAN LEAST SQUARES (G-LS)
#    Rumus: {A} = ([Z]T [Z])^-1 * [Z]T {Y_vec}
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
A0 = A_linear[0]
A1 = A_linear[1]

# =========================================================================
# 3. TRANSFORMASI KOEFISIEN KEMBALI KE BENTUK NON-LINEAR
# =========================================================================
# Hubungan: A0 = log(alpha)  ;  A1 = beta
beta = A1 
alpha = 10**A0 # Jika menggunakan log10, maka alpha = 10^(A0)

# Nilai prediksi model pada y ASLI: y_model = alpha * x^beta
y_model = alpha * (x_i ** beta)

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
print("HASIL REGRESI SIMPLE POWER (y = alpha * x^beta)")
print("-" * 75)

print(f"Koefisien Linear: A0 = {A0:.7f}, A1 = {A1:.7f}")
print(f"Koefisien Non-Linear: alpha = {alpha:.7f}, beta = {beta:.7f}")
print(f"\nPersamaan Regresi Final: y = {alpha:.4f} * x^({beta:.4f})")

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
    'Xi=log(xi)': X_i,
    'Yi=log(yi)': Y_i, 
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