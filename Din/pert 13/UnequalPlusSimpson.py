import sys

# --- BAGIAN 1: Definisi Fungsi Polinomial ---
def fungsi_f(x):
    """
    f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    """
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# --- BAGIAN 2: Algoritma Mixed Integration ---
def integrasi_campuran(x_points):
    n = len(x_points)
    total_integral = 0
    data_tabel = []
    
    # Toleransi perbedaan float (karena komputer kadang 0.1 != 0.100000001)
    epsilon = 1e-9 
    
    i = 0
    while i < n - 1:
        # Hitung jarak segmen saat ini dan segmen-segmen berikutnya (jika ada)
        h1 = x_points[i+1] - x_points[i]
        
        h2 = 0
        if i + 2 < n:
            h2 = x_points[i+2] - x_points[i+1]
            
        h3 = 0
        if i + 3 < n:
            h3 = x_points[i+3] - x_points[i+2]

        # --- CEK 1: Apakah bisa pakai Simpson 3/8? (Butuh 3 segmen h sama) ---
        if (i + 3 < n) and (abs(h1 - h2) < epsilon) and (abs(h2 - h3) < epsilon):
            # Rumus Simpson 3/8: (3h/8) * (f0 + 3f1 + 3f2 + f3)
            f0 = fungsi_f(x_points[i])
            f1 = fungsi_f(x_points[i+1])
            f2 = fungsi_f(x_points[i+2])
            f3 = fungsi_f(x_points[i+3])
            
            luas = (3 * h1 / 8) * (f0 + 3*f1 + 3*f2 + f3)
            metode = "3/8 Simpson"
            
            # Simpan data & Loncat 3 langkah
            data_tabel.append((x_points[i], f0, luas, metode))
            # Tambahkan baris kosong untuk titik tengah agar rapi di tabel
            data_tabel.append((x_points[i+1], f1, "", ""))
            data_tabel.append((x_points[i+2], f2, "", ""))
            
            total_integral += luas
            i += 3
            
        # --- CEK 2: Apakah bisa pakai Simpson 1/3? (Butuh 2 segmen h sama) ---
        elif (i + 2 < n) and (abs(h1 - h2) < epsilon):
            # Rumus Simpson 1/3: (h/3) * (f0 + 4f1 + f2)
            f0 = fungsi_f(x_points[i])
            f1 = fungsi_f(x_points[i+1])
            f2 = fungsi_f(x_points[i+2])
            
            luas = (h1 / 3) * (f0 + 4*f1 + f2)
            metode = "1/3 Simpson"
            
            # Simpan data & Loncat 2 langkah
            data_tabel.append((x_points[i], f0, luas, metode))
            data_tabel.append((x_points[i+1], f1, "", ""))
            
            total_integral += luas
            i += 2
            
        # --- OPSI TERAKHIR: Pakai Trapezoidal (1 segmen) ---
        else:
            # Rumus Trapz: (h/2) * (f0 + f1)
            f0 = fungsi_f(x_points[i])
            f1 = fungsi_f(x_points[i+1])
            
            luas = (h1 / 2) * (f0 + f1)
            metode = "Trapz"
            
            # Simpan data & Loncat 1 langkah
            data_tabel.append((x_points[i], f0, luas, metode))
            
            total_integral += luas
            i += 1

    # Tambahkan titik paling terakhir ke tabel
    data_tabel.append((x_points[-1], fungsi_f(x_points[-1]), "", ""))
    
    return total_integral, data_tabel

# --- BAGIAN 3: PROGRAM UTAMA ---
def main():
    print("\n=== PROGRAM INTEGRASI CAMPURAN (UNEQUAL + SIMPSON) ===")
    print("Mendeteksi otomatis: Simpson 3/8 -> Simpson 1/3 -> Trapezoidal")
    print("-" * 65)

    try:
        # --- INPUT USER ---
        print("Silakan masukkan deret x (pisahkan dengan koma).")
        print("-" * 65)
        
        input_str = input("Masukkan nilai x: ")
        
        # Konversi string ke list float dan urutkan
        x_points = sorted([float(x) for x in input_str.split(',')])

        if len(x_points) < 2:
            print("Error: Butuh minimal 2 titik.")
            return

        # --- PROSES HITUNG ---
        hasil, tabel = integrasi_campuran(x_points)

        # --- OUTPUT HASIL ---
        print("\n" + "="*65)
        print(f"HASIL INTEGRAL (I) : {hasil:.6f}")
        print("="*65)

        # --- OUTPUT TABEL ---
        print("\n--- Detail Perhitungan ---")
        print(f"{'x':<8} | {'f(x)':<12} | {'Luas Segmen':<15} | {'Metode Digunakan':<15}")
        print("-" * 65)
        
        for baris in tabel:
            x_val, fx_val, luas, metode = baris
            
            # Formatting agar rapi (jika luas kosong/string kosong)
            if luas != "":
                luas_str = f"{luas:.6f}"
            else:
                luas_str = ""
                
            print(f"{x_val:<8.3f} | {fx_val:<12.5f} | {luas_str:<15} | {metode:<15}")

    except ValueError:
        print("\nError: Format input salah.")

if __name__ == "__main__":
    main()