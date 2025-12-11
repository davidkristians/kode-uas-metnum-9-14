import numpy as np

# ==========================================
# 1. KONFIGURASI SOAL (UBAH DISINI)
# ==========================================

# A. Masukkan Rumus Fungsi f(x) atau v(t)
# Contoh: Soal Roket -> v(t) = 2000*ln(140000/(140000 - 2100t)) - 9.8t
def fungsi_soal(t):
    # np.log adalah logaritma natural (ln)
    # Gunakan np.exp(x) untuk bilangan e pangkat x
    term_dalam_ln = 140000 / (140000 - (2100 * t))
    v = 2000 * np.log(term_dalam_ln) - (9.8 * t)
    return v

# B. Tentukan Titik yang dicari dan Step Size
titik_x = 16   # Nilai t atau x yang ingin dicari turunannya
step_h  = 2    # Nilai step size (h atau delta t)

# ==========================================
# 2. RUMUS METODE NUMERIK (JANGAN UBAH)
# ==========================================

def backward_basic(func, x, h):
    """
    Rumus O(h): (f(x) - f(x-h)) / h
    """
    return (func(x) - func(x - h)) / h

def backward_high_accuracy(func, x, h):
    """
    Rumus O(h^2): (3f(x) - 4f(x-h) + f(x-2h)) / 2h
    """
    return (3*func(x) - 4*func(x - h) + func(x - 2*h)) / (2 * h)

# ==========================================
# 3. EKSEKUSI DAN HASIL
# ==========================================

print(f"--- HASIL PERHITUNGAN BACKWARD DIFFERENCE ---")
print(f"Titik x (t) : {titik_x}")
print(f"Step size (h): {step_h}")
print("-" * 45)

# Hitung Basic
hasil_basic = backward_basic(fungsi_soal, titik_x, step_h)
print(f"1. Basic Formula (2 titik):")
print(f"   Nilai = {hasil_basic:.6f}")

# Hitung High Accuracy
hasil_high = backward_high_accuracy(fungsi_soal, titik_x, step_h)
print(f"\n2. High Accuracy Formula (3 titik):")
print(f"   Nilai = {hasil_high:.6f}")

print("-" * 45)
# Cek nilai fungsi untuk validasi manual (seperti di Excel)
print("Data pendukung (Cek Excel):")
print(f"v({titik_x})      = {fungsi_soal(titik_x):.4f}")
print(f"v({titik_x}-{step_h})    = {fungsi_soal(titik_x - step_h):.4f}")
print(f"v({titik_x}-{2*step_h})    = {fungsi_soal(titik_x - (2*step_h)):.4f}")