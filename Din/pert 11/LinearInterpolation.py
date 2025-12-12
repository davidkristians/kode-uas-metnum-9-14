import numpy as np

# =========================================================================
# 1. INPUT DATA (GANTI BAGIAN INI SESUAI SOAL)
# =========================================================================
# Contoh Data: Kita punya dua titik (x0, y0) dan (x1, y1)
# Misal: Mencari nilai log(2) pakai data log(1) dan log(6) (hanya contoh)
x0 = 1.0
y0 = 0.0

x1 = 6.0
y1 = 1.791759

# Titik x yang ingin dicari nilai y-nya
x_ask = 2.0 

# =========================================================================
# 2. PERHITUNGAN (RUMUS NEWTON ORDE 1)
# Rumus: y = y0 + (y1 - y0)/(x1 - x0) * (x - x0)
# =========================================================================

# Langkah 1: Hitung Gradient / Slope (b1) / Divided Difference pertama
# b1 = (y1 - y0) / (x1 - x0)
pembilang = y1 - y0
penyebut  = x1 - x0

if penyebut == 0:
    print("Error: x0 dan x1 tidak boleh sama (pembagian dengan nol).")
    exit()

b1 = pembilang / penyebut

# Langkah 2: Hitung Hasil Interpolasi
# y_ask = y0 + b1 * (x_ask - x0)
y_ask = y0 + b1 * (x_ask - x0)

# =========================================================================
# 3. OUTPUT STEP-BY-STEP (UNTUK BELAJAR/UJIAN)
# =========================================================================
print("=" * 60)
print("              HASIL INTERPOLASI LINEAR")
print("=" * 60)

print("Diketahui Titik Data:")
print(f"Titik 0: (x0={x0}, y0={y0})")
print(f"Titik 1: (x1={x1}, y1={y1})")
print(f"Ditanya: Nilai y saat x = {x_ask}")
print("-" * 60)

print("\nLANGKAH 1: Hitung Kemiringan (Slope / b1)")
print("Rumus b1 = (y1 - y0) / (x1 - x0)")
print(f"b1 = ({y1} - {y0}) / ({x1} - {x0})")
print(f"b1 = {pembilang:.6f} / {penyebut:.6f}")
print(f"b1 = {b1:.7f}")

print("\nLANGKAH 2: Masukkan ke Persamaan Linear")
print("Rumus: y = y0 + b1 * (x - x0)")
print(f"y = {y0} + {b1:.7f} * ({x_ask} - {x0})")
print(f"y = {y0} + {b1:.7f} * ({x_ask - x0})")
print(f"y = {y0} + {b1 * (x_ask - x0):.7f}")
print(f"y = {y_ask:.7f}")

print("-" * 60)
print(f"HASIL AKHIR: y({x_ask}) ≈ {y_ask:.7f}")
print("-" * 60)