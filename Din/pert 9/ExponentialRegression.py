import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. INPUT DATA & MODEL (EKSPONENSIAL: y = alpha * e^(beta*x))
# =========================================================================
# Data Contoh (Gunakan data dari Pertemuan 9.xlsx - Exponential.csv Anda)
# x_i = np.array([0, 1, 2, 3, 4, 5]) 
# y_i = np.array([10.5, 12.0, 14.5, 17.0, 20.0, 25.0])
x_i = np.array([2, 3, 4, 5, 6])
y_i = np.array([2.47, 3.18, 4.08, 5.24, 6.72])
n = len(y_i)

# --- TAHAP LINEARISASI (Transformasi y menjadi Y) ---
# Model Linear: Y = A0 + A1 * x, di mana Y = ln(y)
try:
    Y_i = np.log(y_i) # Menggunakan Logaritma Natural (ln)
except:
    print("Error: Data y harus positif untuk logaritma.")
    exit()

# --- DEFINISI FUNGSI BASIS (Matriks [Z]) ---
z_0 = np.ones_like(x_i)
z_1 = x_i
Z = np.stack([z_0, z_1], axis=1)  # Matriks Z (n x 2)

# Vektor Y (sudah ditransformasi)
Y_vec = Y_i.reshape(-1, 1)

# =========================================================================
# 2. PERHITUNGAN KOEFISIEN LINEAR MENGGUNAKAN LEAST SQUARES (G-LS)
# =========================================================================
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y_vec

try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
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
beta = A1 
alpha = np.exp(A0) 

# Nilai prediksi model pada y ASLI: y_model = alpha * e^(beta*x)
y_model = alpha * np.exp(beta * x_i)

# =========================================================================
# 4. ANALISIS KUALITAS REGRESI LENGKAP
# =========================================================================
m_vars = Z.shape[1] 

# -------------------------------------------------------------------------
# A. METRIK BERDASARKAN DATA ASLI (y_i): Mengukur kecocokan MODEL NON-LINEAR
# -------------------------------------------------------------------------
y_bar = np.mean(y_i)
St_y = np.sum((y_i - y_bar)**2) # St (Total Sum of Squares pada y ASLI)
Sr_y = np.sum((y_i - y_model)**2) # Sr (Sum of Squares of Residuals pada y ASLI)

# Koefisien Determinasi ASLI (r^2)
r2_asli = (St_y - Sr_y) / St_y
r_asli = np.sqrt(r2_asli)

# Standar Error Estimasi ASLI (Sy/x)
Sy_x_asli = np.sqrt(Sr_y / (n - m_vars))

# Standar Deviasi ASLI (Sy)
Sy_asli = np.sqrt(St_y / (n - 1))

# -------------------------------------------------------------------------
# B. METRIK BERDASARKAN DATA TRANSFORMASI (Y_i): Mengukur kecocokan LINEAR
# -------------------------------------------------------------------------
Y_bar = np.mean(Y_i)
Y_model = A0 + A1 * x_i # Nilai Y prediksi (linear)

St_Y = np.sum((Y_i - Y_bar)**2) # St (pada Y)
Sr_Y = np.sum((Y_i - Y_model)**2) # Sr (pada Y)

# Koefisien Korelasi LINEAR (r)
r2_linear = (St_Y - Sr_Y) / St_Y
r_linear = np.sqrt(r2_linear)

# Standar Deviasi LINEAR (Sy)
Sy_linear = np.sqrt(St_Y / (n - 1))


# =========================================================================
# 5. HASIL OUTPUT & TABEL DETAIL
# =========================================================================
print("-" * 75)
print("HASIL REGRESI EKSPONENSIAL (y = alpha * e^(beta*x))")
print("-" * 75)

print(f"Koefisien Linear: A0 = {A0:.7f}, A1 = {A1:.7f}")
print(f"Koefisien Non-Linear: alpha = {alpha:.7f}, beta = {beta:.7f}")
print(f"\nPersamaan Regresi Final: y = {alpha:.4f} * e^({beta:.4f} * x)")

print("-" * 75)
print("METRIK KUALITAS MODEL (Dihitung pada data ASLI 'y'):")
print(f"Sy (Standard Deviation Asli)    = {Sy_asli:.7f}")
print(f"Sy/x (Std Error Estimasi Asli)  = {Sy_x_asli:.7f}")
print(f"r^2 (Koef. Determinasi Asli)    = {r2_asli:.7f} ({r2_asli*100:.2f}%)")
print(f"r (Koef. Korelasi Asli)         = {r_asli:.7f}")

print("\nMETRIK KUALITAS LINEARISASI (Dihitung pada data TRANSFORMASI 'Y'):")
print(f"Sy (Standard Deviation Transformasi) = {Sy_linear:.7f}")
print(f"r (Koef. Korelasi Transformasi)      = {r_linear:.7f}")
print("-" * 75)

# Membuat Tabel Menggunakan Pandas
df = pd.DataFrame({
    'xi': x_i,
    'yi_asli': y_i,
    'Yi=ln(yi)': Y_i, 
    'Y_pred_linear': Y_model,
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