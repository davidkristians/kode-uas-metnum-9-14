import math

# -- Parameter --
g = 9.81   # gravitasi
m = 70   # massa (kg)
c = 12   # koef hambatan udara

# -- Persamaan --
def v(t):
    term1 = (g * m) / c
    term2 = 1 - math.exp(-(c / m) * t)
    return term1 * term2

# -- ALGORITMA TRAPEZOIDAL RULE --
def hitung_trapezoidal(t0, t1, h):
    # jumlah segmen (n)
    n = int((t1 - t0) / h)
    
    # jumlahan fungsi titik tengah
    sum_mid = 0
    for i in range(1, n):
        t_curr = t0 + i * h
        sum_mid += v(t_curr)
    
    # Nilai fungsi di ujung awal dan akhir
    f_awal = v(t0)
    f_akhir = v(t1)
    
    # Rumus Trapesium
    integral = (h / 2) * (f_awal + 2 * sum_mid + f_akhir)
    
    return integral, n

# -- Process --
t_start = 0
t_end = 10
step_sizes = [1, 0.5, 0.05]

print("=" * 75)
print(f"MENCARI JARAK TEMPUH (INTEGRAL v(t)) DARI t={t_start} s.d t={t_end}")
print(f"Parameter: g={g}, m={m}, c={c}")
print("=" * 75)

for h in step_sizes:
    jarak, n = hitung_trapezoidal(t_start, t_end, h)
    print(f"Step Size (h) = {h:<5} | Segmen (n) = {n:<4} | Jarak = {jarak:.6f} meter")

print("-" * 75)

# -- Perbandingan Hasil --
term_const = (g * m) / c
def S_analitik(t):
    return term_const * (t + (m/c) * math.exp(-(c/m)*t))

jarak_eksak = S_analitik(t_end) - S_analitik(t_start)
print(f"Jarak Eksak (Analitik) = {jarak_eksak:.6f} meter")
print("=" * 75)