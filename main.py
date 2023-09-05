from random import *
import matplotlib.pyplot as plt
import numpy as np


i = 0
new_list = [i for i in range(1000)]


def epsilon(eps):
    t_avg = [0] * 1000
    reward_list = [1, 10, 100, 1000]
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
        r = reward_list[randint(0, 3)]
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
        r = reward_list[randint(0, 3)]
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
        t_avg[i] = avg[5]
    return t_avg


xpoints = np.array(new_list)
y1 = np.array(epsilon(0.85))
y2 = np.array(epsilon(0))
y3 = np.array(epsilon(0.01))
plt.plot(xpoints, y1)
plt.plot(xpoints,y2)
plt.plot(xpoints,y3)
plt.show()
