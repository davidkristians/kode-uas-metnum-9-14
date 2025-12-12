import numpy as np
import pandas as pd
import math

# Atur tampilan angka desimal agar rapi
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== TRAPEZOIDAL RULE (MULTIPLE SEGMENT) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. TENTUKAN FUNGSI f(x)
def f(x):
    # --- CONTOH 1: Soal Parachutist (Eksponensial) ---
    # g = 9.8; m = 68.1; c = 12.5
    # return (g*m/c) * (1 - np.exp(-(c/m) * x))
    
    # --- CONTOH 2: Soal Polinomial (Orde 5) ---
    # f(x) = 0.2 + 25x ...
    return 0.2 + 25*x - 200*x**2 + 675*x**3 - 900*x**4 + 400*x**5

    # --- CONTOH 3: Fungsi Trigonometri ---
    # return np.sin(x)

# 2. TENTUKAN BATAS DAN JUMLAH SEGMEN
a = 0.0     # Batas Bawah (x0)
b = 0.8     # Batas Atas (xn)
n = 2       # Jumlah Segmen / Bias (Semakin besar n, semakin akurat)

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (JANGAN UBAH BAGIAN INI)
# ==============================================================================

def calculate_trapezoidal(a, b, n):
    # 1. Hitung Lebar Segmen (h)
    h = (b - a) / n
    
    print("-" * 50)
    print(f"Rentang Integasi : {a} s/d {b}")
    print(f"Jumlah Segmen (n): {n}")
    print(f"Lebar Segmen (h) : {h:.6f}")
    print("-" * 50)
    
    # 2. Buat Titik-Titik x dan Hitung f(x)
    # np.linspace membuat deret angka dari a sampai b sebanyak n+1 titik
    x_vals = np.linspace(a, b, n + 1)
    y_vals = f(x_vals) # Masukkan array x ke fungsi f
    
    # 3. Tampilkan Tabel Data (Seperti Excel)
    data = {
        'i (Index)': range(n + 1),
        'x': x_vals,
        'f(x)': y_vals,
        'Ket': [''] * (n + 1)
    }
    # Tandai f(x0) dan f(xn)
    data['Ket'][0]  = "f(x0) -> Dikali 1"
    data['Ket'][-1] = "f(xn) -> Dikali 1"
    for i in range(1, n):
        data['Ket'][i] = "2 * f(xi)"
        
    df = pd.DataFrame(data)
    print("\n[TABEL DATA]")
    print(df.to_string(index=False))
    print("-" * 50)
    
    # 4. Hitung Luas (Integral)
    # Rumus: (h/2) * [ f(x0) + 2*Sigma(fi) + f(xn) ]
    
    f_x0 = y_vals[0]
    f_xn = y_vals[-1]
    sum_middle = np.sum(y_vals[1:-1]) # Jumlahkan semua kecuali awal & akhir
    
    result = (h / 2) * (f_x0 + 2 * sum_middle + f_xn)
    
    # 5. Tampilkan Penjabaran Rumus
    print("\n[PERHITUNGAN DETAIL]")
    print(f"I = (h/2) * [ f(x0) + 2 * (Jumlah Tengah) + f(xn) ]")
    print(f"I = ({h:.4f}/2) * [ {f_x0:.4f} + 2 * ({sum_middle:.4f}) + {f_xn:.4f} ]")
    print(f"I = ({h/2:.4f}) * [ {f_x0 + 2*sum_middle + f_xn:.4f} ]")
    
    print("=" * 50)
    print(f"HASIL AKHIR (I) = {result:.6f}")
    print("=" * 50)

# Jalankan Fungsi
calculate_trapezoidal(a, b, n)