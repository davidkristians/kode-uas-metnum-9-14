import numpy as np

# --- BAGIAN INPUT DATA TABEL ---
data_tabel = {
    0.00 : 1.2,
    0.25 : 1.1035156,
    0.50 : 0.925,       
    0.75 : 0.6363281,   
    1.00 : 0.2
}

def fungsi_soal(x):
    # Pembulatan biar aman (komputer kadang baca 0.5 sebagai 0.499999)
    kunci = round(x, 2) 
    return data_tabel[kunci]

# --- KONFIGURASI ---
titik_x = 0.5    # x yang dicari
step_h  = 0.25   # selisih antar x di tabel

# --- RUMUS FORWARD (Tetap Sama) ---
def forward_basic(func, x, h):
    return (func(x + h) - func(x)) / h

def forward_high_accuracy(func, x, h):
    return (-func(x + 2*h) + 4*func(x + h) - 3*func(x)) / (2 * h)

# --- EKSEKUSI ---
print(f"Mencari f'({titik_x}) dengan Forward Difference")
print("-" * 30)

try:
    # 1. Basic (Butuh data 0.5 dan 0.75) -> Ada di tabel
    hasil_basic = forward_basic(fungsi_soal, titik_x, step_h)
    print(f"Basic Formula: {hasil_basic:.6f}")

    # 2. High Accuracy (Butuh data 0.5, 0.75, dan 1.0) -> Ada di tabel
    hasil_high = forward_high_accuracy(fungsi_soal, titik_x, step_h)
    print(f"High Accuracy: {hasil_high:.6f}")

except KeyError as e:
    print(f"Error: Data tabel kurang lengkap! Tidak ada nilai untuk x={e}")