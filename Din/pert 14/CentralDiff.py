import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. DEFINISI FUNGSI FISIKA (Persamaan Kecepatan Roket)
# =========================================================================
# Parameter sesuai rumus di Excel:
u = 2000      # Kecepatan gas buang
m0 = 140000   # Massa awal
q = 2100      # Laju konsumsi bahan bakar
g = 9.8       # Gravitasi

def v(t):
    """Menghitung kecepatan v pada waktu t."""
    # Cek agar tidak error logaritma (massa tidak boleh <= 0)
    if (m0 - q*t) <= 0:
        return None
    
    # Rumus: 2000 * ln(140000 / (140000 - 2100*t)) - 9.8*t
    val = u * math.log(m0 / (m0 - q * t)) - g * t
    return val

# =========================================================================
# 2. ALGORITMA CENTRAL DIFFERENCE
# =========================================================================
def hitung_central_diff_rocket(t, h):
    """
    Menghitung turunan pertama (percepatan) menggunakan Central Difference.
    Rumus: f'(x) approx (f(x+h) - f(x-h)) / (2*h)
    """
    # 1. Hitung v(t+h) -> v(16+2) -> v(18)
    # Ini sesuai dengan B19 di Excel Anda (asumsi urutan)
    vt_plus = v(t + h)
    
    # 2. Hitung v(t-h) -> v(16-2) -> v(14)
    # Ini sesuai dengan B20 di Excel Anda
    vt_minus = v(t - h)
    
    # 3. Hitung Selisih Pusat
    # Rumus Excel: =(B19 - B20) / (2*2)
    # Pembilang: Selisih antara Depan dan Belakang
    # Penyebut : 2 kali step size (jarak total dari t-h ke t+h)
    derivative = (vt_plus - vt_minus) / (2 * h)
    
    return vt_minus, vt_plus, derivative

# =========================================================================
# 3. PERHITUNGAN ANALITIK (TRUE VALUE)
# =========================================================================
def get_true_acceleration(t):
    """
    Turunan analitik dari v(t) untuk menghitung True Error.
    a(t) = (u*q)/(m0 - q*t) - g
    """
    return (u * q) / (m0 - q * t) - g

# =========================================================================
# 4. PROGRAM UTAMA
# =========================================================================
def main():
    print("=" * 85)
    print("       DIFERENSIASI NUMERIK: CENTRAL DIFFERENCE (SELISIH PUSAT)")
    print("=" * 85)
    print(f"Fungsi v(t) = {u} * ln({m0} / ({m0} - {q}*t)) - {g}*t")
    print("-" * 85)
    
    # Input Data Sesuai Excel
    t_target = 16  # Titik yang dicari (x)
    h = 2          # Step size (h)

    # Hitung Numerik
    v_back, v_fwd, a_num = hitung_central_diff_rocket(t_target, h)
    
    # Hitung Analitik (True Value)
    a_true = get_true_acceleration(t_target)
    error_rel = abs((a_true - a_num) / a_true) * 100

    # --- OUTPUT STEP-BY-STEP ---
    print(f"Diketahui:")
    print(f"   t     = {t_target}")
    print(f"   h     = {h}")
    print(f"   t - h = {t_target - h}")
    print(f"   t + h = {t_target + h}")
    print("-" * 85)

    print("## LANGKAH 1: Hitung Titik Belakang dan Depan")
    
    print(f"\n1. v({t_target} - {h}) = v({t_target-h})")
    print(f"   = {u} * ln({m0} / ({m0} - {q}*{t_target-h})) - {g}*{t_target-h}")
    print(f"   = {v_back:.7f}  (v_mundur)")
    
    print(f"\n2. v({t_target} + {h}) = v({t_target+h})")
    print(f"   = {u} * ln({m0} / ({m0} - {q}*{t_target+h})) - {g}*{t_target+h}")
    print(f"   = {v_fwd:.7f}   (v_maju)")

    print("\n## LANGKAH 2: Hitung Central Difference")
    print("Rumus: f'(x) ≈ (f(x+h) - f(x-h)) / 2h")
    print(f"a({t_target}) ≈ (v({t_target+h}) - v({t_target-h})) / (2 * {h})")
    print(f"       ≈ ({v_fwd:.7f} - {v_back:.7f}) / {2*h}")
    print(f"       ≈ {v_fwd - v_back:.7f} / {2*h}")
    print(f"       ≈ {a_num:.7f}")

    print("-" * 85)
    print("## ANALISIS ERROR")
    print(f"Hasil Numerik (Central Diff) : {a_num:.7f}")
    print(f"Hasil Analitik (True Value)  : {a_true:.7f}")
    print(f"Error Relatif                : {error_rel:.4f}%")
    print("-" * 85)
    print("Catatan: Bandingkan error ini dengan Forward Difference sebelumnya.")
    print("Central Difference biasanya memiliki error jauh lebih kecil.")
    print("=" * 85)

if __name__ == "__main__":
    main()