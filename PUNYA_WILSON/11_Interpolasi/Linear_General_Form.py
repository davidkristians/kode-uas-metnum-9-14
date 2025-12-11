import numpy as np
import pandas as pd

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== NEWTON'S DIVIDED DIFFERENCE INTERPOLATION (GENERAL ORDER) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI)
# ==============================================================================
# 1. Masukkan Data Titik (x dan y)
#    Tips: Jika soal memberi rumus f(x), hitung dulu y-nya manual, lalu masukkan kesini.
#    CONTOH DATA (Dari file 'General Form.csv' atau 'Extrapolation.csv')
x_points = np.array([1.0, 4.0, 5.0, 6.0]) 
y_points = np.array([0.0, 1.386294, 1.609438, 1.791759])

# 2. Masukkan Nilai x yang ingin dicari (xf)
xf = 2.0

# 3. Tentukan Orde Interpolasi (PENTING!)
#    1 = Linear (2 titik), 2 = Kuadratik (3 titik), 3 = Kubik (4 titik)
orde_diminta = 3 
# ==============================================================================

def newton_interpolation_general(x_all, y_all, x_target, order):
    n_points_needed = order + 1
    
    # 1. Cek Ketersediaan Data
    if len(x_all) < n_points_needed:
        print(f"Error: Untuk orde {order}, Anda butuh minimal {n_points_needed} titik data.")
        return

    # 2. Pilih Titik-Titik Terdekat secara Otomatis
    #    Kita mencari kombinasi titik yang paling dekat dengan x_target
    dist = np.abs(x_all - x_target)
    sorted_indices = np.argsort(dist) # Urutkan index berdasarkan jarak terdekat
    selected_indices = sorted(sorted_indices[:n_points_needed]) # Ambil n titik terdekat, lalu urutkan indexnya kembali
    
    x = x_all[selected_indices]
    y = y_all[selected_indices]
    
    print("-" * 60)
    print(f"Orde: {order} (Butuh {n_points_needed} titik)")
    print(f"Mencari nilai f({x_target})")
    print(f"Titik yang digunakan (x, y):")
    for i in range(n_points_needed):
        print(f"  x{i}={x[i]:<5} | y{i}={y[i]:.6f}")
    print("-" * 60)

    # 3. Membuat Tabel Divided Difference (b0, b1, b2...)
    n = len(x)
    # Matriks untuk menyimpan tabel selisih (kolom 0 adalah y asli)
    div_diff = np.zeros((n, n))
    div_diff[:, 0] = y
    
    # Hitung selisih terbagi kolom demi kolom
    for j in range(1, n):
        for i in range(n - j):
            # Rumus: (Next_val - Curr_val) / (x_bawah - x_atas)
            numerator = div_diff[i+1, j-1] - div_diff[i, j-1]
            denominator = x[i+j] - x[i]
            div_diff[i, j] = numerator / denominator

    # 4. Ambil Koefisien b (Baris paling atas dari setiap kolom)
    b = div_diff[0, :] # [b0, b1, b2, ...]
    
    # 5. Tampilkan Tabel Step-by-Step (Sesuai Excel)
    cols = ['yi (f[xi])'] + [f'Order {k}' for k in range(1, n)]
    df_table = pd.DataFrame(div_diff, columns=cols)
    df_table.insert(0, 'xi', x)
    
    # Bersihkan tampilan (ganti 0 di segitiga bawah jadi kosong)
    df_display = df_table.copy()
    for j in range(1, n): # Kolom diff
        for i in range(n - j, n): # Baris bawah
            df_display.iloc[i, j+1] = np.nan # Kosongkan biar rapi
            
    print("\n--- TABEL SELISIH TERBAGI (DIVIDED DIFFERENCE) ---")
    print(df_display.fillna("").to_string(index=False))
    
    # 6. Hitung Hasil Akhir (Polinomial Newton)
    # Rumus: b0 + b1(x-x0) + b2(x-x0)(x-x1) + ...
    
    y_pred = b[0] # Suku pertama (b0)
    term_str = f"{b[0]:.4f}" # Untuk print rumus
    
    # Loop untuk menghitung suku-suku berikutnya
    accumulation_x = 1.0
    for i in range(1, n):
        accumulation_x *= (x_target - x[i-1])
        term_val = b[i] * accumulation_x
        y_pred += term_val
        
        # Format string untuk display rumus
        sign = "+" if term_val >= 0 else "-"
        term_str += f" {sign} {abs(b[i]):.4f}"
        for k in range(i):
            term_str += f"({x_target}-{x[k]})"

    print("\n--- PERHITUNGAN POLINOMIAL ---")
    print(f"Rumus: f(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + ...")
    print(f"Substitusi:\n f({x_target}) = {term_str}")
    
    print("-" * 60)
    print(f"HASIL AKHIR: {y_pred:.6f}")
    print("-" * 60)

# Jalankan Fungsi
newton_interpolation_general(x_points, y_points, xf, orde_diminta)