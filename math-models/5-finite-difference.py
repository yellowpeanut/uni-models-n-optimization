import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

# T(0,x)
def phi(x):
    return 20 + 5*x + x*x
# T(t,0)
def f1(t):
    return 0.001*t*t+5*math.sin(t)+20
# T(t,X)
def f2(t):
    return 20+4*math.cos(t)


def find_new_T(T2, T1, T0, dt, dx):
    a = 1.3*10**-2
    return (a*dt/(dx*dx))*(T2 - 2*T1 + T0) + T1


X = 1
t_max = 100
dx = 0.1
# dt controls graph's density
# dt = 0.5*dx*dx
dt = 0.5*dx*dx*25


Tji = [[]]

t = 0
x = 0
while x+dx < X:
    Ti = phi(x)
    Tji[0].append(Ti)
    x += dx
Tji[0].append(f2(t))
t += dt

j = 1
while t < t_max:
    Tj = f1(t)
    Tji.append([Tj])
    i = 1
    x = dx
    while x+dx < X:
        Ti = find_new_T(Tji[j - 1][i + 1], Tji[j - 1][i], Tji[j - 1][i - 1], dt, dx)
        Tji[j].append(Ti)
        x += dx
        i += 1
    Tji[j].append(f2(t))
    t += dt
    j += 1

# graph
Tt = []
Tx = []
T_arr = []
for j in range(len(Tji)):
    for i in range(len(Tji[j])):
        Tt.append(dt*j)
        Tx.append(dx*i)
        T_arr.append(Tji[j][i])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(Tx, Tt, T_arr, marker=".")

plt.show()
