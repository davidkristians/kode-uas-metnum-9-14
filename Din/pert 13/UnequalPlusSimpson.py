import numpy as np
import pandas as pd

# =========================================================================
# 1. DEFINISI FUNGSI POLINOMIAL (SESUAI EXCEL)
# f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
# =========================================================================
def f(x):
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# =========================================================================
# 2. ALGORITMA INTEGRASI CAMPURAN
# =========================================================================
def integrasi_campuran_otomatis(points_x):
    n = len(points_x)
    total_integral = 0
    data_tabel = []
    
    # Toleransi untuk membandingkan float (misal 0.1 vs 0.100000001)
    epsilon = 1e-9 
    
    i = 0
    while i < n - 1:
        # Hitung h untuk segmen saat ini
        h1 = points_x[i+1] - points_x[i]
        
        # Cek h untuk segmen berikutnya (jika ada)
        h2 = points_x[i+2] - points_x[i+1] if i + 2 < n else -1
        h3 = points_x[i+3] - points_x[i+2] if i + 3 < n else -1

        # --- LOGIKA PRIORITAS ---
        
        # 1. Cek Simpson 3/8 (Butuh 3 segmen dengan h sama)
        if (i + 3 < n) and (abs(h1 - h2) < epsilon) and (abs(h2 - h3) < epsilon):
            method = "Simpson 3/8"
            f0, f1, f2, f3 = f(points_x[i]), f(points_x[i+1]), f(points_x[i+2]), f(points_x[i+3])
            
            # Rumus: (3h/8) * (f0 + 3f1 + 3f2 + f3)
            area = (3 * h1 / 8) * (f0 + 3*f1 + 3*f2 + f3)
            
            data_tabel.append({'x': points_x[i], 'f(x)': f0, 'h': h1, 'Ii': area, 'Method': method})
            data_tabel.append({'x': points_x[i+1], 'f(x)': f1, 'h': h1, 'Ii': "-", 'Method': "  (cont'd)"})
            data_tabel.append({'x': points_x[i+2], 'f(x)': f2, 'h': h1, 'Ii': "-", 'Method': "  (cont'd)"})
            
            total_integral += area
            i += 3 # Lompat 3 titik
            
        # 2. Cek Simpson 1/3 (Butuh 2 segmen dengan h sama)
        elif (i + 2 < n) and (abs(h1 - h2) < epsilon):
            method = "Simpson 1/3"
            f0, f1, f2 = f(points_x[i]), f(points_x[i+1]), f(points_x[i+2])
            
            # Rumus: (h/3) * (f0 + 4f1 + f2)
            area = (h1 / 3) * (f0 + 4*f1 + f2)
            
            data_tabel.append({'x': points_x[i], 'f(x)': f0, 'h': h1, 'Ii': area, 'Method': method})
            data_tabel.append({'x': points_x[i+1], 'f(x)': f1, 'h': h1, 'Ii': "-", 'Method': "  (cont'd)"})
            
            total_integral += area
            i += 2 # Lompat 2 titik
            
        # 3. Default: Trapesium (1 segmen)
        else:
            method = "Trapezoidal"
            f0, f1 = f(points_x[i]), f(points_x[i+1])
            
            # Rumus: (h/2) * (f0 + f1)
            area = (h1 / 2) * (f0 + f1)
            
            data_tabel.append({'x': points_x[i], 'f(x)': f0, 'h': h1, 'Ii': area, 'Method': method})
            
            total_integral += area
            i += 1 # Lompat 1 titik

    # Tambahkan titik terakhir untuk display
    data_tabel.append({'x': points_x[-1], 'f(x)': f(points_x[-1]), 'h': "-", 'Ii': "-", 'Method': "End"})
    
    return total_integral, pd.DataFrame(data_tabel)

# =========================================================================
# 3. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 95)
    print("       INTEGRASI NUMERIK: CAMPURAN (UNEQUAL + SIMPSON)")
    print("       Logika: Cek Simpson 3/8 -> Cek Simpson 1/3 -> Trapesium")
    print("=" * 95)

    # Input Data Sesuai Excel
    x_input = [0, 0.12, 0.22, 0.32, 0.36, 0.40, 0.44, 0.54, 0.64, 0.70, 0.80]
    
    print(f"Data Input x: {x_input}")
    print("-" * 95)

    I, df = integrasi_campuran_otomatis(x_input)
    
    # Tampilkan Tabel
    # Format agar rapi
    print(df.to_string(index=False))
    
    print("-" * 95)
    print(f"HASIL INTEGRAL TOTAL (I) = {I:.6f}")
    
    # Perbandingan dengan True Value
    def F_integral(x):
        return 0.2*x + 12.5*x**2 - (200/3)*x**3 + (675/4)*x**4 - 180*x**5 + (200/3)*x**6
        
    true_val = F_integral(0.8) - F_integral(0)
    error = abs((true_val - I)/true_val) * 100
    
    print(f"True Value (Analitik)    = {true_val:.6f}")
    print(f"Error Relatif            = {error:.4f}%")
    print("=" * 95)

if __name__ == "__main__":
    main()