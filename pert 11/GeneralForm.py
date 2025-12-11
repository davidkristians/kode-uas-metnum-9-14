import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def divided_difference_table(x_points, y_points):
    """
    Menghitung tabel Divided Difference untuk n titik.
    Mengembalikan matriks koefisien (tabel).
    """
    n = len(x_points)
    # Membuat matriks n x n diisi nol
    coef = [[0] * n for _ in range(n)]
    
    # Kolom pertama adalah nilai y (f(x))
    for i in range(n):
        coef[i][0] = y_points[i]
    
    # Menghitung kolom-kolom berikutnya (First, Second, Third, dst)
    for j in range(1, n):
        for i in range(n - j):
            # Rumus: (Next_Val - Curr_Val) / (x_jauh - x_dekat)
            numerator = coef[i+1][j-1] - coef[i][j-1]
            denominator = x_points[i+j] - x_points[i]
            coef[i][j] = numerator / denominator
            
    return coef

def newton_general_interpolation(x_points, y_points, x_find):
    """
    Menghitung nilai prediksi f(x) menggunakan koefisien diagonal tabel.
    """
    coef_table = divided_difference_table(x_points, y_points)
    n = len(x_points)
    
    # Ambil koefisien b0, b1, b2... (elemen diagonal atas: coef[0][0], coef[0][1]...)
    b = [coef_table[0][i] for i in range(n)]
    
    # Hitung nilai polinomial
    # Mulai dengan b0
    result = b[0]
    
    # Loop untuk menambah suku-suku berikutnya
    # term menyimpan nilai perkalian (x - x0)*(x - x1)...
    term_product = 1.0
    
    steps = [] # Untuk menyimpan detail langkah perhitungan
    steps.append(f"b0 = {b[0]}")
    
    for i in range(1, n):
        term_product *= (x_find - x_points[i-1])
        add_val = b[i] * term_product
        result += add_val
        steps.append(f"Term {i} (b{i} * product): {add_val:.6f}")
        
    return result, coef_table, b

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("General Form Interpolation")
    print("Mendukung N titik data (Linear, Kuadratik, Kubik, dst)")
    print("-" * 55)

    try:
        x_pts = []
        y_pts = []
        
        # --- INPUT USER ---
        n_titik = int(input("Masukkan jumlah titik data yang diketahui: "))
        
        for i in range(n_titik):
            print(f"\nMasukkan data titik (i={i}):")
            xi = float(input(f"   x{i}: "))
            yi = float(input(f"   f(x{i}): "))
            x_pts.append(xi)
            y_pts.append(yi)
            
        print("\nTitik yang dicari:")
        x_target = float(input("   Cari f(x) untuk x = "))

        # --- PROSES HITUNG ---
        hasil_akhir, tabel, koef_b = newton_general_interpolation(x_pts, y_pts, x_target)

        # --- OUTPUT TABEL (DINAMIS SESUAI JUMLAH TITIK) ---
        print("\n" + "="*80)
        print("Tabel Perbedaan:")
        
        # Header Tabel
        header = f"{'i':<3} | {'xi':<8} | {'f(xi)':<10}"
        col_names = ["First", "Second", "Third", "Fourth", "Fifth"]
        for i in range(n_titik - 1):
            name = col_names[i] if i < len(col_names) else f"Orde-{i+1}"
            header += f" | {name:<12}"
        print(header)
        print("-" * 80)
        
        # Isi Tabel
        for i in range(n_titik):
            row_str = f"{i:<3} | {x_pts[i]:<8.3f} | {y_pts[i]:<10.6f}"
            
            # Print kolom difference yang valid untuk baris ini
            for j in range(1, n_titik - i):
                val = tabel[i][j]
                row_str += f" | {val:<12.6f}"
            
            print(row_str)

        # --- OUTPUT LANGKAH PERHITUNGAN ---
        print("\n" + "="*80)
        print("Koefisien Polinomial (b):")
        for i, val in enumerate(koef_b):
            print(f"b{i} = {val:.6f}")
            
        print("-" * 80)
        print(f"Hasil Akhir f({x_target}) = {hasil_akhir:.5f}")
        print("="*80)

    except ValueError:
        print("\nError: Masukkan angka yang valid.")
    except ZeroDivisionError:
        print("\nError: Ada nilai x yang sama, menyebabkan pembagian nol.")

if __name__ == "__main__":
    main()