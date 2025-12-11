import numpy as np
import pandas as pd
import math

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== REGRESI NON-LINEAR (METODE GAUSS-NEWTON) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA & TEBAKAN AWAL (UBAH DISINI)
# ==============================================================================
# 1. Masukkan Data X dan Y
# ##############################################################################
# Contoh Data dari Excel Pertemuan 10 (Non Linear)
x_i = np.array([0.25, 0.75, 1.25, 1.75, 2.25]) 
y_i = np.array([0.28, 0.57, 0.68, 0.74, 0.79])
# ##############################################################################

# 2. Masukkan Tebakan Awal (Initial Guess)
# ##############################################################################
# Berapa banyak parameter (a0, a1, ...)? Sesuaikan jumlahnya.
a_init = np.array([1.0, 1.0]) 
# ##############################################################################

# ==============================================================================
# BAGIAN 2: DEFINISI MODEL & TURUNAN ( !!! BAGIAN INI SANGAT PENTING !!! )
# ==============================================================================
def get_model_and_derivatives(x, a):
    """
    Disini Anda harus menuliskan RUMUS FUNGSI dan TURUNAN PARSIALNYA.
    a[0] adalah a0, a[1] adalah a1, dst.
    """
    a0 = a[0]
    a1 = a[1]
    
    # --- MODEL 1: y = a0 * (1 - e^(-a1 * x)) --- (Sesuai Excel)
    # 1. Tulis Fungsi Asli
    fx = a0 * (1 - np.exp(-a1 * x))
    
    # 2. Tulis Turunan Parsial terhadap a0 (Anggap a1 konstan)
    df_da0 = 1 - np.exp(-a1 * x)
    
    # 3. Tulis Turunan Parsial terhadap a1 (Anggap a0 konstan)
    # Turunan e^(-u) adalah -u' * e^(-u)
    # Jadi turunan (1 - e^(-a1*x)) thd a1 adalah: -(-x) * e^(-a1*x) = x * e^(-a1*x)
    df_da1 = a0 * x * np.exp(-a1 * x)
    
    return fx, df_da0, df_da1

    # --- MODEL 2: y = a0 * x / (a1 + x) --- (Contoh Michaelis-Menten Tanpa Log)
    # fx = (a0 * x) / (a1 + x)
    # df_da0 = x / (a1 + x)              # Turunan thd a0
    # df_da1 = -(a0 * x) / ((a1 + x)**2) # Turunan thd a1 (Pakai rumus u/v)
    # return fx, df_da0, df_da1

# ==============================================================================
# BAGIAN 3: PROSES ITERASI (JANGAN UBAH INI)
# ==============================================================================
max_iter = 20       # Batas maksimum iterasi
tolerance = 1e-6    # Toleransi error
a_current = a_init.copy()

print(f"Tebakan Awal: {a_current}\n")

for i in range(max_iter):
    # 1. Hitung Fungsi dan Jacobian
    # Unpack sesuai jumlah parameter. Jika ada 3 parameter, tambah z2_col
    fx, z0_col, z1_col = get_model_and_derivatives(x_i, a_current)
    
    # 2. Hitung Residual (D)
    D = y_i - fx
    
    # 3. Susun Matriks Jacobian [Z]
    Z = np.stack([z0_col, z1_col], axis=1)
    
    # Tampilkan Iterasi
    print(f"--- ITERASI KE-{i+1} ---")
    
    # 4. Hitung Delta A: [Z]T[Z] {dA} = [Z]T{D}
    Z_T_Z = Z.T @ Z
    Z_T_D = Z.T @ D
    
    try:
        delta_a = np.linalg.inv(Z_T_Z) @ Z_T_D
    except np.linalg.LinAlgError:
        print("Error: Matriks Singular. Cek tebakan awal atau model.")
        break
    
    # 5. Update Nilai Koefisien
    a_new = a_current + delta_a
    
    # Hitung Error Relatif (%) untuk cek berhenti
    ea = np.max(np.abs((a_new - a_current) / a_new) * 100)
    
    print(f"Koefisien Lama : {a_current}")
    print(f"Perubahan (dA) : {delta_a}")
    print(f"Koefisien Baru : {a_new}")
    print(f"Error Relatif  : {ea:.5f} %\n")
    
    if ea < tolerance:
        print(">> KONVERGEN! Hasil sudah stabil.")
        a_current = a_new
        break
        
    a_current = a_new

# ==============================================================================
# BAGIAN 4: HASIL AKHIR
# ==============================================================================
print("="*60)
print("HASIL AKHIR KOEFISIEN:")
print("="*60)
for j in range(len(a_current)):
    print(f"a{j} = {a_current[j]:.7f}")

# Hitung R^2 Akhir
y_pred, _, _ = get_model_and_derivatives(x_i, a_current)
St = np.sum((y_i - np.mean(y_i))**2)
Sr = np.sum((y_i - y_pred)**2)
r2 = (St - Sr) / St

print("-" * 60)
print(f"r^2 (Determinasi) = {r2:.7f} ({r2*100:.4f}%)")
print("-" * 60)