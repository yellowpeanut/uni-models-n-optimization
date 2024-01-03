import math
import matplotlib.pyplot as plt

# conversion C from % to mol/m^3
def C_proc_to_molm3(C):
    # mol/kg
    nu_et = 35.65
    ro = 1.4
    return (C * ro) / (100 * nu_et)


# conversion C from % to mol/m^3
def C_molm3_to_proc(C):
    # mol/kg
    nu_et = 35.65
    ro = 1.4
    return (C*100*nu_et)/ro


def find_k1k2(T):
    A1 = 2 * (10 ** 11)
    A2 = 8 * (10 ** 12)
    E1 = 251000
    E2 = 297000
    R = 8.31
    k1 = A1 * math.exp(-E1 / (R * T))
    k2 = A2 * math.exp(-E2 / (R * T))
    return k1, k2


def find_new_C1(m, k1, C1, dl):
    D = 0.1
    ro = 1.4
    return (-k1*C1*math.pi*D*D*ro/4)/m * dl + C1


def find_new_C2(m, k1, k2, C1, C2, dl):
    D = 0.1
    ro = 1.4
    return ((k1*C1-k2*C2)*math.pi*D*D*ro/4)/m * dl + C2


def f(T, m, C1, C2, dl):
    k1, k2 = find_k1k2(T)
    new_C1 = find_new_C1(m, k1, C1, dl)
    new_C2 = find_new_C2(m, k1, k2, C1, C2, dl)
    return new_C1, new_C2


_C_in = 30
_m = 3
_Ts = [1310, 1360]
L = 120
dl = 0.5

dT = 25
dC = 5
dm = 0.15

_C1 = C_proc_to_molm3(_C_in)
_C2 = 0

T_graph, l_graph, C1_graph, C2_graph = [], [], [], []

_T = _Ts[0]
while _T <= _Ts[1]:
    T_graph.append(_T)
    _l = 0
    _C1 = C_proc_to_molm3(_C_in)
    _C2 = 0
    C1_graph.append([C_molm3_to_proc(_C1)])
    C2_graph.append([C_molm3_to_proc(_C2)])
    C_ind = len(C1_graph)-1
    while _l < L:
        _l += dl
        _C1, _C2 = f(_T, _m, _C1, _C2, dl)
        C1_graph[C_ind].append(C_molm3_to_proc(_C1))
        C2_graph[C_ind].append(C_molm3_to_proc(_C2))
        print(f"{_C1} - {C_molm3_to_proc(_C1)}%")
        print(f"{_C2} - {C_molm3_to_proc(_C2)}%")
        print("\n")

    _T += dT

_l = 0
while _l <= L:
    l_graph.append(_l)
    _l += dl

fig, axis = plt.subplots(2, len(T_graph))
fig.tight_layout()
for i in range(len(T_graph)):
    axis[0][i].plot(l_graph, C1_graph[i])
    axis[0][i].set_title(f"T = {T_graph[i]}")
    axis[0][i].set_xlabel("l")
    axis[0][i].set_ylabel("C1")
    axis[1][i].plot(l_graph, C2_graph[i])
    axis[1][i].set_title(f"T = {T_graph[i]}")
    axis[1][i].set_xlabel("l")
    axis[1][i].set_ylabel("C2")

plt.show()
