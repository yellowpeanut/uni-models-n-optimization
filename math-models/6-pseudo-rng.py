import math
import matplotlib.pyplot as plt
import numpy as np


def randNext(x):
    l1 = 5**13
    l2 = 3**11
    return ((l1 * x) % l2) / l2 - 0.5
    # return (x * l2) % 1 - 0.5


# M - arithmetic mean
def find_M(z):
    res = 0
    for i in range(len(z)):
        res += z[i]
    res /= len(z)
    return res


# sig2 - dispersion
def find_sig2(z):
    _M = find_M(z)
    res = 0
    for i in range(len(z)):
        res += (z[i]-_M)**2
    res /= len(z)
    return res


# K - correlational function
def find_K(z, S):
    _M = find_M(z)
    res = 0
    for i in range(len(z)-S):
        res += (z[i]-_M)*(z[i+S]-_M)
    res /= (len(z)-S)
    return res


def find_Ka(sig2, a, S):
    # print(sig2, a, S, math.exp(-a*S))
    return sig2*math.exp(-a*S)


def find_process(z, k, Ns, sig2_x, A1, A2):
    M0 = 140
    sig2_0 = 2025
    a0 = 0.13
    res = 0
    for i in range(k, k+Ns):
        res += z[i]*math.sqrt(sig2_0/(sig2_x*a0*A2))*A1*math.exp(-A2*a0*(i-k))
    res = res/Ns + M0
    return res


lamb1 = 5**13
lamb2 = 3**11
_A1 = 1
_A2 = 0.44
_N = 200
_S = 5
_Ns = 10
_z = []
Ks = []

x = []
x.append((lamb1 % lamb2)/lamb2 - 0.5)
# x.append((lamb1 % 1) - 0.5)

for j in range(_N-1):
    x.append(randNext(x[j]))

Mx = find_M(x)
sig2_x = find_sig2(x)
print("Mx = ", Mx, " sig2_x = ", sig2_x)

for j in range(_N-_Ns):
    _z.append(find_process(x, j, _Ns, sig2_x, _A1, _A2))
    # print(proc[j], " ")

for j in range(_S):
    Ks.append(find_K(_z, j))

Mz = find_M(_z)
sig2_z = find_sig2(_z)

az = 0.01
da = 0.01
diff2 = 0

for j in range(_S):
    diff2 += abs(find_Ka(sig2_z, az, j) - Ks[j])
diff = diff2+1

while diff2 < diff:
    diff = diff2
    az += da
    diff2 = 0
    for j in range(_S):
        diff2 += abs(find_Ka(sig2_z, az, j) - Ks[j])
        # print(diff2)
    # print(az, diff, diff2)
az -= da

print("M0 = ", 140, " Mz = ", Mz, "\nsig2_0 = ", 2025, " sig2_z = ", sig2_z, "\na0 = ", 0.13, " az = ", az)

# print(sig2_z)
# graph
Ka = []
TN = []
TS = []

for j in range(_N-_Ns):
    TN.append(j)
for j in range(_S):
    TS.append(j)
    Ka.append(find_Ka(sig2_z, az, j))
    # print(j, _S, find_Ka(sig2_z, az, j))


fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.set_ylabel('Знач. случ. процесса')
ax1.set_xlabel('N')

ax1.plot(TN, _z)

ax2.set_ylabel('Знач. коррел. функции')
ax2.set_xlabel('S')

ax2.plot(TS, Ks,  marker=".")
ax2.plot(TS, Ka,  marker=".")

plt.show()
