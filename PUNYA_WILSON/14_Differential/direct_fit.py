import numpy as np
import pandas as pd

# Atur tampilan float agar rapi
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("=== DIRECT FIT POLYNOMIAL (DETAILED MATRIX OUTPUT) ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH DISINI)
# ==============================================================================
# 1. Masukkan Data Titik (Contoh Roket dari Excel)
x_data = np.array([10.0, 15.0, 20.0, 22.5]) 
y_data = np.array([227.04, 362.78, 517.35, 602.97])

# 2. Titik yang ingin dicari turunannya
x_find = 16
# ==============================================================================

def direct_fit_detailed(x, y, target):
    n = len(x)
    degree = n - 1 # Orde = n-1
    
    print("-" * 60)
    print(f"Jumlah Data: {n} titik")
    print(f"Maka dibentuk Polinomial Orde {degree}")
    print(f"Model: f(x) = a0 + a1*x + a2*x^2 + ... + a{degree}*x^{degree}")
    print("-" * 60)
    
    # 1. MENYUSUN MATRIKS (VANDERMONDE)
    # Kita menyusun sistem persamaan:
    # a0 + a1*x1 + a2*x1^2 + ... = y1
    # a0 + a1*x2 + a2*x2^2 + ... = y2
    
    A = np.zeros((n, n))
    B = y.copy()
    
    col_names = []
    for i in range(n):
        col_names.append(f"x^{i} (a{i})")
        # Isi kolom ke-i dengan x dipangkatkan i
        A[:, i] = x ** i

    # Tampilkan Tabel Matriks
    df_matrix = pd.DataFrame(A, columns=col_names)
    df_matrix.insert(0, 'x_val', x)
    df_matrix['= y_val'] = y
    
    print("\n[TABEL MATRIKS SISTEM PERSAMAAN]")
    print(df_matrix.to_string(index=False))
    
    # 2. MENYELESAIKAN MATRIKS (Mencari a0, a1, a2...)
    try:
        a_coeffs = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        print("Error: Matriks Singular. Data tidak bisa di-fitting.")
        return

    # 3. TAMPILKAN HASIL KOEFISIEN (a0, a1, a2...)
    print("\n" + "="*40)
    print("HASIL KOEFISIEN (a0, a1, a2...)")
    print("="*40)
    
    eq_str = "f(x) = "
    deriv_str = "f'(x) = "
    
    for i in range(n):
        val = a_coeffs[i]
        print(f"a{i} = {val:.8f}")
        
        # Susun string persamaan f(x)
        if i == 0:
            eq_str += f"{val:.4f}"
        else:
            sign = "+" if val >= 0 else "-"
            eq_str += f" {sign} {abs(val):.4f}x^{i}"
            
        # Susun string persamaan turunan f'(x)
        # Turunan a_i * x^i adalah i * a_i * x^(i-1)
        if i > 0:
            deriv_val = val * i
            power = i - 1
            if power == 0: # Konstanta (dari a1)
                deriv_str += f"{deriv_val:.4f}"
            else:
                sign_d = "+" if deriv_val >= 0 else "-"
                # Cek jika ini suku pertama turunan, jangan pakai tanda + di depan
                if i == 1:
                    deriv_str += f"{deriv_val:.4f}" # Hapus tanda + jika awal
                else:
                    deriv_str += f" {sign_d} {abs(deriv_val):.4f}x^{power}"

    print("-" * 60)
    print(f"Persamaan Polinomial:\n{eq_str}")
    print(f"Persamaan Turunan:\n{deriv_str}")
    print("-" * 60)

    # 4. HITUNG HASIL AKHIR (SUBSTITUSI)
    # Rumus Turunan: Sum( i * a_i * x^(i-1) ) mulai dari i=1
    
    final_result = 0
    print(f"\n[PERHITUNGAN SUBSTITUSI x = {target}]")
    calculation_steps = f"f'({target}) = "
    
    for i in range(1, n):
        term = i * a_coeffs[i] * (target ** (i - 1))
        final_result += term
        
        # Tampilkan step
        if i == 1:
            calculation_steps += f"({i} * {a_coeffs[i]:.4f})"
        else:
            calculation_steps += f" + ({i} * {a_coeffs[i]:.4f} * {target}^{i-1})"
            
    print(calculation_steps)
    print("=" * 60)
    print(f"HASIL AKHIR f'({target}) = {final_result:.8f}")
    print("=" * 60)

# Jalankan Fungsi
direct_fit_detailed(x_data, y_data, x_find)