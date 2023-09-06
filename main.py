from random import *
import matplotlib.pyplot as plt
import numpy as np


def gaussian_filter(kernel_size, sigma=1, muu=0):
    x, y = np.meshgrid(np.linspace(-1, 1, kernel_size),
                       np.linspace(-1, 1, kernel_size))
    dst = np.sqrt(x ** 2 + y ** 2)

    # lower normal part of gaussian
    normal = 1 / (2.0 * np.pi * sigma ** 2)

    # Calculating Gaussian filter
    return np.exp(-((dst - muu) ** 2 / (2.0 * sigma ** 2))) * normal


kernel_size = 5
gaussian = gaussian_filter(kernel_size)

i = 0
new_list = [i for i in range(50)]
t_avg = [[0] * 50] * 3


def epsilon(eps):
    reward_list = gaussian
    sum = [0, 0, 0, 0, 0, 0]
    num = [0, 0, 0, 0, 0, 0]
    avg = [0, 0, 0, 0, 0, 0]

    l = [0] * 5
    d = 0

    def closest():
        for i in range(5):
            l[i] = abs(avg[i] - avg[5])
        d = l.index(min(l))
        return l.index(min(l))

    def exploration():
        arm = randint(0, 4)
        r = reward_list[arm][randint(0, 4)]
        sum[arm] = sum[arm] + r
        sum[5] += r
        num[arm] = num[arm] + 1
        num[5] += 1
        avg[arm] = round(sum[arm] / num[arm], 2)
        avg[5] = round(sum[5] / num[5], 2)
        change(eps)

    def change(eps):
        flag = 0
        if d == closest():
            flag = 1
        if flag == 1:
            eps = eps / 2
        else:
            eps = eps * 2

    def exploitation(i):
        r = reward_list[i][randint(0, 4)]
        sum[i] = sum[i] + r
        num[i] = num[i] + 1
        avg[i] = round(sum[i] / num[i], 2)
        change(eps)

    for i in range(1000):
        a = random()
        if a <= eps:
            exploitation(closest())
        else:
            exploration()
    return avg[5]


for i in range(50):
    t_avg[0][i] = epsilon(0.4)
    t_avg[1][i] = epsilon(0)
    t_avg[2][i] = epsilon(0.8)

xpoints = np.array(new_list)
y1 = np.array(t_avg[0])
y2 = np.array(t_avg[1])
y3 = np.array(t_avg[2])
plt.plot(xpoints, y1)
plt.plot(xpoints, y2)
plt.plot(xpoints, y3)
plt.show()
