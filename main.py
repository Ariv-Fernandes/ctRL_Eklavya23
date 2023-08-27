from random import *

i = 0
reward_list = [1, 10, 100, 1000]
sum = [0, 0, 0, 0, 0, 0]
num = [0, 0, 0, 0, 0, 0]
avg = [0, 0, 0, 0, 0, 0]
eps = 0.85
l = [0] * 5


def closest():
    for i in range(5):
        l[i] = abs(avg[i] - avg[5])
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
    closest()

def change(eps):
    if avg[5] < avg[i]:
        eps = eps/2
    else:
        eps = eps*2


def exploitation(i):
    r = reward_list[randint(0, 3)]
    sum[i] = sum[i] + r
    num[i] = num[i] + 1
    avg[i] = round(sum[i] / num[i], 2)
    closest()


for _ in range(1000):
    a = random()
    if a <= eps:
        exploration()
    else:
        exploitation(closest())
print(sum[5])
