import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_lagrange_linear(p0, p1, x_find):
    x0, y0 = p0
    x1, y1 = p1

    # Cek pembagian nol
    if (x0 - x1) == 0:
        return None, "Error: Nilai x0 dan x1 tidak boleh sama."

    # 1. Hitung Koefisien Lagrange (L0 dan L1)
    L0 = (x_find - x1) / (x0 - x1)
    L1 = (x_find - x0) / (x1 - x0)

    # 2. Hitung Hasil Akhir f(x)
    hasil_fx = (L0 * y0) + (L1 * y1)

    result_data = {
        'hasil': hasil_fx,
        'L0': L0,
        'L1': L1,
        'term0': L0 * y0,
        'term1': L1 * y1
    }
    
    # PERBAIKAN WAJIB:
    # Fungsi ini harus mengembalikan 2 hal (Data, Pesan Error)
    # supaya cocok dengan pemanggilan "data, msg = ..." di bawah
    return result_data, None

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("Linear Lagrange Interpolation")
    print("Mencari nilai f(x) menggunakan pembobotan koefisien (L).")
    print("-" * 60)

    try:
        # --- INPUT USER (TANPA REPLACE/STRIP) ---
        print("Masukkan Titik Pertama (i=0):")
        x0 = float(input("   x0: "))
        y0 = float(input("   f(x0): "))

        print("\nMasukkan Titik Kedua (i=1):")
        x1 = float(input("   x1: "))
        y1 = float(input("   f(x1): "))

        print("\nTitik yang dicari:")
        xf = float(input("   Cari f(x) untuk x = "))

        # --- PROSES HITUNG ---
        p0 = (x0, y0)
        p1 = (x1, y1)
        
        # Menerima 2 nilai dari fungsi
        data, msg = hitung_lagrange_linear(p0, p1, xf)
        
        if data is None:
            print(f"\n[GAGAL] {msg}")
            return

        # --- OUTPUT TABEL ---
        print("\n" + "="*50)
        print(f"{'i':<5} | {'xi':<10} | {'f(xi)':<10} | {'Coeff (Li)':<12}")
        print("-" * 50)
        
        print(f"{0:<5} | {x0:<10.1f} | {y0:<10.5f} | {data['L0']:<12.5f}")
        print(f"{1:<5} | {x1:<10.1f} | {y1:<10.5f} | {data['L1']:<12.5f}")
        
        print("-" * 50)

        # --- OUTPUT HASIL ---
        print("Langkah Perhitungan:")
        print("f(x) = L0 * f(x0) + L1 * f(x1)")
        print(f"f({xf}) = {data['L0']:.5f} * {y0} + {data['L1']:.5f} * {y1}")
        print(f"f({xf}) = {data['term0']:.5f} + {data['term1']:.5f}")
        
        print("\n" + "="*50)
        print(f"Hasil Akhir f({xf}) = {data['hasil']:.4f}")
        print("="*50)

    except ValueError:
        print("\nError: Pastikan Anda memasukkan angka yang valid (gunakan titik untuk desimal).")

if __name__ == "__main__":
    main()