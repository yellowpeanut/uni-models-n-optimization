import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np


def find_T0(l):
    return 20 + 5*l - l*l
def find_T_in(t):
    return 0.1*t*t + 5*math.sin(t) + 20


def find_new_T(T, da):
    kt = 6500
    ct = 4190
    ro = 1000
    Tt = 80
    D = 0.05

    return ((Tt - T)*4*kt/(ct*ro*D))*da + T


def appendVals(T, a, b):
    T_arr.append(T)
    a_arr.append(a)
    b_arr.append(b)
    l_arr.append(u*(a-b))
    t_arr.append(a+b)


# initial values
T_arr, a_arr, b_arr, l_arr, t_arr = [], [], [], [], []
L = 1
u = 0.2
t_max = 10
ts = L/u


da = 0.3
db = 0.2


# computing

# first domain
b = -ts/2
a = -b
T = find_T0(-2*u*b)
while b <= 0:
    a = -b
    T = find_T0(-2 * u * b)
    while a <= b + ts:
        appendVals(T, a, b)
        T = find_new_T(T, da)
        a += da
    b += db

# second domain
b = 0
a = b
T = find_T_in(2*b)
while b <= (t_max - ts)/2:
    a = b
    T = find_T_in(2 * b)
    while a <= b + ts:
        appendVals(T, a, b)
        T = find_new_T(T, da)
        a += da
    b += db

# third domain
b = (t_max - ts) / 2
a = b
T = find_T_in(2*b)
while b <= t_max/2:
    a = b
    T = find_T_in(2 * b)
    while a <= -b + ts:
        appendVals(T, a, b)
        T = find_new_T(T, da)
        a += da
    b += db


print(len(l_arr), len(t_arr), len(T_arr))

# graph


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# x = np.reshape(l_arr, (len(l_arr), len(t_arr)))
# y = np.reshape(t_arr, (len(l_arr), len(t_arr)))
# z = np.reshape(T_arr, (len(l_arr), len(t_arr)))

ax.scatter(l_arr, t_arr, T_arr)

plt.show()
