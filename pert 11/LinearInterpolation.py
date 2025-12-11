import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_b1(x0, y0, x1, y1):
    """
    Menghitung kemiringan (slope) atau b1.
    Rumus: (y1 - y0) / (x1 - x0)
    """
    if (x1 - x0) == 0:
        return None  # Menghindari pembagian dengan nol
    return (y1 - y0) / (x1 - x0)

def interpolasi_linear(x0, y0, x1, y1, x_find):
    """
    Menghitung nilai f(x_find) menggunakan rumus interpolasi linear.
    """
    # 1. Hitung Gradien (b1)
    b1 = hitung_b1(x0, y0, x1, y1)
    
    if b1 is None:
        return None, None, "Error: Nilai x0 dan x1 tidak boleh sama."
    
    # 2. Hitung hasil interpolasi
    # Rumus: f(x) = f(x0) + b1 * (x - x0)
    term_koreksi = b1 * (x_find - x0)
    hasil_y = y0 + term_koreksi
    
    return hasil_y, b1, term_koreksi

# --- BAGIAN 2: PROGRAM UTAMA (INPUT USER) ---
def main():
    print("Interpolasi Linear")
    print("Mencari nilai f(x) di antara dua titik.")
    print("-" * 45)

    try:
        # --- INPUT USER ---
        print("Masukkan Titik Pertama (i=0):")
        x0 = float(input("   x0: "))
        y0 = float(input("   f(x0): "))
        
        print("\nMasukkan Titik Kedua (i=1):")
        x1 = float(input("   x1: "))
        y1 = float(input("   f(x1): "))
        
        print("\nTitik yang dicari:")
        xf = float(input("   Cari f(x) untuk x = "))

        # --- PROSES HITUNG ---
        hasil, b1, koreksi = interpolasi_linear(x0, y0, x1, y1, xf)

        if hasil is None:
            print(f"\n[GAGAL] {koreksi}")
            return

        # --- OUTPUT TABEL DATA (Mirip Kiri Gambar) ---
        print("\n" + "="*45)
        print("Data yg diketahui:")
        print(f"{'i':<5} | {'xi':<10} | {'f(xi)':<10}")
        print("-" * 30)
        print(f"{'0':<5} | {x0:<10.4f} | {y0:<10.5f}")
        print(f"{'1':<5} | {x1:<10.4f} | {y1:<10.5f}")
        
        # --- OUTPUT HASIL PERHITUNGAN (Mirip Kanan Gambar) ---
        print("\n" + "="*45)
        print("Langkah Perhitungan:")
        print(f"1. Slope (b1) / First : {b1:.5f}")
        print(f"2. Rumus: f(x) = f(x0) + b1 * (xf - x0)")
        
        # Menampilkan substitusi angka agar mirip gambar
        # Contoh: f(xi) = 0 + 0.3584 * 1
        print(f"          f({xf}) = {y0} + {b1:.4f} * ({xf} - {x0})")
        print(f"          f({xf}) = {y0} + {b1:.4f} * {xf - x0}")
        
        print("-" * 45)
        print(f"Hasil Akhir f({xf}) = {hasil:.5f}")
        print("="*45)

    except ValueError:
        print("\nError: Masukkan angka yang valid.")

if __name__ == "__main__":
    main()