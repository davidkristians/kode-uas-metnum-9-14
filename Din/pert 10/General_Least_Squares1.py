import numpy as np
import pandas as pd
import math

# Atur presisi output
np.set_printoptions(precision=7, suppress=True)

# =========================================================================
# 1. INPUT DATA & MODEL (G-LS: y = a0 + a1*cos(2x) + a2*sin(x))
# =========================================================================
# Data Contoh (Ambil dari data Anda yang sesuai)
x_i = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4])
y_i = np.array([3.0, 2.5, 1.0, 0.5])
n = len(y_i)

# Vektor Y 
Y = y_i.reshape(-1, 1)

# =========================================================================
# 2. DEFINISI FUNGSI BASIS & PEMBENTUKAN MATRIKS [Z]
# --- Ubah bagian ini untuk model G-LS lainnya ---
# =========================================================================
def create_Z_matrix(x_data):
    """Membentuk Matriks Z berdasarkan fungsi basis G-LS."""
    # Basis fungsi: z0=1, z1=cos(2x), z2=sin(x)
    z_0 = np.ones_like(x_data)
    z_1 = np.cos(2 * x_data)
    z_2 = np.sin(x_data)
    
    # Gabungkan menjadi Matriks Z
    Z = np.stack([z_0, z_1, z_2], axis=1)
    
    # Juga kembalikan nama kolom untuk tabel detail
    column_names = ['z0 (1)', 'z1 (cos(2x))', 'z2 (sin(x))']
    return Z, column_names

Z, z_names = create_Z_matrix(x_i)
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

# Ambil hasil koefisien [a0, a1, ..., aM]
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

# Metrik
r2_asli = (St_y - Sr_y) / St_y
r_asli = np.sqrt(r2_asli)
Sy_x_asli = np.sqrt(Sr_y / (n - m_vars))
Sy_asli = np.sqrt(St_y / (n - 1))


# =========================================================================
# 5. HASIL OUTPUT TERSTRUKTUR
# =========================================================================
print("=" * 75)
print(f"       HASIL REGRESI GENERAL LEAST SQUARES (G-LS) ORDE {m_vars - 1}")
print("=" * 75)

## --- OUTPUT STEP 1: MATRIKS SISTEM PERSAMAAN ---
print("\n## 1. PEMBENTUKAN MATRIKS SISTEM PERSAMAAN NORMAL")
print("-" * 75)
print("Konsep: [Z]T[Z] {A} = [Z]T{Y}")
print(f"Model: y = a0 * {z_names[0].split('(')[1][:-1]} + a1 * {z_names[1].split('(')[1][:-1]} + a2 * {z_names[2].split('(')[1][:-1]}")
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
print(f"y = {a_0:.4f} + {a_1:.4f}cos(2x) + {a_2:.4f}sin(x)")


## --- OUTPUT STEP 3: ANALISIS KUALITAS MODEL ---
print("\n## 3. ANALISIS KUALITAS REGRESI")
print("-" * 75)
print(f"n (Jumlah data) = {n}")
print(f"m (Jumlah koef.) = {m_vars}")
print(f"St (Total Sum of Squares)    = {St_y:.7f}")
print(f"Sr (Sum of Residuals)        = {Sr_y:.7f}")
print(f"Sy (Standard Deviation)      = {Sy_asli:.7f}")
print(f"Sy/x (Std Error Estimasi)    = {Sy_x_asli:.7f}")
print(f"r^2 (Koef. Determinasi)      = {r2_asli:.7f} ({r2_asli*100:.2f}%)")
print(f"r (Koef. Korelasi)           = {r_asli:.7f}")


## --- OUTPUT STEP 4: TABEL DETAIL PERHITUNGAN ---
print("\n## 4. TABEL DETAIL PERHITUNGAN LANGKAH DEMI LANGKAH")
print("-" * 75)

# Siapkan data untuk DataFrame
data = {
    'xi': x_i,
    'yi_asli': y_i,
}

# Tambahkan kolom Z (Fungsi Basis)
df_Z = pd.DataFrame(Z, columns=z_names)
data.update(df_Z.to_dict('list'))

# Tambahkan kolom perhitungan error
data.update({
    'y_pred_model': y_model,
    '(yi-ybar)^2': (y_i - y_bar)**2,
    '(yi-model)^2': (y_i - y_model)**2
})

# Buat DataFrame
df = pd.DataFrame(data)

# Tambahkan Baris Total (Sum)
sum_row = df.sum(numeric_only=True)
sum_row.name = 'Σ'
df_final = pd.concat([df, sum_row.to_frame().T])

# Tampilkan tabel dengan pembulatan 7 desimal
print(df_final.round(7).to_string())
print("-" * 75)