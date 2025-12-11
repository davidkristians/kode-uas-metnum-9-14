import numpy as np
import pandas as pd

# Atur tampilan
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== ESTIMASI ERROR INTERPOLASI NEWTON ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI)
# ==============================================================================
# Masukkan SEMUA titik yang diketahui (Titik Interpolasi + Titik Tambahan)
# Urutkan berdasarkan x dari kecil ke besar agar rapi

# --- CONTOH 1: Error Linear (Butuh 3 Titik) ---
# Sesuai file 'Error Linear.csv': x=1, x=4, x=6
x_all = np.array([1.0, 4.0, 6.0])
y_all = np.array([0.0, 1.386294, 1.791759])

# --- CONTOH 2: Error Quadratic (Butuh 4 Titik) ---
# Hapus tanda pagar '#' di bawah untuk mencoba
# x_all = np.array([1.0, 4.0, 5.0, 6.0]) 
# y_all = np.array([0.0, 1.386294, 1.609438, 1.791759])

# Masukkan Nilai x yang dicari
xf = 2.0
# ==============================================================================

def calculate_interpolation_error(x, y, x_find):
    n = len(x)
    orde_interp = n - 2 # Karena n titik digunakan untuk estimasi error orde n-2
    
    if n < 3:
        print("Error: Butuh minimal 3 titik untuk estimasi error (Linear).")
        return

    print("-" * 60)
    if orde_interp == 1:
        print("MODE: ESTIMASI ERROR LINEAR (Interpolasi 2 Titik + 1 Titik Cek)")
    elif orde_interp == 2:
        print("MODE: ESTIMASI ERROR KUADRATIK (Interpolasi 3 Titik + 1 Titik Cek)")
    else:
        print(f"MODE: ESTIMASI ERROR ORDE {orde_interp}")
        
    print(f"Mencari nilai di x = {x_find}")
    print("-" * 60)

    # ---------------------------------------------------------
    # 1. MEMBUAT TABEL SELISIH TERBAGI (UNTUK SEMUA TITIK)
    # ---------------------------------------------------------
    div_diff = np.zeros((n, n))
    div_diff[:, 0] = y
    
    for j in range(1, n):
        for i in range(n - j):
            # Rumus Newton: (bawah - atas) / (x_bawah - x_atas)
            div_diff[i, j] = (div_diff[i+1, j-1] - div_diff[i, j-1]) / (x[i+j] - x[i])
            
    # Ambil koefisien b (baris pertama)
    b = div_diff[0, :]
    
    # Tampilkan Tabel
    cols = ['yi'] + [f'Order {k}' for k in range(1, n)]
    df_table = pd.DataFrame(div_diff, columns=cols)
    df_table.insert(0, 'xi', x)
    
    # Rapikan tampilan (hilangkan nol)
    df_display = df_table.copy()
    for j in range(1, n):
        for i in range(n - j, n):
            df_display.iloc[i, j+1] = np.nan
            
    print("\n[STEP 1] TABEL SELISIH TERBAGI LENGKAP:")
    print(df_display.fillna("").to_string(index=False))
    
    # ---------------------------------------------------------
    # 2. HITUNG HASIL INTERPOLASI (TANPA TITIK TERAKHIR)
    # ---------------------------------------------------------
    # Kita gunakan b0 sampai b_(n-2)
    y_pred = b[0]
    accumulation_x = 1.0
    
    print(f"\n[STEP 2] HASIL INTERPOLASI (Orde {orde_interp}):")
    print(f"Menggunakan {n-1} titik pertama: {x[:-1]}")
    
    # Hitung suku per suku
    for i in range(1, n - 1): # Loop sampai n-2
        accumulation_x *= (x_find - x[i-1])
        term = b[i] * accumulation_x
        y_pred += term
        
    print(f"Hasil Interpolasi f({x_find}) = {y_pred:.6f}")
    
    # ---------------------------------------------------------
    # 3. HITUNG ESTIMASI ERROR (PAKAI SUKU TERAKHIR)
    # ---------------------------------------------------------
    # Error = b_terakhir * (x - x0) * (x - x1) * ... * (x - x_terakhir_interp)
    
    print(f"\n[STEP 3] ESTIMASI ERROR (Menggunakan titik tambahan x={x[-1]}):")
    
    # Ambil koefisien terakhir (b untuk error)
    b_error = b[n-1] 
    
    # Hitung perkalian (x - xi) untuk semua titik interpolasi
    term_error_x = 1.0
    term_str = f"{b_error:.6f}"
    
    for i in range(n - 1):
        diff = (x_find - x[i])
        term_error_x *= diff
        term_str += f" * ({diff:.2f})"
        
    estimated_error = b_error * term_error_x
    
    print(f"Rumus Error = b{n-1} * (xf-x0) * ... * (xf-x{n-2})")
    print(f"            = {term_str}")
    print(f"Nilai Error = {estimated_error:.6f}")
    
    # Hitung % Error (Jika y_pred tidak 0)
    if y_pred != 0:
        error_pct = abs(estimated_error / y_pred) * 100
    else:
        error_pct = 0
        
    print("-" * 60)
    print(f"KESIMPULAN:")
    print(f"Nilai Taksiran      : {y_pred:.6f}")
    print(f"Estimasi Kesalahan  : {estimated_error:.6f}")
    print("-" * 60)

# Jalankan Fungsi
calculate_interpolation_error(x_all, y_all, xf)