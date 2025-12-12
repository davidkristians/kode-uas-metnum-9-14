import numpy as np
import pandas as pd

# =========================================================================
# 1. DEFINISI FUNGSI POLINOMIAL (SESUAI EXCEL)
# f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
# =========================================================================
def f(x):
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# =========================================================================
# 2. ALGORITMA SIMPSON 3/8
# =========================================================================
def hitung_simpson_3_8(a, b, n):
    # Validasi: n harus KELIPATAN 3
    if n % 3 != 0:
        print(f"ERROR: Jumlah segmen n={n} harus KELIPATAN 3 untuk Simpson 3/8!")
        return None, None, None

    h = (b - a) / n
    sum_fx = 0.0
    
    # List untuk menyimpan data tabel
    data = []
    
    for i in range(n + 1):
        x_val = a + i * h
        fx = f(x_val)
        
        # Tentukan Koefisien (Pola: 1, 3, 3, 2, 3, 3, ..., 1)
        if i == 0 or i == n:
            coeff = 1
        elif i % 3 == 0: # Kelipatan 3 (titik interior)
            coeff = 2
        else:            # Lainnya
            coeff = 3
            
        term = coeff * fx
        sum_fx += term
        
        # Simpan data
        note = "=> f(x0)" if i == 0 else ("=> f(xn)" if i == n else "")
        data.append({
            'i': i,
            'x': x_val,
            'f(xi)': fx,
            'Coeff': coeff,
            'Term (C*f)': term,
            'Note': note
        })
        
    # Rumus: I = (3h/8) * sum
    integral = (3 * h / 8) * sum_fx
    
    return integral, h, pd.DataFrame(data)

# =========================================================================
# 3. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       INTEGRASI NUMERIK: ATURAN SIMPSON 3/8")
    print("       f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5")
    print("=" * 85)

    # Input Data Sesuai Excel
    a = 0.0
    b = 0.8
    n = 3  # Harus Kelipatan 3

    I, h, df = hitung_simpson_3_8(a, b, n)
    
    if I is not None:
        print(f"Batas Bawah (a) : {a}")
        print(f"Batas Atas (b)  : {b}")
        print(f"Jumlah Segmen(n): {n} (h = {h:.6f})")
        print("-" * 85)
        
        # Tampilkan Tabel
        pd.set_option('display.float_format', lambda x: '%.6f' % x)
        print(df.to_string(index=False))
        
        print("-" * 85)
        print(f"HASIL INTEGRAL (I) = {I:.6f}")
        
        # Hitung Nilai Sebenarnya (True Value) secara analitik
        def F_integral(x):
            return 0.2*x + 12.5*x**2 - (200/3)*x**3 + (675/4)*x**4 - 180*x**5 + (200/3)*x**6
            
        true_val = F_integral(b) - F_integral(a)
        error = abs((true_val - I)/true_val) * 100
        
        print(f"True Value (Analitik) = {true_val:.6f}")
        print(f"Error Relatif         = {error:.4f}%")
        print("=" * 85)

if __name__ == "__main__":
    main()