import math

def simpsonOneperThree():
    n = int(input("Masukkan jumlah segmen (n): "))
    batas_bawah = float(input("Masukkan batas bawah (a): "))
    batas_atas = float(input("Masukkan batas atas (b): "))
    h = (batas_atas - batas_bawah) / n
    x0 = 0.2
    x1 = 25
    x2 = -200
    x3 = 675
    x4 = -900
    x5 = 400

    for i in range(n + 1):
        t = batas_bawah + i * h
        x_i = x0 + x1*t + x2*(t**2) + x3*(t**3) + x4*(t**4) + x5*(t**5)
        print(f"f({t:.2f}) = {x_i:.4f}")

        if i == 0:
            x0 = x_i
        elif i == n:
            xn = x_i

    I = (h / 3) * (x0 + 4 * sum([x0 + x1*(batas_bawah + j * h) + x2*((batas_bawah + j * h)**2) + x3*((batas_bawah + j * h)**3) + x4*((batas_bawah + j * h)**4) + x5*((batas_bawah + j * h)**5) for j in range(1, n, 2)]) + 2 * sum([x0 + x1*(batas_bawah + j * h) + x2*((batas_bawah + j * h)**2) + x3*((batas_bawah + j * h)**3) + x4*((batas_bawah + j * h)**4) + x5*((batas_bawah + j * h)**5) for j in range(2, n-1, 2)]) + xn)
    print(f"I = {I:.4f}")
    print(h)


simpsonOneperThree()