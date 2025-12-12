import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI EXCEL Pertemuan 14 - Direct Fit 1)
# =========================================================================
# Titik Data (x, y)
# x0 = 0, y0 = 13.5
# x1 = 1.25, y1 = 12
# x2 = 3.75, y2 = 10

x = np.array([0.0, 1.25, 3.75])
y = np.array([13.5, 12.0, 10.0])

# Titik yang ingin dicari turunannya (x target)
x_target = 0.0

# =========================================================================
# 2. ALGORITMA DIRECT FIT (TURUNAN LAGRANGE 3 TITIK)
# =========================================================================
def hitung_direct_fit_deriv(x, y, xt):
    """
    Menghitung f'(xt) menggunakan interpolasi Lagrange 3 titik.
    Cocok untuk data dengan jarak (h) yang tidak sama.
    """
    x0, x1, x2 = x[0], x[1], x[2]
    y0, y1, y2 = y[0], y[1], y[2]
    
    # --- SUKU 1 (Terkait y0) ---
    # Rumus: y0 * (2x - x1 - x2) / ((x0 - x1)(x0 - x2))
    pembilang1 = (2 * xt) - x1 - x2
    penyebut1  = (x0 - x1) * (x0 - x2)
    term1      = y0 * (pembilang1 / penyebut1)
    
    # --- SUKU 2 (Terkait y1) ---
    # Rumus: y1 * (2x - x0 - x2) / ((x1 - x0)(x1 - x2))
    pembilang2 = (2 * xt) - x0 - x2
    penyebut2  = (x1 - x0) * (x1 - x2)
    term2      = y1 * (pembilang2 / penyebut2)
    
    # --- SUKU 3 (Terkait y2) ---
    # Rumus: y2 * (2x - x0 - x1) / ((x2 - x0)(x2 - x1))
    pembilang3 = (2 * xt) - x0 - x1
    penyebut3  = (x2 - x0) * (x2 - x1)
    term3      = y2 * (pembilang3 / penyebut3)
    
    # Total Turunan
    f_prime = term1 + term2 + term3
    
    return f_prime, (term1, term2, term3)

# =========================================================================
# 3. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       DIFERENSIASI NUMERIK: DIRECT FIT (LAGRANGE 3 TITIK)")
    print("       (Solusi untuk Jarak Antar Titik Tidak Sama)")
    print("=" * 85)
    
    # Hitung
    hasil, terms = hitung_direct_fit_deriv(x, y, x_target)
    
    # --- OUTPUT STEP-BY-STEP ---
    print(f"Data Input:")
    print(f"   (x0, y0) = ({x[0]}, {y[0]})")
    print(f"   (x1, y1) = ({x[1]}, {y[1]})")
    print(f"   (x2, y2) = ({x[2]}, {y[2]})")
    print(f"   Target x = {x_target}")
    print("-" * 85)
    
    print("## PERHITUNGAN PER SUKU (Sesuai Rumus Excel)")
    
    # Suku 1
    # Excel: (F9*(2*F15-F13-F14)/((F12-F13)*(F12-F14)))
    # y0 * (2x - x1 - x2) / ((x0 - x1)(x0 - x2))
    top1 = (2*x_target - x[1] - x[2])
    bot1 = (x[0] - x[1]) * (x[0] - x[2])
    print(f"\n1. Suku Pertama (Basis y0):")
    print(f"   = {y[0]} * ({2*x_target} - {x[1]} - {x[2]}) / (({x[0]}-{x[1]}) * ({x[0]}-{x[2]}))")
    print(f"   = {y[0]} * ({top1}) / ({bot1})")
    print(f"   = {terms[0]:.7f}")

    # Suku 2
    # Excel: (F10*(2*F15-F12-F14)/((F13-F12)*(F13-F14)))
    top2 = (2*x_target - x[0] - x[2])
    bot2 = (x[1] - x[0]) * (x[1] - x[2])
    print(f"\n2. Suku Kedua (Basis y1):")
    print(f"   = {y[1]} * ({2*x_target} - {x[0]} - {x[2]}) / (({x[1]}-{x[0]}) * ({x[1]}-{x[2]}))")
    print(f"   = {y[1]} * ({top2}) / ({bot2})")
    print(f"   = {terms[1]:.7f}")

    # Suku 3
    # Excel: (F11*(2*F15-F12-F13)/((F14-F12)*(F14-F13)))
    top3 = (2*x_target - x[0] - x[1])
    bot3 = (x[2] - x[0]) * (x[2] - x[1])
    print(f"\n3. Suku Ketiga (Basis y2):")
    print(f"   = {y[2]} * ({2*x_target} - {x[0]} - {x[1]}) / (({x[2]}-{x[0]}) * ({x[2]}-{x[1]}))")
    print(f"   = {y[2]} * ({top3}) / ({bot3})")
    print(f"   = {terms[2]:.7f}")

    print("-" * 85)
    print(f"HASIL AKHIR f'({x_target}) = {terms[0]:.7f} + {terms[1]:.7f} + {terms[2]:.7f}")
    print(f"                        = {hasil:.7f}")
    print("=" * 85)

if __name__ == "__main__":
    main()