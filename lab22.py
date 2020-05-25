# Єрмоленко В.Р., ІО-71, № заліковки: 7105
# #  n w    N
# 05 14 2000 256

# Додаткове завдання: реалізувати обчислення "половинок" у потоках та порівняти час виконання

import random as r
import math
import matplotlib.pyplot as plt
import datetime
import concurrent.futures

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


def fft_I(x: list):
    return fft(x[:len(x)//2])


def fft_II(x: list):
    return fft(x[len(x)//2:])


def parall():
    X = graph()
    with concurrent.futures.ThreadPoolExecutor() as exec:
        fft_one = exec.submit(fft_I, X)
        fft_two = exec.submit(fft_II, X)
        result_I = fft_one.result()
        result_II = fft_two.result()
        return result_I, result_II


single_t = datetime.datetime.now()

X = graph()
fftt = fft(X)

single_t = datetime.datetime.now() - single_t

double_t = datetime.datetime.now()

parall()

double_t = datetime.datetime.now() - double_t

print('Single:', single_t, ', double:', double_t)
exit(0)

data_fft = [math.sqrt(fftt[i][0] ** 2 + fftt[i][1] ** 2) for i in range(N)]

plt.plot([i for i in range(N)], X)
plt.show()
plt.plot([i for i in range(N)], data_fft)
plt.show()
