import numpy as np

# =========================================================================
# 1. INPUT DATA (SESUAI EXCEL PERTEMUAN 14 - HIGH ACCURACY)
# =========================================================================
# Diketahui dari Excel:
x0 = 0.5
fx0 = 0.925         # f(x)

x1 = 0.75
fx1 = 0.6363281     # f(x+h)

x2 = 1.0
fx2 = 0.2           # f(x+2h)

# Hitung step size h
h = x1 - x0

# =========================================================================
# 2. PERHITUNGAN (BASIC & HIGH ACCURACY)
# =========================================================================

# --- A. Basic Forward Difference O(h) ---
# Rumus: (f(x+h) - f(x)) / h
f_basic = (fx1 - fx0) / h

# --- B. High Accuracy Forward Difference O(h^2) ---
# Rumus: (-f(x+2h) + 4*f(x+h) - 3*f(x)) / (2*h)
# Perhatikan pembilangnya: -1, +4, -3
pembilang = -fx2 + (4 * fx1) - (3 * fx0)
penyebut = 2 * h
f_high = pembilang / penyebut

# =========================================================================
# 3. OUTPUT STEP-BY-STEP
# =========================================================================
print("=" * 80)
print("       DIFERENSIASI NUMERIK: FORWARD DIFFERENCE (HIGH ACCURACY)")
print("=" * 80)

print(f"Diketahui:")
print(f"   x      = {x0}  -> f(x)    = {fx0}")
print(f"   x+h    = {x1} -> f(x+h)  = {fx1}")
print(f"   x+2h   = {x2}  -> f(x+2h) = {fx2}")
print(f"   h      = {h}")
print("-" * 80)

print("\n## 1. BASIC FORMULA (Forward Difference O(h))")
print("Rumus: f'(x) ≈ (f(x+h) - f(x)) / h")
print(f"f'({x0}) ≈ ({fx1} - {fx0}) / {h}")
print(f"        ≈ {fx1 - fx0:.7f} / {h}")
print(f"        ≈ {f_basic:.7f}")

print("\n## 2. HIGH ACCURACY FORMULA (Forward Difference O(h^2))")
print("Rumus: f'(x) ≈ (-f(x+2h) + 4f(x+h) - 3f(x)) / 2h")
print(f"f'({x0}) ≈ (-({fx2}) + 4({fx1}) - 3({fx0})) / (2 * {h})")
print(f"        ≈ ({-fx2} + {4*fx1:.7f} - {3*fx0:.7f}) / {penyebut}")
print(f"        ≈ {pembilang:.7f} / {penyebut}")
print(f"        ≈ {f_high:.7f}")

# --- ANALISIS ERROR (OPSIONAL: JIKA KITA TAHU TRUE VALUE) ---
# Fungsi asli polinomial: f(x) = -0.1x^4 - 0.15x^3 - 0.5x^2 - 0.25x + 1.2
# Turunan aslinya: f'(x) = -0.4x^3 - 0.45x^2 - x - 0.25
def true_deriv(x):
    return -0.4*(x**3) - 0.45*(x**2) - 1.0*x - 0.25

true_val = true_deriv(x0)
err_basic = abs((true_val - f_basic)/true_val) * 100
err_high = abs((true_val - f_high)/true_val) * 100

print("-" * 80)
print("## ANALISIS ERROR (Perbandingan)")
print(f"Nilai Sebenarnya (True Value) : {true_val:.7f}")
print(f"Error Basic Formula           : {err_basic:.4f}%")
print(f"Error High Accuracy           : {err_high:.4f}%")
print("=" * 80)