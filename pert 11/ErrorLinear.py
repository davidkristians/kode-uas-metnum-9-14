import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_slope(xa, ya, xb, yb):
    """Menghitung First Divided Difference (b1)"""
    if (xb - xa) == 0: return 0
    return (yb - ya) / (xb - xa)

def hitung_estimasi_error(p0, p1, p_extra, x_find):
    """
    Menghitung estimasi error interpolasi linear.
    """
    x0, y0 = p0
    x1, y1 = p1
    xm, ym = p_extra # Titik tambahan (x_extra)

    # 1. Hitung Hasil Linear (Prediksi Awal)
    b1_linear = hitung_slope(x0, y0, x1, y1)
    f_linear = y0 + b1_linear * (x_find - x0)

    # 2. Hitung Koefisien b2 (untuk Error)
    # Slope tingkat 1
    slope_0_m = hitung_slope(x0, y0, xm, ym)
    slope_m_1 = hitung_slope(xm, ym, x1, y1)
    
    # Slope tingkat 2 (b2)
    b2 = (slope_m_1 - slope_0_m) / (x1 - x0)

    # 3. Hitung Estimasi Error (Nilai Absolut)
    # Rumus: R = b2 * (x - x0) * (x - x1)
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
    print("Estimation Error Linear")
    print("Membutuhkan 3 titik: Awal, Akhir, dan Tambahan (untuk cek kurva).")
    print("-" * 65)

    try:
        # --- INPUT USER ---
        print("1. Masukkan Titik Awal (x0):")
        x0 = float(input("   x0: "))
        y0 = float(input("   f(x0): "))

        print("\n2. Masukkan Titik Akhir Linear (x1):")
        x1 = float(input("   x1: "))
        y1 = float(input("   f(x1): "))

        print("\n3. Masukkan Titik Tambahan/Tengah (x_extra):")
        print("   (Diperlukan untuk menghitung kelengkungan/b2)")
        xm = float(input("   x_extra: "))
        ym = float(input("   f(x_extra): "))
        
        print("\n4. Titik yang dicari:")
        xf = float(input("   Cari error untuk x = "))

        # --- PROSES HITUNG ---
        p0 = (x0, y0)
        p1 = (x1, y1)
        pe = (xm, ym)
        
        res = hitung_estimasi_error(p0, p1, pe, xf)
        
        # Hitung Persentase (Sesuai gambar: Value * 100)
        error_percent = res['error_val'] * 100

        # --- OUTPUT HASIL ---
        print("\n" + "="*65)
        print("Hasil Perhitungan")
        print("-" * 65)
        
        # 1. Hasil Linear
        print(f"Hasil Interpolasi Linear (f1) : {res['linear_result']:.5f}")
        print("-" * 65)

        # 2. Tabel Kelengkungan (b2)
        print("Data Koefisien Error (b2):")
        print(f"{'xi':<8} | {'f(xi)':<10} | {'First':<10} | {'Second (b2)':<10}")
        print("-" * 50)
        print(f"{x0:<8.2f} | {y0:<10.6f} | {res['slope_0_m']:<10.6f} | {res['b2']:<10.6f}")
        print(f"{xm:<8.2f} | {ym:<10.6f} | {res['slope_m_1']:<10.6f} | -")
        print(f"{x1:<8.2f} | {y1:<10.6f} | -          | -")
        
        print("-" * 65)
        
        # 3. Langkah Perhitungan Error
        print("Rumus Estimasi Error:")
        print("Error = b2 * (xf - x0) * (xf - x1)")
        print(f"Error = {res['b2']:.5f} * ({xf} - {x0}) * ({xf} - {x1})")
        
        print("\n" + "="*65)
        print(f"Total Estimated Error      = {res['error_val']:.5f}")
        print(f"Presentase Estimated Error = {error_percent:.4f} %")
        print("="*65)

    except ValueError:
        print("\nError: Masukkan angka yang valid.")

if __name__ == "__main__":
    main()