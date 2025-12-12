import numpy as np
import pandas as pd
import math

# Atur presisi output
np.set_printoptions(precision=7, suppress=True)

# =========================================================================
# 1. INPUT DATA & MODEL (MLR: y = a0 + a1*x1 + a2*x2)
# =========================================================================
# Data Contoh (Ambil dari Pertemuan 10.xlsx - Multiple Linear Regresi 1.csv)
# x1_i = np.array([0, 1, 1, 2, 2, 3]) 
# x2_i = np.array([0, 0, 1, 1, 2, 2])
# y_i = np.array([1, 1.2, 2.2, 2.5, 3.8, 3.5])

# data_input = {
#     'x1': np.array([2, 3, 5, 7, 4]),       # Variabel Bebas 1
#     'x2': np.array([3, 4, 2, 3, 6]),       # Variabel Bebas 2
#     # 'x3': np.array([1, 1, 1, 1, 1, 1]),     # (Opsional: Tambah jika ada)
#     'y':  np.array([12, 15, 14, 19, 18])  # Variabel Terikat (Target)
# }

x1_i = np.array([2, 3, 5, 7, 4]) 
x2_i = np.array([3, 4, 2, 3, 6])
y_i = np.array([12, 15, 14, 19, 18])

n = len(y_i)

# Vektor Y 
Y = y_i.reshape(-1, 1)

# =========================================================================
# 2. DEFINISI FUNGSI BASIS & PEMBENTUKAN MATRIKS [Z]
# --- Fungsi Basis: z0=1, z1=x1, z2=x2 ---
# =========================================================================
def create_Z_matrix_mlr(x1_data, x2_data):
    """Membentuk Matriks Z untuk Multiple Linear Regression."""
    
    # Basis fungsi: z0=1 (konstanta), z1=x1, z2=x2
    z_0 = np.ones_like(x1_data)
    z_1 = x1_data
    z_2 = x2_data
    
    # Gabungkan menjadi Matriks Z
    Z = np.stack([z_0, z_1, z_2], axis=1)
    
    # Nama kolom
    column_names = ['z0 (1)', 'z1 (x1)', 'z2 (x2)']
    return Z, column_names

Z, z_names = create_Z_matrix_mlr(x1_i, x2_i)
m_vars = Z.shape[1] # Jumlah koefisien (a0, a1, a2)

# =========================================================================
# 3. PERHITUNGAN KOEFISIEN (SISTEM PERSAMAAN NORMAL)
#    Rumus: [Z]T[Z] {A} = [Z]T{Y}
# =========================================================================
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

# Menyelesaikan sistem persamaan
try:
    A = np.linalg.solve(Z_T_Z, Z_T_Y)
except np.linalg.LinAlgError:
    print("Error: Matriks Singular.")
    exit()

# Ambil hasil koefisien [a0, a1, a2]
a = A.flatten()
a_0, a_1, a_2 = a[0], a[1], a[2]

# Nilai prediksi model: y_model = Z @ A
y_model = Z @ A.flatten()

# =========================================================================
# 4. ANALISIS KUALITAS REGRESI
# =========================================================================
y_bar = np.mean(y_i)

# St (Total Sum of Squares)
St_y = np.sum((y_i - y_bar)**2) 
# Sr (Sum of Squares of Residuals)
Sr_y = np.sum((y_i - y_model)**2) 

# Metrik Kualitas Model (MLR)
r2_asli = (St_y - Sr_y) / St_y
r_asli = np.sqrt(r2_asli)

# Standard Error Estimasi (Sy/x)
# Catatan: Pembagi adalah n - m_vars
Sy_x_asli = np.sqrt(Sr_y / (n - m_vars))

# Standard Deviation (Sy)
Sy_asli = np.sqrt(St_y / (n - 1))

# =========================================================================
# 5. HASIL OUTPUT TERSTRUKTUR
# =========================================================================
print("=" * 75)
print(f"       HASIL MULTIPLE LINEAR REGRESSION (MLR) - {m_vars-1} Variabel")
print("=" * 75)

## --- OUTPUT STEP 1: MATRIKS SISTEM PERSAMAAN ---
print("\n## 1. PEMBENTUKAN MATRIKS SISTEM PERSAMAAN NORMAL")
print("-" * 75)
print("Konsep: [Z]T[Z] {A} = [Z]T{Y}")
print(f"Model: y = a0 + a1(x1) + a2(x2)")
print("\nMatriks Koefisien [Z]T[Z]:")
print(Z_T_Z.round(7))
print("\nVektor Sisi Kanan [Z]T{Y}:")
print(Z_T_Y.round(7).T)

## --- OUTPUT STEP 2: KOEFISIEN AKHIR ---
print("\n## 2. SOLUSI KOEFISIEN {A}")
print("-" * 75)
print("Hasil penyelesaian {A} = ([Z]T[Z])^-1 * [Z]T{Y}")
for i in range(m_vars):
    print(f"Koefisien a{i} = {a[i]:.7f}")

print("\nPersamaan Regresi Final:")
eq_str = f"y = {a_0:.4f}"
eq_str += f" + {a_1:.4f}x1" if a_1 >= 0 else f" - {abs(a_1):.4f}x1"
eq_str += f" + {a_2:.4f}x2" if a_2 >= 0 else f" - {abs(a_2):.4f}x2"
print(eq_str)

## --- OUTPUT STEP 3: ANALISIS KUALITAS MODEL ---
print("\n## 3. ANALISIS KUALITAS REGRESI")
print("-" * 75)
print(f"n (Jumlah data) = {n}")
print(f"m (Jumlah koef.) = {m_vars}")
print(f"St (Total Sum of Squares)    = {St_y:.7f}")
print(f"Sr (Sum of Residuals)        = {Sr_y:.7f}")
print(f"Sy (Standard Deviation)      = {Sy_asli:.7f}")
print(f"Sy/x (Std Error Estimasi)    = {Sy_x_asli:.7f}")
print(f"R^2 (Koef. Determinasi)      = {r2_asli:.7f} ({r2_asli*100:.2f}%)")
print(f"R (Koef. Korelasi)           = {r_asli:.7f}")

## --- OUTPUT STEP 4: TABEL DETAIL PERHITUNGAN LANGKAH DEMI LANGKAH ---
print("\n## 4. TABEL DETAIL PERHITUNGAN LANGKAH DEMI LANGKAH")
print("-" * 75)

# Siapkan data untuk DataFrame
df = pd.DataFrame({
    'xi': x1_i,
    'x2i': x2_i,
    'yi_asli': y_i,
    'z0 (1)': Z[:, 0], 
    'z1 (x1)': Z[:, 1], 
    'z2 (x2)': Z[:, 2],
    'y_pred_model': y_model,
    '(yi-ybar)^2': (y_i - y_bar)**2,
    '(yi-model)^2': (y_i - y_model)**2
})

sum_row = df.sum(numeric_only=True)
sum_row.name = 'Σ'
df_final = pd.concat([df, sum_row.to_frame().T])

print(df_final.round(7).to_string())
print("-" * 75)