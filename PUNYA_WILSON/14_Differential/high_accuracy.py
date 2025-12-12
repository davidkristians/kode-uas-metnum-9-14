import numpy as np
import pandas as pd
import math

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== HIGH ACCURACY NUMERICAL DIFFERENTIATION ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI SESUAI SOAL)
# ==============================================================================

# 1. Definisikan Fungsi f(x)
def f(x):
    # --- CONTOH 1: Polinomial (Sesuai Excel High Accuracy) ---
    # f(x) = -0.1*x^4 - 0.15*x^3 - 0.5*x^2 - 0.25*x + 1.2
    return -0.1*x**4 - 0.15*x**3 - 0.5*x**2 - 0.25*x + 1.2

    # --- CONTOH 2: Soal Roket ---
    # term1 = 2000 * math.log(140000 / (140000 - 2100 * x))
    # term2 = 9.8 * x
    # return term1 - term2

# 2. Parameter
xi = 0.5    # Titik x yang dicari turunannya
h  = 0.25   # Step size

# 3. Pilih Metode High Accuracy: 'forward', 'backward', atau 'central'
metode = 'backward' 

# ==============================================================================
# BAGIAN 2: PROSES HITUNG (OTOMATIS)
# ==============================================================================

def calculate_high_accuracy(xi, h, method):
    print(f"Metode : High Accuracy {method.upper()}")
    print(f"Posisi : x = {xi}")
    print(f"Step(h): {h}")
    print("-" * 50)
    
    table_data = []
    result = 0
    rumus_str = ""
    
    # --- LOGIKA PEMILIHAN METODE ---
    
    if method == 'forward':
        # Butuh: xi, xi+1, xi+2
        # Rumus: (-f(i+2) + 4f(i+1) - 3f(i)) / 2h
        
        x0 = xi
        x1 = xi + h
        x2 = xi + 2*h
        
        y0, y1, y2 = f(x0), f(x1), f(x2)
        
        # Simpan data untuk tabel
        table_data.append({'Titik': 'xi (i)',     'x': x0, 'f(x)': y0, 'Koef': -3})
        table_data.append({'Titik': 'xi+1 (i+1)', 'x': x1, 'f(x)': y1, 'Koef': 4})
        table_data.append({'Titik': 'xi+2 (i+2)', 'x': x2, 'f(x)': y2, 'Koef': -1})
        
        result = (-y2 + 4*y1 - 3*y0) / (2*h)
        rumus_str = "(-f(i+2) + 4*f(i+1) - 3*f(i)) / 2h"

    elif method == 'backward':
        # Butuh: xi, xi-1, xi-2
        # Rumus: (3f(i) - 4f(i-1) + f(i-2)) / 2h
        
        x0 = xi
        x_minus1 = xi - h
        x_minus2 = xi - 2*h
        
        y0, y_m1, y_m2 = f(x0), f(x_minus1), f(x_minus2)
        
        table_data.append({'Titik': 'xi (i)',     'x': x0,       'f(x)': y0,   'Koef': 3})
        table_data.append({'Titik': 'xi-1 (i-1)', 'x': x_minus1, 'f(x)': y_m1, 'Koef': -4})
        table_data.append({'Titik': 'xi-2 (i-2)', 'x': x_minus2, 'f(x)': y_m2, 'Koef': 1})
        
        result = (3*y0 - 4*y_m1 + y_m2) / (2*h)
        rumus_str = "(3*f(i) - 4*f(i-1) + f(i-2)) / 2h"

    elif method == 'central':
        # Butuh: xi-2, xi-1, xi+1, xi+2 (4 Titik)
        # Rumus: (-f(i+2) + 8f(i+1) - 8f(i-1) + f(i-2)) / 12h
        
        xp2 = xi + 2*h
        xp1 = xi + h
        xm1 = xi - h
        xm2 = xi - 2*h
        
        yp2, yp1, ym1, ym2 = f(xp2), f(xp1), f(xm1), f(xm2)
        
        table_data.append({'Titik': 'xi+2 (i+2)', 'x': xp2, 'f(x)': yp2, 'Koef': -1})
        table_data.append({'Titik': 'xi+1 (i+1)', 'x': xp1, 'f(x)': yp1, 'Koef': 8})
        table_data.append({'Titik': 'xi-1 (i-1)', 'x': xm1, 'f(x)': ym1, 'Koef': -8})
        table_data.append({'Titik': 'xi-2 (i-2)', 'x': xm2, 'f(x)': ym2, 'Koef': 1})
        
        result = (-yp2 + 8*yp1 - 8*ym1 + ym2) / (12*h)
        rumus_str = "(-f(i+2) + 8*f(i+1) - 8*f(i-1) + f(i-2)) / 12h"

    else:
        print("Metode tidak dikenal. Pilih: forward, backward, atau central")
        return

    # --- TAMPILKAN OUTPUT ---
    df = pd.DataFrame(table_data)
    # Urutkan berdasarkan x agar rapi
    df = df.sort_values(by='x', ascending=True)
    
    print("\n[TABEL DATA YANG DIGUNAKAN]")
    print(df[['Titik', 'x', 'f(x)', 'Koef']].to_string(index=False))
    print("-" * 50)
    
    print(f"Rumus: {rumus_str}")
    
    # Tampilkan hitungan kasar
    print("Hitungan:")
    print(f"Pembilang = ", end="")
    coeffs_val = 0
    for item in table_data:
        val = item['f(x)'] * item['Koef']
        coeffs_val += val
        print(f"({item['Koef']} * {item['f(x)']:.4f}) + ", end="")
    print("0")
    
    if method == 'central':
        divisor = 12 * h
        print(f"Penyebut  = 12 * {h} = {divisor}")
    else:
        divisor = 2 * h
        print(f"Penyebut  = 2 * {h} = {divisor}")
        
    print("-" * 50)
    print(f"HASIL AKHIR f'({xi}) = {result:.6f}")
    print("=" * 50)

# Jalankan
calculate_high_accuracy(xi, h, metode)