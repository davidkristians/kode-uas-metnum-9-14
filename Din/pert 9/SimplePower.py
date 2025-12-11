import math

# --- 1. Fungsi Transformasi Logaritma Basis 10 ---
def transform_to_log10(data):
    # Mengubah data menjadi log10(data)
    return [math.log10(val) for val in data]

# --- 2. Fungsi Hitung Slope (Beta) ---
def hitung_slope(x_log, y_log):
    n = len(x_log)
    sum_x = sum(x_log)
    sum_y = sum(y_log)
    sum_xy = sum([xi * yi for xi, yi in zip(x_log, y_log)])
    sum_x2 = sum([xi ** 2 for xi in x_log])

    # Rumus Regresi Linear pada data Log
    pembilang = (n * sum_xy) - (sum_x * sum_y)
    penyebut = (n * sum_x2) - (sum_x ** 2)
    
    return pembilang / penyebut

# --- 3. Fungsi Hitung Intercept (Log Alpha) ---
def hitung_intercept_log(x_log, y_log, slope):
    n = len(x_log)
    mean_x = sum(x_log) / n
    mean_y = sum(y_log) / n
    
    # a0 = y_bar - slope * x_bar
    return mean_y - (slope * mean_x)

# --- 4. Fungsi Prediksi Power Model ---
def prediksi_power(x_val, alpha, beta):
    # Rumus: y = alpha * x^beta
    return alpha * (x_val ** beta)

# --- 5. Fungsi Standard Deviation (Sy) - Data Asli ---
def hitung_std_dev(y):
    n = len(y)
    mean_y = sum(y) / n
    sum_sq_diff = sum([(yi - mean_y)**2 for yi in y])
    return math.sqrt(sum_sq_diff / (n - 1))

# --- 6. Fungsi Standard Error of Estimation (Sy/x) ---
def hitung_std_error_power(x, y, alpha, beta):
    n = len(x)
    sum_error_sq = 0
    
    # Menghitung residual pada skala ASLI
    # (yi - y_pred)^2
    for i in range(n):
        y_pred = prediksi_power(x[i], alpha, beta)
        residual = y[i] - y_pred
        sum_error_sq += residual ** 2
        
    # Rumus: sqrt( sum_error_sq / (n-2) )
    return math.sqrt(sum_error_sq / (n - 2))

# --- 7. Fungsi Korelasi (r) pada Data Log-Log ---
def hitung_korelasi_log(x_log, y_log):
    n = len(x_log)
    sum_x = sum(x_log)
    sum_y = sum(y_log)
    sum_xy = sum([xi * yi for xi, yi in zip(x_log, y_log)])
    sum_x2 = sum([xi ** 2 for xi in x_log])
    sum_y2 = sum([yi ** 2 for yi in y_log])

    pembilang = (n * sum_xy) - (sum_x * sum_y)
    term_x = (n * sum_x2) - (sum_x ** 2)
    term_y = (n * sum_y2) - (sum_y ** 2)
    
    r = pembilang / math.sqrt(term_x * term_y)
    return r, r**2

# ==========================================
# MAIN PROGRAM
# ==========================================

# 1. INPUT DATA DARI GAMBAR
x = [1, 2, 3, 4, 5]
y = [0.5, 1.7, 3.4, 5.7, 8.4]

print("=== HASIL SIMPLE POWER REGRESSION ===")

# 2. TRANSFORMASI DATA (Log-Log)
x_log = transform_to_log10(x)
y_log = transform_to_log10(y)

# 3. HITUNG SLOPE (Beta / b)
beta = hitung_slope(x_log, y_log)
print(f"1. Slope (Beta/a1)     : {beta:.6f}")

# 4. HITUNG INTERCEPT LOG (Log Alpha / a0)
log_alpha = hitung_intercept_log(x_log, y_log, beta)
print(f"2. Log(Alpha) / a0     : {log_alpha:.6f}")

# 5. KONVERSI KE ALPHA ASLI
# Karena pakai log10, maka alpha = 10^log_alpha
alpha = 10 ** log_alpha
print(f"3. Alpha (Antilog a0)  : {alpha:.6f}")
print(f"   Persamaan akhirnya  : y = {alpha:.2f} * x^{beta:.2f}")

# 6. HITUNG STANDARD DEVIATION (Data Asli)
sy = hitung_std_dev(y)
print(f"4. Standard Deviasi (Sy)  : {sy:.6f}")

# 7. HITUNG STANDARD ERROR (Sy/x)
# Error dihitung antara Y Asli dengan Y Prediksi Rumus Power
syx = hitung_std_error_power(x, y, alpha, beta)
print(f"5. Standard Error (Sy/x)  : {syx:.6f}")

# 8. HITUNG KORELASI (Linearized Data)
r, r2 = hitung_korelasi_log(x_log, y_log)
print(f"6. Koefisien Korelasi (r)      : {r:.6f}")
print(f"7. Koefisien Determinasi (r²)  : {r2:.6f} ({r2*100:.5f}%)")