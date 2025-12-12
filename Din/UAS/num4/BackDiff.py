import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. DEFINISI FUNGSI FISIKA (Persamaan Kecepatan Roket)
# =========================================================================
# Parameter sesuai rumus di Excel:
u = 2000      # Kecepatan gas buang
m0 = 70000   # Massa awal
q = 2100      # Laju konsumsi bahan bakar
g = 9.81       # Gravitasi

def v(t):
    """Menghitung kecepatan v pada waktu t."""
    # Syarat: Massa tidak boleh <= 0
    if (m0 - q*t) <= 0:
        return None
    
    # Rumus Excel: =2000*LN(140000/(140000-2100*t))-9.8*t
    val = u * math.log(m0 / (m0 - q * t)) - g * t
    return val

# =========================================================================
# 2. ALGORITMA BACKWARD DIFFERENCE
# =========================================================================
def hitung_backward_diff_rocket(t, h):
    """
    Menghitung turunan pertama (percepatan) menggunakan Backward Difference.
    f'(x) approx (f(x) - f(x-h)) / h
    """
    # 1. Hitung v(t) -> v(16)
    # Ini sesuai Cell B21 di Excel Anda
    vt = v(t)
    
    # 2. Hitung v(t-h) -> v(16-2) -> v(14)
    # Ini sesuai Cell B22 di Excel Anda
    vt_minus_h = v(t - h)
    
    # 3. Hitung Selisih Mundur
    # Rumus Excel: =(B21 - B22) / 2
    derivative = (vt - vt_minus_h) / h
    
    return vt, vt_minus_h, derivative

# =========================================================================
# 3. PERHITUNGAN ANALITIK (TRUE VALUE)
# =========================================================================
def get_true_acceleration(t):
    """
    Turunan analitik dari v(t): a(t) = (u * q) / (m0 - q*t) - g
    """
    return (u * q) / (m0 - q * t) - g

# =========================================================================
# 4. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       DIFERENSIASI NUMERIK: BACKWARD DIFFERENCE (KASUS ROKET)")
    print("=" * 85)
    print(f"Fungsi v(t) = {u} * ln({m0} / ({m0} - {q}*t)) - {g}*t")
    print("-" * 85)
    
    # Input Data Sesuai Excel
    t_target = 16  # Titik yang dicari (x)
    h = 2          # Step size (h)

    # Hitung Numerik
    vt, vt_prev, a_num = hitung_backward_diff_rocket(t_target, h)
    
    # Hitung Analitik (True Value)
    a_true = get_true_acceleration(t_target)
    error_rel = abs((a_true - a_num) / a_true) * 100

    # --- OUTPUT STEP-BY-STEP ---
    print(f"Diketahui:")
    print(f"   t     = {t_target}")
    print(f"   h     = {h}")
    print(f"   t - h = {t_target - h}")
    print("-" * 85)

    print("## LANGKAH 1: Hitung Nilai Fungsi v(t)")
    
    print(f"1. v({t_target})")
    print(f"   = {u} * ln({m0} / ({m0} - {q}*{t_target})) - {g}*{t_target}")
    print(f"   = {vt:.7f}  (Sesuai Cell B21)")
    
    print(f"\n2. v({t_target} - {h}) = v({t_target-h})")
    print(f"   = {u} * ln({m0} / ({m0} - {q}*{t_target-h})) - {g}*{t_target-h}")
    print(f"   = {vt_prev:.7f}  (Sesuai Cell B22)")

    print("\n## LANGKAH 2: Hitung Backward Difference")
    print("Rumus: f'(x) ≈ (f(x) - f(x-h)) / h")
    print(f"a({t_target}) ≈ (v({t_target}) - v({t_target-h})) / {h}")
    print(f"       ≈ ({vt:.7f} - {vt_prev:.7f}) / {h}")
    print(f"       ≈ {a_num:.7f}")

    print("-" * 85)
    print("## ANALISIS ERROR")
    print(f"Hasil Numerik (Backward Diff) : {a_num:.7f}")
    print(f"Hasil Analitik (True Value)   : {a_true:.7f}")
    print(f"Error Relatif                 : {error_rel:.4f}%")
    print("=" * 85)

if __name__ == "__main__":
    main()