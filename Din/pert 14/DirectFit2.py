import numpy as np
import pandas as pd

# =========================================================================
# 1. INPUT DATA (SESUAI EXCEL Pertemuan 14 - Direct Fit 2)
# =========================================================================
# 4 Titik Data (t, v) yang diambil dari CSV
t_points = np.array([10.00, 15.00, 20.00, 22.50])
v_points = np.array([227.04, 362.78, 517.35, 602.97])

# Titik target untuk mencari turunan
t_target = 16.0

# =========================================================================
# 2. ALGORITMA DIRECT FIT (SOLUSI MATRIKS)
# =========================================================================
def hitung_koefisien_kubik(t, v):
    """
    Mencari koefisien a0, a1, a2, a3 untuk v(t) = a0 + a1*t + a2*t^2 + a3*t^3
    Menggunakan Matriks Vandermonde.
    """
    # Bentuk Matriks Vandermonde
    # Baris 1: [1, t0, t0^2, t0^3]
    # Baris 2: [1, t1, t1^2, t1^3] ...
    A = np.vander(t, increasing=True)
    
    # Selesaikan Sistem Linear A * x = v
    # x adalah vektor [a0, a1, a2, a3]
    coeffs = np.linalg.solve(A, v)
    
    return coeffs, A

# =========================================================================
# 3. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       DIFERENSIASI NUMERIK: DIRECT FIT 2 (POLINOMIAL KUBIK)")
    print("       (Menggunakan 4 Titik Data)")
    print("=" * 85)
    
    # 1. Hitung Koefisien
    a_coeffs, Matriks_A = hitung_koefisien_kubik(t_points, v_points)
    a0, a1, a2, a3 = a_coeffs
    
    # --- OUTPUT STEP 1: MATRIKS ---
    print("Data Input:")
    for i in range(4):
        print(f"   t{i}={t_points[i]:<5} -> v(t)={v_points[i]}")
    print("-" * 85)
    
    print("## LANGKAH 1: Membentuk Sistem Persamaan (Matriks Vandermonde)")
    print("Model: v(t) = a0 + a1*t + a2*t^2 + a3*t^3")
    print("\nMatriks Koefisien [A]:")
    print(Matriks_A)
    print("\nVektor Hasil [v]:")
    print(v_points)
    
    # --- OUTPUT STEP 2: KOEFISIEN ---
    print("\n## LANGKAH 2: Solusi Koefisien (Hasil Eliminasi Gauss/Invers)")
    print(f"a0 = {a0:.10f}")
    print(f"a1 = {a1:.10f}")
    print(f"a2 = {a2:.10f}")
    print(f"a3 = {a3:.10f}")
    
    print(f"\nPolinomial: v(t) = {a0:.3f} + {a1:.3f}t + {a2:.5f}t^2 + {a3:.6f}t^3")

    # --- OUTPUT STEP 3: HITUNG TURUNAN ---
    print("\n## LANGKAH 3: Hitung Turunan a(t) pada t = 16")
    print("Rumus Turunan: a(t) = v'(t) = a1 + 2*a2*t + 3*a3*t^2")
    
    # Hitung suku per suku sesuai Excel
    suku1 = a1
    suku2 = 2 * a2 * t_target
    suku3 = 3 * a3 * (t_target ** 2)
    
    a_result = suku1 + suku2 + suku3
    
    print(f"a({t_target}) = {a1:.6f} + 2*({a2:.6f})*({t_target}) + 3*({a3:.6f})*({t_target}^2)")
    print(f"       = {suku1:.6f} + {suku2:.6f} + {suku3:.6f}")
    print(f"       = {a_result:.6f}")
    
    print("-" * 85)
    print(f"HASIL AKHIR a(16) = {a_result:.6f}")
    print("=" * 85)

if __name__ == "__main__":
    main()