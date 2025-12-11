import numpy as np
import math

# --- 1. Persiapan Data ---
x = np.array([0, 1, 2, 3, 4, 5], dtype=float)
y = np.array([2.1, 7.7, 13.6, 27.2, 40.9, 61.1], dtype=float)
n = len(x)

print("=== POLYNOMIAL REGRESSION ===")

# --- 2. Hitung Komponen Sum (Sigma) ---
# Kita butuh sum x^1 sampai x^4
sum_x   = np.sum(x)
sum_x2  = np.sum(x**2)
sum_x3  = np.sum(x**3)
sum_x4  = np.sum(x**4)

# Kita butuh sum y, xy, x^2y
sum_y   = np.sum(y)
sum_xy  = np.sum(x * y)
sum_x2y = np.sum((x**2) * y)

# Tampilkan Sigma (Sesuai tabel atas di gambar)
print("--- Nilai Sigma (Sum) ---")
print(f"Σx: {sum_x}, Σx²: {sum_x2}, Σx³: {sum_x3}, Σx⁴: {sum_x4}")
print(f"Σy: {sum_y}, Σxy: {sum_xy}, Σx²y: {sum_x2y}")
print("")

# --- 3. Membentuk Matriks Sistem Persamaan ---
# Matriks A (Kiri)
A = np.array([
    [n,      sum_x,  sum_x2],
    [sum_x,  sum_x2, sum_x3],
    [sum_x2, sum_x3, sum_x4]
])

# Matriks B (Kanan)
B = np.array([sum_y, sum_xy, sum_x2y])

print("--- Matriks ---")
print("Matriks A (Left):")
print(A)
print("Vektor B (Right):")
print(B)
print("")

# --- 4. Menyelesaikan Matriks (Mencari a0, a1, a2) ---
# Menggunakan fungsi solve dari numpy (setara dengan invers matriks * B)
coeffs = np.linalg.solve(A, B)

a0 = coeffs[0]
a1 = coeffs[1]
a2 = coeffs[2]

print(f"1. a0 (Intercept) : {a0:.6f}")
print(f"2. a1 (Slope 1)   : {a1:.6f}")
print(f"3. a2 (Slope 2)   : {a2:.6f}")
print(f"   Persamaan      : y = {a0:.3f} + {a1:.3f}x + {a2:.3f}x^2")
print("")

# --- 5. Statistik Error dan Korelasi ---
# Prediksi nilai Y berdasarkan rumus baru
y_pred = a0 + a1*x + a2*(x**2)

# Hitung Rata-rata Y
mean_y = np.mean(y)

# Hitung Sum of Squared Errors (Residuals) -> (yi - y_pred)^2
sum_error_sq = np.sum((y - y_pred)**2)

# Hitung Total Sum of Squares -> (yi - y_rata)^2
sum_total_sq = np.sum((y - mean_y)**2)

# --- A. Standard Deviation (Sy) ---
# Rumus: sqrt( Σ(y - mean_y)^2 / (n-1) )
sy = math.sqrt(sum_total_sq / (n - 1))

# --- B. Standard Error of Estimation (Sy/x) ---
# Rumus Umum Polinomial: sqrt( Σerror^2 / (n - (order+1)) )
# Harusnya dibagi (n-3) untuk orde 2.
# TAPI: Gambar Anda menggunakan pembagi (n-2) untuk menghasilkan 0.9678.
# Kita ikuti rumus gambar agar hasil cocok.
syx = math.sqrt(sum_error_sq / (n - 2)) 

# --- C. Koefisien Determinasi (r^2) ---
# Rumus: 1 - (Sum_Error_Sq / Sum_Total_Sq)
r2 = 1 - (sum_error_sq / sum_total_sq)
r = math.sqrt(r2)

print(f"4. Standard Deviation (Sy)    : {sy:.4f}")
print(f"5. Standard Error (Sy/x)      : {syx:.6f}")
print(f"6. Koefisien Determinasi (r²) : {r2:.6f} ({r2*100:.5f}%)")
print(f"7. Koefisien Korelasi (r)     : {r:.6f}")