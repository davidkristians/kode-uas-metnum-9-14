import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI FILE Pertemuan 11.xlsx - Quadratic.csv)
# =========================================================================
# Titik Data (x, y)
x = np.array([1.0, 4.0, 6.0])      # x0, x1, x2
y = np.array([0.0, 1.386294, 1.791759]) # y0, y1, y2

# Titik yang ingin dicari
x_ask = 2.0

# =========================================================================
# 2. PERHITUNGAN KOEFISIEN (Divided Difference)
# =========================================================================
# b0 = f(x0)
b0 = y[0]

# b1 = (f(x1) - f(x0)) / (x1 - x0)
b1 = (y[1] - y[0]) / (x[1] - x[0])

# Hitung slope sementara antara x1 dan x2 untuk mencari b2
# slope_1_2 = (f(x2) - f(x1)) / (x2 - x1)
slope_1_2 = (y[2] - y[1]) / (x[2] - x[1])

# b2 = (slope_1_2 - b1) / (x2 - x0)
b2 = (slope_1_2 - b1) / (x[2] - x[0])

# =========================================================================
# 3. PERHITUNGAN NILAI AKHIR (Polinomial Newton Orde 2)
# Rumus: y = b0 + b1(x - x0) + b2(x - x0)(x - x1)
# =========================================================================
# Suku per suku agar mudah dicek
term0 = b0
term1 = b1 * (x_ask - x[0])
term2 = b2 * (x_ask - x[0]) * (x_ask - x[1])

y_ask = term0 + term1 + term2

# =========================================================================
# 4. OUTPUT STEP-BY-STEP & TABEL (MIRIP EXCEL)
# =========================================================================
print("=" * 75)
print("           HASIL INTERPOLASI KUADRATIK (NEWTON ORDE 2)")
print("=" * 75)

print(f"Dicari: Nilai y saat x = {x_ask}")
print("-" * 75)

print("## LANGKAH 1: Hitung Koefisien (Divided Difference)")
print(f"b0 = y0 = {b0:.6f}")
print(f"b1 = (y1 - y0) / (x1 - x0)")
print(f"   = ({y[1]} - {y[0]}) / ({x[1]} - {x[0]}) = {b1:.6f}")
print(f"Slope (1-2) = ({y[2]} - {y[1]}) / ({x[2]} - {x[1]}) = {slope_1_2:.6f}")
print(f"b2 = (Slope(1-2) - b1) / (x2 - x0)")
print(f"   = ({slope_1_2:.6f} - {b1:.6f}) / ({x[2]} - {x[0]}) = {b2:.6f}")

print("\n## LANGKAH 2: Masukkan ke Persamaan Polinomial")
print("Rumus: f2(x) = b0 + b1(x - x0) + b2(x - x0)(x - x1)")
print(f"f2({x_ask}) = {b0:.6f} + {b1:.6f}({x_ask} - {x[0]}) + ({b2:.6f})({x_ask} - {x[0]})({x_ask} - {x[1]})")

print("\n## LANGKAH 3: Hitung Nilai Akhir")
print(f"Suku 1 (b0)                        = {term0:.6f}")
print(f"Suku 2 (b1 * (x-x0))               = {term1:.6f}")
print(f"Suku 3 (b2 * (x-x0)*(x-x1))        = {term2:.6f}")
print("-" * 35 + " +")
print(f"Hasil Akhir f2({x_ask})               = {y_ask:.6f}")

# Cek Error relatif (karena kita tahu ini fungsi ln(x))
y_true = np.log(x_ask)
error = abs((y_true - y_ask)/y_true) * 100
print("-" * 75)
print(f"Sebagai perbandingan (True Value ln(2)): {y_true:.6f}")
print(f"Error Relatif: {error:.4f}%")
print("=" * 75)