import sys

# --- BAGIAN 1: Fungsi Perhitungan ---
def hitung_slope(xa, ya, xb, yb):
    """
    Menghitung kemiringan antara dua titik (First Divided Difference).
    Rumus: (yb - ya) / (xb - xa)
    """
    if (xb - xa) == 0: return 0
    return (yb - ya) / (xb - xa)

def interpolasi_kuadratik(points, x_find):
    """
    Melakukan perhitungan interpolasi kuadratik Newton.
    points: List of tuples [(x0,y0), (x1,y1), (x2,y2)]
    """
    # Unpack titik-titik
    x0, y0 = points[0]
    x1, y1 = points[1]
    x2, y2 = points[2]

    # 1. Hitung b0
    b0 = y0

    # 2. Hitung Kolom "First" (First Divided Differences)
    # Slope antara titik 0 dan 1 (Ini adalah b1)
    diff_first_01 = hitung_slope(x0, y0, x1, y1)
    b1 = diff_first_01
    
    # Slope antara titik 1 dan 2 (Diperlukan untuk menghitung b2)
    diff_first_12 = hitung_slope(x1, y1, x2, y2)

    # 3. Hitung Kolom "Second" (Second Divided Difference)
    # Ini adalah b2
    # Rumus: (Slope_12 - Slope_01) / (x2 - x0)
    b2 = (diff_first_12 - diff_first_01) / (x2 - x0)

    # 4. Hitung Hasil Akhir f(x)
    # Rumus: b0 + b1*(x-x0) + b2*(x-x0)*(x-x1)
    term1 = b1 * (x_find - x0)
    term2 = b2 * (x_find - x0) * (x_find - x1)
    hasil_y = b0 + term1 + term2

    return {
        'hasil': hasil_y,
        'b0': b0,
        'b1': b1,
        'b2': b2,
        'diff_12': diff_first_12, # Slope kedua untuk tabel
        'term1': term1,
        'term2': term2
    }

# --- BAGIAN 2: PROGRAM UTAMA ---
def main():
    print("\n=== PROGRAM INTERPOLASI KUADRATIK (NEWTON) ===")
    print("Dibutuhkan 3 titik data untuk estimasi kurva.")
    print("-" * 50)

    try:
        points = []
        # --- INPUT USER ---
        # Loop untuk meminta input 3 titik (i=0, 1, 2)
        for i in range(3):
            print(f"Masukkan Titik ke-{i} (i={i}):")
            xi = float(input(f"   x{i}: "))
            yi = float(input(f"   f(x{i}): "))
            points.append((xi, yi))
        
        print("\nTitik yang dicari:")
        xf = float(input("   Cari f(x) untuk x = "))

        # --- PROSES HITUNG ---
        data = interpolasi_kuadratik(points, xf)
        
        x0, y0 = points[0]
        x1, y1 = points[1]
        x2, y2 = points[2]

        # --- OUTPUT TABEL (MIRIP GAMBAR EXCEL) ---
        print("\n" + "="*60)
        print("TABEL DIVIDED DIFFERENCE:")
        print(f"{'i':<3} | {'xi':<8} | {'f(xi)':<10} | {'First (b1)':<12} | {'Second (b2)':<12}")
        print("-" * 60)
        
        # Baris 0: Menampilkan b1 dan b2
        print(f"0   | {x0:<8.4f} | {y0:<10.5f} | {data['b1']:<12.5f} | {data['b2']:<12.5f}")
        
        # Baris 1: Menampilkan slope kedua (untuk perhitungan b2)
        print(f"1   | {x1:<8.4f} | {y1:<10.5f} | {data['diff_12']:<12.5f} | -")
        
        # Baris 2: Data saja
        print(f"2   | {x2:<8.4f} | {y2:<10.5f} | -            | -")

        # --- OUTPUT LANGKAH PERHITUNGAN ---
        print("\n" + "="*60)
        print("LANGKAH PERHITUNGAN FORMULA:")
        print(f"f(x) = b0 + b1*(x-x0) + b2*(x-x0)*(x-x1)")
        print("-" * 60)
        
        # Tampilkan substitusi angka (mirip sisi kanan gambar Excel Anda)
        print(f"f({xf}) = {data['b0']} + {data['b1']:.4f} * ({xf} - {x0}) + {data['b2']:.5f} * ({xf} - {x0}) * ({xf} - {x1})")
        
        # Tampilkan hasil perhitungan per bagian
        print(f"f({xf}) = {data['b0']} + {data['term1']:.4f} + ({data['term2']:.4f})")
        
        print("-" * 60)
        print(f"HASIL AKHIR f({xf}) = {data['hasil']:.4f}")
        print("="*60)

    except ValueError:
        print("\nError: Pastikan Anda memasukkan angka yang valid.")
    except ZeroDivisionError:
        print("\nError: Pembagian dengan nol. Pastikan nilai x tidak ada yang sama.")

if __name__ == "__main__":
    main()