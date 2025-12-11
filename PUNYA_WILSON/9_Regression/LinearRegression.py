import numpy as np

# Atur opsi pencetakan agar lebih mudah dibaca, mirip dengan gambar Anda
np.set_printoptions(precision=7, suppress=True)

# --- Data Awal ---
# Data x_i dalam radian (0, pi/4, pi/2, 3pi/4)
x_i = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4])
# Data y_i
y_i = np.array([3, 2.5, 1, 0.5])

print(f"Data x_i: {x_i}")
print(f"Data y_i: {y_i}")
print("-" * 30)

# =========================================================
# Step 1: Membentuk Matriks [Z] dan {Y}
# =========================================================
print("\n--- Step 1: Membentuk [Z] dan {Y} ---")

# Model: y = a0*z0 + a1*z1 + a2*z2
# z0 = 1
# z1 = cos(2x)
# z2 = sin(x)

# 1. Hitung nilai z untuk setiap x_i
z_0 = np.ones_like(x_i)
z_1 = np.cos(2 * x_i)
z_2 = np.sin(x_i)

# 2. Susun menjadi matriks [Z] (menggabungkan z0, z1, z2 sebagai kolom)
Z = np.stack([z_0, z_1, z_2], axis=1)

# 3. Ubah y_i menjadi vektor kolom {Y}
Y = y_i.reshape(-1, 1) # Bentuk ulang menjadi matriks 4x1

print("Matriks [Z]:")
print(Z)
# Catatan: Nilai seperti 6.13e-17 adalah nol (terjadi karena galat presisi float)
# Ini sama dengan yang Anda lihat di gambar (6,13E-17 dan -1,84E-16)

print("\nVektor {Y}:")
print(Y)

# =========================================================
# Step 2: Menghitung [Z]T[Z]
# =========================================================
print("\n--- Step 2: Menghitung [Z]T[Z] ---")

# [Z]T adalah transpose dari Z
# @ adalah operator untuk perkalian matriks (dot product)
Z_T_Z = Z.T @ Z

print("[Z]T[Z]:")
print(Z_T_Z)
# Hasilnya sama persis dengan matriks di gambar Anda

# =========================================================
# Step 3: Menghitung [Z]T{Y}
# =========================================================
print("\n--- Step 3: Menghitung [Z]T{Y} ---")

Z_T_Y = Z.T @ Y

print("[Z]T{Y}:")
print(Z_T_Y)
# Hasilnya sama persis dengan vektor di gambar Anda (7, 2, 3.12132)

# =========================================================
# Step 4: Menyelesaikan {A}
# =========================================================
print("\n--- Step 4: Menyelesaikan {A} ---")
print("Sistem Persamaan: [Z]T[Z] {A} = [Z]T{Y}\n")

print("Matriks [Z]T[Z]:")
print(Z_T_Z)
print("\nVektor [Z]T{Y}:")
print(Z_T_Y)

# --- Sesuai gambar: Menggunakan Invers Matriks ---
print("\n--- Metode Invers (seperti di gambar) ---")

# 1. Hitung invers dari [Z]T[Z]
Z_T_Z_inv = np.linalg.inv(Z_T_Z)
print("Invers dari [Z]T[Z] ( ([Z]T[Z])^-1 ):")
print(Z_T_Z_inv)
# Ini adalah matriks kuning kedua di gambar Anda

# 2. Hitung {A} = ([Z]T[Z])^-1 * [Z]T{Y}
A = Z_T_Z_inv @ Z_T_Y

print("\nSolusi {A}:")
print(A)

# --- Menampilkan hasil akhir dengan rapi ---
a_0 = A[0, 0]
a_1 = A[1, 0]
a_2 = A[2, 0]

print("\n--- Hasil Akhir Koefisien ---")
print(f"a_0 = {a_0:.7f}")
print(f"a_1 = {a_1:.7f}")
print(f"a_2 = {a_2:.7f}")

print("\nPersamaan Regresi Final:")
print(f"y = {a_0:.7f} + ({a_1:.7f}) cos(2x) + ({a_2:.7f}) sin(x)")