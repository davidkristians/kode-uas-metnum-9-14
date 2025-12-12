import numpy as np
import pandas as pd
import math

# Atur presisi output
np.set_printoptions(precision=7, suppress=True)

# =========================================================================
# 1. DEFINISI MODEL DAN TURUNAN PARSIAL (Growth/Creation Model)
# Model: f(x, a0, a1) = a0 * (1 - e^(-a1 * x))
# =========================================================================

def model_function(x, a):
    """Fungsi Model Non-Linear f(x, a0, a1)."""
    a0, a1 = a[0], a[1]
    return a0 * (1 - np.exp(-a1 * x))

def create_jacobian_Z(x, a):
    """Membentuk Matriks Jacobian [Z] (Turunan Parsial)"""
    a0, a1 = a[0], a[1]
    
    # Kolom 1: Turunan terhadap a0 (df/da0) = 1 - e^(-a1 * x)
    z0 = (1 - np.exp(-a1 * x))
    
    # Kolom 2: Turunan terhadap a1 (df/da1) = a0 * x * e^(-a1 * x)
    z1 = a0 * x * np.exp(-a1 * x)
    
    Z = np.stack([z0, z1], axis=1)
    z_names = ['z0 (df/da0)', 'z1 (df/da1)']
    return Z, z_names

# =========================================================================
# 2. INPUT DATA & PARAMETER ITERASI
# =========================================================================
# Data yang Diberikan Pengguna
x_i = np.array([0.25, 0.75, 1.25, 1.75, 2.25]) 
y_i = np.array([0.28, 0.57, 0.68, 0.74, 0.79])
n = len(y_i)

# Parameter Gauss-Newton yang diminta
a_guess = np.array([1.0, 1.0]) # Tebakan Awal [a0=1, a1=1]
max_iterations = 100
tolerance = 1e-6 
m_vars = len(a_guess)

# =========================================================================
# 3. PROSES ITERASI GAUSS-NEWTON (DETIL PER STEP)
# =========================================================================

a_current = a_guess.copy()
k = 0
Sr_list = []

print("=" * 100)
print(f"       REGRESI NON-LINEAR GAUSS-NEWTON (Model: a0 * (1 - e^(-a1*x)))")
print("=" * 100)
print(f"Tebakan Awal: a0={a_guess[0]:.7f}, a1={a_guess[1]:.7f}")

for k in range(max_iterations):
    print("\n" + "=" * 100)
    print(f"### ITERASI {k} (Tebakan Awal: a0={a_current[0]:.7f}, a1={a_current[1]:.7f})")
    print("=" * 100)

    # 1. Hitung Matriks Jacobian [Z] dan Prediksi y
    Z, z_names = create_jacobian_Z(x_i, a_current)
    y_pred = model_function(x_i, a_current)
    
    # 2. Hitung Vektor Residual {D} dan Sr (SSE)
    D = (y_i - y_pred).reshape(-1, 1) # D = y_measured - f(x, a_current)
    Sr = np.sum(D**2)
    Sr_list.append(Sr)
    
    # --- OUTPUT STEP 1 & 2: TABEL JACOBIAN DAN RESIDUAL ---
    print("\n## STEP 1 & 2: TITIK BARIS JACOBIAN [Z] DAN RESIDUAL {D}")
    print("-" * 100)
    
    # Siapkan data untuk DataFrame Z, D, dan y_pred
    df_Z_D = pd.DataFrame({
        'xi': x_i,
        'yi_asli': y_i,
        'y_pred_f(x)': y_pred,
        z_names[0]: Z[:, 0], # df/da0 (Z0)
        z_names[1]: Z[:, 1], # df/da1 (Z1)
        'D (yi - f(x))': D.flatten(),
        'D^2': D.flatten()**2
    })
    sum_row_Z_D = df_Z_D.sum(numeric_only=True)
    sum_row_Z_D.name = 'Σ'
    df_Z_D_final = pd.concat([df_Z_D, sum_row_Z_D.to_frame().T])
    
    print(df_Z_D_final.round(7).to_string())
    print("-" * 100)
    print(f"SSE / Sr (Sum of Squares of Error) Iterasi {k} = {Sr:.7f}")
    
    # 3. Hitung Matriks Sistem Persamaan Normal
    Z_T_Z = Z.T @ Z
    Z_T_D = Z.T @ D
    
    # --- OUTPUT STEP 3: SISTEM PERSAMAAN NORMAL ---
    print("\n## STEP 3: SISTEM PERSAMAAN NORMAL [Z]T[Z] {ΔA} = [Z]T{D}")
    print("-" * 100)
    print("Matriks [Z]T[Z] (Sisi Kiri):")
    print(Z_T_Z.round(7))
    print("\nVektor Sisi Kanan [Z]T{D}:")
    print(Z_T_D.round(7).T)

    # 3. Lanjutkan menyelesaikan untuk Koreksi {Delta A}
    try:
        Delta_A = np.linalg.solve(Z_T_Z, Z_T_D)
    except np.linalg.LinAlgError:
        print(f"\n[ERROR] Iterasi {k}: Matriks Singular. Hentikan iterasi.")
        break
    
    # 4. Update Koefisien
    a_new = a_current + Delta_A.flatten()
    
    # --- OUTPUT STEP 3 LANJUTAN: DELTA A DAN KOEFISIEN BARU ---
    Delta_A0 = Delta_A[0,0]
    Delta_A1 = Delta_A[1,0]
    
    print("\nSolusi Koreksi Koefisien {ΔA}:")
    print(f"Δa0 = {Delta_A0:.7f}")
    print(f"Δa1 = {Delta_A1:.7f}")
    
    print("\nKoefisien Baru (a^k+1 = a^k + Δa):")
    print(f"a0_baru = {a_new[0]:.7f}")
    print(f"a1_baru = {a_new[1]:.7f}")
    
    # 5. Cek Kriteria Berhenti
    max_delta = np.max(np.abs(Delta_A))
    
    # Jika ΔA terlalu kecil, hentikan loop
    if max_delta < tolerance:
        a_current = a_new
        print("-" * 100)
        print(f"\n[SUKSES] Konvergensi tercapai pada iterasi {k} (Max Delta: {max_delta:.7f})")
        break
        
    a_current = a_new
else:
    print("-" * 100)
    print(f"\n[PERINGATAN] Mencapai batas maksimal iterasi ({max_iterations}). Konvergensi mungkin belum tercapai.")

# =========================================================================
# 4. HASIL AKHIR & METRIK KUALITAS
# =========================================================================
a_final = a_current
Sr_final = np.sum((y_i - model_function(x_i, a_final))**2)

y_pred_final = model_function(x_i, a_final)
y_bar = np.mean(y_i)
St_y = np.sum((y_i - y_bar)**2) 

r2_asli = (St_y - Sr_final) / St_y
r_asli = np.sqrt(r2_asli)
Sy_x_asli = np.sqrt(Sr_final / (n - m_vars))
Sy_asli = np.sqrt(St_y / (n - 1))

print("\n" + "=" * 100)
print("### HASIL REGRESI NON-LINEAR FINAL ###")
print("=" * 100)
print(f"Koefisien Final: a0 = {a_final[0]:.7f}, a1 = {a_final[1]:.7f}")
print(f"Persamaan Final: y = {a_final[0]:.4f} * (1 - e^(-{a_final[1]:.4f} * x))")

print("\nANALISIS KUALITAS MODEL:")
print("-" * 50)
print(f"Sr (Sum of Residuals)       = {Sr_final:.7f}")
print(f"Sy/x (Std Error Estimasi)   = {Sy_x_asli:.7f}")
print(f"r^2 (Koef. Determinasi)     = {r2_asli:.7f}")
print(f"r (Koef. Korelasi)          = {r_asli:.7f}")
print("-" * 50)