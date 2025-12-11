import sys

# --- BAGIAN 1: Definisi Fungsi Polinomial ---
def fungsi_f(x):
    """
    f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    """
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# --- BAGIAN 2: Proses Integrasi Simpson 1/3 ---
def integrasi_simpson(a, b, n):
    # Validasi: Simpson 1/3 wajib n genap
    if n % 2 != 0:
        return None, None, "Error: Jumlah segmen (n) harus GENAP untuk Simpson 1/3."

    # 1. Hitung lebar segmen (h)
    h = (b - a) / n
    
    # 2. Hitung ujung awal dan akhir f(x0) + f(xn)
    f_awal = fungsi_f(a)
    f_akhir = fungsi_f(b)
    total_sum = f_awal + f_akhir
    
    # List untuk menyimpan data tabel
    data_tabel = []
    # Masukkan data baris pertama (x0)
    data_tabel.append((0, a, f_awal, 1)) # Format: (i, x, fx, koefisien)

    # 3. Loop untuk menghitung bagian tengah
    # Rumus: 4 * (jumlah ganjil) + 2 * (jumlah genap)
    
    for i in range(1, n):
        x = a + i * h
        fx = fungsi_f(x)
        
        # Tentukan koefisien pengali (4 untuk ganjil, 2 untuk genap)
        if i % 2 != 0:
            koefisien = 4
        else:
            koefisien = 2
            
        total_sum += koefisien * fx
        data_tabel.append((i, x, fx, koefisien))

    # Masukkan data baris terakhir (xn)
    data_tabel.append((n, b, f_akhir, 1))

    # 4. Hasil akhir dikali (h/3)
    integral = (h / 3) * total_sum
    
    return integral, h, data_tabel

# --- BAGIAN 3: PROGRAM UTAMA (INPUT USER) ---
def main():
    print("\n=== PROGRAM INTEGRASI SIMPSON'S 1/3 RULE ===")
    print("f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5")
    print("-" * 50)

    try:
        # --- INPUT USER ---
        a = float(input("Masukkan batas bawah (a) : ")) # Sesuai gambar: 0
        b = float(input("Masukkan batas atas  (b) : ")) # Sesuai gambar: 0.8
        n = int(input("Masukkan jumlah segmen (n): ")) # Harus Genap, misal: 4

        # Panggil fungsi perhitungan
        hasil, h, tabel = integrasi_simpson(a, b, n)

        # Cek jika ada error (karena ganjil)
        if tabel is str: # Jika kembalian berupa pesan error
            print(f"\n[GAGAL] {tabel}")
            return

        # --- OUTPUT HASIL UTAMA ---
        print("\n" + "="*50)
        print(f"Lebar segmen (h)      : {h}")
        print(f"HASIL INTEGRAL (I)    : {hasil:.6f}")
        print("="*50)

        # --- OUTPUT TABEL ---
        # Menampilkan tabel dengan kolom Koefisien agar jelas mana dikali 4 atau 2
        print("\n--- Tabel Langkah Perhitungan ---")
        print(f"{'i':<5} | {'x':<10} | {'f(x)':<15} | {'Koef':<5} | {'Term (Koef*fx)':<15}")
        print("-" * 60)
        
        for baris in tabel:
            idx, x_val, fx_val, koef = baris
            term = koef * fx_val
            
            # Penanda khusus
            ket = ""
            if idx == 0: ket = " (Awal)"
            elif idx == n: ket = " (Akhir)"

            print(f"{idx:<5} | {x_val:<10.1f} | {fx_val:<15.3f} | {koef:<5} | {term:<15.4f}{ket}")

    except ValueError:
        print("\nError: Masukkan angka yang valid.")

if __name__ == "__main__":
    main()