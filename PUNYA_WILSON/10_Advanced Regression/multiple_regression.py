import numpy as np
import pandas as pd
import math

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
    'x1': np.array([2, 3, 5, 7, 4]),       # Variabel Bebas 1
    'x2': np.array([3, 4, 2, 3, 6]),       # Variabel Bebas 2
    # 'x3': np.array([1, 1, 1, 1, 1, 1]),     # (Opsional: Tambah jika ada)
    'y':  np.array([12, 15, 14, 19, 18])  # Variabel Terikat (Target)
}

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
    x1 = data['x1']
    x2 = data['x2']
    # x3 = data['x3'] # Uncomment jika ada x3
    
    n = len(x1)
    
    # --- MODEL 1: Multiple Linear Biasa (y = a0 + a1*x1 + a2*x2) ---
    z0 = np.ones(n) # Konstanta a0
    z1 = x1         # a1 * x1
    z2 = x2         # a2 * x2
    
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
# BAGIAN 3: PERHITUNGAN OTOMATIS (JANGAN UBAH INI)
# ==============================================================================
# 1. Bentuk Matriks Z dan Y
Z = get_Z_matrix(data_input)
Y = data_input['y'].reshape(-1, 1)
n_data = len(Y)
n_vars = Z.shape[1] # Jumlah koefisien (a0, a1...)

# 2. Tampilkan Tabel Z (Fungsi Basis)
col_names = [f'z{i}' for i in range(n_vars)]
df_z = pd.DataFrame(Z, columns=col_names)
# Gabungkan dengan data asli untuk tampilan
df_display = pd.DataFrame(data_input)
df_display = pd.concat([df_display, df_z], axis=1)

print("\n--- STEP 1: MATRIKS Z (Variabel Transformasi) ---")
print(df_display.to_string(index=False))

# 3. Hitung Matriks Normal [Z]T[Z] dan [Z]T{Y}
Z_T_Z = Z.T @ Z
Z_T_Y = Z.T @ Y

print("\n\n--- STEP 2 & 3: MATRIKS NORMAL ---")
print("Matriks Kiri [Z]T [Z]:")
print(Z_T_Z)
print("\nVektor Kanan [Z]T {Y}:")
print(Z_T_Y)

# 4. Solusi Sistem Persamaan Linear
try:
    Z_T_Z_inv = np.linalg.inv(Z_T_Z)
    A = Z_T_Z_inv @ Z_T_Y
    a = A.flatten()
except np.linalg.LinAlgError:
    print("\nERROR: Matriks Singular! Model tidak bisa diselesaikan.")
    a = np.zeros(n_vars)

# ==============================================================================
# BAGIAN 4: ANALISIS ERROR & HASIL AKHIR
# ==============================================================================
# Hitung Prediksi
y_pred = np.zeros(n_data)
for i in range(n_vars):
    y_pred += a[i] * Z[:, i]

# Hitung Statistik Error
y_actual = data_input['y']
y_bar = np.mean(y_actual)
yi_ybar_sq = (y_actual - y_bar)**2      # Total Error
yi_model_sq = (y_actual - y_pred)**2    # Residual Error

St = np.sum(yi_ybar_sq)
Sr = np.sum(yi_model_sq)
Sy = math.sqrt(St / (n_data - 1)) if n_data > 1 else 0
Sy_x = math.sqrt(Sr / (n_data - n_vars)) if n_data > n_vars else 0
r2 = (St - Sr) / St if St != 0 else 0
r = math.sqrt(r2) if r2 >= 0 else 0

# Tabel Detail Evaluasi
df_final = df_display.copy()
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
eq_str = "y ="
for i in range(n_vars):
    sign = " + " if a[i] >= 0 else " - "
    val = abs(a[i])
    if i == 0:
        eq_str += f" {a[i]:.4f}" # Konstanta biasanya tidak dikali z0 di penulisan umum
    else:
        eq_str += f"{sign}{val:.4f} * z{i}"
print(f"PERSAMAAN MODEL:\n{eq_str}")
print("(Lihat tabel di atas untuk definisi z1, z2, dst)")
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