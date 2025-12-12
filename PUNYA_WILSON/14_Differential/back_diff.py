import numpy as np
import math

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)

print("=== NUMERICAL DIFFERENTIATION: BACKWARD DIFFERENCE ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. Definisikan Fungsi f(x)
def f(x):
    # --- CONTOH 1: Soal Roket (Sesuai Excel Back Diff.csv) ---
    # v(t) = 2000 * ln(140000 / (140000 - 2100*t)) - 9.8*t
    term1 = 2000 * math.log(140000 / (140000 - 2100 * x))
    term2 = 9.8 * x
    return term1 - term2

# 2. Tentukan Titik yang Dicari dan Ukuran Langkah
xi = 16.0    # Titik x yang ingin dicari turunannya
h  = 2.0     # Step size

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (OTOMATIS)
# ==============================================================================

def calculate_backward_difference(xi, h):
    print(f"Mencari turunan f'(x) pada x = {xi} dengan h = {h}")
    print("-" * 60)
    
    # --- A. BACKWARD DIFFERENCE BIASA (O(h)) ---
    # Rumus: f'(x) = [ f(xi) - f(xi - h) ] / h
    # Butuh 2 titik: xi dan xi-1
    
    y_i = f(xi)
    y_im1 = f(xi - h) # i minus 1
    
    deriv_standard = (y_i - y_im1) / h
    
    print("[1] BACKWARD DIFFERENCE STANDARD (2 Titik)")
    print(f"    f({xi})       = {y_i:.6f}")
    print(f"    f({xi}-{h})    = {y_im1:.6f}")
    print(f"    Rumus: ( {y_i:.4f} - {y_im1:.4f} ) / {h}")
    print(f"    HASIL f'(x)  = {deriv_standard:.6f}")
    print("-" * 60)
    
    # --- B. BACKWARD DIFFERENCE HIGH ACCURACY (O(h^2)) ---
    # Rumus: f'(x) = [ 3*f(xi) - 4*f(xi - h) + f(xi - 2h) ] / (2*h)
    # Butuh 3 titik: xi, xi-1, xi-2
    
    y_im2 = f(xi - 2*h) # i minus 2
    
    deriv_high_acc = (3*y_i - 4*y_im1 + y_im2) / (2 * h)
    
    print("[2] HIGH ACCURACY BACKWARD (3 Titik)")
    print(f"    f({xi}-2*{h})  = {y_im2:.6f}")
    print(f"    Rumus: ( 3*{y_i:.4f} - 4*{y_im1:.4f} + {y_im2:.4f} ) / (2*{h})")
    print(f"    HASIL f'(x)  = {deriv_high_acc:.6f}")
    print("-" * 60)

# Jalankan Fungsi
calculate_backward_difference(xi, h)