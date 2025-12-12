import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI FILE EXCEL Pertemuan 11 - Quadratic Lagrange)
# =========================================================================
# 3 Titik Data (x, y)
x = np.array([1.0, 4.0, 6.0])      # x0, x1, x2
y = np.array([0.0, 1.386294, 1.791759]) # y0, y1, y2

# Titik yang dicari (xf)
xf = 2.0

# =========================================================================
# 2. PERHITUNGAN LAGRANGE KUADRATIK (MANUAL STEP-BY-STEP)
# =========================================================================

# --- Hitung L0 ---
# Pembilang: (x - x1)(x - x2)
# Penyebut : (x0 - x1)(x0 - x2)
num0 = (xf - x[1]) * (xf - x[2])
den0 = (x[0] - x[1]) * (x[0] - x[2])
L0 = num0 / den0

# --- Hitung L1 ---
# Pembilang: (x - x0)(x - x2)
# Penyebut : (x1 - x0)(x1 - x2)
num1 = (xf - x[0]) * (xf - x[2])
den1 = (x[1] - x[0]) * (x[1] - x[2])
L1 = num1 / den1

# --- Hitung L2 ---
# Pembilang: (x - x0)(x - x1)
# Penyebut : (x2 - x0)(x2 - x1)
num2 = (xf - x[0]) * (xf - x[1])
den2 = (x[2] - x[0]) * (x[2] - x[1])
L2 = num2 / den2

# --- Hitung Nilai Akhir ---
# f2(x) = L0*y0 + L1*y1 + L2*y2
val0 = L0 * y[0]
val1 = L1 * y[1]
val2 = L2 * y[2]

fx = val0 + val1 + val2

# =========================================================================
# 3. OUTPUT STEP-BY-STEP & TABEL
# =========================================================================
print("=" * 85)
print("           INTERPOLASI LAGRANGE KUADRATIK (ORDE 2)")
print("=" * 85)
print(f"Titik 0 : ({x[0]}, {y[0]})")
print(f"Titik 1 : ({x[1]}, {y[1]})")
print(f"Titik 2 : ({x[2]}, {y[2]})")
print(f"Mencari x : {xf}")
print("-" * 85)

print("\n## 1. PERHITUNGAN BOBOT LAGRANGE (L)")

print(f"\n[L0] (Abaikan x0 di atas):")
print(f"L0 = (({xf} - {x[1]}) * ({xf} - {x[2]})) / (({x[0]} - {x[1]}) * ({x[0]} - {x[2]}))")
print(f"   = ({xf - x[1]} * {xf - x[2]}) / ({x[0] - x[1]} * {x[0] - x[2]})")
print(f"   = {num0} / {den0}")
print(f"   = {L0:.8f}")

print(f"\n[L1] (Abaikan x1 di atas):")
print(f"L1 = (({xf} - {x[0]}) * ({xf} - {x[2]})) / (({x[1]} - {x[0]}) * ({x[1]} - {x[2]}))")
print(f"   = ({xf - x[0]} * {xf - x[2]}) / ({x[1] - x[0]} * {x[1] - x[2]})")
print(f"   = {num1} / {den1}")
print(f"   = {L1:.8f}")

print(f"\n[L2] (Abaikan x2 di atas):")
print(f"L2 = (({xf} - {x[0]}) * ({xf} - {x[1]})) / (({x[2]} - {x[0]}) * ({x[2]} - {x[1]}))")
print(f"   = ({xf - x[0]} * {xf - x[1]}) / ({x[2] - x[0]} * {x[2] - x[1]})")
print(f"   = {num2} / {den2}")
print(f"   = {L2:.8f}")

print("-" * 85)
# Validasi Sigma L = 1
sum_L = L0 + L1 + L2
print(f"CHECK: Total Bobot L0 + L1 + L2 = {sum_L:.8f} (Harus 1.0)")
if abs(sum_L - 1.0) > 1e-9:
    print("WARNING: Jumlah bobot tidak sama dengan 1. Cek perhitungan!")
else:
    print("STATUS: OK (Valid)")

print("\n## 2. TABEL HASIL")
print("-" * 85)
data = {
    'i': [0, 1, 2],
    'xi': x,
    'f(xi)': y,
    'Coeff (Li)': [L0, L1, L2],
    'Li * f(xi)': [val0, val1, val2]
}
df = pd.DataFrame(data)
print(df.to_string(index=False))
print("-" * 85)

print("\n## 3. HASIL AKHIR")
print(f"f2({xf}) = Σ (Li * f(xi))")
print(f"       = {val0:.6f} + {val1:.6f} + {val2:.6f}")
print(f"       = {fx:.6f}")
print("=" * 85)