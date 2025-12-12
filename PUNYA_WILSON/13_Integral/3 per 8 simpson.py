import numpy as np
import pandas as pd
import math

# Atur tampilan angka desimal
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== SIMPSON'S 3/8 RULE (NUMERICAL INTEGRATION) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. TENTUKAN FUNGSI f(x)
def f(x):
    # --- CONTOH SOAL (Polinomial Orde 5) ---
    # f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    return 0.2 + 25*x - 200*x**2 + 675*x**3 - 900*x**4 + 400*x**5

    # --- CONTOH LAIN ---
    # return np.sin(x)

# 2. TENTUKAN BATAS DAN JUMLAH SEGMEN
a = 0.0     # Batas Bawah
b = 0.8     # Batas Atas
n = 3       # Jumlah Segmen (WAJIB KELIPATAN 3: 3, 6, 9, 12...)

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (SIMPSON 3/8)
# ==============================================================================

def calculate_simpson_38(a, b, n):
    # 0. Validasi Syarat Kelipatan 3
    if n % 3 != 0:
        print(f"ERROR: Simpson 3/8 wajib n KELIPATAN 3. Nilai n={n} tidak valid.")
        return

    # 1. Hitung Lebar Segmen (h)
    h = (b - a) / n
    
    print("-" * 60)
    print(f"Rentang Integasi : {a} s/d {b}")
    print(f"Jumlah Segmen (n): {n} (Valid: Kelipatan 3)")
    print(f"Lebar Segmen (h) : {h:.6f}")
    print("-" * 60)
    
    # 2. Buat Titik-Titik x dan Hitung f(x)
    x_vals = np.linspace(a, b, n + 1)
    y_vals = f(x_vals)
    
    # 3. Tampilkan Tabel Data dengan Faktor Pengali Simpson 3/8
    # Pola: 1, 3, 3, 2, 3, 3, 2, ..., 1
    ket_list = []
    for i in range(n + 1):
        if i == 0 or i == n:
            ket_list.append("Dikali 1 (Ujung)")
        elif i % 3 == 0: 
            ket_list.append("Dikali 2 (Kelipatan 3)")
        else:            
            ket_list.append("Dikali 3 (Biasa)")
            
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
    
    # 4. Hitung Integral (Rumus Simpson 3/8)
    # I = (3h/8) * [ f(0) + 3*sum(Bukan Kelipatan 3) + 2*sum(Kelipatan 3) + f(n) ]
    
    f_x0 = y_vals[0]
    f_xn = y_vals[-1]
    
    sum_others = 0  # Untuk yang dikali 3
    sum_multi3 = 0  # Untuk yang dikali 2
    
    # Loop dari 1 sampai n-1
    for i in range(1, n):
        if i % 3 == 0:
            sum_multi3 += y_vals[i]
        else:
            sum_others += y_vals[i]
    
    result = (3 * h / 8) * (f_x0 + 3 * sum_others + 2 * sum_multi3 + f_xn)
    
    # 5. Tampilkan Penjabaran Rumus
    print("\n[PERHITUNGAN DETAIL]")
    print(f"I = (3h/8) * [ f(x0) + 3*(Sigma Lain) + 2*(Sigma Kelipatan 3) + f(xn) ]")
    print(f"I = (3*{h:.4f}/8) * [ {f_x0:.4f} + 3*({sum_others:.4f}) + 2*({sum_multi3:.4f}) + {f_xn:.4f} ]")
    
    total_bracket = f_x0 + 3*sum_others + 2*sum_multi3 + f_xn
    coeff = 3 * h / 8
    print(f"I = ({coeff:.6f}) * [ {total_bracket:.6f} ]")
    
    print("=" * 60)
    print(f"HASIL AKHIR (I) = {result:.6f}")
    print("=" * 60)

# Jalankan Fungsi
calculate_simpson_38(a, b, n)