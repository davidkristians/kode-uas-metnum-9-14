import numpy as np
import pandas as pd

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== INTERPOLASI KUADRATIK (NEWTON ORDE 2) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH SESUAI SOAL)
# ==============================================================================
# 1. Masukkan Data Titik (x dan y)
#    Contoh dari Excel Quadratic.csv (ln x):
x_data = np.array([1.0, 4.0, 6.0]) 
y_data = np.array([0.0, 1.386294, 1.791759])

# 2. Masukkan Nilai x yang ingin dicari (xf)
xf = 2.0
# ==============================================================================

def quadratic_interpolation_step_by_step(x_points, y_points, x_find):
    # 1. Validasi & Cari 3 Titik Terdekat
    if len(x_points) < 3:
        print("Error: Interpolasi Kuadratik butuh minimal 3 titik data.")
        return

    # Urutkan berdasarkan jarak terdekat ke xf
    dist = np.abs(x_points - x_find)
    idx_sorted = np.argsort(dist)
    # Ambil 3 titik terdekat, lalu urutkan kembali indexnya agar x0 < x1 < x2
    selected_indices = sorted(idx_sorted[:3])
    
    x = x_points[selected_indices]
    y = y_points[selected_indices]
    
    x0, x1, x2 = x[0], x[1], x[2]
    y0, y1, y2 = y[0], y[1], y[2]
    
    print("-" * 60)
    print(f"Mencari nilai f({x_find})")
    print(f"Menggunakan 3 titik terdekat:")
    print(f"x0 = {x0:<8} => f(x0) = {y0}")
    print(f"x1 = {x1:<8} => f(x1) = {y1}")
    print(f"x2 = {x2:<8} => f(x2) = {y2}")
    print("-" * 60)
    
    # 2. Hitung Divided Differences (Manual Step-by-Step)
    # Tahap 1: First Divided Difference (b1 dan temannya)
    div1_0 = (y1 - y0) / (x1 - x0)  # Ini b1 sementara
    div1_1 = (y2 - y1) / (x2 - x1)  # Ini jembatan ke b2
    
    # Tahap 2: Second Divided Difference (b2)
    div2_0 = (div1_1 - div1_0) / (x2 - x0) # Ini b2
    
    # Koefisien Akhir
    b0 = y0
    b1 = div1_0
    b2 = div2_0
    
    # 3. Tampilkan Tabel (Sesuai Excel)
    print("\n--- STEP 1: TABEL SELISIH TERBAGI ---")
    data_table = {
        'i': [0, 1, 2],
        'xi': [x0, x1, x2],
        'f(xi)': [y0, y1, y2],
        'First (b1)': [b1, div1_1, ""], # Kolom selisih pertama
        'Second (b2)': [b2, "", ""]     # Kolom selisih kedua
    }
    df = pd.DataFrame(data_table)
    print(df.fillna("").to_string(index=False))
    
    # 4. Hitung Hasil Akhir
    # Rumus: f2(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1)
    
    term1 = b1 * (x_find - x0)
    term2 = b2 * (x_find - x0) * (x_find - x1)
    y_result = b0 + term1 + term2
    
    # 5. Penjabaran Rumus
    print("\n--- STEP 2: PERHITUNGAN POLINOMIAL ---")
    print(f"Rumus: f2(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1)")
    print(f"             = {b0:.6f} + {b1:.6f}({x_find}-{x0}) + {b2:.6f}({x_find}-{x0})({x_find}-{x1})")
    print(f"             = {b0:.6f} + {b1:.6f}({x_find - x0}) + {b2:.6f}({x_find - x0})({x_find - x1})")
    print(f"             = {b0:.6f} + ({term1:.6f}) + ({term2:.6f})")
    print(f"             = {y_result:.6f}")
    
    print("-" * 60)
    print(f"HASIL AKHIR: f({x_find}) = {y_result:.6f}")
    print("-" * 60)

# Jalankan Fungsi
quadratic_interpolation_step_by_step(x_data, y_data, xf)