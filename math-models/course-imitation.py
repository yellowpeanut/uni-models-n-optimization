import math
import matplotlib.pyplot as plt



import math
import matplotlib.pyplot as plt

def randNext(n):
    l1 = math.sqrt(2)
    l2 = math.sqrt(2)
    return (l2*n) % 1 - 0.5


def find_M(z):
    res = 0
    for i in range(len(z)):
        res += z[i]
    res /= len(z)
    return res


def find_sig2(z):
    _M = find_M(z)
    res = 0
    for i in range(len(z)):
        res += (z[i]-_M)**2
    res /= len(z)
    return res


def find_process(x, k, Ns, A1, A2, sig2_x=None):
    M0 = 7
    sig2_0 = 14
    a0 = 0.08
    if sig2_x is None:
        sig2_x = find_sig2(x)
    res = 0
    for i in range(k, k+Ns):
        res += x[i]*math.sqrt(sig2_0/(sig2_x*a0*A2))*A1*math.exp(-A2*a0*(i-k))
    res = res/Ns + M0
    return res


def find_K(z, S):
    _M = find_M(z)
    res = 0
    for i in range(len(z)-S):
        res += (z[i]-_M)*(z[i+S]-_M)
    res /= (len(z)-S)
    return res


def find_Ka(sig2, a, S):
    return sig2*math.exp(-a*S)


def variation(AA1, AA2):

    _z.clear()
    Ks.clear()
    for j in range(len(_x) - _Ns):
        _z.append(find_process(_x, j, _Ns, AA1, AA2, sig2x))

    Mz = find_M(_z)
    sig2z = find_sig2(_z)

    for j in range(_S):
        Ks.append(find_K(_z, j))

    _e = 0.01
    az = 0.01
    da = 0.01
    diff2 = 0

    for j in range(_S):
        diff2 += abs(find_Ka(sig2z, az, j) - Ks[j])
    diff = diff2 + 1

    while (diff - diff2) > _e:
        diff = diff2
        az += da
        diff2 = 0
        for j in range(_S):
            diff2 += abs(find_Ka(sig2z, az, j) - Ks[j])
    az -= da
    #print("M0 = ", 18.7, " Mz = ", Mz, "\nsig2_0 = ", 23, " sig2_z = ", sig2z, "\na0 = ", 0.08, " az = ", az)
    return Mz, sig2z, az


lamb1 = math.sqrt(2)
lamb2 = math.sqrt(2)
_A1 = 1
_A2 = 1
_N = 200
_Ns = 10
_S = 5
_z = []
Ks = []

_x = []
_x.append(lamb1 % 1 - 0.5)

for o in range(_N-1):
    _x.append(randNext(_x[o]))

Mx = find_M(_x)
sig2x = find_sig2(_x)
#print("Mx = ", Mx, " sig2_x = ", sig2x)

dA = 0.001
_Mz, _sig2z, _az = variation(_A1, _A2)

_A1 -= dA
M2, s2, a2 = variation(_A1, _A2)
while abs(M2-18.7)+abs(s2-23)+abs(a2-0.08) <= abs(_Mz-18.7)+abs(_sig2z-23)+abs(_az-0.08):
    _Mz, _sig2z, _az = M2, s2, a2
    _A1 -= dA
    M2, s2, a2 = variation(_A1, _A2)
_A1 += dA

_A2 -= dA
M2, s2, a2 = variation(_A1, _A2)
while abs(M2-18.7)+abs(s2-23)+abs(a2-0.08) <= abs(_Mz-18.7)+abs(_sig2z-23)+abs(_az-0.08):
    _Mz, _sig2z, _az = M2, s2, a2
    _A2 -= dA
    M2, s2, a2 = variation(_A1, _A2)
_A2 += dA







# conversion C from % to mol/m^3
def C_proc_to_molm3(C, nu):
    ro = 2.8
    return (C * ro) / (100 * nu)


# conversion C from mol/m^3 to %
def C_molm3_to_proc(C, nu):
    ro = 2.8
    return (C*100*nu)/ro


def find_ks(T):
    J = 4.184
    A1 = 5 * (10 ** 10)
    A2 = 1.5 * (10 ** 13)
    A3 = 34 * (10 ** 17)
    A4 = 55000
    E1 = 19213*J
    E2 = 24430*J
    E3 = 35400*J
    E4 = 8000*J
    R = 8.31
    k1 = A1 * math.exp(-E1 / (R * T))
    k2 = A2 * math.exp(-E2 / (R * T))
    k3 = A3 * math.exp(-E3 / (R * T))
    k4 = A4 * math.exp(-E4 / (R * T))
    return k1, k2, k3, k4


def find_u(v):
    D = 0.1
    return (4*v)/(math.pi*D*D)


def find_new_C1(k1, C1, u, dl):
    return ((-k1*C1)/u) * dl + C1


def find_new_C2(k1, k2, k4, C1, C2, u, dl):
    return ((-k2*C2 - k4*C2 + k1*C1)/u) * dl + C2


def find_new_C3(k2, k3, C2, C3, u, dl):
    return ((-k3*C3 + k2*C2)/u) * dl + C3


def f(ks, u, C1, C2, C3, dl):
    k1, k2, k3, k4 = ks[0], ks[1], ks[2], ks[3]
    new_C1 = find_new_C1(k1, C1, u, dl)
    new_C2 = find_new_C2(k1, k2, k4, C1, C2, u, dl)
    new_C3 = find_new_C3(k2, k3, C2, C3, u, dl)
    return new_C1, new_C2, new_C3


def euler_method(L_bounds, N, C_in):
    #C_in = C_in
    T = 450
    Ls = L_bounds

    dig = len(str(abs(N)))-len(str(abs(Ls[1])))

    dl = round(Ls[1]/N, dig)

    nu1 = 0.105
    nu3 = 0.116

    v = 0.3
    u = find_u(v)
    # print(u)

    C1 = C_proc_to_molm3(C_in, nu1)
    C2 = 0
    C3 = 0

    ks = find_ks(T)

    # print(f(T, u, _C1, _C2, _C3, dl))

    C1_graph, C2_graph, C3_graph = [], [], []

    C1_graph.append(C_molm3_to_proc(C1, nu1))
    C2_graph.append(C2)
    C3_graph.append(C_molm3_to_proc(C3, nu3))

    l = 0
    l_max = L_bounds[1]
    while l < l_max:
        l = round(l+dl, dig)
        C1, C2, C3 = f(ks, u, C1, C2, C3, dl)
        C1_graph.append(C_molm3_to_proc(C1, nu1))
        C2_graph.append(C2)
        C3_graph.append(C_molm3_to_proc(C3, nu3))

    l_graph = []
    l = 0
    while l < l_max:
        l_graph.append(l)
        l = round(l+dl, dig)
    l_graph.append(l_max)

    return l_graph, C1_graph, C2_graph, C3_graph


def parabolic_interpolation(L_bounds, Ls, Cs, e):

    def arrange(x, y, ind):
        y.sort(reverse=True)
        while len(y) > 3:
            y.pop()
        ind = [Cs.index(y[0]), Cs.index(y[1]), Cs.index(y[2])]
        x = [Ls[ind[0]], Ls[ind[1]], Ls[ind[2]]]
        return x, y, ind

    dig = len(str(abs(Ls[1]))) - 2

    x = [L_bounds[0], round((L_bounds[1]-L_bounds[0])/2, dig), L_bounds[1]]
    ind = [Ls.index(x[0]), Ls.index(x[1]), Ls.index(x[2])]
    y = [Cs[ind[0]], Cs[ind[1]], Cs[ind[2]]]

    x, y, ind = arrange(x, y, ind)

    while abs(y[0]-y[1]) > e and ind[0]+1 != ind[1] and ind[0]-1 != ind[1]:
        x_new = round(
            (0.5 * (y[0]*(x[1]**2 - x[2]**2) + y[1]*(x[2]**2 - x[0]**2) + y[2]*(x[0]**2 - x[1]**2)) /
                 (y[0]*(x[1] - x[2]) + y[1]*(x[2] - x[0]) + y[2]*(x[0] - x[1]))),
            dig)
        ind_new = Ls.index(x_new)
        y_new = Cs[ind_new]
        y.append(y_new)
        x, y, ind = arrange(x, y, ind)

    return x[0]


e = 1e-6
L_bounds = [1, 10]
N = 10000

lls = []
print(_z)

for zz in _z:
    C_inn = zz

    l_graph, C1_graph, C2_graph, C3_graph = euler_method(L_bounds, N, C_inn)
    L = parabolic_interpolation(L_bounds, l_graph, C3_graph, e)

    lls.append(L)

# print(f"Длина трубы, при которой концентрация целевого продукта (C3) максимальна: {L}"
#       f"\nЗначение концентрации целевого продукта: {C3_graph[l_graph.index(L)]}")


xx = []
yy = []

h = 1
for i in range(1000):
    xx.append(h)
    yy.append((h**(1/3)+0.5))
    h+=0.01

fig, axis = plt.subplots(1, 1)

axis.set_title("")
axis.set_xlabel("C1")
axis.set_ylabel("L")
axis.plot(xx, yy)

# axis[0].legend()

# axis[1].set_title("Концентрация C2 по длине")
# axis[1].set_xlabel("l")
# axis[1].set_ylabel("C2")
# # axis[1].plot(l_graph, C2_graph)
#
# axis[1].legend()

# axis[1].set_title("Концентрация C3 по длине")
# axis[1].set_xlabel("l")
# axis[1].set_ylabel("C3")
# axis[1].plot(l_graph, C3_graph)
# axis[1].plot(L, C3_graph[l_graph.index(L)], marker=".", color="r")
#
# axis[1].legend()

plt.show()
