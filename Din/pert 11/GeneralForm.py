import numpy as np
import pandas as pd

# Atur tampilan agar rapi
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

# =========================================================================
# 1. INPUT DATA (GANTI BAGIAN INI SESUAI FILE EXCEL ANDA)
# =========================================================================
# Contoh Data (Misalnya ada 4 atau 5 titik)
# Masukkan data berurutan dari x0, x1, x2, dst.
x = np.array([1.0, 4.0, 6.0, 5.0])    # Data x
y = np.array([0.0, 1.386294, 1.791759, 1.609438]) # Data y atau f(x)

# Titik yang ingin dicari nilainya
x_ask = 2.0

# =========================================================================
# 2. ALGORITMA UTAMA: MEMBUAT TABEL DIVIDED DIFFERENCE
# =========================================================================
n = len(x)
# Buat matriks kosong ukuran n x n
# Kolom ke-0 diisi nilai y (f(x))
table = np.zeros((n, n))
table[:, 0] = y

# Proses Loop untuk mengisi kolom ke-1 sampai ke-(n-1)
# Rumus: (Nilai Bawah - Nilai Atas) / (x_Bawah - x_Atas)
for j in range(1, n):
    for i in range(n - j):
        # i = baris, j = kolom
        # Pembilang: Selisih nilai di kolom sebelumnya (j-1)
        numerator = table[i + 1, j - 1] - table[i, j - 1]
        
        # Penyebut: Selisih x. Perhatikan jaraknya semakin lebar seiring kolom bertambah
        denominator = x[i + j] - x[i]
        
        table[i, j] = numerator / denominator

# Koefisien b (b0, b1, b2...) adalah baris pertama (indeks 0) dari setiap kolom
b_coeffs = table[0, :]

# =========================================================================
# 3. PERHITUNGAN NILAI PREDIKSI (INTERPOLASI)
# =========================================================================
# Rumus: y = b0 + b1(x-x0) + b2(x-x0)(x-x1) + ...
y_ask = b_coeffs[0] # Inisialisasi dengan b0
x_term = 1.0

detailed_terms = [] # Untuk menyimpan nilai per suku (agar bisa dicek step-by-step)
detailed_terms.append(b_coeffs[0])

for k in range(1, n):
    # Update suku perkalian (x - x0)(x - x1)...
    x_term = x_term * (x_ask - x[k-1])
    
    # Hitung nilai suku ke-k: bk * (x - ...)...
    term_val = b_coeffs[k] * x_term
    y_ask += term_val
    
    detailed_terms.append(term_val)

# =========================================================================
# 4. OUTPUT STEP-BY-STEP (FORMAT TABEL LENGKAP)
# =========================================================================
print("=" * 80)
print(f"       HASIL INTERPOLASI BENTUK UMUM (ORDE {n-1})")
print("=" * 80)
print(f"Jumlah Titik Data: {n}")
print(f"Mencari nilai y saat x = {x_ask}")
print("-" * 80)

print("\n## LANGKAH 1: Tabel Divided Difference (Selisih Terbagi)")
print("Kolom 0 adalah y. Kolom 1 adalah 1st DD, Kolom 2 adalah 2nd DD, dst.")
print("-" * 80)

# Membuat DataFrame Pandas untuk tampilan cantik
col_names = ['f(xi)'] + [f'{k}th DD' for k in range(1, n)]
df_table = pd.DataFrame(table, columns=col_names)
# Tambahkan kolom x di depan agar jelas
df_table.insert(0, 'xi', x)

# Trik: Ubah nilai 0.00000 di segitiga bawah menjadi kosong string agar bersih
df_clean = df_table.astype(object)
for j in range(1, n+1): # Kolom 1 sampai n (kolom DD)
    for i in range(n):
        if i > (n - j): # Logika segitiga bawah
            df_clean.iloc[i, j] = ""

print(df_clean.to_string(index=False))
print("-" * 80)

print("\n## LANGKAH 2: Ambil Koefisien b (Baris Teratas)")
for i, b in enumerate(b_coeffs):
    print(f"b{i} = {b:.7f}")

print("\n## LANGKAH 3: Hitung Polinomial Newton")
print(f"f(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + ...")

print("\nDetail Penjumlahan Suku:")
eq_string = f"y = {detailed_terms[0]:.6f}"
for i in range(1, n):
    val = detailed_terms[i]
    sign = "+" if val >= 0 else ""
    print(f"Suku {i} (Order {i}) : {sign} {val:.7f}")
    eq_string += f" {sign} {val:.7f}"

print("-" * 40 + " +")
print(f"Hasil Akhir y({x_ask}) = {y_ask:.7f}")
print("=" * 80)