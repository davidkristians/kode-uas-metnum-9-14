import numpy as np
import pandas as pd
import math

# Atur tampilan agar angka 0 yang sangat kecil (misal 1e-17) dianggap 0
np.set_printoptions(precision=4, suppress=True)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

print("=== GENERAL LEAST SQUARES (FLEXIBLE AUTOMATIC VERSION) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (GANTI SESUAI SOAL)
# ==============================================================================
# Contoh Data dari 'General Least Square 1.csv' (Trigonometri)
x_i = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4]) 
y_i = np.array([3, 2.5, 1, 0.5])

print("Data Awal:")
print(f"x: {x_i}")
print(f"y: {y_i}")
print("-" * 80)

# ==============================================================================
# BAGIAN 2: DEFINISI FUNGSI BASIS (Z) - !!! UBAH RUMUS DI SINI !!!
# ==============================================================================
def get_Z_matrix(x):
    """
    Fungsi ini menentukan model matematika yang dipakai.
    Sesuaikan isinya dengan rumus yang diminta soal UAS.
    """
    
    # --- CONTOH 1: Model Trigonometri (Sesuai Excel Anda) ---
    # y = a0 + a1*cos(2x) + a2*sin(x)
    z0 = np.ones_like(x)        # a0 (Konstanta)
    z1 = np.cos(2 * x)          # a1 (Pasangan cos 2x)
    z2 = np.sin(x)              # a2 (Pasangan sin x)
    
    # Bersihkan error numerik (misal 0.0000000000001 jadi 0)
    z1 = np.where(np.abs(z1) < 1e-10, 0, z1)
    z2 = np.where(np.abs(z2) < 1e-10, 0, z2)
    
    return np.stack([z0, z1, z2], axis=1)

    # --- CONTOH 2: Jika Soal y = a0 + a1*x^3 (Hapus tanda # untuk pakai) ---
    # z0 = np.ones_like(x)
    # z1 = x**3
    # return np.stack([z0, z1], axis=1)

    # --- CONTOH 3: Jika Soal Polinomial Derajat 4 ---
    # Z_list = [np.ones_like(x)]
    # for p in range(1, 5): # Pangkat 1 sampai 4
    #     Z_list.append(x**p)
    # return np.stack(Z_list, axis=1)

# ==============================================================================
# BAGIAN 3: PERHITUNGAN MATRIKS OTOMATIS (JANGAN UBAH INI)
# ==============================================================================
# 1. Bentuk Matriks Z
Z = get_Z_matrix(x_i)
Y = y_i.reshape(-1, 1)
n_data = len(y_i)
n_vars = Z.shape[1] # Jumlah koefisien (a0, a1...)

# 2. Tampilkan Tabel Z (Step 1 di Excel)
col_names = [f'z{i}' for i in range(n_vars)]
df_z = pd.DataFrame(Z, columns=col_names)
df_z.insert(0, 'y', y_i)
df_z.insert(0, 'x', x_i)

print("\n--- STEP 1: MATRIKS Z (FUNGSI BASIS) ---")
print(df_z.to_string(index=False))

# 3. Hitung Matriks Normal [Z]T[Z] dan Vektor [Z]T{Y} (Step 2 & 3 di Excel)
# Ini menggantikan perhitungan manual z0_sq, z0_z1, dll.
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

print("\n\n--- STEP 2 & 3: MATRIKS NORMAL (HASIL PERKALIAN) ---")
print("Matriks Kiri [Z]T [Z]:")
print(Z_T_Z)
print("\nVektor Kanan [Z]T {Y}:")
print(Z_T_Y)

# 4. Solusi Sistem Persamaan Linear (Step 4)
try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
    a = A.flatten()
    
    # Tampilkan Invers (Opsional, ada di Excel)
    print("\nInvers Matriks [Z]T[Z]:")
    print(Z_T_Z_inv)
    
except np.linalg.LinAlgError:
    print("\nERROR: Matriks Singular! Model tidak bisa diselesaikan.")
    a = np.zeros(n_vars)

# ==============================================================================
# BAGIAN 4: ANALISIS ERROR & HASIL AKHIR
# ==============================================================================
# Hitung Prediksi
y_pred = np.zeros_like(y_i, dtype=float)
for i in range(n_vars):
    y_pred += a[i] * Z[:, i]

# Hitung Statistik Error
y_bar = np.mean(y_i)
yi_ybar_sq = (y_i - y_bar)**2      # Total Error
yi_model_sq = (y_i - y_pred)**2    # Residual Error

St = np.sum(yi_ybar_sq)
Sr = np.sum(yi_model_sq)
Sy = math.sqrt(St / (n_data - 1)) if n_data > 1 else 0
Sy_x = math.sqrt(Sr / (n_data - n_vars)) if n_data > n_vars else 0
r2 = (St - Sr) / St if St != 0 else 0
r = math.sqrt(r2) if r2 >= 0 else 0

# Tabel Detail Akhir
df_final = df_z.copy()
df_final['y_pred'] = y_pred
df_final['(yi-ybar)^2'] = yi_ybar_sq
df_final['(yi-model)^2'] = yi_model_sq

# ==============================================================================
# OUTPUT HASIL
# ==============================================================================
print("\n" + "="*60)
print("HASIL KOEFISIEN:")
print("="*60)
for i in range(n_vars):
    print(f"a{i} = {a[i]:.7f}")

print("-" * 60)
# Membuat persamaan string otomatis
eq_str = "y ="
for i in range(n_vars):
    sign = " + " if a[i] >= 0 else " - "
    val = abs(a[i])
    if i == 0:
        eq_str += f" {a[i]:.4f} * z0"
    else:
        eq_str += f"{sign}{val:.4f} * z{i}"
print(f"PERSAMAAN MODEL:\n{eq_str}")
print("(z0, z1... sesuai definisi fungsi Anda di atas)")
print("-" * 60)

print("\n[TABEL DETAIL EVALUASI]:")
print(df_final.round(5).to_string(index=False))

print("-" * 60)
print("STATISTIK ERROR:")
print(f"Sy (Standard Deviation)   = {Sy:.7f}")
print(f"Sy/x (Std Error Est)      = {Sy_x:.7f}")
print(f"r^2 (Determinasi)         = {r2:.7f} ({r2*100:.4f}%)")
print(f"r (Korelasi)              = {r:.7f}")
print("-" * 60)