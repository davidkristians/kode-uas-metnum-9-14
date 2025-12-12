# Quadratic Spline

import numpy as np
import pandas as pd

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== QUADRATIC SPLINE INTERPOLATION ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH SESUAI SOAL)
# ==============================================================================
# 1. Masukkan Data Titik (Contoh dari Excel Quadratic Spline.csv)
# x_data = np.array([3.0, 4.5, 7.0, 9.0])
# y_data = np.array([2.5, 1.0, 2.5, 0.5])

x_data = np.array([3, 4.5, 7, 9, 11, 13, 15, 17])
y_data = np.array([2.5, 1, 2.5, 0.5, 0.5, 0, -0.4, -1])

# 2. Nilai x yang ingin dicari
# x_find = 5.0
x_find = 14
# ==============================================================================

def quadratic_spline_calculation(x, y, x_target=None):
    n = len(x)
    n_intervals = n - 1
    n_unknowns = 3 * n_intervals # a, b, c untuk setiap interval
    
    # Matriks A dan Vektor B untuk Ax = B
    A = np.zeros((n_unknowns, n_unknowns))
    B = np.zeros(n_unknowns)
    
    equation_desc = [] # Untuk menyimpan deskripsi persamaan agar mirip Excel

    print("-" * 80)
    print("MENYUSUN SISTEM PERSAMAAN (MATRIKS)")
    print("-" * 80)
    
    row = 0
    
    # --- 1. Persamaan FUNGSI di setiap titik (Interior & Exterior) ---
    # Setiap interval i punya persamaan: ai*x^2 + bi*x + ci = y
    
    for i in range(n_intervals):
        # Titik Kiri interval ke-i
        # a_i * x_i^2 + b_i * x_i + c_i = y_i
        curr_x = x[i]
        curr_y = y[i]
        
        col_start = 3 * i
        A[row, col_start]   = curr_x ** 2   # a_i
        A[row, col_start+1] = curr_x        # b_i
        A[row, col_start+2] = 1             # c_i
        B[row] = curr_y
        
        desc = f"Interval {i+1} (Titik Kiri x={curr_x}): {curr_x**2}*a{i+1} + {curr_x}*b{i+1} + c{i+1} = {curr_y}"
        equation_desc.append(desc)
        row += 1
        
        # Titik Kanan interval ke-i
        # a_i * x_{i+1}^2 + b_i * x_{i+1} + c_i = y_{i+1}
        next_x = x[i+1]
        next_y = y[i+1]
        
        A[row, col_start]   = next_x ** 2
        A[row, col_start+1] = next_x
        A[row, col_start+2] = 1
        B[row] = next_y
        
        desc = f"Interval {i+1} (Titik Kanan x={next_x}): {next_x**2}*a{i+1} + {next_x}*b{i+1} + c{i+1} = {next_y}"
        equation_desc.append(desc)
        row += 1

    # --- 2. Persamaan KONTINUITAS TURUNAN PERTAMA di titik dalam (Interior Knots) ---
    # Turunan: 2*a_i*x + b_i = 2*a_{i+1}*x + b_{i+1}
    # Pindah ruas: 2*x*a_i + b_i - 2*x*a_{i+1} - b_{i+1} = 0
    
    for i in range(n_intervals - 1):
        interior_x = x[i+1] # Titik sambung
        
        col_i = 3 * i
        col_next = 3 * (i+1)
        
        # Suku interval kiri
        A[row, col_i]   = 2 * interior_x # 2*a_i*x
        A[row, col_i+1] = 1              # b_i
        
        # Suku interval kanan (dikurang)
        A[row, col_next]   = -2 * interior_x # -2*a_{i+1}*x
        A[row, col_next+1] = -1              # -b_{i+1}
        
        B[row] = 0
        
        desc = f"Kontinuitas Turunan di x={interior_x}: {2*interior_x}*a{i+1} + b{i+1} = {2*interior_x}*a{i+2} + b{i+2}"
        equation_desc.append(desc)
        row += 1
        
    # --- 3. KONDISI BATAS (Boundary Condition) ---
    # Asumsi umum Quadratic Spline: Garis pertama adalah Linear (a1 = 0)
    # Persamaan: 1 * a1 = 0
    
    A[row, 0] = 1 # Koefisien a1
    B[row] = 0
    desc = f"Kondisi Batas (Asumsi Linear Awal): a1 = 0"
    equation_desc.append(desc)
    row += 1
    
    # --- TAMPILKAN PERSAMAAN ---
    for i, eq in enumerate(equation_desc):
        print(f"Eq {i+1}: {eq}")
    
    # --- HITUNG SOLUSI ---
    try:
        Coeffs = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        print("\nError: Matriks Singular. Tidak bisa diselesaikan.")
        return

    # Susun ulang koefisien agar mudah dibaca
    results = []
    print("\n" + "-" * 80)
    print("HASIL KOEFISIEN & PERSAMAAN SPLINE")
    print("-" * 80)
    
    for i in range(n_intervals):
        idx = 3 * i
        ai = Coeffs[idx]
        bi = Coeffs[idx+1]
        ci = Coeffs[idx+2]
        
        eq_str = f"{ai:.6f}x^2 + {bi:.6f}x + {ci:.6f}"
        range_str = f"{x[i]} < x < {x[i+1]}"
        
        print(f"Interval {i+1} [{range_str}]:")
        print(f"  y = {eq_str}")
        print(f"  (a{i+1}={ai:.6f}, b{i+1}={bi:.6f}, c{i+1}={ci:.6f})")
        print("-" * 40)
        
        results.append({
            'range': (x[i], x[i+1]),
            'coeffs': (ai, bi, ci),
            'eq_str': eq_str
        })
        
    # --- PREDIKSI NILAI ---
    if x_target is not None:
        print(f"\n[PREDIKSI] Mencari nilai y saat x = {x_target}")
        found = False
        for res in results:
            xmin, xmax = res['range']
            if xmin <= x_target <= xmax:
                a, b, c = res['coeffs']
                y_res = a*(x_target**2) + b*x_target + c
                
                print(f">> x={x_target} berada di interval {xmin} s/d {xmax}")
                print(f">> Menggunakan: y = {res['eq_str']}")
                print(f">> Hitungan: {a:.6f}({x_target}^2) + {b:.6f}({x_target}) + {c:.6f}")
                print(f">> HASIL AKHIR: {y_res:.6f}")
                found = True
                break
        
        if not found:
            print(">> Peringatan: x berada di luar rentang (Ekstrapolasi). Menggunakan interval terdekat.")
            # Logika ekstrapolasi sederhana (ambil ujung)
            if x_target < x[0]:
                res = results[0]
            else:
                res = results[-1]
            
            a, b, c = res['coeffs']
            y_res = a*(x_target**2) + b*x_target + c
            print(f">> HASIL EKSTRAPOLASI: {y_res:.6f}")

# Jalankan Fungsi
quadratic_spline_calculation(x_data, y_data, x_find)