import math

def Unequal():
    try:
        n = int(input("Masukkan jumlah segmen (n): "))
        if n <= 0:
            print("n harus > 0")
            return
        batas_bawah = float(input("Masukkan batas bawah (a): "))
        batas_atas = float(input("Masukkan batas atas (b): "))
    except ValueError:
        print("Input tidak valid")
        return

    h = (batas_atas - batas_bawah) / n

    # Koefisien polinomial
    c0, c1, c2, c3, c4, c5 = 0.2, 25, -200, 675, -900, 400

    def f(t):
        return c0 + c1*t + c2*(t**2) + c3*(t**3) + c4*(t**4) + c5*(t**5)

    # Hitung nilai fungsi pada node dan tampilkan
    values = []
    for i in range(n + 1):
        t = batas_bawah + i * h
        fx = f(t)
        values.append(fx)
        print(f"f({t:.2f}) = {fx:.4f}")

    # Aturan trapezoid
    if n >= 1:
        I = h * (0.5 * values[0] + sum(values[1:-1]) + 0.5 * values[-1])
    else:
        I = 0.0

    print(f"I = {I:.4f}")

Unequal()