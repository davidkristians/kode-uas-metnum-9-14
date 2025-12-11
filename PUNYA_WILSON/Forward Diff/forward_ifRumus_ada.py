import numpy as np

# ==========================================
# 1. KONFIGURASI SOAL (UBAH DISINI)
# ==========================================

# A. Masukkan Rumus Fungsi f(x) atau v(t)
# Default: Soal Roket dari gambar pertama
def fungsi_soal(t):
    # Rumus: v(t) = 2000*ln(140000/(140000 - 2100t)) - 9.8t
    term_dalam_ln = 140000 / (140000 - (2100 * t))
    v = 2000 * np.log(term_dalam_ln) - (9.8 * t)
    return v

# B. Tentukan Titik yang dicari dan Step Size
titik_x = 16   # Titik t = 16
step_h  = 2    # Step size delta t = 2

# ==========================================
# 2. RUMUS FORWARD DIFFERENCE
# ==========================================

def forward_basic(func, x, h):
    """
    Rumus O(h): (f(x+h) - f(x)) / h
    Menggunakan 2 titik: sekarang dan 1 langkah ke depan.
    """
    return (func(x + h) - func(x)) / h

def forward_high_accuracy(func, x, h):
    """
    Rumus O(h^2): (-f(x+2h) + 4f(x+h) - 3f(x)) / 2h
    Menggunakan 3 titik: sekarang, 1 langkah ke depan, dan 2 langkah ke depan.
    """
    return (-func(x + 2*h) + 4*func(x + h) - 3*func(x)) / (2 * h)

# ==========================================
# 3. EKSEKUSI DAN HASIL
# ==========================================

print(f"--- HASIL PERHITUNGAN FORWARD DIFFERENCE ---")
print(f"Titik x (t) : {titik_x}")
print(f"Step size (h): {step_h}")
print("-" * 45)

# Hitung Basic
hasil_basic = forward_basic(fungsi_soal, titik_x, step_h)
print(f"1. Basic Formula (2 titik):")
print(f"   Nilai = {hasil_basic:.6f}")

# Hitung High Accuracy
hasil_high = forward_high_accuracy(fungsi_soal, titik_x, step_h)
print(f"\n2. High Accuracy Formula (3 titik):")
print(f"   Nilai = {hasil_high:.6f}")

print("-" * 45)
# Validasi Data (Cek dengan Gambar Excel pertama kamu)
print("Data pendukung (Cek Excel):")
print(f"v({titik_x})      = {fungsi_soal(titik_x):.4f}")
print(f"v({titik_x}+{step_h})    = {fungsi_soal(titik_x + step_h):.4f}")
print(f"v({titik_x}+{2*step_h})    = {fungsi_soal(titik_x + (2*step_h)):.4f}")