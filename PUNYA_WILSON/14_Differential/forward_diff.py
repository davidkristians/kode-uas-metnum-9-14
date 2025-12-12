import numpy as np
import math

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)

print("=== NUMERICAL DIFFERENTIATION: FORWARD DIFFERENCE ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. Definisikan Fungsi f(x) atau v(t)
def f(x):
    # --- CONTOH 1: Soal Roket (Sesuai Excel Forward Diff.csv) ---
    # v(t) = 2000 * ln(140000 / (140000 - 2100*t)) - 9.8*t
    # x disini adalah t (waktu)
    
    term1 = 2000 * math.log(140000 / (140000 - 2100 * x))
    term2 = 9.8 * x
    return term1 - term2

    # --- CONTOH 2: Polinomial ---
    # return -0.1*x**4 - 0.15*x**3 - 0.5*x**2 - 0.25*x + 1.2

    # --- CONTOH 3: Trigonometri ---
    # return math.sin(x)

# 2. Tentukan Titik yang Dicari dan Ukuran Langkah
xi = 16.0    # Titik x yang ingin dicari turunannya
h  = 2.0     # Step size (Jarak antar titik)

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (OTOMATIS)
# ==============================================================================

def calculate_forward_difference(xi, h):
    print(f"Mencari turunan f'(x) pada x = {xi} dengan h = {h}")
    print("-" * 60)
    
    # --- A. FORWARD DIFFERENCE BIASA (O(h)) ---
    # Rumus: f'(x) = [ f(xi + h) - f(xi) ] / h
    # Butuh 2 titik: xi dan xi+1
    
    y_i = f(xi)
    y_ip1 = f(xi + h) # i plus 1
    
    deriv_standard = (y_ip1 - y_i) / h
    
    print("[1] FORWARD DIFFERENCE STANDARD (2 Titik)")
    print(f"    f({xi})       = {y_i:.6f}")
    print(f"    f({xi}+{h})    = {y_ip1:.6f}")
    print(f"    Rumus: ( {y_ip1:.4f} - {y_i:.4f} ) / {h}")
    print(f"    HASIL f'(x)  = {deriv_standard:.6f}")
    print("-" * 60)
    
    # --- B. FORWARD DIFFERENCE HIGH ACCURACY (O(h^2)) ---
    # Rumus: f'(x) = [ -f(xi + 2h) + 4*f(xi + h) - 3*f(xi) ] / (2*h)
    # Butuh 3 titik: xi, xi+1, xi+2
    
    y_ip2 = f(xi + 2*h) # i plus 2
    
    deriv_high_acc = (-y_ip2 + 4*y_ip1 - 3*y_i) / (2 * h)
    
    print("[2] HIGH ACCURACY FORWARD (3 Titik)")
    print(f"    f({xi}+2*{h})  = {y_ip2:.6f}")
    print(f"    Rumus: ( -{y_ip2:.4f} + 4*{y_ip1:.4f} - 3*{y_i:.4f} ) / (2*{h})")
    print(f"    HASIL f'(x)  = {deriv_high_acc:.6f}")
    print("-" * 60)

# Jalankan Fungsi
calculate_forward_difference(xi, h)