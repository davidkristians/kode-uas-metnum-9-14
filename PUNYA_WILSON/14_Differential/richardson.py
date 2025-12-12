import numpy as np
import pandas as pd

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== RICHARDSON EXTRAPOLATION (NUMERICAL DIFFERENTIATION) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. Definisikan Fungsi f(x)
def f(x):
    # --- CONTOH: Polinomial (Sesuai Excel Richardson) ---
    # f(x) = -0.1*x^4 - 0.15*x^3 - 0.5*x^2 - 0.25*x + 1.2
    return -0.1*x**4 - 0.15*x**3 - 0.5*x**2 - 0.25*x + 1.2

    # --- CONTOH 2: Fungsi Lain ---
    # return np.sin(x)

# 2. Parameter
xi = 0.5     # Titik x yang dicari turunannya
h1 = 0.5     # Step size besar (Langkah 1)
h2 = 0.25    # Step size kecil (Langkah 2) -> Biasanya h1 / 2

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (OTOMATIS)
# ==============================================================================

def calculate_richardson(xi, h1, h2):
    print(f"Mencari turunan f'(x) pada x = {xi}")
    print(f"Langkah 1 (h1) = {h1}")
    print(f"Langkah 2 (h2) = {h2}")
    print("-" * 60)
    # Misal Anda butuh data untuk x=0.5 dengan h1​=0.5 dan h2​=0.25.
    # x+h1​→0.5+0.5=1.0→ Lihat tabel, y=0.20
    # x−h1​→0.5−0.5=0.0→ Lihat tabel, y=1.20
    # x+h2​→0.5+0.25=0.75→ Lihat tabel, y=0.63
    # x−h2​→0.5−0.25=0.25→ Lihat tabel, y=1.10
    
    # --- LANGKAH 1: Hitung Turunan dengan h1 (Central Difference) ---
    # Rumus Central: ( f(x+h) - f(x-h) ) / 2h
    
    y_plus_h1  = f(xi + h1)
    y_minus_h1 = f(xi - h1)
    # --- UBAH JADI INI (Pakai Angka Tabel Manual) ---
    # y_plus_h1  = 0.20  # Nilai y saat x = 1.0
    # y_minus_h1 = 1.20  # Nilai y saat x = 0.0
    D_h1 = (y_plus_h1 - y_minus_h1) / (2 * h1)
    
    print("[1] BASIC ESTIMATE (h1 = %.2f)" % h1)
    print(f"    f({xi}+{h1}) = {y_plus_h1:.6f}")
    print(f"    f({xi}-{h1}) = {y_minus_h1:.6f}")
    print(f"    D(h1) = ({y_plus_h1:.4f} - {y_minus_h1:.4f}) / {2*h1}")
    print(f"    Hasil D(h1) = {D_h1:.6f}")
    print("-" * 60)
    
    # --- LANGKAH 2: Hitung Turunan dengan h2 (Central Difference) ---
    
    y_plus_h2  = f(xi + h2)
    y_minus_h2 = f(xi - h2)
    # Lakukan hal yang sama untuk h2
    # y_plus_h2  = 0.63  # Nilai y saat x = 0.75
    # y_minus_h2 = 1.10  # Nilai y saat x = 0.25
    D_h2 = (y_plus_h2 - y_minus_h2) / (2 * h2)
    
    print("[2] BASIC ESTIMATE (h2 = %.2f)" % h2)
    print(f"    f({xi}+{h2}) = {y_plus_h2:.6f}")
    print(f"    f({xi}-{h2}) = {y_minus_h2:.6f}")
    print(f"    D(h2) = ({y_plus_h2:.4f} - {y_minus_h2:.4f}) / {2*h2}")
    print(f"    Hasil D(h2) = {D_h2:.6f}")
    print("-" * 60)
    
    # --- LANGKAH 3: RICHARDSON EXTRAPOLATION ---
    # Rumus: D = (4/3) * D(h2) - (1/3) * D(h1)
    # Rumus ini berlaku KHUSUS jika h2 = h1 / 2
    
    D_richardson = (4/3) * D_h2 - (1/3) * D_h1
    
    print("[3] HASIL AKHIR (RICHARDSON EXTRAPOLATION)")
    print("    Rumus: D = (4/3) * D(h2) - (1/3) * D(h1)")
    print(f"    D = (1.3333 * {D_h2:.6f}) - (0.3333 * {D_h1:.6f})")
    
    term1 = (4/3) * D_h2
    term2 = (1/3) * D_h1
    
    print(f"    D = {term1:.6f} - {term2:.6f}")
    print("=" * 60)
    print(f"    HASIL f'({xi}) = {D_richardson:.6f}")
    print("=" * 60)
    
    # Cek Error Sebenarnya (True Error)
    # Turunan asli: -0.4x^3 - 0.45x^2 - x - 0.25
    true_val = -0.4*(xi**3) - 0.45*(xi**2) - xi - 0.25
    error = abs(true_val - D_richardson)
    print(f"    (True Value = {true_val:.6f}, Error = {error:.8f})")

# Jalankan Fungsi
calculate_richardson(xi, h1, h2)