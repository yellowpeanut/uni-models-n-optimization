import math
import matplotlib.pyplot as plt

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


def euler_method(L_bounds, N):
    C_in = 20
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
l_graph, C1_graph, C2_graph, C3_graph = euler_method(L_bounds, N)
L = parabolic_interpolation(L_bounds, l_graph, C3_graph, e)
print(f"Длина трубы, при которой концентрация целевого продукта (C3) максимальна: {L}"
      f"\nЗначение концентрации целевого продукта: {C3_graph[l_graph.index(L)]}")

fig, axis = plt.subplots(1, 2)

axis[0].set_title("Концентрация C1 по длине")
axis[0].set_xlabel("l")
axis[0].set_ylabel("C1")
axis[0].plot(l_graph, C1_graph)

# axis[0].legend()

# axis[1].set_title("Концентрация C2 по длине")
# axis[1].set_xlabel("l")
# axis[1].set_ylabel("C2")
# # axis[1].plot(l_graph, C2_graph)
#
# axis[1].legend()

axis[1].set_title("Концентрация C3 по длине")
axis[1].set_xlabel("l")
axis[1].set_ylabel("C3")
axis[1].plot(l_graph, C3_graph)
axis[1].plot(L, C3_graph[l_graph.index(L)], marker=".", color="r")

# axis[1].legend()

plt.show()
