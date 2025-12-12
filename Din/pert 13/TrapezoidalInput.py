import numpy as np
import pandas as pd
import math

# =========================================================================
# 1. PARAMETER FISIKA (SESUAI EXCEL)
# =========================================================================
g = 9.8
m = 68.1
c = 12.5

# Fungsi v(t) - Kecepatan
def v(t):
    term1 = (g * m) / c
    # Mencegah overflow untuk t sangat besar (opsional)
    try:
        term2 = 1 - math.exp(-(c / m) * t)
    except OverflowError:
        term2 = 1.0
    return term1 * term2

# =========================================================================
# 2. ALGORITMA TRAPEZOIDAL (FUNGSI UMUM)
# =========================================================================
def hitung_trapezoidal(t0, t1, n):
    """
    Menghitung Integral Trapesium Gabungan.
    Mengembalikan: (integral, h, dataframe_tabel)
    """
    h = (t1 - t0) / n
    
    # List untuk menyimpan data per baris
    data = []
    
    sum_fx = 0.0
    
    # Loop dari i=0 sampai n
    for i in range(n + 1):
        t_val = t0 + i * h
        fx = v(t_val)
        
        # Tentukan koefisien bobot (1 untuk ujung, 2 untuk tengah)
        weight = 1 if (i == 0 or i == n) else 2
        
        term = weight * fx
        sum_fx += term
        
        # Tambahkan ke data tabel
        note = "=> f(x0)" if i == 0 else ("=> f(xn)" if i == n else "")
        data.append({
            'i': i,
            't': t_val,
            'f(xi)': fx,
            'Weight': weight,
            'Weight * f(xi)': term,
            'Note': note
        })
        
    # Rumus Akhir: I = (h/2) * [f0 + 2*sigma + fn]
    integral = (h / 2) * sum_fx
    
    return integral, h, pd.DataFrame(data)

# =========================================================================
# 3. PROGRAM UTAMA (MENJALANKAN SKENARIO EXCEL)
# =========================================================================
def main():
    print("=" * 80)
    print("       INTEGRASI NUMERIK: ATURAN TRAPEZOIDAL")
    print(f"       Fungsi: v(t) = gm/c * (1 - e^(-c/m * t))")
    print(f"       Parameter: g={g}, m={m}, c={c}")
    print("=" * 80)

    # Batas Integrasi Default
    t_start = 0.0
    t_end = 10.0

    # Skenario sesuai Excel
    scenarios = [10, 20, 50] 

    for n in scenarios:
        I, h, df = hitung_trapezoidal(t_start, t_end, n)
        
        print(f"\n>>> SKENARIO n = {n} (h = {h:.4f})")
        print("-" * 80)
        
        # Tampilkan 5 baris pertama dan 5 baris terakhir agar tidak kepanjangan
        if n > 15:
            print("Tabel Perhitungan (Awal & Akhir):")
            print(df.head(5).to_string(index=False))
            print("... [Data Tengah Disembunyikan] ...")
            print(df.tail(5).to_string(index=False))
        else:
            print(df.to_string(index=False))
            
        print("-" * 80)
        print(f"HASIL INTEGRAL (JARAK) = {I:.6f}")
        print("=" * 80)

    # --- OPSI INPUT MANUAL ---
    print("\nIngin mencoba nilai n sendiri? (Ketik 0 untuk keluar)")
    try:
        n_user = int(input("Masukkan n: "))
        if n_user > 0:
            I, h, df = hitung_trapezoidal(t_start, t_end, n_user)
            print("-" * 80)
            print(f"Hasil untuk n={n_user} (h={h:.4f}) : {I:.6f}")
            print("-" * 80)
    except ValueError:
        pass

if __name__ == "__main__":
    main()