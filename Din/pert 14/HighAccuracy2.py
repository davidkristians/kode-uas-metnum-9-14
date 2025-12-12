import numpy as np

# =========================================================================
# 1. INPUT DATA (SESUAI EXCEL PERTEMUAN 14 - HIGH ACCURACY 2)
# =========================================================================
# Target x = 0.5, Step size h = 0.25

# Data yang dibutuhkan untuk Central Difference High Accuracy (x-2h s/d x+2h)
x_min_2h = 0.00
fx_min_2h = 1.2         # f(x-2h) atau f(0)

x_min_h = 0.25
fx_min_h = 1.1035156    # f(x-h) atau f(0.25)

x_curr = 0.50
fx_curr = 0.925         # f(x) atau f(0.5)

x_plus_h = 0.75
fx_plus_h = 0.6363281   # f(x+h) atau f(0.75)

x_plus_2h = 1.00
fx_plus_2h = 0.2        # f(x+2h) atau f(1.0)

h = 0.25

# =========================================================================
# 2. PERHITUNGAN (BASIC & HIGH ACCURACY)
# =========================================================================

# --- A. Basic Formula (Central Difference O(h^2)) ---
# Rumus: (f(x+h) - f(x-h)) / (2h)
# Excel: =(B19-B18)/(2*B20)  -> (f(0.75) - f(0.25)) / (2*h)
pembilang_basic = fx_plus_h - fx_min_h
penyebut_basic  = 2 * h
f_basic = pembilang_basic / penyebut_basic

# --- B. High Accuracy Formula (Central Difference O(h^4)) ---
# Rumus: (-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)) / (12h)
# Excel: =(-B24 + 8*B25 - 8*B26 + B27)/(12*B28)
# Mapping Excel Anda:
# B24 = f(1)      -> fx_plus_2h
# B25 = f(0.75)   -> fx_plus_h
# B26 = f(0.25)   -> fx_min_h
# B27 = f(0)      -> fx_min_2h
term1 = -fx_plus_2h
term2 = 8 * fx_plus_h
term3 = -8 * fx_min_h
term4 = fx_min_2h

pembilang_high = term1 + term2 + term3 + term4
penyebut_high  = 12 * h
f_high = pembilang_high / penyebut_high

# =========================================================================
# 3. OUTPUT STEP-BY-STEP
# =========================================================================
print("=" * 85)
print("       DIFERENSIASI NUMERIK: CENTRAL DIFFERENCE (HIGH ACCURACY 2)")
print("=" * 85)

print(f"Diketahui:")
print(f"   h      = {h}")
print(f"   x-2h   = {x_min_2h:<4} -> f = {fx_min_2h}")
print(f"   x-h    = {x_min_h:<4} -> f = {fx_min_h}")
print(f"   x      = {x_curr:<4} -> f = {fx_curr}")
print(f"   x+h    = {x_plus_h:<4} -> f = {fx_plus_h}")
print(f"   x+2h   = {x_plus_2h:<4} -> f = {fx_plus_2h}")
print("-" * 85)

print("\n## 1. BASIC FORMULA (Central Difference O(h^2))")
print("Rumus: f'(x) ≈ (f(x+h) - f(x-h)) / 2h")
print(f"f'({x_curr}) ≈ ({fx_plus_h} - {fx_min_h}) / (2 * {h})")
print(f"        ≈ {pembilang_basic:.7f} / {penyebut_basic:.2f}")
print(f"        ≈ {f_basic:.7f}")

print("\n## 2. HIGH ACCURACY FORMULA (Central Difference O(h^4))")
print("Rumus: f'(x) ≈ (-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)) / 12h")
print(f"Term 1 (-f(x+2h)) : {-fx_plus_2h}")
print(f"Term 2 (+8f(x+h)) : 8 * {fx_plus_h} = {term2:.7f}")
print(f"Term 3 (-8f(x-h)) : -8 * {fx_min_h} = {term3:.7f}")
print(f"Term 4 (+f(x-2h)) : {fx_min_2h}")
print("-" * 40 + " +")
print(f"Pembilang         : {pembilang_high:.7f}")
print(f"Penyebut (12*h)   : {penyebut_high:.2f}")
print(f"Hasil Akhir       : {f_high:.7f}")

# --- ANALISIS ERROR ---
# Fungsi asli: f(x) = -0.1x^4 - 0.15x^3 - 0.5x^2 - 0.25x + 1.2
# Turunan: f'(x) = -0.4x^3 - 0.45x^2 - x - 0.25
def true_deriv(x):
    return -0.4*(x**3) - 0.45*(x**2) - 1.0*x - 0.25

true_val = true_deriv(x_curr)
err_basic = abs((true_val - f_basic)/true_val) * 100
err_high = abs((true_val - f_high)/true_val) * 100

print("-" * 85)
print("## ANALISIS ERROR (Perbandingan)")
print(f"Nilai Sebenarnya (True Value) : {true_val:.7f}")
print(f"Error Basic Formula           : {err_basic:.4f}%")
print(f"Error High Accuracy           : {err_high:.4f}% (Sangat Akurat!)")
print("=" * 85)