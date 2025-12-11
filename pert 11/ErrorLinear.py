import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_slope(xa, ya, xb, yb):
    """Menghitung First Divided Difference (b1)"""
    if (xb - xa) == 0: return 0
    return (yb - ya) / (xb - xa)

def hitung_estimasi_error(p0, p1, p_extra, x_find):
    """
    Menghitung estimasi error interpolasi linear.
    p0      : Tuple (x0, y0) -> Titik awal
    p1      : Tuple (x1, y1) -> Titik akhir (pasangan linear p0)
    p_extra : Tuple (xm, ym) -> Titik tambahan untuk cek kurva
    x_find  : Nilai x yang dicari
    """
    x0, y0 = p0
    x1, y1 = p1
    xm, ym = p_extra # Titik tengah/tambahan (x=4 di gambar)

    # 1. Hitung Hasil Linear (Prediksi Awal)
    b1_linear = hitung_slope(x0, y0, x1, y1)
    f_linear = y0 + b1_linear * (x_find - x0)

    # 2. Hitung Koefisien b2 (Second Divided Difference)
    # Kita butuh slope (0 ke Extra) dan (Extra ke 1)
    # Urutan data untuk tabel: x0 -> xm -> x1
    
    # Slope tingkat 1
    slope_0_m = hitung_slope(x0, y0, xm, ym)
    slope_m_1 = hitung_slope(xm, ym, x1, y1)
    
    # Slope tingkat 2 (b2)
    # Rumus: (Slope_Bawah - Slope_Atas) / (x_Bawah - x_Atas)
    # Di sini x_Bawah adalah x1, x_Atas adalah x0
    b2 = (slope_m_1 - slope_0_m) / (x1 - x0)

    # 3. Hitung Estimasi Error
    # Rumus: R = b2 * (x - x0) * (x - x1)
    # Perhatikan: dikali (x - x1) karena x1 adalah ujung segmen linear
    term_error = b2 * (x_find - x0) * (x_find - x1)

    return {
        'linear_result': f_linear,
        'b1_linear': b1_linear,
        'b2': b2,
        'error_val': term_error,
        'slope_0_m': slope_0_m,
        'slope_m_1': slope_m_1
    }

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("\n=== PROGRAM ESTIMASI ERROR INTERPOLASI LINEAR ===")
    print("Membutuhkan 2 titik untuk Linear, dan 1 titik tambahan untuk cek Error.")
    print("-" * 65)

    try:
        # --- INPUT USER ---
        print("1. Masukkan Titik Awal (x0):")
        x0 = float(input("   x0: "))
        y0 = float(input("   f(x0): "))

        print("\n2. Masukkan Titik Akhir Linear (x1):")
        x1 = float(input("   x1: "))
        y1 = float(input("   f(x1): "))

        print("\n3. Masukkan Titik Tambahan/Tengah (x_extra) untuk hitung b2:")
        xm = float(input("   x_extra: "))
        ym = float(input("   f(x_extra): "))
        
        print("\n4. Titik yang dicari:")
        xf = float(input("   Cari error untuk x = "))

        # --- PROSES HITUNG ---
        # Mengemas titik menjadi tuple
        p0 = (x0, y0)
        p1 = (x1, y1)
        pe = (xm, ym)
        
        res = hitung_estimasi_error(p0, p1, pe, xf)

        # --- OUTPUT HASIL ---
        print("\n" + "="*65)
        print("HASIL PERHITUNGAN")
        print("-" * 65)
        
        # 1. Hasil Linear
        print(f"Hasil Interpolasi Linear (f1): {res['linear_result']:.4f}")
        print(f"(Menggunakan slope b1: {res['b1_linear']:.6f})")
        print("-" * 65)

        # 2. Tabel Kelengkungan (b2)
        print("Data untuk Estimasi Error (b2):")
        print(f"{'xi':<8} | {'f(xi)':<10} | {'First':<10} | {'Second (b2)':<10}")
        print("-" * 50)
        # Baris 0
        print(f"{x0:<8.4f} | {y0:<10.5f} | {res['slope_0_m']:<10.5f} | {res['b2']:<10.5f}")
        # Baris Extra
        print(f"{xm:<8.4f} | {ym:<10.5f} | {res['slope_m_1']:<10.5f} | -")
        # Baris 1
        print(f"{x1:<8.4f} | {y1:<10.5f} | -          | -")
        
        print("-" * 65)
        
        # 3. Langkah Perhitungan Error (Sesuai Gambar)
        term_1 = xf - x0
        term_2 = xf - x1
        
        print("RUMUS ERROR:")
        print("Estimated Error = b2 * (xf - x0) * (xf - x1)")
        print(f"Estimated Error = {res['b2']:.5f} * ({xf} - {x0}) * ({xf} - {x1})")
        print(f"Estimated Error = {res['b2']:.5f} * {term_1} * {term_2}")
        
        print("\n" + "="*65)
        print(f"TOTAL ESTIMATED ERROR = {res['error_val']:.4f}")
        print("="*65)

    except ValueError:
        print("\nError: Masukkan angka yang valid.")

if __name__ == "__main__":
    main()