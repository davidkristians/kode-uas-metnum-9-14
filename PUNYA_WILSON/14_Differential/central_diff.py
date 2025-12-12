import numpy as np
import math

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)

print("=== NUMERICAL DIFFERENTIATION: CENTRAL DIFFERENCE ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. Definisikan Fungsi f(x)
def f(x):
    # --- CONTOH 1: Soal Roket (Sesuai Excel Central Diff.csv) ---
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

def calculate_central_difference(xi, h):
    print(f"Mencari turunan f'(x) pada x = {xi} dengan h = {h}")
    print("-" * 60)
    
    # --- A. CENTRAL DIFFERENCE BIASA (O(h^2)) ---
    # Konsep: Ambil titik depan dan belakang, lalu bagi 2h
    # Rumus: f'(x) = [ f(xi + h) - f(xi - h) ] / (2*h)
    
    y_ip1 = f(xi + h) # i plus 1 (Depan)
    y_im1 = f(xi - h) # i minus 1 (Belakang)
    
    deriv_standard = (y_ip1 - y_im1) / (2 * h)
    
    print("[1] CENTRAL DIFFERENCE STANDARD (2 Titik: Depan & Belakang)")
    print(f"    f({xi}+{h})    = {y_ip1:.6f}")
    print(f"    f({xi}-{h})    = {y_im1:.6f}")
    print(f"    Rumus: ( {y_ip1:.4f} - {y_im1:.4f} ) / (2*{h})")
    print(f"    HASIL f'(x)  = {deriv_standard:.6f}")
    print("-" * 60)
    
    # --- B. CENTRAL DIFFERENCE HIGH ACCURACY (O(h^4)) ---
    # Rumus: f'(x) = [ -f(xi+2h) + 8f(xi+h) - 8f(xi-h) + f(xi-2h) ] / (12*h)
    # Butuh 4 titik: xi+2, xi+1, xi-1, xi-2
    
    y_ip2 = f(xi + 2*h) # i plus 2
    y_im2 = f(xi - 2*h) # i minus 2
    
    term_plus = -y_ip2 + 8*y_ip1
    term_mins = -8*y_im1 + y_im2
    
    deriv_high_acc = (term_plus + term_mins) / (12 * h)
    
    print("[2] HIGH ACCURACY CENTRAL (4 Titik)")
    print(f"    f({xi}+2*{h})  = {y_ip2:.6f}")
    print(f"    f({xi}-2*{h})  = {y_im2:.6f}")
    print(f"    Rumus: (-f_ip2 + 8*f_ip1 - 8*f_im1 + f_im2) / (12*{h})")
    print(f"    HASIL f'(x)  = {deriv_high_acc:.6f}")
    print("-" * 60)

# Jalankan Fungsi
calculate_central_difference(xi, h)