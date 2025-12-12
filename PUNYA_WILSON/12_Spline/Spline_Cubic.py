import numpy as np
import pandas as pd

# Atur tampilan float agar rapi & lebar kolom cukup
np.set_printoptions(precision=4, suppress=True)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
pd.set_option('display.max_columns', None) # Tampilkan semua kolom
pd.set_option('display.width', 1000)

print("=== CUBIC SPLINE INTERPOLATION (FULL MATRIX OUTPUT) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH SESUAI SOAL)
# ==============================================================================
# 1. Masukkan Data Titik
x_data = np.array([0.0, 1.0, 2.0, 3.0]) 
y_data = np.array([1.0, 3.0, 2.0, 4.0])

# CATATAN:
# Jika data hanya 4 titik (0,1,2,3), maka hanya ada 3 interval (1,2,3).
# Jadi hanya akan muncul a1..d1, a2..d2, a3..d3.
# Jika Anda ingin muncul a4..d4, Anda harus memasukkan 5 titik data.

# 2. Nilai x yang ingin dicari
x_find = 2.5
# ==============================================================================

def cubic_spline_full(x, y, x_target=None):
    n_points = len(x)
    n_intervals = n_points - 1
    n_unknowns = 4 * n_intervals 
    
    # Matriks Ax = B
    A = np.zeros((n_unknowns, n_unknowns))
    B = np.zeros(n_unknowns)
    
    # List nama baris untuk label tabel matriks
    row_labels = []

    print("-" * 80)
    print("MENYUSUN MATRIKS (Sama seperti area Matriks di Excel)")
    print("-" * 80)

    row = 0

    # --- 1. SYARAT FUNGSI ---
    for i in range(n_intervals):
        # Kiri
        curr_x, curr_y = x[i], y[i]
        col_start = 4 * i
        A[row, col_start:col_start+4] = [curr_x**3, curr_x**2, curr_x, 1]
        B[row] = curr_y
        row_labels.append(f"Interval {i+1} (Kiri x={curr_x})")
        row += 1
        
        # Kanan
        next_x, next_y = x[i+1], y[i+1]
        A[row, col_start:col_start+4] = [next_x**3, next_x**2, next_x, 1]
        B[row] = next_y
        row_labels.append(f"Interval {i+1} (Kanan x={next_x})")
        row += 1

    # --- 2. SYARAT TURUNAN PERTAMA ---
    for i in range(n_intervals - 1):
        interior_x = x[i+1]
        col_curr = 4 * i
        col_next = 4 * (i+1)
        
        # 3ax^2 + 2bx + c (Kiri) - (Kanan) = 0
        A[row, col_curr:col_curr+4] = [3*interior_x**2, 2*interior_x, 1, 0]
        A[row, col_next:col_next+4] = [-3*interior_x**2, -2*interior_x, -1, 0]
        B[row] = 0
        row_labels.append(f"Turunan 1 Kontinu (x={interior_x})")
        row += 1

    # --- 3. SYARAT TURUNAN KEDUA ---
    for i in range(n_intervals - 1):
        interior_x = x[i+1]
        col_curr = 4 * i
        col_next = 4 * (i+1)
        
        # 6ax + 2b (Kiri) - (Kanan) = 0
        A[row, col_curr:col_curr+4] = [6*interior_x, 2, 0, 0]
        A[row, col_next:col_next+4] = [-6*interior_x, -2, 0, 0]
        B[row] = 0
        row_labels.append(f"Turunan 2 Kontinu (x={interior_x})")
        row += 1

    # --- 4. SYARAT BATAS (NATURAL) ---
    # Ujung Kiri
    x0 = x[0]
    A[row, 0:4] = [6*x0, 2, 0, 0]
    B[row] = 0
    row_labels.append(f"Natural Boundary (Kiri x={x0})")
    row += 1
    
    # Ujung Kanan
    xn = x[-1]
    col_last = 4 * (n_intervals - 1)
    A[row, col_last:col_last+4] = [6*xn, 2, 0, 0]
    B[row] = 0
    row_labels.append(f"Natural Boundary (Kanan x={xn})")
    row += 1

    # --- TAMPILKAN TABEL MATRIKS ---
    # Membuat nama kolom (a1, b1, c1, d1, a2...)
    col_names = []
    for i in range(n_intervals):
        for var in ['a', 'b', 'c', 'd']:
            col_names.append(f"{var}{i+1}")
            
    df_matrix = pd.DataFrame(A, columns=col_names)
    df_matrix['= B (Hasil)'] = B
    df_matrix.index = row_labels
    
    print("\n[TABEL MATRIKS LENGKAP]")
    print(df_matrix.to_string())

    # --- SOLVE ---
    try:
        Coeffs = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        print("\nError: Matriks Singular.")
        return

    # --- OUTPUT HASIL KOEFISIEN (DAFTAR KE BAWAH) ---
    print("\n" + "="*40)
    print("HASIL KOEFISIEN (a, b, c, d)")
    print("="*40)
    
    # Loop untuk print a1, b1, c1, d1...
    for i in range(n_intervals):
        idx = 4 * i
        print(f"--- Interval {i+1} ---")
        print(f"a{i+1} = {Coeffs[idx]:.8f}")
        print(f"b{i+1} = {Coeffs[idx+1]:.8f}")
        print(f"c{i+1} = {Coeffs[idx+2]:.8f}")
        print(f"d{i+1} = {Coeffs[idx+3]:.8f}")
        print("") # Spasi

    # --- PREDIKSI ---
    if x_target is not None:
        print("="*40)
        print(f"PREDIKSI NILAI SAAT x = {x_target}")
        print("="*40)
        found = False
        for i in range(n_intervals):
            if x[i] <= x_target <= x[i+1]:
                idx = 4 * i
                a, b, c, d = Coeffs[idx:idx+4]
                y_res = a*x_target**3 + b*x_target**2 + c*x_target + d
                print(f"Menggunakan Koefisien Interval {i+1}")
                print(f"Hasil: {y_res:.6f}")
                found = True
                break
        if not found:
            print("Nilai x diluar rentang (Ekstrapolasi).")

# Jalankan
cubic_spline_full(x_data, y_data, x_find)