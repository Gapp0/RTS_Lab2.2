# Єрмоленко В.Р., ІО-71, № заліковки: 7105
# #  n w    N
# 05 14 2000 256

import random as r
import math
import matplotlib.pyplot as plt

n = 14
w_max = 2000
N = 256


def graph():
    x = [0] * N

    for i in range(n):
        A = r.randrange(2)
        W = r.randrange(w_max)
        f = r.randrange(1e9)
        for t in range(N):
            x[t] += A * math.sin(W * t + f)
    return x


def fft(x: list):
    N = len(x)
    fftt = [[0] * 2 for i in range(N)]
    for i in range(N // 2):
        array1 = [0] * 2
        array2 = [0] * 2
        for j in range(N // 2):
            cos = math.cos(4 * math.pi * i * j / N)
            sin = math.sin(4 * math.pi * i * j / N)
            array1[0] += x[2 * j + 1] * cos # real
            array1[1] += x[2 * j + 1] * sin # imag
            array2[0] += x[2 * j] * cos # real
            array2[1] += x[2 * j] * sin # imag
        cos = math.cos(2 * math.pi * i / N)
        sin = math.sin(2 * math.pi * i / N)
        fftt[i][0] = array2[0] + array1[0] * cos - array1[1] * sin # real
        fftt[i][1] = array2[1] + array1[0] * sin + array1[1] * cos # imag
        fftt[i + N // 2][0] = array2[0] - (array1[0] * cos - array1[1] * sin) # real
        fftt[i + N // 2][1] = array2[1] - (array1[0] * sin + array1[1] * cos) # imag
    return fftt


X = graph()
fftt = fft(X)

data_fft = [math.sqrt(fftt[i][0] ** 2 + fftt[i][1] ** 2) for i in range(N)]

plt.plot([i for i in range(N)], X)
plt.show()
plt.plot([i for i in range(N)], data_fft)
plt.show()