import matplotlib.pyplot as plt


def find_m_sv(Tv):
    # Tv - temperature of vapor
    # Ts - temperature of solution
    kt = 5000
    F = 10
    Ts = 90
    tau = 2260000
    ct = 4187
    return (kt*F*(Tv-Ts))\
           / (tau-ct*Ts)

def find_m_out(m_in, m_sv):
    return m_in - m_sv

def find_C_out(C_in, m_in, m_out):
    return m_in*C_in/m_out


def f(C_in, m_in, Tv):

    m_sv = find_m_sv(Tv)
    m_out = find_m_out(m_in, m_sv)
    C_out = find_C_out(C_in, m_in, m_out)

    return C_out


C_ins = [5, 9]
dC = 0.4
_C_in = 6

m_ins = [4.8, 7.5]
dm = 0.2
_m_in = 5.2

Tvs = [130, 150]
dTv = 0.5
_Tv = 140

C_outs_C = []
Cs = []
C_outs_m = []
ms = []
C_outs_Tv = []
Tv_s = []

c = C_ins[0]
while c <= C_ins[1]:
    C_outs_C.append(f(c, _m_in, _Tv))
    Cs.append(c)
    c += dC

m = m_ins[0]
while m <= m_ins[1]:
    C_outs_m.append(f(_C_in, m, _Tv))
    ms.append(m)
    m += dm

t = Tvs[0]
while t <= Tvs[1]:
    C_outs_Tv.append(f(_C_in, _m_in, t))
    Tv_s.append(t)
    t += dTv


print(f(7, _m_in, _Tv))
print(f(_C_in, 6.15, _Tv))
print(f(_C_in, _m_in, 140))

print(f(7+2, _m_in, _Tv))
print(f(_C_in, 6.15+3.5, _Tv))
print(f(_C_in, _m_in, 140+5))

print(find_m_sv(140))

fig, axis = plt.subplots(1, 3)
fig.tight_layout()

axis[0].plot(Cs, C_outs_C)
axis[0].set_title("C_in to C_out")
axis[0].set_xlabel("C_in")
axis[0].set_ylabel("C_out")
axis[1].plot(ms, C_outs_m)
axis[1].set_title("m_in to C_out")
axis[1].set_xlabel("m_in")
axis[1].set_ylabel("C_out")
axis[2].plot(Tv_s, C_outs_Tv)
axis[2].set_title("Tv_in to C_out")
axis[2].set_xlabel("Tv_in")
axis[2].set_ylabel("C_out")

plt.show()
