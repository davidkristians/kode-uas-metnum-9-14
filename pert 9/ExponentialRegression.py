import math

# --- 1. Fungsi Transformasi Logaritma (Ln) ---
def transform_to_log(y_data):
    # Mengubah semua y menjadi ln(y)
    return [math.log(yi) for yi in y_data]

# --- 2. Fungsi Slope (a1 / beta1) pada Data Log ---
def hitung_slope(x, y_log):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y_log)
    sum_xy = sum([xi * yi for xi, yi in zip(x, y_log)])
    sum_x2 = sum([xi ** 2 for xi in x])

    # Rumus Linear Regression biasa, tapi menggunakan y_log
    pembilang = (n * sum_xy) - (sum_x * sum_y)
    penyebut = (n * sum_x2) - (sum_x ** 2)
    
    return pembilang / penyebut

# --- 3. Fungsi Intercept (a0) pada Data Log ---
def hitung_intercept_log(x, y_log, slope):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y_log) / n
    
    # a0 = ln(y)_rata2 - (slope * x_rata2)
    return mean_y - (slope * mean_x)

# --- 4. Fungsi Prediksi Eksponensial ---
def prediksi_eksponensial(x_val, alpha, beta):
    # Rumus: y = alpha * e^(beta * x)
    return alpha * math.exp(beta * x_val)

# --- 5. Fungsi Standard Deviation (Sy) - Data Asli ---
def hitung_std_dev(y):
    n = len(y)
    mean_y = sum(y) / n
    sum_sq_diff = sum([(yi - mean_y)**2 for yi in y])
    return math.sqrt(sum_sq_diff / (n - 1))

# --- 6. Fungsi Standard Error of Estimation (Sy/x) ---
def hitung_std_error_exp(x, y, alpha, beta):
    n = len(x)
    sum_error_sq = 0
    
    # Menghitung residual pada skala ASLI (bukan log)
    # Sesuai tabel bawah di gambar: (yi - y_pred)^2
    for i in range(n):
        y_pred = prediksi_eksponensial(x[i], alpha, beta)
        residual = y[i] - y_pred
        sum_error_sq += residual ** 2
        
    # Rumus: sqrt( sum_error_sq / (n-2) )
    return math.sqrt(sum_error_sq / (n - 2))

# --- 7. Fungsi Korelasi (r) pada Data Terlinearisasi ---
def hitung_korelasi_log(x, y_log):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y_log)
    sum_xy = sum([xi * yi for xi, yi in zip(x, y_log)])
    sum_x2 = sum([xi ** 2 for xi in x])
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
x = [2, 3, 4, 5, 6]
y = [2.47, 3.18, 4.08, 5.24, 6.72]

print("=== HASIL EXPONENTIAL REGRESSION ===")

# 2. TRANSFORMASI DATA (y -> ln y)
y_log = transform_to_log(y)
# Tampilkan Ln(y) untuk verifikasi
# print(f"Ln(y): {[round(val, 4) for val in y_log]}")

# 3. HITUNG SLOPE (Beta 1)
beta1 = hitung_slope(x, y_log)
print(f"1. Slope (Beta1/a1)  : {beta1:.6f}")

# 4. HITUNG INTERCEPT LOG (Ln Alpha 1)
ln_alpha1 = hitung_intercept_log(x, y_log, beta1)
print(f"2. Ln(Alpha1) / a0   : {ln_alpha1:.6f}")

# 5. KONVERSI KE ALPHA ASLI
# alpha = e^(ln_alpha)
alpha1 = math.exp(ln_alpha1)
print(f"3. Alpha1 (Exp a0)   : {alpha1:.6f}")
print(f"   Persamaan akhir   : y = {alpha1:.1f} * e^({beta1:.2f}x)")

# 6. HITUNG STANDARD DEVIATION (Data Asli)
sy = hitung_std_dev(y)
print(f"4. Standard Dev (Sy)          : {sy:.6f}")

# 7. HITUNG STANDARD ERROR (Sy/x)
# Error dihitung berdasarkan selisih y asli dengan y prediksi eksponensial
syx = hitung_std_error_exp(x, y, alpha1, beta1)
print(f"5. Standard Error (Sy/x)      : {syx:.6f}")

# 8. HITUNG KORELASI (Linearized Data)
r, r2 = hitung_korelasi_log(x, y_log)
print(f"6. Koefisien Korelasi (r)     : {r:.6f}")
print(f"7. Koefisien Determinasi (r²) : {r2:.6f} ({r2*100:.5f}%)")