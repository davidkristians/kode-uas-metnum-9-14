import math

def trapezoidal():
    n = int(input("Masukkan jumlah segmen (n): "))
    batas_bawah = float(input("Masukkan batas bawah (a): "))
    batas_atas = float(input("Masukkan batas atas (b): "))
    h = (batas_atas - batas_bawah) / n
    
    g = 9.8
    m = 68.1
    c = 12.5
    gm = (g*m)/c
    cm = c/m
    print(h)
# Rumus f(xi) = (g*m/c)*(1 - exp(- (c/m)*xi))
    for i in range(n + 1):
        t = batas_bawah + i * h
        x_i = gm * (1 - math.exp(-(cm) * t))
        print(f"f({t:.2f}) = {x_i:.4f}")

        if i == 0:
            x0 = x_i
        elif i == n:
            xn = x_i

    I = (h / 2) * (x0 + 2 * sum([gm * (1 - math.exp(-(cm) * (batas_bawah + j * h))) for j in range(1, n)]) + xn)
    print(f"I = {I:.4f}")
    print(h)


trapezoidal()