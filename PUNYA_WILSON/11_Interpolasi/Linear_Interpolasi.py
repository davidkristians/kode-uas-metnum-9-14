import numpy as np
import pandas as pd

# Atur tampilan float agar rapi
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== INTERPOLASI LINEAR (METODE NEWTON) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH SESUAI SOAL)
# ==============================================================================
# 1. Masukkan Titik Data (x dan y)
#    Bisa masukkan banyak titik, nanti program otomatis pilih 2 titik yang mengapit xf.
#    Contoh data dari Excel: (1, 0) dan (6, 1.791759)
x_data = np.array([1.0, 6.0]) 
y_data = np.array([0.0, 1.791759])

# 2. Masukkan Nilai x yang ingin dicari (xf)
xf = 2.0
# ==============================================================================

def linear_interpolation_step_by_step(x_points, y_points, x_find):
    # 1. Validasi & Mencari Interval
    # Kita butuh 2 titik: x0 dan x1 dimana x0 <= x_find <= x1 (idealnya)
    # Atau cari 2 titik terdekat.
    
    if len(x_points) < 2:
        print("Error: Butuh minimal 2 titik data.")
        return

    # Logika mencari 2 titik tetangga (x0 dan x1)
    # Jika datanya urut, kita cari posisi x_find
    # (Kode ini mengasumsikan data x_points terurut menaik)
    idx = -1
    for i in range(len(x_points) - 1):
        if x_points[i] <= x_find <= x_points[i+1]:
            idx = i
            break
    
    if idx == -1:
        # Jika x_find di luar rentang (Ekstrapolasi), ambil 2 titik terdekat ujung
        if x_find < x_points[0]:
            idx = 0 # Ambil 2 titik pertama
            print(f"Catatan: Melakukan Ekstrapolasi (xf < min(x))")
        else:
            idx = len(x_points) - 2 # Ambil 2 titik terakhir
            print(f"Catatan: Melakukan Ekstrapolasi (xf > max(x))")
    
    # Ambil 2 titik terpilih
    x0, x1 = x_points[idx], x_points[idx+1]
    y0, y1 = y_points[idx], y_points[idx+1]
    
    print("-" * 60)
    print(f"Mencari nilai f({x_find})")
    print(f"Menggunakan titik data:")
    print(f"x0 = {x0:<10} => f(x0) = {y0}")
    print(f"x1 = {x1:<10} => f(x1) = {y1}")
    print("-" * 60)
    
    # 2. Hitung 'First Divided Difference' (b1 atau a1)
    # Rumus: b1 = (y1 - y0) / (x1 - x0)
    # Ini adalah kemiringan (slope) garis
    
    diff_y = y1 - y0
    diff_x = x1 - x0
    b1 = diff_y / diff_x
    
    # Konstanta b0 adalah y0
    b0 = y0
    
    # 3. Tampilkan Tabel Perhitungan (Seperti Excel)
    # Tabel: i, xi, f(xi), First
    print("\n--- STEP 1: TABEL SELISIH TERBAGI (DIVIDED DIFFERENCE) ---")
    data_table = {
        'i': [0, 1],
        'xi': [x0, x1],
        'f(xi)': [y0, y1],
        'First (b1)': [b1, ""] # Baris kedua kosong untuk b1 karena b1 terletak "di antara"
    }
    df = pd.DataFrame(data_table)
    print(df.to_string(index=False))
    
    # 4. Hitung Hasil Akhir
    # Rumus Newton Orde 1: f1(x) = b0 + b1 * (x - x0)
    y_result = b0 + b1 * (x_find - x0)
    
    # 5. Tampilkan Penjabaran Rumus (Seperti Kolom Kanan Excel)
    print("\n--- STEP 2: PERHITUNGAN DETAIL ---")
    print(f"Rumus: f1(x) = f(x0) + b1 * (x - x0)")
    print(f"             = {b0} + {b1:.6f} * ({x_find} - {x0})")
    
    # Hitung bagian dalam kurung dulu untuk visualisasi
    delta_x = x_find - x0
    term_b1 = b1 * delta_x
    
    print(f"             = {b0} + {b1:.6f} * ({delta_x})")
    print(f"             = {b0} + {term_b1:.6f}")
    print(f"             = {y_result:.6f}")
    
    print("-" * 60)
    print(f"HASIL AKHIR: f({x_find}) = {y_result:.6f}")
    print("-" * 60)

# ==============================================================================
# EKSEKUSI FUNGSI
# ==============================================================================
linear_interpolation_step_by_step(x_data, y_data, xf)