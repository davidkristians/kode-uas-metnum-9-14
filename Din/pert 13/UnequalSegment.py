import numpy as np
import pandas as pd

# =========================================================================
# 1. DEFINISI FUNGSI POLINOMIAL (SESUAI EXCEL)
# f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
# =========================================================================
def f(x):
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# =========================================================================
# 2. ALGORITMA TRAPESIUM UNTUK SEGMEN TIDAK SAMA
# =========================================================================
def hitung_unequal_segments(points_x):
    """
    Menghitung integral dengan menjumlahkan luas trapesium
    untuk setiap segmen yang lebarnya (h) berbeda.
    """
    n = len(points_x)
    total_integral = 0.0
    
    # List untuk menyimpan data tabel
    data = []
    
    # Loop dari titik pertama sampai sebelum terakhir
    for i in range(n - 1):
        x_curr = points_x[i]
        x_next = points_x[i+1]
        
        # Hitung lebar segmen ini (h)
        h = x_next - x_curr
        
        # Hitung nilai fungsi
        fx_curr = f(x_curr)
        fx_next = f(x_next)
        
        # Luas Trapesium Segmen Ini
        segment_area = h * (fx_curr + fx_next) / 2.0
        
        total_integral += segment_area
        
        # Simpan data
        data.append({
            'x': x_curr,
            'f(x)': fx_curr,
            'h (Lebar)': h,
            'Luas Segmen (Ii)': segment_area
        })
        
    # Tambahkan baris terakhir (hanya untuk display f(xn))
    last_x = points_x[-1]
    data.append({
        'x': last_x,
        'f(x)': f(last_x),
        'h (Lebar)': '-',
        'Luas Segmen (Ii)': '-'
    })
    
    return total_integral, pd.DataFrame(data)

# =========================================================================
# 3. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       INTEGRASI NUMERIK: UNEQUAL SEGMENTS (TRAPEZOIDAL)")
    print("       f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5")
    print("=" * 85)

    # Input Data Manual (Sesuai Excel)
    x_input = [0, 0.12, 0.22, 0.32, 0.36, 0.40, 0.44, 0.54, 0.64, 0.70, 0.80]
    
    print(f"Data Input x: {x_input}")
    print("-" * 85)

    I, df = hitung_unequal_segments(x_input)
    
    # Tampilkan Tabel
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    # Format float agar rapi
    print(df.to_string(index=False))
    
    print("-" * 85)
    print(f"HASIL INTEGRAL (I) = {I:.6f}")
    
    # Perbandingan dengan True Value
    def F_integral(x):
        return 0.2*x + 12.5*x**2 - (200/3)*x**3 + (675/4)*x**4 - 180*x**5 + (200/3)*x**6
        
    true_val = F_integral(0.8) - F_integral(0)
    error = abs((true_val - I)/true_val) * 100
    
    print(f"True Value         = {true_val:.6f}")
    print(f"Error Relatif      = {error:.4f}%")
    print("=" * 85)

if __name__ == "__main__":
    main()