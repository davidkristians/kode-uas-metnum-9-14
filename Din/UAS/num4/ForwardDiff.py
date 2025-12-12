import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. DEFINISI FUNGSI FISIKA (Persamaan Kecepatan Roket)
# =========================================================================
# Parameter sesuai rumus di Excel:
# v(t) = 2000 * ln(140000 / (140000 - 2100*t)) - 9.8*t
u = 2000      # Kecepatan gas buang
m0 = 70000   # Massa awal
q = 2100      # Laju konsumsi bahan bakar
g = 9.81       # Gravitasi

def v(t):
    """Menghitung kecepatan v pada waktu t."""
    # Syarat: (m0 - q*t) > 0 agar tidak error logaritma
    if (m0 - q*t) <= 0:
        return None
    
    # Rumus Excel: =2000*LN(140000/(140000-2100*t))-9.8*t
    val = u * math.log(m0 / (m0 - q * t)) - g * t
    return val

# =========================================================================
# 2. ALGORITMA FORWARD DIFFERENCE
# =========================================================================
def hitung_forward_diff_rocket(t, h):
    """
    Menghitung turunan pertama (percepatan) menggunakan Forward Difference.
    f'(x) approx (f(x+h) - f(x)) / h
    """
    # 1. Hitung v(t) -> v(16)
    vt = v(t)
    
    # 2. Hitung v(t+h) -> v(16+2)
    vt_plus_h = v(t + h)
    
    # 3. Hitung Selisih Maju
    # Rumus Excel: =(B20 - B19) / 2
    # Dimana B20 = v(t+h) dan B19 = v(t)
    derivative = (vt_plus_h - vt) / h
    
    return vt, vt_plus_h, derivative

# =========================================================================
# 3. PERHITUNGAN ANALITIK (TRUE VALUE)
# =========================================================================
def get_true_acceleration(t):
    """
    Turunan analitik dari v(t):
    a(t) = v'(t) = (u * q) / (m0 - q*t) - g
    """
    return (u * q) / (m0 - q * t) - g

# =========================================================================
# 4. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 80)
    print("       DIFERENSIASI NUMERIK: FORWARD DIFFERENCE (KASUS ROKET)")
    print("=" * 80)
    print(f"Fungsi v(t) = {u} * ln({m0} / ({m0} - {q}*t)) - {g}*t")
    print("-" * 80)
    
    # Input Data Sesuai Excel
    t_target = 16  # Titik yang dicari (x)
    h = 2          # Step size (x+2)

    # Hitung Numerik
    vt, vt_next, a_num = hitung_forward_diff_rocket(t_target, h)
    
    # Hitung Analitik (True Value)
    a_true = get_true_acceleration(t_target)
    error_rel = abs((a_true - a_num) / a_true) * 100

    # --- OUTPUT STEP-BY-STEP ---
    print(f"Diketahui:")
    print(f"   t     = {t_target}")
    print(f"   h     = {h}")
    print(f"   t + h = {t_target + h}")
    print("-" * 80)

    print("## LANGKAH 1: Hitung Nilai Fungsi v(t)")
    print(f"1. v({t_target})")
    print(f"   = {u} * ln({m0} / ({m0} - {q}*{t_target})) - {g}*{t_target}")
    print(f"   = {vt:.7f}  (Sesuai Cell B19)")
    
    print(f"\n2. v({t_target} + {h}) = v({t_target+h})")
    print(f"   = {u} * ln({m0} / ({m0} - {q}*{t_target+h})) - {g}*{t_target+h}")
    print(f"   = {vt_next:.7f}  (Sesuai Cell B20)")

    print("\n## LANGKAH 2: Hitung Forward Difference")
    print("Rumus: f'(x) ≈ (f(x+h) - f(x)) / h")
    print(f"a({t_target}) ≈ (v({t_target+h}) - v({t_target})) / {h}")
    print(f"       ≈ ({vt_next:.7f} - {vt:.7f}) / {h}")
    print(f"       ≈ {a_num:.7f}")

    print("-" * 80)
    print("## ANALISIS ERROR")
    print(f"Hasil Numerik (Forward Diff) : {a_num:.7f}")
    print(f"Hasil Analitik (True Value)  : {a_true:.7f}")
    print(f"Error Relatif                : {error_rel:.4f}%")
    print("=" * 80)

if __name__ == "__main__":
    main()