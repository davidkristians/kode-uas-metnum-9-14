import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. DEFINISI FUNGSI DAN TURUNAN
# =========================================================================
# Fungsi: f(x) = 9 * e^(4x)
def f(x):
    return 9 * math.exp(4 * x)

# Turunan Sebenarnya (Analitik): f'(x) = 36 * e^(4x)
def f_prime_true(x):
    return 36 * math.exp(4 * x)

# =========================================================================
# 2. PARAMETER SIMULASI
# =========================================================================
x_target = 0.2
true_val = f_prime_true(x_target) # ~ 80.1194734257288

# Kita mulai dengan h yang agak besar, lalu dikecilkan separuhnya berulang kali
# Di Excel biasanya dimulai misal dari h=0.1 atau h=0.05
h_start = 0.05 
iterations = 10 # Jumlah baris simulasi

# =========================================================================
# 3. PROSES ITERASI (MENGECILKAN STEP SIZE h)
# =========================================================================
results = []
h = h_start

for i in range(iterations):
    # 1. Hitung Forward Difference: (f(x+h) - f(x)) / h
    f_x = f(x_target)
    f_x_plus_h = f(x_target + h)
    
    deriv_approx = (f_x_plus_h - f_x) / h
    
    # 2. Hitung True Error (%)
    # Rumus Excel: ((Approx - True) / True) * 100
    error_percent = abs((deriv_approx - true_val) / true_val) * 100
    
    # Simpan hasil
    results.append({
        'Iterasi': i+1,
        'Step Size (h)': h,
        'f\'(x) Approx': deriv_approx,
        'True Error (%)': error_percent
    })
    
    # Perkecil h untuk iterasi berikutnya (h = h / 2)
    h = h / 2

# =========================================================================
# 4. OUTPUT TABEL HASIL
# =========================================================================
print("=" * 85)
print("       ANALISIS PENGARUH STEP SIZE (h) TERHADAP ERROR")
print(f"       Fungsi: f(x) = 9e^(4x)  |  Titik x = {x_target}")
print(f"       True Value f'(0.2) = {true_val:.13f}")
print("=" * 85)

df = pd.DataFrame(results)

# Format display agar rapi
pd.set_option('display.float_format', lambda x: '%.9f' % x)

# Tampilkan tabel tanpa index default pandas
print(df.to_string(index=False))

print("-" * 85)
print("KESIMPULAN:")
print("1. Perhatikan kolom 'Step Size (h)' yang semakin kecil (dibagi 2).")
print("2. Perhatikan kolom 'True Error (%)' yang juga ikut mengecil secara drastis.")
print("   Ini membuktikan teori: Semakin kecil h, semakin akurat hasil Forward Difference.")
print("   (Hingga batas presisi mesin komputer tercapai).")
print("=" * 85)