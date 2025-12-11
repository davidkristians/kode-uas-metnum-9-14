import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_lagrange_quadratic_split(points, x_find):
    """
    Menghitung Interpolasi Lagrange Orde 2 dengan memecah koefisien.
    """
    x0, y0 = points[0]
    x1, y1 = points[1]
    x2, y2 = points[2]

    # Cek pembagian nol
    if (x0 == x1) or (x0 == x2) or (x1 == x2):
        return None, "Error: Nilai x tidak boleh ada yang sama."

    # --- BARIS 0 (i=0) ---
    # L0 = [(x - x1)/(x0 - x1)] * [(x - x2)/(x0 - x2)]
    c0_1 = (x_find - x1) / (x0 - x1)  # Coeff 1
    c0_2 = (x_find - x2) / (x0 - x2)  # Coeff 2
    term0 = c0_1 * c0_2 * y0

    # --- BARIS 1 (i=1) ---
    # L1 = [(x - x0)/(x1 - x0)] * [(x - x2)/(x1 - x2)]
    c1_1 = (x_find - x0) / (x1 - x0)  # Coeff 1
    c1_2 = (x_find - x2) / (x1 - x2)  # Coeff 2
    term1 = c1_1 * c1_2 * y1

    # --- BARIS 2 (i=2) ---
    # L2 = [(x - x0)/(x2 - x0)] * [(x - x1)/(x2 - x1)]
    c2_1 = (x_find - x0) / (x2 - x0)  # Coeff 1
    c2_2 = (x_find - x1) / (x2 - x1)  # Coeff 2
    term2 = c2_1 * c2_2 * y2

    # Total Hasil
    hasil_fx = term0 + term1 + term2

    # Simpan semua detail untuk tabel
    result_data = {
        'hasil': hasil_fx,
        'coeff_1': [c0_1, c1_1, c2_1],
        'coeff_2': [c0_2, c1_2, c2_2],
        'points': points
    }
    
    return result_data, None

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("\n=== PROGRAM INTERPOLASI LAGRANGE (KUADRATIK) ===")
    print("Menampilkan Coeff 1 dan Coeff 2 secara terpisah.")
    print("-" * 75)

    try:
        points = []
        # --- INPUT USER ---
        print("Masukkan Titik ke-0:")
        x0 = float(input("   x0: "))
        y0 = float(input("   f(x0): "))
        points.append((x0, y0))

        print("\nMasukkan Titik ke-1:")
        x1 = float(input("   x1: "))
        y1 = float(input("   f(x1): "))
        points.append((x1, y1))

        print("\nMasukkan Titik ke-2:")
        x2 = float(input("   x2: "))
        y2 = float(input("   f(x2): "))
        points.append((x2, y2))

        print("\nTitik yang dicari:")
        xf = float(input("   Cari f(x) untuk x = "))

        # --- PROSES HITUNG ---
        data, msg = hitung_lagrange_quadratic_split(points, xf)

        if data is None:
            print(f"\n[GAGAL] {msg}")
            return

        # --- OUTPUT TABEL ---
        print("\n" + "="*75)
        # Header Tabel
        print(f"{'i':<4} | {'xi':<8} | {'f(xi)':<10} | {'Coeff 1':<10} | {'Coeff 2':<10}")
        print("-" * 75)
        
        c1_list = data['coeff_1']
        c2_list = data['coeff_2']
        pts = data['points']
        
        for i in range(3):
            xi, yi = pts[i]
            val_c1 = c1_list[i]
            val_c2 = c2_list[i]
            
            # Format angka agar rapi
            print(f"{i:<4} | {xi:<8.1f} | {yi:<10.6f} | {val_c1:<10.6f} | {val_c2:<10.5f}")
            
        print("-" * 75)

        # --- OUTPUT LANGKAH PERHITUNGAN ---
        print("LANGKAH PERHITUNGAN FORMULA:")
        print("f(x) = (c1*c2 * f0) + (c1*c2 * f1) + (c1*c2 * f2)")
        print("-" * 75)
        
        # Mengambil nilai untuk ditampilkan dalam rumus panjang
        y0, y1, y2 = pts[0][1], pts[1][1], pts[2][1]
        
        # Baris Substitusi (Panjang)
        # Format: C1 * C2 * f(x)
        print(f"f({xf}) = {c1_list[0]:.4f} * {c2_list[0]:.4f} * {y0}  +")
        print(f"         {c1_list[1]:.4f} * {c2_list[1]:.4f} * {y1}  +")
        print(f"         {c1_list[2]:.4f} * {c2_list[2]:.4f} * {y2}")

        print("\n" + "="*75)
        print(f"HASIL AKHIR f({xf}) = {data['hasil']:.4f}")
        print("="*75)

    except ValueError:
        print("\nError: Pastikan Anda memasukkan angka yang valid.")

if __name__ == "__main__":
    main()