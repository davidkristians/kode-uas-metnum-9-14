import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_tabel_diff(points):
    """
    Menghitung tabel divided difference untuk N titik.
    points: list of tuples [(x, y), ...]
    Mengembalikan tabel lengkap (matriks).
    """
    n = len(points)
    # Buat matriks n x n
    tabel = [[0] * n for _ in range(n)]
    
    # Isi kolom 0 dengan nilai f(x) / y
    for i in range(n):
        tabel[i][0] = points[i][1]
        
    # Hitung kolom selanjutnya (First, Second, Third...)
    for j in range(1, n):
        for i in range(n - j):
            numerator = tabel[i+1][j-1] - tabel[i][j-1]
            denominator = points[i+j][0] - points[i][0]
            tabel[i][j] = numerator / denominator
            
    return tabel

def hitung_error_kuadratik(base_points, extra_point, x_find):
    """
    base_points : 3 titik utama [(x0,y0), (x1,y1), (x2,y2)]
    extra_point : 1 titik tambahan (x3, y3)
    """
    # 1. Gabungkan semua titik untuk membuat Tabel Difference
    # Sesuai gambar, titik-titik diurutkan berdasarkan nilai x (1, 4, 5, 6)
    all_points = base_points + [extra_point]
    all_points.sort(key=lambda p: p[0]) # Urutkan agar tabel rapi seperti gambar
    
    # 2. Hitung Tabel untuk mendapatkan b3 (Third Difference)
    tabel = hitung_tabel_diff(all_points)
    
    # Ambil koefisien b3 (First element of the 4th column/index 3)
    # Pada tabel Newton diagonal atas, ini adalah coef[0][3]
    b3 = tabel[0][3]
    
    # 3. Hitung Nilai Error
    # Rumus: b3 * (x - x0) * (x - x1) * (x - x2)
    # x0, x1, x2 diambil dari base_points (titik pembentuk kuadratik)
    x0 = base_points[0][0]
    x1 = base_points[1][0]
    x2 = base_points[2][0]
    
    term1 = x_find - x0
    term2 = x_find - x1
    term3 = x_find - x2
    
    error_val = b3 * term1 * term2 * term3
    
    return {
        'b3': b3,
        'error_val': error_val,
        'tabel': tabel,
        'all_points': all_points,
        'terms': (term1, term2, term3)
    }

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("Error Estimation Quadratic")
    print("Membutuhkan 3 titik utama + 1 titik tambahan.")
    print("-" * 60)

    try:
        base_points = []
        # --- INPUT USER ---
        print("Masukkan 3 Titik Utama (Untuk Interpolasi)")
        for i in range(3):
            xi = float(input(f"   x{i}: "))
            yi = float(input(f"   f(x{i}): "))
            base_points.append((xi, yi))
            
        print("\nMasukkan 1 Titik Tambahan (Untuk Cek Error)")
        xe = float(input("   x_extra: "))
        ye = float(input("   f(x_extra): "))
        extra_point = (xe, ye)
        
        print("\nTitik yang dicari")
        xf = float(input("   Cari error untuk x = "))

        # --- PROSES HITUNG ---
        res = hitung_error_kuadratik(base_points, extra_point, xf)
        
        # Hitung Persen (Nilai error * 100)
        persen = res['error_val'] * 100

        # --- OUTPUT TABEL ---
        print("\n" + "="*75)
        print("Tabel Perbedaan (Termasuk Titik Extra):")
        print(f"{'i':<3} | {'xi':<8} | {'f(xi)':<10} | {'First':<10} | {'Second':<10} | {'Third (b3)':<10}")
        print("-" * 75)
        
        # Menampilkan tabel
        pts = res['all_points']
        tbl = res['tabel']
        n = len(pts)
        
        for i in range(n):
            row_str = f"{i:<3} | {pts[i][0]:<8.4f} | {pts[i][1]:<10.5f}"
            
            # Loop kolom difference
            for j in range(1, n - i):
                val = tbl[i][j]
                row_str += f" | {val:<10.5f}"
            
            print(row_str)

        # --- OUTPUT PERHITUNGAN ERROR ---
        print("\n" + "="*75)
        print("Langkah Perhitungan Error:")
        print(f"Koefisien b3 (Third Diff) = {res['b3']:.6f}")
        print("-" * 75)
        
        # Menampilkan Rumus Substitusi (Mirip Gambar)
        t1, t2, t3 = res['terms']
        x0 = base_points[0][0]
        x1 = base_points[1][0]
        x2 = base_points[2][0]

        print("Rumus: Error = b3 * (xf - x0) * (xf - x1) * (xf - x2)")
        print(f"Error = {res['b3']:.5f} * ({xf} - {x0}) * ({xf} - {x1}) * ({xf} - {x2})")
        print(f"Error = {res['b3']:.5f} * {t1} * {t2} * {t3}")
        
        print("-" * 75)
        print(f"Total Estimated Error       = {res['error_val']:.5f}")
        print(f"Presentase Estimated Error  = {persen:.4f} %")
        print("="*75)

    except ValueError:
        print("\nError: Pastikan Anda memasukkan angka yang valid.")

if __name__ == "__main__":
    main()