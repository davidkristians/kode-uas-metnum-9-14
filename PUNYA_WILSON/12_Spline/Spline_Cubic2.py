import numpy as np
import pandas as pd

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)

print("=== CUBIC SPLINE INTERPOLATION (RESULT ONLY) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH SESUAI SOAL)
# ==============================================================================
# 1. Masukkan Data Titik
x_data = np.array([0.0, 1.0, 2.0, 3.0]) 
y_data = np.array([1.0, 3.0, 2.0, 4.0])

# 2. Nilai x yang ingin dicari
x_find = 2.5
# ==============================================================================

def cubic_spline_clean(x, y, x_target=None):
    n_points = len(x)
    n_intervals = n_points - 1
    n_unknowns = 4 * n_intervals 
    
    # --- MENYUSUN MATRIKS (Di balik layar) ---
    A = np.zeros((n_unknowns, n_unknowns))
    B = np.zeros(n_unknowns)
    row = 0

    # 1. Syarat Fungsi
    for i in range(n_intervals):
        curr_x, curr_y = x[i], y[i]
        next_x, next_y = x[i+1], y[i+1]
        col_start = 4 * i
        
        A[row, col_start:col_start+4] = [curr_x**3, curr_x**2, curr_x, 1]
        B[row] = curr_y
        row += 1
        
        A[row, col_start:col_start+4] = [next_x**3, next_x**2, next_x, 1]
        B[row] = next_y
        row += 1

    # 2. Syarat Turunan Pertama
    for i in range(n_intervals - 1):
        interior_x = x[i+1]
        col_curr = 4 * i
        col_next = 4 * (i+1)
        A[row, col_curr:col_curr+4] = [3*interior_x**2, 2*interior_x, 1, 0]
        A[row, col_next:col_next+4] = [-3*interior_x**2, -2*interior_x, -1, 0]
        B[row] = 0
        row += 1

    # 3. Syarat Turunan Kedua
    for i in range(n_intervals - 1):
        interior_x = x[i+1]
        col_curr = 4 * i
        col_next = 4 * (i+1)
        A[row, col_curr:col_curr+4] = [6*interior_x, 2, 0, 0]
        A[row, col_next:col_next+4] = [-6*interior_x, -2, 0, 0]
        B[row] = 0
        row += 1

    # 4. Syarat Batas (Natural)
    x0, xn = x[0], x[-1]
    A[row, 0:4] = [6*x0, 2, 0, 0]
    B[row] = 0
    row += 1
    col_last = 4 * (n_intervals - 1)
    A[row, col_last:col_last+4] = [6*xn, 2, 0, 0]
    B[row] = 0
    row += 1

    # --- HITUNG KOEFISIEN ---
    try:
        Coeffs = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        print("Error: Matriks Singular.")
        return

    # --- TAMPILKAN HASIL SESUAI PERMINTAAN ---
    results = []
    print("-" * 80)
    print("HASIL KOEFISIEN & PERSAMAAN CUBIC SPLINE")
    print("-" * 80)
    
    for i in range(n_intervals):
        idx = 4 * i
        ai, bi, ci, di = Coeffs[idx], Coeffs[idx+1], Coeffs[idx+2], Coeffs[idx+3]
        
        # Format string persamaan
        eq_str = f"{ai:.4f}x^3 + {bi:.4f}x^2 + {ci:.4f}x + {di:.4f}"
        range_str = f"{x[i]} < x < {x[i+1]}"
        
        print(f"Interval {i+1} [{range_str}]:")
        print(f"  y = {eq_str}")
        print(f"  (a={ai:.6f}, b={bi:.6f}, c={ci:.6f}, d={di:.6f})")
        print("-" * 40)
        
        results.append({
            'range': (x[i], x[i+1]),
            'coeffs': (ai, bi, ci, di),
            'eq_str': eq_str
        })

    # --- TAMPILKAN PREDIKSI SESUAI PERMINTAAN ---
    if x_target is not None:
        print("")
        print(f"[PREDIKSI] Mencari nilai y saat x = {x_target}")
        found = False
        for res in results:
            xmin, xmax = res['range']
            if xmin <= x_target <= xmax:
                a, b, c, d = res['coeffs']
                y_res = a*(x_target**3) + b*(x_target**2) + c*x_target + d
                
                print(f">> x={x_target} berada di interval {xmin} s/d {xmax}")
                print(f">> Menggunakan: y = {res['eq_str']}")
                print(f">> Hitungan: {a:.4f}({x_target})^3 + ... + {d:.4f}")
                print(f">> HASIL AKHIR: {y_res:.6f}")
                found = True
                break
        
        if not found:
            # Ekstrapolasi sederhana (ambil ujung)
            if x_target < x[0]: res = results[0]
            else: res = results[-1]
            a, b, c, d = res['coeffs']
            y_res = a*(x_target**3) + b*(x_target**2) + c*x_target + d
            print(">> Peringatan: Ekstrapolasi (Menggunakan interval terdekat)")
            print(f">> HASIL AKHIR: {y_res:.6f}")

# Jalankan
cubic_spline_clean(x_data, y_data, x_find)