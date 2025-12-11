import math

# --- 1. Fungsi Perhitungan Slope (a1) ---
def hitung_slope(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([xi * yi for xi, yi in zip(x, y)])
    sum_x2 = sum([xi ** 2 for xi in x])

    pembilang = (n * sum_xy) - (sum_x * sum_y)
    penyebut = (n * sum_x2) - (sum_x ** 2)
    
    return pembilang / penyebut

# --- 2. Fungsi Perhitungan Intercept (a0) ---
def hitung_intercept(x, y, a1):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Rumus: a0 = y_rata2 - (a1 * x_rata2)
    return mean_y - (a1 * mean_x)

# --- 3. Fungsi Prediksi (y = a0 + a1x) ---
# Fungsi bantu untuk mendapatkan nilai y prediksi (y topi)
def prediksi_y(x_val, a0, a1):
    return a0 + (a1 * x_val)

# --- 4. Fungsi Standard Deviation (Sy) ---
def hitung_std_dev(y):
    n = len(y)
    mean_y = sum(y) / n
    
    # Rumus: sqrt( sum(y - y_rata)^2 / (n-1) )
    sum_sq_diff = sum([(yi - mean_y)**2 for yi in y])
    
    return math.sqrt(sum_sq_diff / (n - 1))

# --- 5. Fungsi Standard Error of Estimation (Sy/x) ---
def hitung_std_error(x, y, a0, a1):
    n = len(x)
    
    # Hitung error kuadrat: sum(y_asli - y_prediksi)^2
    sum_error_sq = 0
    for i in range(n):
        y_pred = prediksi_y(x[i], a0, a1)
        residual = y[i] - y_pred
        sum_error_sq += residual ** 2
        
    # Rumus: sqrt( sum_error_sq / (n-2) )
    return math.sqrt(sum_error_sq / (n - 2))

# --- 6. Fungsi Korelasi (r) dan Determinasi (r^2) ---
def hitung_korelasi(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum([xi * yi for xi, yi in zip(x, y)])
    sum_x2 = sum([xi ** 2 for xi in x])
    sum_y2 = sum([yi ** 2 for yi in y])

    pembilang = (n * sum_xy) - (sum_x * sum_y)
    
    term_x = (n * sum_x2) - (sum_x ** 2)
    term_y = (n * sum_y2) - (sum_y ** 2)
    penyebut = math.sqrt(term_x * term_y)
    
    r = pembilang / penyebut
    r_sq = r ** 2
    return r, r_sq

# ==========================================
# MAIN PROGRAM (Eksekusi)
# ==========================================

# Data Input
data_x = [1, 2, 3, 4, 5, 6, 7]
data_y = [0.5, 2.5, 2, 4, 3.5, 6, 5.5]

print("=== HASIL PERHITUNGAN MODULAR ===")

# 1. Hitung Slope
a1 = hitung_slope(data_x, data_y)
print(f"1. Slope (a1)      : {a1:.7f}")

# 2. Hitung Intercept (butuh a1)
a0 = hitung_intercept(data_x, data_y, a1)
print(f"2. Intercept (a0)  : {a0:.7f}")
print(f"   -> Persamaan    : y = {a0:.2f} + {a1:.2f}x")

# 3. Hitung Standard Deviation
sy = hitung_std_dev(data_y)
print(f"3. Standard Deviasi   : {sy:.5f}")

# 4. Hitung Standard Error (butuh a0 dan a1 untuk prediksi)
syx = hitung_std_error(data_x, data_y, a0, a1)
print(f"4. Standard Error (Sy/x): {syx:.5f}")

# 5. Hitung Korelasi
r, r2 = hitung_korelasi(data_x, data_y)
print(f"5. Koefisien Korelasi (r)    : {r:.5f}")
print(f"6. Koefisien Determinasi (r²): {r2:.5f} ({r2*100:.2f}%)")