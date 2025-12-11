import numpy as np
import pandas as pd
import math

# ==========================================
# 1. INPUT DATA (GANTI BAGIAN INI SAJA SAAT UJIAN)
# ==========================================
# Masukkan data x dan y dari soal
x_i = np.array([1, 2, 3, 4, 5, 6, 7])
y_i = np.array([0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5])

# Tentukan Model
# Untuk Linear (y = a0 + a1*x): Gunakan z_0 dan z_1
z_0 = np.ones_like(x_i)  # Selalu ada (untuk a0)
z_1 = x_i                # Variabel x (untuk a1)

# Gabungkan kolom-kolom z tadi
Z = np.stack([z_0, z_1], axis=1)

# ==========================================
# 2. PERHITUNGAN MATRIKS
# ==========================================
Y = y_i.reshape(-1, 1)
# Jika fungsi nya Y memakai perkalian maka ubahlah menjadi log
# Y = np.log10(y_i).reshape(-1, 1)
n = len(y_i)

# Rumus: {A} = ([Z]T [Z])^-1 * [Z]T {Y}
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
except np.linalg.LinAlgError:
    print("Error: Matriks Singular (tidak bisa diselesaikan). Cek data input.")
    A = np.zeros((Z.shape[1], 1))

# Ambil hasil koefisien
a = A.flatten()

# ==========================================
# 3. ANALISIS ERROR & TABEL DETAIL
# ==========================================
# Hitung nilai prediksi (y_model)
y_model = np.zeros_like(y_i, dtype=float)
for i in range(len(a)):
    y_model += a[i] * Z[:, i]

# Rata-rata y (y_bar)
y_bar = np.mean(y_i)

# Perhitungan kolom-kolom tambahan
xi_yi = x_i * y_i
xi_2 = x_i ** 2
yi_ybar_2 = (y_i - y_bar)**2      # (yi - y_rata)^2
yi_model_2 = (y_i - y_model)**2   # (yi - y_prediksi)^2 atau (yi - a0 - a1xi)^2

# St (Total Sum of Squares)
St = np.sum(yi_ybar_2)

# Sr (Sum of Squares of Residuals)
Sr = np.sum(yi_model_2)

# Koefisien Determinasi (r^2)
r2 = (St - Sr) / St
r = math.sqrt(r2) if r2 >= 0 else 0

# Standar Error Estimasi (Sy/x)
m_vars = Z.shape[1] 
Sy_x = math.sqrt(Sr / (n - m_vars))

# Standar Deviasi (Sy)
# Rumus: sqrt( Sigma(yi - ybar)^2 / (n - 1) )
Sy = math.sqrt(St / (n - 1))

# Membuat Tabel Menggunakan Pandas agar rapi
df = pd.DataFrame({
    'xi': x_i,
    'yi': y_i,
    'xi.yi': xi_yi,
    'xi^2': xi_2,
    'y_pred': y_model,
    '(yi-ybar)^2': yi_ybar_2,
    '(yi-model)^2': yi_model_2
})

# Menambahkan Baris Total (Sum)
sum_row = df.sum()
sum_row.name = 'SUM'
df = pd.concat([df, sum_row.to_frame().T])

# ==========================================
# 4. HASIL OUTPUT
# ==========================================
print("-" * 60)
print("HASIL PERHITUNGAN REGRESI")
print("-" * 60)

# Print Koefisien
for i in range(len(a)):
    print(f"a_{i} = {a[i]:.7f}")

print("-" * 60)
print("PERSAMAAN:")
eq_str = f"y = {a[0]:.4f}"
for i in range(1, len(a)):
    sign = "+" if a[i] >= 0 else ""
    eq_str += f" {sign} {a[i]:.4f} * x" if i == 1 else f" {sign} {a[i]:.4f} * x^{i}"
print(eq_str)

print("-" * 60)
print("TABEL DETAIL PERHITUNGAN:")
print(df.round(5).to_string()) # Menampilkan tabel dengan pembulatan 5 desimal
print("-" * 60)

print("ANALISIS ERROR:")
print(f"Sy (Standard Deviation)  = {Sy:.7f}")
print(f"Sy/x (Std Error Est)     = {Sy_x:.7f}")
print(f"Sr (Sum of Residuals)    = {Sr:.7f}")
print(f"r^2 (Determinasi)        = {r2:.7f} ({r2*100:.2f}%)")
print(f"r (Korelasi)             = {r:.7f}")
print("-" * 60)