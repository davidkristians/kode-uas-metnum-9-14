import numpy as np
import pandas as pd
import math

# Atur presisi output agar rapi
np.set_printoptions(precision=7, suppress=True)

# Pilihan logaritma: Gunakan np.log10 (Basis 10) sesuai Excel/Wilson
LOG_BASE = np.log10 

# =========================================================================
# 1. INPUT DATA & MODEL (POWER MODEL: y = alpha * x1^beta1 * x2^beta2)
# =========================================================================
# Data dari Pertemuan 10.xlsx - Multiple Linear Regresi 2.csv
x1_i = np.array([2, 3, 4, 5, 6]) 
x2_i = np.array([5, 7, 9, 11, 13])
y_i = np.array([15.1, 25.4, 41.3, 60.2, 85.1])
n = len(y_i)

# --- TAHAP LINEARISASI (Transformasi Data) ---
# Model Asli: y = alpha * x1^beta1 * x2^beta2
# Model Linear: log(y) = log(alpha) + beta1*log(x1) + beta2*log(x2)
# Bentuk Matriks: Y = A0 + A1*X1 + A2*X2
# Dimana: Y=log(y), X1=log(x1), X2=log(x2), A0=log(alpha), A1=beta1, A2=beta2

X1_i = LOG_BASE(x1_i) 
X2_i = LOG_BASE(x2_i)
Y_i = LOG_BASE(y_i) 

# Vektor Y (sudah ditransformasi) untuk perhitungan matriks
Y_vec = Y_i.reshape(-1, 1)

# =========================================================================
# 2. DEFINISI FUNGSI BASIS & PEMBENTUKAN MATRIKS [Z]
# =========================================================================
def create_Z_matrix_mlr2(X1_data, X2_data):
    """Membentuk Matriks Z untuk Multiple Linear Regression Power Model."""
    # Basis fungsi linear: z0=1, z1=X1, z2=X2
    z_0 = np.ones_like(X1_data)
    z_1 = X1_data
    z_2 = X2_data
    
    Z = np.stack([z_0, z_1, z_2], axis=1)
    column_names = ['z0 (1)', 'z1 (log x1)', 'z2 (log x2)']
    return Z, column_names

Z, z_names = create_Z_matrix_mlr2(X1_i, X2_i)
m_vars = Z.shape[1] # Jumlah koefisien (A0, A1, A2)

# =========================================================================
# 3. PERHITUNGAN KOEFISIEN (SISTEM PERSAMAAN NORMAL)
#    Rumus: [Z]T[Z] {A} = [Z]T{Y}
# =========================================================================
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y_vec

try:
    A = np.linalg.solve(Z_T_Z, Z_T_Y)
except np.linalg.LinAlgError:
    print("Error: Matriks Singular.")
    exit()

# Ambil hasil koefisien Linear [A0, A1, A2]
A_linear = A.flatten()
A0, A1, A2 = A_linear[0], A_linear[1], A_linear[2]

# =========================================================================
# 4. TRANSFORMASI BALIK KOEFISIEN (LINEAR -> NON-LINEAR)
# =========================================================================
# A0 = log10(alpha) -> alpha = 10^A0
# A1 = beta1
# A2 = beta2
alpha = 10**A0 
beta1 = A1 
beta2 = A2

# Hitung nilai prediksi pada skala ASLI (Model Power)
y_model = alpha * (x1_i ** beta1) * (x2_i ** beta2)

# =========================================================================
# 5. ANALISIS KUALITAS REGRESI (Diukur pada data ASLI y)
# =========================================================================
y_bar = np.mean(y_i)

# St (Total Sum of Squares) - Variansi data asli
St_y = np.sum((y_i - y_bar)**2) 

# Sr (Sum of Squares of Residuals) - Error kuadrat data asli vs model
Sr_y = np.sum((y_i - y_model)**2) 

# Metrik Statistik
r2_asli = (St_y - Sr_y) / St_y
r_asli = np.sqrt(r2_asli)
Sy_x_asli = np.sqrt(Sr_y / (n - m_vars)) # Std Error Estimasi
Sy_asli = np.sqrt(St_y / (n - 1))        # Std Deviasi Data

# =========================================================================
# 6. OUTPUT HASIL LENGKAP & RAPI
# =========================================================================
print("=" * 85)
print(f"       HASIL MULTIPLE LINEAR REGRESSION 2 (POWER MODEL)")
print("=" * 85)

## --- OUTPUT STEP 1: MATRIKS SISTEM PERSAMAAN ---
print("\n## 1. PEMBENTUKAN MATRIKS SISTEM PERSAMAAN NORMAL")
print("-" * 85)
print("Konsep: [Z]T[Z] {A} = [Z]T{Y}")
print(f"Model Linear: Y = A0 + A1(X1) + A2(X2) | Transformasi: Log10")
print("\nMatriks Koefisien [Z]T[Z]:")
print(Z_T_Z.round(7))
print("\nVektor Sisi Kanan [Z]T{Y} (Y dari data log(y)):")
print(Z_T_Y.round(7).T)

## --- OUTPUT STEP 2: SOLUSI KOEFISIEN ---
print("\n## 2. SOLUSI KOEFISIEN")
print("-" * 85)
print("Koefisien Linear (Hasil Eliminasi Gauss/Invers Matriks):")
print(f"A0 = {A0:.7f}")
print(f"A1 = {A1:.7f}")
print(f"A2 = {A2:.7f}")

print("\nTransformasi Balik ke Model Power (y = alpha * x1^beta1 * x2^beta2):")
print(f"alpha = 10^A0   = {alpha:.7f}")
print(f"beta1 = A1      = {beta1:.7f}")
print(f"beta2 = A2      = {beta2:.7f}")

print("\nPersamaan Regresi Final:")
print(f"y = {alpha:.4f} * x1^({beta1:.4f}) * x2^({beta2:.4f})")

## --- OUTPUT STEP 3: ANALISIS KUALITAS MODEL ---
print("\n## 3. ANALISIS KUALITAS REGRESI (Pada Data Asli)")
print("-" * 85)
print(f"St (Total Sum of Squares)    = {St_y:.7f}")
print(f"Sr (Sum of Residuals)        = {Sr_y:.7f}")
print(f"Sy (Standard Deviation)      = {Sy_asli:.7f}")
print(f"Sy/x (Std Error Estimasi)    = {Sy_x_asli:.7f}")
print(f"R^2 (Koef. Determinasi)      = {r2_asli:.7f} ({r2_asli*100:.4f}%)")
print(f"R (Koef. Korelasi)           = {r_asli:.7f}")

## --- OUTPUT STEP 4: TABEL DETAIL PERHITUNGAN ---
print("\n## 4. TABEL DETAIL PERHITUNGAN LANGKAH DEMI LANGKAH")
print("-" * 85)

# Hitung Y_pred linear (hanya untuk perbandingan internal)
Y_pred_linear = Z @ A.flatten()

# Siapkan DataFrame
df = pd.DataFrame({
    'x1': x1_i,
    'x2': x2_i,
    'yi_asli': y_i,
    'log(x1)': X1_i,
    'log(x2)': X2_i,
    'log(yi)': Y_i,
    'log(y)_pred': Y_pred_linear,
    'y_pred_model': y_model,
    '(yi-ybar)^2': (y_i - y_bar)**2,
    '(yi-model)^2': (y_i - y_model)**2
})

# Tambahkan baris total
sum_row = df.sum(numeric_only=True)
sum_row.name = 'Σ'
df_final = pd.concat([df, sum_row.to_frame().T])

# Tampilkan tabel
print(df_final.round(5).to_string())
print("-" * 85)