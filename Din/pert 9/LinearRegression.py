import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. INPUT DATA & MODEL (REGRESI LINEAR SEDERHANA: y = a0 + a1*x)
# =========================================================================
# Data dari Pertemuan 9.xlsx - Linear.csv
x_i = np.array([1, 2, 3, 4, 5, 6, 7])
y_i = np.array([0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5])
n = len(y_i)

# --- DEFINISI FUNGSI BASIS (Matriks [Z]) ---
# z0 = 1 (untuk koefisien a0)
# z1 = x (untuk koefisien a1)
z_0 = np.ones_like(x_i)
z_1 = x_i
Z = np.stack([z_0, z_1], axis=1)  # Matriks Z berukuran n x 2

# Vektor Y
Y = y_i.reshape(-1, 1)

# =========================================================================
# 2. PERHITUNGAN KOEFISIEN MENGGUNAKAN LEAST SQUARES (G-LS)
#    Rumus: {A} = ([Z]T [Z])^-1 * [Z]T {Y}
# =========================================================================
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

# Menyelesaikan sistem persamaan linear
try:
    # Menggunakan np.linalg.solve() lebih disarankan daripada invers, 
    # tetapi invers juga benar untuk kasus matriks kecil ini.
    # Kita tetap menggunakan invers agar sesuai dengan langkah G-LS.
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
except np.linalg.LinAlgError:
    print("Error: Matriks Singular. Regresi tidak dapat diselesaikan.")
    A = np.zeros((Z.shape[1], 1))

# Ambil hasil koefisien [a0, a1, ...]
a = A.flatten()
a_0 = a[0]
a_1 = a[1]

# =========================================================================
# 3. ANALISIS KUALITAS REGRESI (ERROR)
# =========================================================================
# Nilai prediksi model: y_model = a0*z0 + a1*z1 + ...
y_model = Z @ A

# Rata-rata y
y_bar = np.mean(y_i)
m_vars = Z.shape[1] # Jumlah koefisien (a0, a1, ...)

# St (Total Sum of Squares)
St = np.sum((y_i - y_bar)**2)

# Sr (Sum of Squares of Residuals)
Sr = np.sum((y_i - y_model.flatten())**2)

# Koefisien Determinasi (r^2)
r2 = (St - Sr) / St
r = np.sqrt(r2)

# Standar Deviasi (Sy)
Sy = np.sqrt(St / (n - 1))

# Standar Error Estimasi (Sy/x)
Sy_x = np.sqrt(Sr / (n - m_vars))


# =========================================================================
# 4. HASIL OUTPUT & TABEL DETAIL
# =========================================================================
print("-" * 65)
print("HASIL REGRESI LINEAR (y = a0 + a1*x)")
print("-" * 65)

# Tampilkan Koefisien
print(f"Koefisien a0 (Intersep) = {a_0:.7f}")
print(f"Koefisien a1 (Slope)    = {a_1:.7f}")
print(f"\nPersamaan Regresi: y = {a_0:.4f} + {a_1:.4f} * x")

print("-" * 65)
print("ANALISIS KUALITAS REGRESI:")
print(f"Sy (Standard Deviation)     = {Sy:.7f}")
print(f"Sy/x (Std Error Estimasi)   = {Sy_x:.7f}")
print(f"Sr (Sum of Residuals)       = {Sr:.7f}")
print(f"r^2 (Koef. Determinasi)     = {r2:.7f} ({r2*100:.2f}%)")
print(f"r (Koef. Korelasi)          = {r:.7f}")

print("-" * 65)
# Membuat Tabel Menggunakan Pandas
df = pd.DataFrame({
    'xi': x_i,
    'yi': y_i,
    'xi.yi': x_i * y_i,
    'xi^2': x_i ** 2,
    'y_pred': y_model.flatten(),
    '(yi-ybar)^2': (y_i - y_bar)**2,
    '(yi-model)^2': (y_i - y_model.flatten())**2
})
sum_row = df.sum(numeric_only=True)
sum_row.name = 'Σ'
df_final = pd.concat([df, sum_row.to_frame().T])
print("TABEL DETAIL PERHITUNGAN:")
# Membulatkan hasil untuk tampilan
print(df_final.round(7).to_string())
print("-" * 65)