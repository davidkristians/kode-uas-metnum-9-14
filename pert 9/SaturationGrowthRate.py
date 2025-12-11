import math

# --- 1. Fungsi Transformasi (Inversi / Kebalikan) ---
def transform_inverse(data):
    # Mengubah data menjadi 1/data
    return [1/val for val in data]

# --- 2. Fungsi Hitung Slope (a1) pada Data Ter-inversi ---
def hitung_slope(x_inv, y_inv):
    n = len(x_inv)
    sum_x = sum(x_inv)
    sum_y = sum(y_inv)
    sum_xy = sum([xi * yi for xi, yi in zip(x_inv, y_inv)])
    sum_x2 = sum([xi ** 2 for xi in x_inv])

    # Rumus Linear Regression biasa
    pembilang = (n * sum_xy) - (sum_x * sum_y)
    penyebut = (n * sum_x2) - (sum_x ** 2)
    
    return pembilang / penyebut

# --- 3. Fungsi Hitung Intercept (a0) pada Data Ter-inversi ---
def hitung_intercept(x_inv, y_inv, slope):
    n = len(x_inv)
    mean_x = sum(x_inv) / n
    mean_y = sum(y_inv) / n
    
    # a0 = y_rata - (slope * x_rata)
    return mean_y - (slope * mean_x)

# --- 4. Fungsi Prediksi Saturation Growth ---
def prediksi_saturation(x_val, alpha, beta):
    # Rumus: y = alpha * (x / (beta + x))
    return alpha * (x_val / (beta + x_val))

# --- 5. Fungsi Standard Deviation (Sy) - Data Asli ---
def hitung_std_dev(y):
    n = len(y)
    mean_y = sum(y) / n
    sum_sq_diff = sum([(yi - mean_y)**2 for yi in y])
    return math.sqrt(sum_sq_diff / (n - 1))

# --- 6. Fungsi Standard Error (Sy/x) ---
def hitung_std_error_sat(x, y, alpha, beta):
    n = len(x)
    sum_error_sq = 0
    
    # Menghitung residual pada skala ASLI: (y_asli - y_prediksi)^2
    for i in range(n):
        y_pred = prediksi_saturation(x[i], alpha, beta)
        residual = y[i] - y_pred
        sum_error_sq += residual ** 2
        
    # Rumus: sqrt( sum_error_sq / (n-2) )
    return math.sqrt(sum_error_sq / (n - 2))

# --- 7. Fungsi Korelasi (r) pada Data Ter-inversi ---
def hitung_korelasi_inv(x_inv, y_inv):
    n = len(x_inv)
    sum_x = sum(x_inv)
    sum_y = sum(y_inv)
    sum_xy = sum([xi * yi for xi, yi in zip(x_inv, y_inv)])
    sum_x2 = sum([xi ** 2 for xi in x_inv])
    sum_y2 = sum([yi ** 2 for yi in y_inv])

    pembilang = (n * sum_xy) - (sum_x * sum_y)
    term_x = (n * sum_x2) - (sum_x ** 2)
    term_y = (n * sum_y2) - (sum_y ** 2)
    
    r = pembilang / math.sqrt(term_x * term_y)
    return r, r**2

# ==========================================
# MAIN PROGRAM
# ==========================================

# 1. INPUT DATA DARI GAMBAR
x = [2, 4, 6, 8, 10]
y = [4, 5.71, 6.67, 7.27, 7.69]

print("=== HASIL SATURATION GROWTH RATE REGRESSION ===")

# 2. TRANSFORMASI DATA (1/x dan 1/y)
x_inv = transform_inverse(x)
y_inv = transform_inverse(y)

# 3. HITUNG SLOPE (a1)
a1 = hitung_slope(x_inv, y_inv)
print(f"1. Slope (a1)      : {a1:.6f}")

# 4. HITUNG INTERCEPT (a0)
a0 = hitung_intercept(x_inv, y_inv, a1)
print(f"2. Intercept (a0)  : {a0:.6f}")

# 5. KONVERSI KE PARAMETER ASLI (Alpha dan Beta)
# a0 = 1/alpha  -> alpha = 1/a0
alpha = 1 / a0

# a1 = beta/alpha -> beta = a1 * alpha
beta = a1 * alpha

print(f"3. Alpha (α)       : {alpha:.6f}")
print(f"4. Beta (β)        : {beta:.6f}")
print(f"   Persamaan akhir : y = {round(alpha)} * (x / ({round(beta)} + x))")

# 6. HITUNG STANDARD DEVIATION (Data Asli)
sy = hitung_std_dev(y)
print(f"5. Standard Deviasi (Sy)  : {sy:.6f}")

# 7. HITUNG STANDARD ERROR (Sy/x)
# Error dihitung antara Y Asli dengan Y Prediksi Rumus Saturation
syx = hitung_std_error_sat(x, y, alpha, beta)
print(f"6. Standard Error (Sy/x)  : {syx:.6f}")

# 8. HITUNG KORELASI (Linearized Data)
r, r2 = hitung_korelasi_inv(x_inv, y_inv)
print(f"7. Koefisien Korelasi (r)     : {r:.6f}")
print(f"8. Koefisien Determinasi (r²) : {r2:.6f} ({r2*100:.5f}%)")