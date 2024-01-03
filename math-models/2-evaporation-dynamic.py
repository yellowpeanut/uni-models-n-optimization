import math
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


def find_M(m_in, m_sv):
    sig = 0.12
    P0 = 7900
    P1 = 7600
    S = 0.75
    return S*(((m_in-m_sv)/sig)**2+P1-P0)


def find_m_out(M):
    sig = 0.12
    P0 = 7900
    P1 = 7600
    S = 0.75
    return sig*math.sqrt(P0+M/S-P1)


def find_prime(y2, y1, dx):
    return (y2-y1) / dx


def find_new_M(m_in, m_out, Tv, M, dt):
    kt = 5000
    F = 10
    Ts = 90
    r = 2260000
    ct = 4187
    return (((r*m_in - r*m_out - kt*F*(Tv-Ts)-(m_in-m_out)*ct*Ts)*dt) / (r - ct*Ts)) + M


def find_new_C_out(C_in, C_out, m_in, m_out, M, dM, dt):
    return (((m_in * C_in - m_out * C_out - C_out * dM)*dt) / M) + C_out


def f(C_in, C_out, m_in, M, Tv, dt):
    m_out = find_m_out(M)
    M_2 = find_new_M(m_in, m_out, Tv, M, dt)
    dM = find_prime(M_2, M, dt)
    C_out2 = find_new_C_out(C_in, C_out, m_in, m_out, M_2, dM, dt)

    return [C_out2, M_2]


C_ins = [7, 6, 6]
m_ins = [5.2, 6.15, 5.2]
Tvs = [140, 140, 140]
#m_svs = [1.33, 1.33, 1.33]
C_outs = [9.4, 7.65, 8]
C_outs2 = [12.09, 6.96, 8.34]
Cs1, Cs2, Cs3 = [], [], []

dC_in = 2
dm_in = 3.5
dTv = 5

ts = [0, 500]
_dt = 0.1

# finding C_in to C_out
_C_in = C_ins[0] + dC_in
_m_sv = find_m_sv(Tvs[0])
M1 = find_M(m_ins[0], _m_sv)
_C_out = C_outs[0]
t = ts[0]
while t <= ts[1]:
    _C_out, M1 = f(_C_in, _C_out, m_ins[0], M1, Tvs[0], _dt)
    Cs1.append(_C_out)
    t += _dt

# finding m_in to C_out
_m_in = m_ins[1] + dm_in
_m_sv = find_m_sv(Tvs[1])
M2 = find_M(_m_in, _m_sv)
_C_out = C_outs[1]
t = ts[0]
while t <= ts[1]:
    _C_out, M2 = f(C_ins[1], _C_out, _m_in, M2, Tvs[1], _dt)
    Cs2.append(_C_out)
    t += _dt

# finding Tv to C_out
_Tv = Tvs[2] + dTv
_m_sv = find_m_sv(_Tv)
M3 = find_M(m_ins[2], _m_sv)
_C_out = C_outs[2]
t = ts[0]
while t <= ts[1]:
    _C_out, M3 = f(C_ins[2], _C_out, m_ins[2], M3, _Tv, _dt)
    Cs3.append(_C_out)
    t += _dt


print("C_in to C_out:\nFrom ", C_outs[0], " to ", Cs1[len(Cs1)-1], " (true is ", C_outs2[0], ")")
print("m_in to C_out:\nFrom ", C_outs[1], " to ", Cs2[len(Cs2)-1], " (true is ", C_outs2[1], ")")
print("Tv to C_out:\nFrom ", C_outs[2], " to ", Cs3[len(Cs3)-1], " (true is ", C_outs2[2], ")")


# graphs
tt = []
t = ts[0]-100
while t <= ts[1]+100:
    tt.append(t)
    t += _dt

C1, C2, C3 = [], [], []
CCs1, CCs2, CCs3 = [], [], []
for i in range(1000):
    Cs1.append(Cs1[len(Cs1)-1])
    Cs2.append(Cs2[len(Cs2) - 1])
    Cs3.append(Cs3[len(Cs3) - 1])
    CCs1.append(C_outs[0])
    CCs2.append(C_outs[1])
    CCs3.append(C_outs[2])
    C1.append(C_ins[0])
    C2.append(m_ins[1])
    C3.append(Tvs[2])
Cs1 = CCs1 + Cs1
Cs2 = CCs2 + Cs2
Cs3 = CCs3 + Cs3


for i in range(6000):
    C1.append(C_ins[0]+dC_in)
    C2.append(m_ins[1]+dm_in)
    C3.append(Tvs[2]+dTv)



fig, axis = plt.subplots(2, 3)
fig.tight_layout()

axis[0][0].plot(tt, Cs1)
axis[0][0].set_title("C_in to C_out")
axis[0][0].set_xlabel("t")
axis[0][0].set_ylabel("C_out")
axis[1][0].plot(tt, C1)
axis[1][0].set_xlabel("t")
axis[1][0].set_ylabel("C_in")

axis[0][1].plot(tt, Cs2)
axis[0][1].set_title("m_in to C_out")
axis[0][1].set_xlabel("t")
axis[0][1].set_ylabel("C_out")
axis[1][1].plot(tt, C2)
axis[1][1].set_xlabel("t")
axis[1][1].set_ylabel("m_in")

axis[0][2].plot(tt, Cs3)
axis[0][2].set_title("Tv_in to C_out")
axis[0][2].set_xlabel("t")
axis[0][2].set_ylabel("C_out")
axis[1][2].plot(tt, C3)
axis[1][2].set_xlabel("t")
axis[1][2].set_ylabel("Tv")

plt.show()