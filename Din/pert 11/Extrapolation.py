import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI FILE EXCEL Pertemuan 11 - Extrapolation)
# =========================================================================
# Data Titik (x, y)
# Dari Excel: 1, 1.5, 2, 2.5
points = [
    (1.0, 2.718),
    (1.5, 4.481),
    (2.0, 7.389),
    (2.5, 12.182)
]

# Titik yang dicari (xf)
# Dari Excel: Cari x = 3
xf = 3.0

# =========================================================================
# 2. ALGORITMA NEWTON DIVIDED DIFFERENCE
# =========================================================================
n = len(points)
x = np.array([p[0] for p in points])
y = np.array([p[1] for p in points])

# Buat Tabel Divided Difference
table = np.zeros((n, n))
table[:, 0] = y

# Isi Tabel
for j in range(1, n):
    for i in range(n - j):
        numerator = table[i + 1, j - 1] - table[i, j - 1]
        denominator = x[i + j] - x[i]
        table[i, j] = numerator / denominator

# Ambil Koefisien b (Baris Teratas / Diagonal)
b = table[0, :]

# =========================================================================
# 3. PERHITUNGAN NILAI PREDIKSI (SUBSTITUSI)
# =========================================================================
# Rumus: y = b0 + b1(x-x0) + b2(x-x0)(x-x1) + b3(x-x0)(x-x1)(x-x2)
y_pred = b[0]
terms = [b[0]] # Simpan nilai per suku untuk display

x_term_accumulated = 1.0

for i in range(1, n):
    # Hitung (x - x0)...(x - x_i-1)
    x_term_accumulated *= (xf - x[i-1])
    
    # Hitung suku ke-i: bi * akumulasi_x
    term_val = b[i] * x_term_accumulated
    y_pred += term_val
    terms.append(term_val)

# =========================================================================
# 4. OUTPUT STEP-BY-STEP (FORMAT EXCEL)
# =========================================================================
print("=" * 85)
print("              EKSTRAPOLASI (NEWTON POLYNOMIAL)")
print("=" * 85)
print(f"Data Titik  : {points}")
print(f"Mencari x   : {xf} (Di luar rentang data -> Ekstrapolasi)")
print("-" * 85)

print("\n## 1. TABEL DIVIDED DIFFERENCE")
print("Sama seperti Interpolasi, kita cari koefisien b dari tabel ini.")
print("-" * 85)

# Format Tabel dengan Pandas
col_names = ['f(xi)'] + [f'{k}th DD' for k in range(1, n)]
df_table = pd.DataFrame(table, columns=col_names)
df_table.insert(0, 'xi', x)
df_table.insert(0, 'i', range(n))

# Bersihkan tampilan
df_clean = df_table.astype(object)
for j in range(1, n+1): 
    for i in range(n):
        if i > (n - j): df_clean.iloc[i, j+1] = ""

print(df_clean.to_string(index=False))
print("-" * 85)

print("\n## 2. HASIL PERHITUNGAN")
print("Rumus: f(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + b3(x-x0)(x-x1)(x-x2)")

print("\nSubstitusi Angka:")
# String manual agar persis Excel
line1 = f"f({xf}) = {b[0]:.4f}"
line1 += f" + {b[1]:.4f} * ({xf}-{x[0]})"
line1 += f" + {b[2]:.4f} * ({xf}-{x[0]}) * ({xf}-{x[1]})"
line1 += f" + {b[3]:.4f} * ({xf}-{x[0]}) * ({xf}-{x[1]}) * ({xf}-{x[2]})"
print(line1)

print("\nNilai per Suku:")
print(f"Suku 0 (b0)                        = {terms[0]:.6f}")
print(f"Suku 1 (b1 * (x-x0))               = {terms[1]:.6f}")
print(f"Suku 2 (b2 * (x-x0)(x-x1))         = {terms[2]:.6f}")
print(f"Suku 3 (b3 * (x-x0)(x-x1)(x-x2))   = {terms[3]:.6f}")
print("-" * 40 + " +")
print(f"Hasil Akhir f({xf})                   = {y_pred:.6f}")

# Cek dengan nilai asli e^3 (approx 20.0855)
true_val = np.exp(3)
err = abs((true_val - y_pred)/true_val) * 100
print("-" * 85)
print(f"Info: Nilai asli e^3 adalah sekitar {true_val:.4f}")
print(f"Error Ekstrapolasi: {err:.2f}%")
print("=" * 85)