import numpy as np
import pandas as pd

# Atur tampilan float
np.set_printoptions(precision=6, suppress=True)
pd.set_option('display.float_format', lambda x: '%.6f' % x)

print("=== LINEAR SPLINE INTERPOLATION ===\n")

# ==============================================================================
# BAGIAN 1: INPUT DATA (UBAH SESUAI SOAL)
# ==============================================================================
# 1. Masukkan Data Titik (Contoh dari Linear Spline.csv)
#    t (Waktu) dan v (Kecepatan)
t_data = np.array([0, 10, 15, 20, 22.5, 30])
v_data = np.array([0, 227.04, 362.78, 517.35, 602.97, 901.67])

# 2. (Opsional) Masukkan nilai t yang ingin dicari (Prediksi)
t_find = 16.0 
# ==============================================================================

def linear_spline_calculation(t, v, t_target=None):
    n = len(t)
    
    # List untuk menyimpan hasil perhitungan per interval
    results = []
    
    print("-" * 80)
    print(f"{'Interval':<15} | {'Slope (m)':<12} | {'Persamaan Garis v(t)':<40}")
    print("-" * 80)
    
    # 1. Loop untuk setiap interval (dari titik i ke i+1)
    for i in range(n - 1):
        t0, t1 = t[i], t[i+1]
        v0, v1 = v[i], v[i+1]
        
        # Hitung Slope (m) = (v1 - v0) / (t1 - t0)
        m = (v1 - v0) / (t1 - t0)
        
        # Format Persamaan String: v(t) = v0 + m * (t - t0)
        # Jika t0 = 0, tulis t saja. Jika tidak, tulis (t - t0)
        if t0 == 0:
            eq_str = f"{v0} + {m:.4f} * t"
        else:
            eq_str = f"{v0} + {m:.4f} * (t - {t0})"
            
        print(f"{t0:<2} < t < {t1:<5} | {m:<12.4f} | v(t) = {eq_str}")
        
        # Simpan data untuk tabel detail nanti
        results.append({
            't_start': t0,
            't_end': t1,
            'v_start': v0,
            'slope_m': m,
            'Persamaan': eq_str
        })

    print("-" * 80)
    
    # 2. Jika ada target t yang ingin dicari
    if t_target is not None:
        print(f"\n[PREDIKSI] Mencari nilai v saat t = {t_target}")
        
        # Cari interval yang sesuai
        found = False
        for res in results:
            if res['t_start'] <= t_target <= res['t_end']:
                t0 = res['t_start']
                v0 = res['v_start']
                m = res['slope_m']
                
                # Hitung Nilai
                v_result = v0 + m * (t_target - t0)
                
                print(f">> t={t_target} berada di interval {res['t_start']} < t < {res['t_end']}")
                print(f">> Menggunakan persamaan: v(t) = {res['Persamaan']}")
                print(f">> Perhitungan: {v0} + {m:.4f} * ({t_target} - {t0})")
                print(f">> Hasil v({t_target}) = {v_result:.4f}")
                found = True
                break
        
        if not found:
            print(">> Error: Nilai t berada di luar rentang data (Ekstrapolasi tidak didukung Linear Spline).")

    # 3. Tampilkan Tabel Detail (Mirip Excel)
    print("\n[TABEL DETAIL SEPERTI EXCEL]")
    df = pd.DataFrame(results)
    # Tambahkan kolom v_start untuk kemudahan baca
    df_display = df[['t_start', 't_end', 'v_start', 'slope_m', 'Persamaan']]
    print(df_display.to_string(index=False))

# Jalankan Fungsi
linear_spline_calculation(t_data, v_data, t_find)