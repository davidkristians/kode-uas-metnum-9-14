import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI FILE EXCEL Pertemuan 11 - Linear Lagrange)
# =========================================================================
# Titik 0 (x0, y0)
x0 = 1.0
y0 = 0.0

# Titik 1 (x1, y1)
x1 = 4.0
y1 = 1.386294

# Titik yang dicari (xf)
xf = 2.0

# =========================================================================
# 2. PERHITUNGAN LAGRANGE LINEAR
# =========================================================================
# Rumus L0 = (x - x1) / (x0 - x1)
L0 = (xf - x1) / (x0 - x1)

# Rumus L1 = (x - x0) / (x1 - x0)
L1 = (xf - x0) / (x1 - x0)

# Hitung Hasil f(x) = L0*y0 + L1*y1
term0 = L0 * y0
term1 = L1 * y1
fx = term0 + term1

# =========================================================================
# 3. OUTPUT STEP-BY-STEP & TABEL (FORMAT LAPORAN)
# =========================================================================
print("=" * 80)
print("           INTERPOLASI LAGRANGE LINEAR (ORDE 1)")
print("=" * 80)
print(f"Titik 0 : ({x0}, {y0})")
print(f"Titik 1 : ({x1}, {y1})")
print(f"Mencari x : {xf}")
print("-" * 80)

print("\n## 1. HITUNG BOBOT LAGRANGE (L)")
print("Rumus Umum Li(x) = Π (x - xj) / (xi - xj)")

print(f"\n[L0]:")
print(f"L0 = (x - x1) / (x0 - x1)")
print(f"   = ({xf} - {x1}) / ({x0} - {x1})")
print(f"   = {xf - x1} / {x0 - x1}")
print(f"   = {L0:.8f}")

print(f"\n[L1]:")
print(f"L1 = (x - x0) / (x1 - x0)")
print(f"   = ({xf} - {x0}) / ({x1} - {x0})")
print(f"   = {xf - x0} / {x1 - x0}")
print(f"   = {L1:.8f}")

print("\n## 2. TABEL KOEFISIEN LAGRANGE")
print("-" * 50)
data = {
    'i': [0, 1],
    'xi': [x0, x1],
    'f(xi)': [y0, y1],
    'Coeff (Li)': [L0, L1]
}
df = pd.DataFrame(data)
print(df.to_string(index=False))
print("-" * 50)

print("\n## 3. HITUNG NILAI AKHIR")
print("Rumus: f1(x) = L0 * f(x0) + L1 * f(x1)")
print(f"f1({xf}) = ({L0:.6f} * {y0}) + ({L1:.6f} * {y1})")
print(f"       = {term0:.6f} + {term1:.6f}")
print(f"       = {fx:.6f}")

print("\n" + "="*80)