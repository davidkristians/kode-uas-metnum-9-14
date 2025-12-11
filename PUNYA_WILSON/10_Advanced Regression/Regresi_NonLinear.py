import numpy as np
import pandas as pd
import math

# Ini adalah kode yang paling "tricky" karena Anda harus menurunkan rumus (kalkulus dasar) sebelum memakainya.
#     Lihat Soal: Misal soalnya: y=a0​(1−e−a1​x).
#     1. Cari Turunan Parsial (Di Kertas Buram):
#         Turunan terhadap a0​ (∂a0​∂f​): Anggap a1​ angka biasa. Hasilnya: (1−e−a1​x).
#         Turunan terhadap a1​ (∂a1​∂f​): Anggap a0​ angka biasa. Turunan dari e−a1​x adalah −xe−a1​x. Dikali minus didepan dan a0​, hasilnya: a0​xe−a1​x.
#     2. Masukkan ke Code (BAGIAN 2):
#         Tulis rumus asli di fx = ....
#         Tulis hasil turunan di df_da0 = ... dan df_da1 = ....
#     3. Tebakan Awal: Jika soal tidak memberi tahu tebakan awal, gunakan 1.0 dan 1.0 biasanya cukup aman untuk memulai.
# Kode ini akan menampilkan tabel iterasi persis seperti yang diminta di file Excel Anda (ada kolom Residual D, ada kolom Turunan Z).

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== REGRESI NON-LINEAR (METODE GAUSS-NEWTON) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA & TEBAKAN AWAL (UBAH DISINI)
# ==============================================================================
# 1. Masukkan Data Soal
x_i = np.array([0.25, 0.75, 1.25, 1.75, 2.25]) 
y_i = np.array([0.28, 0.57, 0.68, 0.74, 0.79])

# 2. Masukkan Tebakan Awal (Initial Guess) untuk a0, a1...
# Soal Non-Linear PASTI butuh tebakan awal. Lihat soal/petunjuk.
a_init = np.array([1.0, 1.0]) # Misal a0=1, a1=1

# ==============================================================================
# BAGIAN 2: DEFINISI MODEL & TURUNAN PARSIAL (INTI PERUBAHAN)
# ==============================================================================
# Anda harus mendefinisikan fungsi (f) dan turunan parsialnya terhadap a0, a1, dst.

def get_model_and_derivatives(x, a):
    a0 = a[0]
    a1 = a[1]
    
    # --- CONTOH 1: Model Excel Anda: y = a0 * (1 - e^(-a1 * x)) ---
    # Fungsi Asli
    fx = a0 * (1 - np.exp(-a1 * x))
    
    # Turunan Parsial terhadap a0 (df/da0)
    # Turunan dari a0*(...) terhadap a0 adalah (...)
    df_da0 = 1 - np.exp(-a1 * x)
    
    # Turunan Parsial terhadap a1 (df/da1)
    # Turunan dari -a0*e^(-a1*x) terhadap a1 adalah a0*x*e^(-a1*x)
    df_da1 = a0 * x * np.exp(-a1 * x)
    
    return fx, df_da0, df_da1

    # --- CONTOH 2: Model y = a0 * e^(a1 * x) (Misal diminta pakai Gauss-Newton) ---
    # fx = a0 * np.exp(a1 * x)
    # df_da0 = np.exp(a1 * x)      # Turunan thd a0
    # df_da1 = a0 * x * np.exp(a1 * x) # Turunan thd a1
    # return fx, df_da0, df_da1

# ==============================================================================
# BAGIAN 3: PROSES ITERASI (LOOPING) - JANGAN UBAH INI
# ==============================================================================
max_iter = 10       # Maksimal iterasi (biar ga looping selamanya)
tolerance = 1e-5    # Batas error berhenti
a_current = a_init.copy()

print(f"Tebakan Awal: {a_current}\n")

for i in range(max_iter):
    print(f"--- ITERASI KE-{i+1} ---")
    
    # 1. Hitung Fungsi (fx) dan Turunan (Jacobian Columns)
    fx, z0_col, z1_col = get_model_and_derivatives(x_i, a_current)
    
    # 2. Hitung Residual D (Selisih Data Asli - Prediksi)
    # D = y - f(x)
    D = y_i - fx
    
    # 3. Susun Matriks Jacobian [Z]
    # Kolom 1 = turunan thd a0, Kolom 2 = turunan thd a1
    Z = np.stack([z0_col, z1_col], axis=1)
    
    # 4. Tampilkan Tabel Detail per Iterasi
    df_iter = pd.DataFrame({
        'xi': x_i, 'yi': y_i, 'f(xi)': fx,
        'df/da0': z0_col, 'df/da1': z1_col,
        'Residual (D)': D
    })
    print(df_iter.to_string(index=False))
    
    # 5. Selesaikan Persamaan Matriks: [Z]T [Z] {Delta_A} = [Z]T {D}
    Z_T_Z = Z.T @ Z
    Z_T_D = Z.T @ D
    
    try:
        # Menghitung Delta A (Perubahan Nilai a)
        delta_a = np.linalg.inv(Z_T_Z) @ Z_T_D
    except np.linalg.LinAlgError:
        print("Error: Matriks Singular di tengah iterasi.")
        break
        
    print(f"\nDelta a (Perubahan): {delta_a}")
    
    # 6. Update Nilai a
    a_new = a_current + delta_a
    print(f"Nilai a Baru: {a_new}\n")
    
    # Cek Konvergensi (Apakah perubahan sudah sangat kecil?)
    # Menghitung error relatif rata-rata
    ea = np.abs((a_new - a_current) / a_new) * 100
    if np.all(ea < tolerance):
        print(">> KONVERGEN (Hasil sudah stabil). Berhenti Iterasi.")
        a_current = a_new
        break
        
    a_current = a_new

# ==============================================================================
# BAGIAN 4: HASIL AKHIR & ANALISIS ERROR
# ==============================================================================
print("\n" + "="*60)
print("HASIL AKHIR KOEFISIEN (Non-Linear):")
print("="*60)
for j in range(len(a_current)):
    print(f"a{j} = {a_current[j]:.7f}")

# Hitung Statistik Akhir
y_pred, _, _ = get_model_and_derivatives(x_i, a_current)
n = len(y_i)
m = len(a_current)

St = np.sum((y_i - np.mean(y_i))**2)
Sr = np.sum((y_i - y_pred)**2)
r2 = (St - Sr) / St
Sy_x = math.sqrt(Sr / (n - m))

print("-" * 60)
print("PERSAMAAN AKHIR (Format sesuai model Anda):")
print(f"y = {a_current[0]:.4f} * (1 - e^(-{a_current[1]:.4f} * x))") # Ganti teks ini jika model berubah
print("-" * 60)
print(f"St (Total Error)        = {St:.7f}")
print(f"Sr (Residual Error)     = {Sr:.7f}")
print(f"r^2 (Determinasi)       = {r2:.7f} ({r2*100:.4f}%)")
print(f"Sy/x (Std Error Est)    = {Sy_x:.7f}")
print("-" * 60)