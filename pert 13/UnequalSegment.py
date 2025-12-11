import sys

# --- BAGIAN 1: Definisi Fungsi Polinomial ---
def fungsi_f(x):
    """
    f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    """
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# --- BAGIAN 2: Proses Integrasi Segmen Tidak Sama ---
def integrasi_unequal(points_x):
    """
    Menghitung integral dengan menjumlahkan luas trapesium
    untuk setiap segmen yang lebarnya berbeda.
    """
    total_integral = 0
    data_tabel = [] # Menyimpan detail per langkah

    # Kita loop dari titik pertama sampai titik sebelum terakhir
    # Karena setiap segmen dibentuk oleh titik i dan i+1
    for i in range(len(points_x) - 1):
        x1 = points_x[i]
        x2 = points_x[i+1]
        
        # Hitung lebar segmen ini (h bisa berubah-ubah)
        h = x2 - x1
        
        # Hitung nilai fungsi di kedua ujung segmen
        fx1 = fungsi_f(x1)
        fx2 = fungsi_f(x2)
        
        # Rumus Luas Trapesium: h * (f(x1) + f(x2)) / 2
        luas_segmen = h * (fx1 + fx2) / 2
        
        total_integral += luas_segmen
        
        # Simpan data untuk tabel (x, f(x), dan Luas yang disumbangkan)
        # Kita simpan fx1 di sini agar sesuai tampilan baris Excel
        data_tabel.append((x1, fx1, luas_segmen))

    # Tambahkan baris terakhir (titik ujung) yang tidak memiliki luas segmen ke depan
    last_x = points_x[-1]
    data_tabel.append((last_x, fungsi_f(last_x), 0.0))
    
    return total_integral, data_tabel

# --- BAGIAN 3: PROGRAM UTAMA (INPUT USER) ---
def main():
    print("\n=== PROGRAM INTEGRASI NUMERIK (UNEQUAL SEGMENTS) ===")
    print("f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5")
    print("-" * 60)
    print("Input deret nilai x secara manual (pisahkan dengan koma)")
    print("-" * 60)

    try:
        # --- INPUT USER ---
        input_str = input("Masukkan deret nilai x: ")
        
        # Mengubah string "0, 0.12, ..." menjadi list float [0.0, 0.12, ...]
        # dan mengurutkannya (sorted) agar segmen berurutan
        points_x = sorted([float(x) for x in input_str.split(',')])

        # Validasi minimal 2 titik
        if len(points_x) < 2:
            print("Error: Minimal harus ada 2 titik x untuk membuat 1 segmen.")
            return

        # Panggil fungsi perhitungan
        hasil_total, tabel = integrasi_unequal(points_x)

        # --- OUTPUT HASIL UTAMA ---
        print("\n" + "="*60)
        print(f"Total Panjang Data (n) : {len(points_x)} titik")
        print(f"HASIL INTEGRAL (I)     : {hasil_total:.5f}")
        print("="*60)

        # --- OUTPUT TABEL (MIRIP GAMBAR EXCEL) ---
        print("\n--- Tabel Perhitungan Per Segmen ---")
        print(f"{'x':<10} | {'f(x)':<15} | {'Ii (Luas Segmen)':<15}")
        print("-" * 50)
        
        for baris in tabel:
            x_val, fx_val, area = baris
            
            # Jika area 0 (baris terakhir), kosongkan tampilannya agar rapi
            str_area = f"{area:.5f}" if area != 0 else "-"
            
            print(f"{x_val:<10.3f} | {fx_val:<15.5f} | {str_area:<15}")

    except ValueError:
        print("\nError: Format input salah. Pastikan hanya memasukkan angka dan koma.")

if __name__ == "__main__":
    main()