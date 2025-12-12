import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI FILE EXCEL Pertemuan 11 - Error Quadratic)
# =========================================================================
# 3 Titik Utama untuk Interpolasi Kuadratik (x0, x1, x2)
base_points = [
    (1.0, 0.0),        # x0, f(x0)
    (4.0, 1.386294),   # x1, f(x1)
    (6.0, 1.791759)    # x2, f(x2)
]

# 1 Titik Tambahan untuk Estimasi Error (xm / extra)
# Dari Excel baris 9: "x  5  1.609438"
extra_point = (5.0, 1.609438)

# Titik yang dicari (xf)
xf = 2.0

# =========================================================================
# 2. LOGIKA UTAMA: NEWTON DIVIDED DIFFERENCE (Mencari b3)
# =========================================================================
# Gabungkan semua titik dan urutkan berdasarkan x agar tabel rapi
# Urutan di Excel: 1, 4, 5, 6
all_points = base_points + [extra_point]
all_points.sort(key=lambda p: p[0]) 

n = len(all_points)
x = np.array([p[0] for p in all_points])
y = np.array([p[1] for p in all_points])

# Buat Tabel Divided Difference
table = np.zeros((n, n))
table[:, 0] = y

# Isi Tabel
for j in range(1, n):
    for i in range(n - j):
        numerator = table[i + 1, j - 1] - table[i, j - 1]
        denominator = x[i + j] - x[i]
        table[i, j] = numerator / denominator

# Ambil b3 (Third Difference) dari baris paling atas (index 0, kolom 3)
b3 = table[0, 3]

# =========================================================================
# 3. PERHITUNGAN ERROR
# =========================================================================
# Rumus Error Kuadratik: Error = b3 * (xf - x0) * (xf - x1) * (xf - x2)
# Gunakan x0, x1, x2 dari titik base_points ASLI (bukan yang sudah disortir)
# Tapi biasanya x0, x1, x2 adalah 3 titik pertama yang berurutan.
x0_orig = base_points[0][0]
x1_orig = base_points[1][0]
x2_orig = base_points[2][0]

term1 = xf - x0_orig
term2 = xf - x1_orig
term3 = xf - x2_orig

error_val = b3 * term1 * term2 * term3
error_percent = error_val * 100

# =========================================================================
# 4. OUTPUT STEP-BY-STEP & TABEL
# =========================================================================
print("=" * 85)
print("         ESTIMASI ERROR INTERPOLASI KUADRATIK (METODE TITIK TAMBAHAN)")
print("=" * 85)
print(f"3 Titik Utama : {base_points}")
print(f"Titik Extra   : {extra_point}")
print(f"Mencari x     : {xf}")
print("-" * 85)

print("\n## 1. TABEL DIVIDED DIFFERENCE (Termasuk Titik Extra)")
print("Tabel ini digunakan untuk mencari b3 (Third Difference).")
print("-" * 85)

# Tampilkan Tabel menggunakan Pandas
col_names = ['f(xi)', 'First', 'Second', 'Third (b3)']
df_table = pd.DataFrame(table, columns=col_names)
df_table.insert(0, 'xi', x)
df_table.insert(0, 'i', range(n))

# Bersihkan tampilan (hapus nilai 0 di segitiga bawah)
df_clean = df_table.astype(object)
for j in range(1, n+1): 
    for i in range(n):
        if i > (n - j): 
            df_clean.iloc[i, j+1] = "" # +1 karena ada kolom 'i'

print(df_clean.to_string(index=False))
print("-" * 85)

print("\n## 2. HASIL ESTIMASI ERROR")
print(f"Koefisien b3 (dari tabel baris 0, kolom Third) = {b3:.8f}")
print("\nRumus: Error = b3 * (xf - x0) * (xf - x1) * (xf - x2)")
print(f"Error = {b3:.8f} * ({xf} - {x0_orig}) * ({xf} - {x1_orig}) * ({xf} - {x2_orig})")
print(f"      = {b3:.8f} * ({term1}) * ({term2}) * ({term3})")
print(f"      = {error_val:.8f}")

print("\n## 3. PERSENTASE ERROR")
print(f"Error % = {error_val:.8f} * 100")
print(f"        = {error_percent:.7f} %")

print("=" * 85)