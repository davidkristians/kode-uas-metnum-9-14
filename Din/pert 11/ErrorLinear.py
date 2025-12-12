import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI FILE EXCEL Pertemuan 11 - Error Linear)
# =========================================================================
# Titik Awal (x0) dan Akhir (x1) untuk Interpolasi Linear
x0 = 1.0
y0 = 0.0

x1 = 6.0
y1 = 1.791759

# Titik Tambahan/Tengah (xm) untuk Estimasi Error
# (Diambil dari baris ke-7 Excel: "x   4   1.386294")
xm = 4.0
ym = 1.386294

# Titik yang dicari (xf)
xf = 2.0

# =========================================================================
# 2. PERHITUNGAN INTERPOLASI LINEAR
# =========================================================================
# Slope Linear (b1) antara x0 dan x1
b1_linear = (y1 - y0) / (x1 - x0)

# Hasil Interpolasi Linear
f1 = y0 + b1_linear * (xf - x0)

# =========================================================================
# 3. PERHITUNGAN ESTIMASI ERROR (MENGGUNAKAN KOEFISIEN b2)
# =========================================================================
# Kita butuh b2 dari 3 titik: (x0, y0), (xm, ym), (x1, y1)

# 1. Hitung First Divided Difference (Slope tingkat 1)
# Slope 0 ke m
slope_0_m = (ym - y0) / (xm - x0)
# Slope m ke 1
slope_m_1 = (y1 - ym) / (x1 - xm)

# 2. Hitung Second Divided Difference (b2)
# Note: Pembaginya adalah ujung ke ujung (x1 - x0)
b2 = (slope_m_1 - slope_0_m) / (x1 - x0)

# 3. Hitung Estimasi Error
# Rumus: Error = b2 * (xf - x0) * (xf - x1)
estimated_error = b2 * (xf - x0) * (xf - x1)

# Hitung Persentase Error (relatif terhadap hasil linear, atau value absolut)
# Sesuai output Excel/David, ini sepertinya hanya estimated_error * 100
error_percent = estimated_error * 100

# =========================================================================
# 4. OUTPUT STEP-BY-STEP & TABEL (FORMAT RAPI)
# =========================================================================
print("=" * 80)
print("         ESTIMASI ERROR INTERPOLASI LINEAR (METODE TITIK TAMBAHAN)")
print("=" * 80)
print(f"Titik Linear : ({x0}, {y0}) sampai ({x1}, {y1})")
print(f"Titik Extra  : ({xm}, {ym})")
print(f"Mencari x    : {xf}")
print("-" * 80)

print("\n## 1. HASIL INTERPOLASI LINEAR")
print(f"Slope (b1) = ({y1} - {y0}) / ({x1} - {x0}) = {b1_linear:.7f}")
print(f"f1({xf})     = {y0} + {b1_linear:.7f} * ({xf} - {x0})")
print(f"           = {f1:.7f}")

print("\n## 2. TABEL KOEFISIEN ERROR (b2)")
print("Menghitung kelengkungan menggunakan titik ekstra (xm).")
print("-" * 80)

# Membuat DataFrame untuk tampilan Tabel Divided Difference
# Urutan data untuk perhitungan b2: x0 -> xm -> x1
data_table = {
    'xi': [x0, xm, x1],
    'f(xi)': [y0, ym, y1],
    'First DD': [f"{slope_0_m:.7f}", f"{slope_m_1:.7f}", "-"],
    'Second DD (b2)': [f"{b2:.7f}", "-", "-"]
}
df = pd.DataFrame(data_table)
print(df.to_string(index=False))
print("-" * 80)

print("\n## 3. HASIL ESTIMASI ERROR")
print("Rumus: Error = b2 * (xf - x0) * (xf - x1)")
print(f"Error = {b2:.7f} * ({xf} - {x0}) * ({xf} - {x1})")
print(f"      = {b2:.7f} * ({xf - x0}) * ({xf - x1})")
print(f"      = {estimated_error:.7f}")

print("\n## 4. PERSENTASE ERROR")
print(f"Error % = {estimated_error:.7f} * 100")
print(f"        = {error_percent:.7f} %")

print("=" * 80)