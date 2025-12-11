import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_tabel_newton(points):
    """
    Menghitung tabel Divided Difference untuk N titik.
    points: list of tuples [(x, y), ...]
    """
    n = len(points)
    # Buat matriks n x n
    coef = [[0] * n for _ in range(n)]
    
    # Isi kolom pertama dengan y
    for i in range(n):
        coef[i][0] = points[i][1]
    
    # Hitung kolom selanjutnya
    for j in range(1, n):
        for i in range(n - j):
            # Rumus: (Next - Curr) / (x_jauh - x_dekat)
            numerator = coef[i+1][j-1] - coef[i][j-1]
            denominator = points[i+j][0] - points[i][0]
            coef[i][j] = numerator / denominator
            
    return coef

def hitung_ekstrapolasi(points, x_find):
    """
    Menghitung nilai f(x) menggunakan koefisien diagonal tabel Newton.
    """
    n = len(points)
    coef_table = hitung_tabel_newton(points)
    
    # Ambil koefisien diagonal atas (b0, b1, b2, dst)
    b = [coef_table[0][i] for i in range(n)]
    
    # Hitung nilai polinomial
    # f(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + ...
    
    hasil_akhir = b[0]
    detail_terms = [] # Untuk menyimpan nilai per suku (b0, b1*.., b2*..)
    detail_terms.append(b[0])
    
    term_product = 1.0
    for i in range(1, n):
        term_product *= (x_find - points[i-1][0])
        nilai_suku = b[i] * term_product
        hasil_akhir += nilai_suku
        detail_terms.append(nilai_suku)
        
    return {
        'hasil': hasil_akhir,
        'b': b,
        'tabel': coef_table,
        'terms': detail_terms
    }, None

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("Ekstrapolasi (Newton Polynomial)")
    print("Mencari nilai f(x) di luar rentang data yang diketahui.")
    print("-" * 55)

    try:
        # --- INPUT USER ---
        # Sesuai gambar, kita butuh input dinamis (bisa 4 titik atau lebih)
        n = int(input("Masukkan jumlah titik data (n): "))
        
        points = []
        print("\nMasukkan data titik secara berurutan:")
        for i in range(n):
            print(f"Titik ke-{i}:")
            xi = float(input(f"   x{i}: "))
            yi = float(input(f"   f(x{i}): "))
            points.append((xi, yi))
            
        print("\nTitik yang dicari (Ekstrapolasi):")
        xf = float(input("   Cari f(x) untuk x = "))

        # --- PROSES HITUNG ---
        data, msg = hitung_ekstrapolasi(points, xf)
        
        if data is None:
            print(f"\n[GAGAL] {msg}")
            return

        # --- OUTPUT TABEL ---
        print("\n" + "="*55)
        print("Tabel Perbedaan:")
        # Header dinamis
        header = f"{'i':<3} | {'xi':<6} | {'f(xi)':<10}"
        col_names = ["First", "Second", "Third", "Fourth", "Fifth"]
        for i in range(n - 1):
            c_name = col_names[i] if i < len(col_names) else f"Orde-{i+1}"
            header += f" | {c_name:<10}"
        print(header)
        print("-" * 55)
        
        # Isi Tabel
        tbl = data['tabel']
        for i in range(n):
            row_str = f"{i:<3} | {points[i][0]:<6.4g} | {points[i][1]:<10.5g}"
            for j in range(1, n - i):
                row_str += f" | {tbl[i][j]:<10.5g}"
            print(row_str)
            
        print("-" * 55)

        # --- OUTPUT LANGKAH PERHITUNGAN (Format Mirip Gambar) ---
        print("Langkah Perhitungan:")
        print("f(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + b3(x-x0)(x-x1)(x-x2) ...")
        print("-" * 55)
        
        b = data['b']
        x = [p[0] for p in points]
        
        # Tampilkan substitusi angka
        # f(xf) = 2.718 + 3.526 * (3-1) + ...
        rumus_str = f"f({xf}) = {b[0]:.4g}"
        for i in range(1, n):
            # Tanda tambah/kurang otomatis
            tanda = " + " if b[i] >= 0 else " - "
            rumus_str += f"{tanda}{abs(b[i]):.4g}"
            
            # Tambahkan (x - xi)
            for j in range(i):
                rumus_str += f" * ({xf - x[j]:.4g})"
        
        print(rumus_str)
        
        # Tampilkan hasil penjumlahan per suku (agar mirip proses manual)
        # Contoh: f(x) = 2.718 + 7.052 + 6.87 + ...
        terms_str = f"f({xf}) = " + " + ".join([f"{t:.4g}" for t in data['terms']])
        print(terms_str)
        
        print("\n" + "="*55)
        print(f"HASIL AKHIR f({xf}) = {data['hasil']:.5g}")
        print("="*55)

    except ValueError:
        print("\nError: Pastikan Anda memasukkan angka yang valid (gunakan titik untuk desimal).")

if __name__ == "__main__":
    main()