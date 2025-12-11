import sys

# --- BAGIAN 1: Definisi Fungsi Polinomial ---
def fungsi_f(x):
    """
    f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5
    Sama seperti yang tertera pada gambar.
    """
    return 0.2 + (25*x) - (200*x**2) + (675*x**3) - (900*x**4) + (400*x**5)

# --- BAGIAN 2: Proses Integrasi Simpson 3/8 ---
def integrasi_simpson_38(a, b, n):
    # Validasi: Simpson 3/8 wajib n kelipatan 3
    if n % 3 != 0:
        return None, None, "Error: Jumlah segmen (n) harus KELIPATAN 3 (misal: 3, 6, 9)."

    # 1. Hitung lebar segmen (h)
    h = (b - a) / n
    
    # 2. Hitung ujung awal dan akhir f(x0) + f(xn)
    f_awal = fungsi_f(a)
    f_akhir = fungsi_f(b)
    total_sum = f_awal + f_akhir
    
    # List untuk menyimpan data tabel
    data_tabel = []
    data_tabel.append((0, a, f_awal, 1)) # Format: (i, x, fx, koefisien)

    # 3. Loop untuk menghitung bagian tengah
    # Pola Simpson 3/8: 1 - 3 - 3 - 2 - 3 - 3 - 1
    # Artinya: Jika indeks habis dibagi 3, dikali 2. Sisanya dikali 3.
    
    for i in range(1, n):
        x = a + i * h
        fx = fungsi_f(x)
        
        # Penentuan Koefisien
        if i % 3 == 0:
            koefisien = 2
        else:
            koefisien = 3
            
        total_sum += koefisien * fx
        data_tabel.append((i, x, fx, koefisien))

    # Masukkan data baris terakhir (xn)
    data_tabel.append((n, b, f_akhir, 1))

    # 4. Hasil akhir dikali (3h / 8)
    integral = (3 * h / 8) * total_sum
    
    return integral, h, data_tabel

# --- BAGIAN 3: PROGRAM UTAMA (INPUT USER) ---
def main():
    print("\n=== PROGRAM INTEGRASI SIMPSON'S 3/8 RULE ===")
    print("f(x) = 0.2 + 25x - 200x^2 + 675x^3 - 900x^4 + 400x^5")
    print("-" * 55)

    try:
        # --- INPUT USER ---
        a = float(input("Masukkan batas bawah (a) : ")) # Gambar: 0
        b = float(input("Masukkan batas atas  (b) : ")) # Gambar: 0.8
        n = int(input("Masukkan jumlah segmen (n): ")) # Gambar: 3 (Wajib kelipatan 3)

        # Panggil fungsi perhitungan
        hasil, h, tabel = integrasi_simpson_38(a, b, n)

        # Cek Error
        if tabel is str: # Jika return berupa pesan error
            print(f"\n[GAGAL] {tabel}")
            return

        # --- OUTPUT HASIL UTAMA ---
        print("\n" + "="*55)
        print(f"Lebar segmen (h)      : {h:.6f}")
        print(f"HASIL INTEGRAL (I)    : {hasil:.6f}")
        print("="*55)

        # --- OUTPUT TABEL ---
        print("\n--- Tabel Langkah Perhitungan (Pola: 1-3-3-2...) ---")
        print(f"{'i':<5} | {'x':<10} | {'f(x)':<15} | {'Koef':<5} | {'Term (Koef*fx)':<15}")
        print("-" * 65)
        
        for baris in tabel:
            idx, x_val, fx_val, koef = baris
            term = koef * fx_val
            
            # Penanda khusus
            ket = ""
            if idx == 0: ket = " (Awal)"
            elif idx == n: ket = " (Akhir)"

            print(f"{idx:<5} | {x_val:<10.6f} | {fx_val:<15.6f} | {koef:<5} | {term:<15.6f}{ket}")

    except ValueError:
        print("\nError: Masukkan angka yang valid.")

if __name__ == "__main__":
    main()