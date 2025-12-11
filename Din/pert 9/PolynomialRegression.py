import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. INPUT DATA & MODEL (POLINOMIAL ORDE M: y = a0 + a1*x + ... + am*x^m)
# =========================================================================
# Data Contoh (Gunakan data dari Pertemuan 9.xlsx - Polynomial.csv Anda)
# x_i = np.array([1, 2, 3, 4, 5, 6, 7]) 
# y_i = np.array([0.5, 2.5, 2.0, 4.0, 3.5, 6.0, 5.5]) # Data Y asli

x_i = np.array([0, 1, 2, 3, 4, 5])
y_i = np.array([2.1, 7.7, 13.6, 27.2, 40.9, 61.1])
n = len(y_i)

# --- TENTUKAN ORDE POLINOMIAL YANG DIINGINKAN (M) ---
# Misalnya, Polinomial Orde 2 (Kuadratik)
M = 2 
# Jika M=1, akan menjadi Regresi Linear biasa.

# =========================================================================
# 2. PEMBENTUKAN MATRIKS [Z]
# --- Konsep: [Z] terdiri dari kolom [1, x, x^2, ..., x^M]
# =========================================================================

# Matriks Z harus memiliki n baris dan M+1 kolom (untuk a0 sampai aM)
Z = np.zeros((n, M + 1)) 

# Isi kolom Matriks Z:
for j in range(M + 1):
    Z[:, j] = x_i ** j  # Kolom j diisi dengan x^j

# Vektor Y 
Y = y_i.reshape(-1, 1)

# =========================================================================
# 3. PERHITUNGAN KOEFISIEN MENGGUNAKAN LEAST SQUARES (G-LS)
#    Rumus: {A} = ([Z]T [Z])^-1 * [Z]T {Y}
# =========================================================================
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

print("Matriks [Z]T[Z] (Sistem Persamaan):")
print(Z_T_Z.round(4))
print("\nVektor [Z]T{Y} (Sisi Kanan):")
print(Z_T_Y.round(4))

try:
    # Menggunakan np.linalg.solve() lebih cepat dan akurat daripada invers
    A = np.linalg.solve(Z_T_Z, Z_T_Y)
except np.linalg.LinAlgError:
    print("Error: Matriks Singular (mungkin orde terlalu tinggi atau data terlalu sedikit).")
    exit()

# Ambil hasil koefisien [a0, a1, ..., aM]
a = A.flatten()
m_vars = M + 1 # Jumlah variabel/koefisien

# =========================================================================
# 4. ANALISIS KUALITAS REGRESI LENGKAP
# =========================================================================

# Nilai prediksi model: y_model = Z @ A
y_model = Z @ A

# --- METRIK BERDASARKAN DATA ASLI (y_i) ---
y_bar = np.mean(y_i)
St_y = np.sum((y_i - y_bar)**2) 
Sr_y = np.sum((y_i - y_model.flatten())**2) 

# Koefisien Determinasi (r^2)
r2_asli = (St_y - Sr_y) / St_y
r_asli = np.sqrt(r2_asli)

# Standar Error Estimasi (Sy/x)
Sy_x_asli = np.sqrt(Sr_y / (n - m_vars))

# Standar Deviasi (Sy)
Sy_asli = np.sqrt(St_y / (n - 1))


# =========================================================================
# 5. HASIL OUTPUT & TABEL DETAIL
# =========================================================================
print("-" * 70)
print(f"HASIL REGRESI POLINOMIAL ORDE {M}")
print("-" * 70)

# Tampilkan Koefisien
for i in range(M + 1):
    print(f"Koefisien a{i} = {a[i]:.7f}")

# Persamaan
eq_str = f"y = {a[0]:.4f}"
for i in range(1, M + 1):
    sign = " + " if a[i] >= 0 else " - "
    val = abs(a[i])
    if i == 1:
        eq_str += f"{sign}{val:.4f}x"
    else:
        eq_str += f"{sign}{val:.4f}x^{i}"
print(f"\nPersamaan Regresi Final: {eq_str}")

print("-" * 70)
print("METRIK KUALITAS MODEL:")
print(f"Sy (Standard Deviation Asli)    = {Sy_asli:.7f}")
print(f"Sy/x (Std Error Estimasi Asli)  = {Sy_x_asli:.7f}")
print(f"r^2 (Koef. Determinasi Asli)    = {r2_asli:.7f} ({r2_asli*100:.2f}%)")
print(f"r (Koef. Korelasi Asli)         = {r_asli:.7f}")
print("-" * 70)

# Membuat Tabel Menggunakan Pandas
df = pd.DataFrame({
    'xi': x_i,
    'yi_asli': y_i,
    'y_pred_model': y_model.flatten(),
    '(yi-ybar)^2': (y_i - y_bar)**2,
    '(yi-model)^2': (y_i - y_model.flatten())**2
})
sum_row = df.sum(numeric_only=True)
sum_row.name = 'Σ'
df_final = pd.concat([df, sum_row.to_frame().T])

print("TABEL DETAIL PERHITUNGAN:")
print(df_final.round(7).to_string())
print("-" * 70)