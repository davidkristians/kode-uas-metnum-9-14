import numpy as np
import pandas as pd
import math

# Syarat Wajib: Jumlah segmen (n) harus GENAP (misal 2, 4, 6...).
# Rumus: Faktor pengalinya adalah 1, 4, 2, 4, ..., 1.
#     Titik Ganjil (1, 3, 5...) dikali 4.
#     Titik Genap (2, 4, 6...) dikali 2.
#     Ujung Awal & Akhir dikali 1.

# Atur tampilan angka desimal
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== SIMPSON'S 1/3 RULE (NUMERICAL INTEGRATION) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. TENTUKAN FUNGSI f(x)
def f(x):
    # --- CONTOH SOAL (Polinomial Orde 5) ---
    # f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    return 0.2 + 25*x - 200*x**2 + 675*x**3 - 900*x**4 + 400*x**5

    # --- CONTOH LAIN (Eksponensial) ---
    # return np.exp(x)

# 2. TENTUKAN BATAS DAN JUMLAH SEGMEN
a = 0.0     # Batas Bawah
b = 0.8     # Batas Atas
n = 4       # Jumlah Segmen (WAJIB GENAP: 2, 4, 6, 8...)

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (SIMPSON 1/3)
# ==============================================================================

def calculate_simpson_13(a, b, n):
    # 0. Validasi Syarat Genap
    if n % 2 != 0:
        print(f"ERROR: Simpson 1/3 wajib n GENAP. Nilai n={n} tidak valid.")
        return

    # 1. Hitung Lebar Segmen (h)
    h = (b - a) / n
    
    print("-" * 60)
    print(f"Rentang Integasi : {a} s/d {b}")
    print(f"Jumlah Segmen (n): {n} (Valid: Genap)")
    print(f"Lebar Segmen (h) : {h:.6f}")
    print("-" * 60)
    
    # 2. Buat Titik-Titik x dan Hitung f(x)
    x_vals = np.linspace(a, b, n + 1)
    y_vals = f(x_vals)
    
    # 3. Tampilkan Tabel Data dengan Faktor Pengali Simpson
    ket_list = []
    for i in range(n + 1):
        if i == 0 or i == n:
            ket_list.append("Dikali 1 (Ujung)")
        elif i % 2 != 0: # Ganjil (1, 3, 5...)
            ket_list.append("Dikali 4 (Ganjil)")
        else:            # Genap (2, 4, 6...)
            ket_list.append("Dikali 2 (Genap)")
            
    data = {
        'i': range(n + 1),
        'x': x_vals,
        'f(x)': y_vals,
        'Keterangan': ket_list
    }
    df = pd.DataFrame(data)
    print("\n[TABEL DATA & FAKTOR PENGALI]")
    print(df.to_string(index=False))
    print("-" * 60)
    
    # 4. Hitung Integral (Rumus Simpson 1/3)
    # I = (h/3) * [ f(0) + 4*sum(Ganjil) + 2*sum(Genap) + f(n) ]
    
    f_x0 = y_vals[0]
    f_xn = y_vals[-1]
    
    # Ambil index ganjil: mulai 1, sampai -1 (sebelum akhir), step 2
    sum_odd = np.sum(y_vals[1:-1:2])
    
    # Ambil index genap: mulai 2, sampai -1, step 2
    sum_even = np.sum(y_vals[2:-1:2]) 
    
    result = (h / 3) * (f_x0 + 4 * sum_odd + 2 * sum_even + f_xn)
    
    # 5. Tampilkan Penjabaran Rumus
    print("\n[PERHITUNGAN DETAIL]")
    print(f"I = (h/3) * [ f(x0) + 4*(Sigma Ganjil) + 2*(Sigma Genap) + f(xn) ]")
    print(f"I = ({h:.4f}/3) * [ {f_x0:.4f} + 4*({sum_odd:.4f}) + 2*({sum_even:.4f}) + {f_xn:.4f} ]")
    
    total_bracket = f_x0 + 4*sum_odd + 2*sum_even + f_xn
    print(f"I = ({h/3:.6f}) * [ {total_bracket:.6f} ]")
    
    print("=" * 60)
    print(f"HASIL AKHIR (I) = {result:.6f}")
    print("=" * 60)

# Jalankan Fungsi
calculate_simpson_13(a, b, n)