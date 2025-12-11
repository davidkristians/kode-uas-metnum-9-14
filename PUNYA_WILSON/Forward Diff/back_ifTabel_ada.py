import numpy as np

# ==========================================
# 1. INPUT DATA TABEL (Manual)
# ==========================================
# Salin data x dan y dari soal/Excel ke sini
data_tabel = {
    0.00 : 1.2,
    0.25 : 1.1035156,
    0.50 : 0.925,       # <-- Titik yang dicari (x)
    0.75 : 0.6363281,
    1.00 : 0.2
}

# ==========================================
# 2. KONFIGURASI PENCARIAN
# ==========================================
titik_x = 0.5    # Nilai x yang ingin dicari turunannya
step_h  = 0.25   # Step size (jarak antar x di tabel)

# Fungsi Helper untuk mengambil data (Wrapper)
def ambil_data(x):
    # Pembulatan penting agar komputer presisi mencocokkan kunci dictionary
    # Misal: 0.5 - 0.25 = 0.25 (kadang komputer baca 0.2499999)
    kunci = round(x, 5) 
    
    if kunci in data_tabel:
        return data_tabel[kunci]
    else:
        # Error jika data masa lalu tidak tersedia
        raise ValueError(f"Data hilang! Tidak ada nilai y untuk x={kunci}")

# ==========================================
# 3. RUMUS BACKWARD DIFFERENCE
# ==========================================

def backward_basic(x, h):
    """
    Rumus O(h): (f(x) - f(x-h)) / h
    Membutuhkan: Data SEKARANG dan 1 langkah KEBELAKANG
    """
    f_x     = ambil_data(x)
    f_xmin1 = ambil_data(x - h)
    
    return (f_x - f_xmin1) / h

def backward_high_accuracy(x, h):
    """
    Rumus O(h^2): (3f(x) - 4f(x-h) + f(x-2h)) / 2h
    Membutuhkan: Data SEKARANG, 1 langkah KEBELAKANG, dan 2 langkah KEBELAKANG
    """
    f_x     = ambil_data(x)
    f_xmin1 = ambil_data(x - h)
    f_xmin2 = ambil_data(x - 2*h)
    
    return (3*f_x - 4*f_xmin1 + f_xmin2) / (2 * h)

# ==========================================
# 4. EKSEKUSI PROGRAM
# ==========================================
print(f"--- BACKWARD DIFFERENCE (DATA TABEL) ---")
print(f"Mencari f'({titik_x}) dengan step h={step_h}")
print("-" * 40)

# Coba Hitung Basic Formula
try:
    hasil_basic = backward_basic(titik_x, step_h)
    print(f"[Basic]    Hasil: {hasil_basic:.6f}")
    print(f"           (Pakai data x={titik_x} dan x={titik_x-step_h})")
except ValueError as e:
    print(f"[Basic]    GAGAL: {e}")

print("-" * 20)

# Coba Hitung High Accuracy Formula
try:
    hasil_high = backward_high_accuracy(titik_x, step_h)
    print(f"[High Acc] Hasil: {hasil_high:.6f}")
    print(f"           (Pakai data x={titik_x}, x={titik_x-step_h}, x={titik_x-(2*step_h)})")
except ValueError as e:
    print(f"[High Acc] GAGAL: {e}")

print("-" * 40)