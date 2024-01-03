import math
import matplotlib.pyplot as plt


def S(x, x1):
    return x - x1*x1
def J(x1):
    return x1*x1
def H(x, x1, la):
    return J(x1)+(la*S(x, x1))



def local_variations(t_ab, x_ab, la, n, e):

    def find_diff():
        _diff = 0
        t = dt
        for j in range(1, n):
            x = xs[j]
            x1 = (x - xs[j-1])/(dt)
            _diff += H(x, x1, la)
            #_diff += (H(x, x1, la[j])-H(true_x(t), true_x1(t), la[j]))
            # _diff += abs(H(x, x1, la) - H(true_x(t), true_x1(t), la))
            # print(x, x1, "\n", true_x(t), true_x1(t))
            # print(H(x, x1, la), "\n", H(true_x(t), true_x1(t), la))
            # print(x, x1, _diff)
            # print(_diff)
            t += dt
        return _diff

    dlt = e*10
    xs = []
    ts = []
    dltx = (x_ab[1]-x_ab[0])/(n + 1)
    dt = (t_ab[1] - t_ab[0])/(n + 1)
    for i in range(n):
        xs.append(dltx*(i+1))
        ts.append(dt*(i+1))
    xs = [x_ab[0]] + xs + [x_ab[1]]
    ts = [t_ab[0]] + ts + [t_ab[1]]
    for i in range(1, n):
        # print(n, xs[i])
        diff = find_diff()
        xs[i] += dlt
        new_diff = find_diff()
        if new_diff < diff:
            while new_diff < diff:
                # print(i, n, new_diff, diff, xs[i])
                diff = new_diff
                xs[i] += dlt
                new_diff = find_diff()
            xs[i] -= dlt
        else:
            xs[i] -= dlt * 2
            new_diff = find_diff()
            while new_diff < diff:
                # print(i, n, new_diff, diff, xs[i])
                diff = new_diff
                xs[i] -= dlt
                new_diff = find_diff()
            xs[i] += dlt

    return xs, ts


def find_lamb(t_ab, x_ab, la, res, n, e):

    def find_res():
        _sum = 0
        for j in range(1, n):
            x = xs[j]
            x1 = (x - xs[j-1])/dt
            _sum += S(x, x1)
        return _sum

    lam = la
    dlt = e*10
    dt = (t_ab[1] - t_ab[0]) / (n + 1)
    xs, ts = local_variations(t_ab, x_ab, la, n, e)
    result = find_res()
    while abs(result-res) > dlt*10:
        lam += dlt
        xs, ts = local_variations(t_ab, x_ab, la, n, e)
        result = find_res()
        print(result, lam, xs)
    # print(result)
    return xs, ts, lam


def true_x(t):
    return 0.11 * t*t + 0.14 * t
def true_x1(t):
    return 0.22*t + 0.14


_e = 1e-5
# lamb = [_e, _e, _e, _e, _e]
lamb = _e
_a = [0.125, 0.125, 0.125, 0.125, 0.125]
_ta = 0
_tb = 1
_xa = 0
_xb = .25
_res = .08333

x3, t3, la3 = find_lamb([_ta, _tb], [_xa, _xb], lamb, _res, 3, _e)
x4, t4, la4 = find_lamb([_ta, _tb], [_xa, _xb], lamb, _res, 4, _e)
x5, t5, la5 = find_lamb([_ta, _tb], [_xa, _xb], lamb, _res, 5, _e)

# print(t3, x3, la3)
# print(t4, x4, la4)
# print(t5, x5, la5)
#
# x3, t3 = local_variations([_ta, _tb], [_xa, _xb], lamb, 3, _e)
# x4, t4 = local_variations([_ta, _tb], [_xa, _xb], lamb, 4, _e)
# x5, t5 = local_variations([_ta, _tb], [_xa, _xb], lamb, 5, _e)

print(x3)
print(x4)
print(x5)

figure, axis = plt.subplots(1, 3)

t_points = []
x_true_points = []
m = 10
for i in range(m):
    t_points.append((_tb * i) / (m - 1))
    x_true_points.append(true_x(t_points[-1]))


axis[0].plot(t_points, x_true_points, color="r")
axis[0].plot(t3, x3, color="b")
axis[0].set_title("n = 3")
axis[1].plot(t_points, x_true_points, color="r")
axis[1].plot(t4, x4, color="b")
axis[1].set_title("n = 4")
axis[2].plot(t_points, x_true_points, color="r")
axis[2].plot(t5, x5, color="b")
axis[2].set_title("n = 5")

plt.show()
