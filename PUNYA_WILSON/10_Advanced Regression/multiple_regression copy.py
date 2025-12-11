import numpy as np
import pandas as pd
import math

# Alasannya sederhana: Matematika Matriks (Linear Algebra) yang kita gunakan hanya bisa memecahkan persamaan yang berbentuk PENJUMLAHAN (+), bukan perkalian (⋅) atau pangkat.
# Model pangkat seperti y=a0​⋅x1a1​​⋅x2a2​​ adalah model Non-Linear. Jika dibiarkan begitu saja, kita tidak bisa menyusunnya ke dalam matriks [Z]T[Z].
# Oleh karena itu, kita menggunakan Logaritma sebagai "alat bantu" karena logaritma memiliki sifat ajaib yang bisa mengubah Perkalian menjadi Penjumlahan dan Pangkat menjadi Perkalian Biasa.
# Berikut adalah pembuktian langkah demi langkahnya:
# 1. Sifat Logaritma yang Dipakai
# Ada dua hukum dasar logaritma yang kita manfaatkan:
#     Hukum 1 (Perkalian → Penjumlahan):
#     log(A⋅B)=log(A)+log(B)
#     Hukum 2 (Pangkat → Perkalian):
#     log(An)=n⋅log(A)
# 2. Transformasi Persamaan
# Mari kita terapkan hukum di atas ke persamaan Anda:
# Persamaan Awal (Non-Linear):
# y=a0​⋅x1a1​​⋅x2a2​​
# Langkah 1: Berikan Log di kiri dan kanan
# log(y)=log(a0​⋅x1a1​​⋅x2a2​​)
# Langkah 2: Pisahkan perkalian menggunakan Hukum 1 Perkalian (⋅) berubah menjadi tambah (+):
# log(y)=log(a0​)+log(x1a1​​)+log(x2a2​​)

# Atur tampilan
np.set_printoptions(precision=4, suppress=True)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

print("=== FLEXIBLE MULTIPLE REGRESSION (General Linear Model) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (MASUKKAN SEMUA VARIABEL DI SINI)
# ==============================================================================
# Masukkan data dalam format Dictionary
# Anda bisa menambah x3, x4, dst sesuka hati
data_input = {
    'x1': np.array([2, 3, 4, 5, 6]),       # Variabel Bebas 1
    'x2': np.array([5, 7, 9, 11, 13]),       # Variabel Bebas 2
    # 'x3': np.array([1, 1, 1, 1, 1, 1]),     # (Opsional: Tambah jika ada)
    'y':  np.array([15.1, 25.4, 41.3, 60.2, 85.1])  # Variabel Terikat (Target)
}

data_input['y_log'] = np.log10(data_input['y'])

print("Data Awal:")
print(pd.DataFrame(data_input).to_string(index=False))
print("-" * 80)

# ==============================================================================
# BAGIAN 2: DEFINISI FUNGSI BASIS (Z) - !!! UBAH MODEL DI SINI !!!
# ==============================================================================
def get_Z_matrix(data):
    """
    Tentukan hubungan antar variabel di sini.
    Ambil variabel dari dictionary 'data' menggunakan kuncinya ('x1', 'x2').
    """
    # x1 = data['x1']
    # x2 = data['x2']
    # x3 = data['x3'] # Uncomment jika ada x3
    x1_log = np.log10(data['x1'])
    x2_log = np.log10(data['x2'])

    
    n = len(x1_log)
    
    # --- MODEL 1: Multiple Linear Biasa (y = a0 + a1*x1 + a2*x2) ---
    # z0 = np.ones(n) # Konstanta a0
    # z1 = x1         # a1 * x1
    # z2 = x2         # a2 * x2
    
    # return np.stack([z0, z1, z2], axis=1)

    # y = a0 x1^a1 x2^a2
    z0 = np.ones(n)
    z1 = x1_log
    z2 = x2_log
    return np.stack([z0, z1, z2], axis=1)
    # --- MODEL 2: Polinomial Multiple (y = a0 + a1*x1 + a2*x2 + a3*x1^2) ---
    # z0 = np.ones(n)
    # z1 = x1
    # z2 = x2
    # z3 = x1**2
    # return np.stack([z0, z1, z2, z3], axis=1)

    # --- MODEL 3: Interaksi (y = a0 + a1*x1 + a2*x2 + a3*(x1*x2)) ---
    # z0 = np.ones(n)
    # z1 = x1
    # z2 = x2
    # z3 = x1 * x2  # Variabel interaksi
    # return np.stack([z0, z1, z2, z3], axis=1)

# ==============================================================================
# BAGIAN 3: PERHITUNGAN OTOMATIS
# ==============================================================================
# 1. Bentuk Matriks Z
Z = get_Z_matrix(data_input)

# !!! PERBAIKAN DI SINI !!!
# Gunakan 'y_log' sebagai target, BUKAN 'y' biasa
Y = data_input['y_log'].reshape(-1, 1) 

n_data = len(Y)
n_vars = Z.shape[1]

# 2. Tampilkan Tabel Z
col_names = [f'z{i}' for i in range(n_vars)]
df_z = pd.DataFrame(Z, columns=col_names)
df_display = pd.DataFrame(data_input)
df_display = pd.concat([df_display, df_z], axis=1)

print("\n--- STEP 1: MATRIKS Z (Variabel Transformasi) ---")
print(df_display.to_string(index=False))

# 3. Hitung Matriks Normal
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

print("\n\n--- STEP 2 & 3: MATRIKS NORMAL ---")
print("Matriks Kiri [Z]T [Z]:")
print(Z_T_Z)
print("\nVektor Kanan [Z]T {Y} (Harusnya sekitar 7.9, bukan 227):")
print(Z_T_Y)

# 4. Solusi Sistem Persamaan Linear
try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
    a = A.flatten()
except np.linalg.LinAlgError:
    print("\nERROR: Matriks Singular!")
    a = np.zeros(n_vars)

# ==============================================================================
# BAGIAN 4: ANALISIS ERROR & HASIL AKHIR
# ==============================================================================
# Hitung Prediksi dalam skala Log
log_y_pred = np.zeros(n_data)
for i in range(n_vars):
    log_y_pred += a[i] * Z[:, i]

# !!! PERBAIKAN DI SINI !!!
# Kembalikan ke bentuk asli (Antilog 10) untuk menghitung error real
y_pred_final = 10 ** log_y_pred 

# Hitung Statistik Error (Bandingkan y_asli dengan y_prediksi_asli)
y_actual = data_input['y']
y_bar = np.mean(y_actual)

yi_ybar_sq = (y_actual - y_bar)**2      
yi_model_sq = (y_actual - y_pred_final)**2  # Gunakan y_pred_final

St = np.sum(yi_ybar_sq)
Sr = np.sum(yi_model_sq)
Sy = math.sqrt(St / (n_data - 1))
Sy_x = math.sqrt(Sr / (n_data - n_vars))
r2 = (St - Sr) / St
r = math.sqrt(r2)

# Tabel Detail Evaluasi
df_final = df_display.copy()
df_final['log_y_pred'] = log_y_pred
df_final['y_pred_final'] = y_pred_final # Nilai prediksi dalam menit
df_final['(yi-ybar)^2'] = yi_ybar_sq
df_final['(yi-model)^2'] = yi_model_sq

# Output Hasil
print("\n" + "="*60)
print("HASIL KOEFISIEN (Skala Log):")
print("="*60)
print(f"a0 (Intercept Log) = {a[0]:.7f} -> a0 Asli = {10**a[0]:.7f}")
print(f"a1 (Pangkat x1)    = {a[1]:.7f}")
print(f"a2 (Pangkat x2)    = {a[2]:.7f}")

print("-" * 60)
print(f"PERSAMAAN AKHIR: y = {10**a[0]:.4f} * x1^({a[1]:.4f}) * x2^({a[2]:.4f})")
print("-" * 60)

print("\n[TABEL DETAIL EVALUASI]:")
print(df_final.round(5).to_string(index=False))

print("-" * 60)
print(f"r^2 (Determinasi)         = {r2:.7f} ({r2*100:.4f}%)")
print("-" * 60)