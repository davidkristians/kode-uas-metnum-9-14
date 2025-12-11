import math

# --- KONFIGURASI PARAMETER FISIKA ---
g = 9.8
m = 68.1
c = 12.5

# --- BAGIAN 1: Definisi Fungsi Matematis ---
def fungsi_v(t):
    """
    Rumus: v(t) = (gm/c) * (1 - e^(-(c/m)t))
    """
    term1 = (g * m) / c
    try:
        term2 = 1 - math.exp(-(c / m) * t)
    except OverflowError:
        term2 = 1.0 
    return term1 * term2

# --- BAGIAN 2: Proses Integrasi ---
def integrasi_trapezoidal(a, b, n):
    # Hitung lebar segmen (h)
    h = (b - a) / n
    
    # Hitung ujung awal dan akhir
    f_awal = fungsi_v(a)
    f_akhir = fungsi_v(b)
    sum_result = f_awal + f_akhir
    
    # Siapkan list untuk menyimpan data tabel
    # Format data: (index, waktu_t, nilai_v)
    data_tabel = []
    data_tabel.append((0, a, f_awal)) 
    
    # Hitung segmen tengah
    for i in range(1, n):
        t = a + i * h
        val = fungsi_v(t)
        sum_result += 2 * val
        data_tabel.append((i, t, val))
        
    data_tabel.append((n, b, f_akhir))
    
    # Hitung hasil akhir Integral
    integral = (h / 2) * sum_result
    return integral, h, data_tabel

# --- BAGIAN 3: PROGRAM UTAMA ---
def main():
    print("\n=== PROGRAM INTEGRASI NUMERIK TRAPEZOIDAL ===")
    print(f"Parameter: g={g}, m={m}, c={c}")
    print("-" * 45)

    try:
        # --- INPUT USER ---
        t0 = float(input("Masukkan batas bawah (t0) : "))
        t1 = float(input("Masukkan batas atas  (t1) : "))
        n  = int(input("Masukkan jumlah segmen (n): "))

        if n <= 0:
            print("Error: Jumlah segmen (n) harus > 0.")
            return

        # --- PROSES PERHITUNGAN ---
        hasil_integral, lebar_h, tabel = integrasi_trapezoidal(t0, t1, n)

        # --- OUTPUT HASIL UTAMA ---
        print("\n" + "="*45)
        print(f"Lebar segmen (h)      : {lebar_h}")
        print(f"HASIL INTEGRAL (I)    : {hasil_integral:.4f}")
        print("="*45)

        # --- OUTPUT TABEL (LANGSUNG TAMPIL) ---
        print("\n--- Tabel Langkah Perhitungan ---")
        print(f"{'i (segmen)':<12} | {'t (waktu)':<12} | {'f(xi) / v(t)':<15}")
        print("-" * 45)
        
        # Loop untuk mencetak baris data
        for baris in tabel:
            idx, t_val, fx_val = baris
            # Penanda khusus untuk f(x0) dan f(xn) agar mirip excel Anda
            keterangan = ""
            if idx == 0: keterangan = "=> f(x0)"
            elif idx == n: keterangan = "=> f(xn)"
            
            print(f"{idx:<12} | {t_val:<12.4f} | {fx_val:<12.6f} {keterangan}")

    except ValueError:
        print("\nError: Pastikan Anda memasukkan angka yang benar.")

if __name__ == "__main__":
    main()