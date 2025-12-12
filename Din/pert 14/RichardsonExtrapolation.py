import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA & FUNGSI (SESUAI EXCEL PERTEMUAN 14)
# =========================================================================
# Fungsi Polinomial dari pertemuan sebelumnya (karena data cocok dengan fungsi ini)
# f(x) = -0.1x^4 - 0.15x^3 - 0.5x^2 - 0.25x + 1.2
def f(x):
    return -0.1*(x**4) - 0.15*(x**3) - 0.5*(x**2) - 0.25*x + 1.2

# Target turunan pada x = 0.5
x_target = 0.5

# Step size kecil (h1)
h1 = 0.25 
# Step size besar (h2 = 2 * h1)
h2 = 0.5

# =========================================================================
# 2. ALGORITMA CENTRAL DIFFERENCE (BASIS)
# =========================================================================
def central_difference(x, h):
    """
    Menghitung turunan f'(x) menggunakan Central Difference.
    Rumus: (f(x+h) - f(x-h)) / (2*h)
    """
    fx_plus = f(x + h)
    fx_minus = f(x - h)
    
    # Sesuai rumus Excel: (f(x+h) - f(x-h)) / (2*h)
    result = (fx_plus - fx_minus) / (2 * h)
    return result, fx_plus, fx_minus

# =========================================================================
# 3. ALGORITMA RICHARDSON EXTRAPOLATION
# =========================================================================
def richardson_extrapolation(D1, D2):
    """
    Meningkatkan akurasi menggunakan rumus Richardson.
    D1: Hasil dengan step h (lebih akurat)
    D2: Hasil dengan step 2h (kurang akurat)
    Rumus: (4/3)*D1 - (1/3)*D2
    """
    return (4/3) * D1 - (1/3) * D2

# =========================================================================
# 4. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       DIFERENSIASI NUMERIK: RICHARDSON EXTRAPOLATION")
    print("=" * 85)
    print(f"Target x = {x_target}")
    print("-" * 85)

    # --- LANGKAH 1: Hitung D1 (Step Size Kecil h=0.25) ---
    D1, f_plus_h1, f_minus_h1 = central_difference(x_target, h1)
    
    print("## LANGKAH 1: Central Difference dengan h1 (Kecil)")
    print(f"h1 = {h1}")
    print(f"x - h1 = {x_target - h1}  -> f({x_target - h1}) = {f_minus_h1:.7f}")
    print(f"x + h1 = {x_target + h1}  -> f({x_target + h1}) = {f_plus_h1:.7f}")
    print(f"D1 = ({f_plus_h1:.7f} - {f_minus_h1:.7f}) / (2 * {h1})")
    print(f"   = {D1:.7f}")

    # --- LANGKAH 2: Hitung D2 (Step Size Besar h=0.5) ---
    D2, f_plus_h2, f_minus_h2 = central_difference(x_target, h2)
    
    print("\n## LANGKAH 2: Central Difference dengan h2 (Besar)")
    print(f"h2 = {h2} (2 * h1)")
    print(f"x - h2 = {x_target - h2}    -> f({x_target - h2}) = {f_minus_h2:.7f}")
    print(f"x + h2 = {x_target + h2}    -> f({x_target + h2}) = {f_plus_h2:.7f}")
    print(f"D2 = ({f_plus_h2:.7f} - {f_minus_h2:.7f}) / (2 * {h2})")
    print(f"   = {D2:.7f}")

    # --- LANGKAH 3: Terapkan Rumus Richardson ---
    richardson_val = richardson_extrapolation(D1, D2)
    
    print("\n## LANGKAH 3: Richardson Extrapolation")
    print("Rumus: f'(x) ≈ (4/3)*D1 - (1/3)*D2")
    print(f"Result = (4/3) * ({D1:.7f}) - (1/3) * ({D2:.7f})")
    print(f"       = {4/3 * D1:.7f} - {1/3 * D2:.7f}")
    print(f"       = {richardson_val:.7f}")

    # --- ANALISIS ERROR ---
    # True Value Analitik: f'(x) = -0.4x^3 - 0.45x^2 - x - 0.25
    def true_deriv(x):
        return -0.4*(x**3) - 0.45*(x**2) - 1.0*x - 0.25
    
    true_val = true_deriv(x_target)
    err_D1 = abs((true_val - D1)/true_val) * 100
    err_rich = abs((true_val - richardson_val)/true_val) * 100
    
    print("-" * 85)
    print("## ANALISIS ERROR (PERBANDINGAN)")
    print(f"Nilai Sebenarnya (True Value) : {true_val:.7f}")
    print(f"Error D1 (Central Diff h={h1})  : {err_D1:.4f}%")
    print(f"Error Richardson (Extrapolated) : {err_rich:.10f}%") # Presisi tinggi untuk lihat bedanya
    print("-" * 85)
    print("KESIMPULAN: Richardson Extrapolation menghilangkan error secara drastis.")
    print("=" * 85)

if __name__ == "__main__":
    main()