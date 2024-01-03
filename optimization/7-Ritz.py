import math
import matplotlib.pyplot as plt


def f(t, c1, c2):
    global lamb
    return lamb / (2 - 2 * lamb) * t * t / 2 + c1 * t + c2


def fa(c1, c2):
    return f(0, c1, c2)


def fb(c1, c2):
    return f(1, c1, c2)


def f1(t, c1):
    global lamb
    return lamb / (2 - 2 * lamb) * t + c1


def f1a(c1):
    return f1(0, c1)


def f1b(c1):
    return f1(1, c1)






def S(x, x1):
    return x - x1*x1


def J(x1):
    return x1*x1


def H(x, x1, la):
    return J(x1)+la*S(x, x1)


def W0(t):
    return t*.25


def Wi(t, p):
    return t**p * (t-1)**p


def W1(t, p):
    return Wi(t, p) * (t*t+t-1)


def W2(t, p):
    return Wi(t, p) * (math.sin(t/2))


def W3(t, p):
    return Wi(t, p) * (math.e**t)


def W4(t, p):
    return Wi(t, p) * (t*t*t-3*t+2)


def W(t, a, n):
    p = 2
    if n == 2:
        return a[1]*W2(t, p) + a[0]*W1(t, p) + W0(t)
    elif n == 3:
        return a[2]*W3(t, p) + a[1]*W2(t, p) + a[0]*W1(t, p) + W0(t)
    elif n == 4:
        return a[3]*W4(t, p) + a[2]*W3(t, p) + a[1]*W2(t, p) + a[0]*W1(t, p) + W0(t)


def Wp1(t, a, n):
    h = 0.00001
    p = 1
    # return (W(t + h, a, n) - W(t + h, a, n))/(2*h)
    if n == 2:
        return a[1]*((W2(t+h, p)-W2(t-h, p))/(h*2)) + a[0]*((W1(t+h, p)-W1(t-h, p))/(h*2)) + (W0(t+h)-W0(t-h))/(h*2)
    elif n == 3:
        return a[2]*((W3(t+h, p)-W3(t-h, p))/(h*2)) + a[1]*((W2(t+h, p)-W2(t-h, p))/(h*2)) + a[0]*((W1(t+h, p)-W1(t-h, p))/(h*2)) + (W0(t+h)-W0(t-h))/(h*2)
    elif n == 4:
        return a[3]*((W4(t+h, p)-W4(t-h, p))/(h*2)) + a[2]*((W3(t+h, p)-W3(t-h, p))/(h*2)) + a[1]*((W2(t+h, p)-W2(t-h, p))/(h*2)) + a[0]*((W1(t+h, p)-W1(t-h, p))/(h*2)) + (W0(t+h)-W0(t-h))/(h*2)


def ritz(ta, tb, a, la, n, e):

    def find_diff():
        t = dt
        _diff = 0
        for j in range(n):
            x = W(t, a, n)
            x1 = Wp1(t, a, n)
            _prev_diff = _diff
            #_diff += (H(x, x1, la[j])-H(true_x(t), true_x1(t), la[j]))
            _diff += H(x, x1, la)
            #print(_diff)
            t += dt
        return abs(_diff)

    dlt = e*10
    dt = (tb-ta)/(n+1)
    diff = find_diff()
    for i in range(n):
        #print(i, n)
        a[i] += dlt
        new_diff = find_diff()
        if new_diff < diff:
            while new_diff < diff:
                #print(i, n, new_diff, diff)
                diff = new_diff
                a[i] += dlt
                new_diff = find_diff()
            a[i] -= dlt
#            ad = [[a[i], new_diff], [a[i]-dlt, diff]]
#            a[i] -= dlt/2
#            new_diff = find_diff()
#            while new_diff > e:
#                if abs(abs(new_diff)-abs(a[0][1])) < abs(abs(new_diff)-abs(a[1][1])):
#                    ad[1] = a[i], new_diff
#                else:
#                    ad[0] = a[i], new_diff
#                a[i] = (ad[0][0]+ad[1][0])/2
#                new_diff = find_diff()

        else:
            a[i] -= dlt*2
            new_diff = find_diff()
            while new_diff < diff:
                #print(i, n, new_diff, diff)
                diff = new_diff
                a[i] -= dlt
                new_diff = find_diff()
            a[i] += dlt
#            ad = [[a[i], new_diff], [a[i]+dlt, diff]]
#            a[i] += dlt/2
#            new_diff = find_diff()
#            while new_diff > e:
#                if abs(abs(new_diff)-abs(ad[0][1])) < abs(abs(new_diff)-abs(ad[1][1])):
#                    ad[1] = a[i], new_diff
#                else:
#                    ad[0] = a[i], new_diff
#                a[i] = (ad[0][0]+ad[1][0])/2
#                new_diff = find_diff()


    #print(a)

    return a


def find_lamb(ta, tb, a, la, res, n, e):

    def find_res():
        x = W(tb, aa, n)
        x1 = Wp1(tb, aa, n)
        return S(x, x1)

    aa = a.copy()
    lam = la
    dlt = e*10
    # for i in range(n):
    #     lam[i] += dlt
    #     aa = ritz(ta, tb, aa, lam, n, e)
    #     result = find_res()
    #     while abs(result-res) > dlt:
    #         lam[i] += dlt
    #         aa = ritz(ta, tb, aa, lam, n, e)
    #         #new_result = find_res()
    #         #print("aaaaa", i, "a= ", aa, "la i = ", lam[i])
    #         #print(new_result, result)
    #         #if abs(new_result - res) <= abs(result-res):
    #         #    result = new_result
    #         #else:
    #         #    break
    #         result = find_res()
    #         print(result, lam[i])
        #lam[i] -= dlt
        #print("\nlam = ", lam[i], "\n")
        # if N == 0:
        #     lam[i] -= dlt
        #     aa = ritz(ta, tb, aa, lam, n, e)
        #     new_result = find_res()
        #     while abs(new_result - res) < abs(result-res):
        #         result = new_result
        #         print(result)
        #         lam[i] -= dlt
        #         aa = ritz(ta, tb, aa, lam, n, e)
        #         new_result = find_res()

    # lam[n] += dlt
    # xx = W(tb, aa, n)
    # xx1 = Wp1(tb, aa, n)
    # result = H(xx, xx1, lam[n])
    # N = 10000
    # while abs(result-res) > dlt:
    #     N -= 1
    #     lam[n] += dlt
    #     #new_result = H(xx, xx1, lam[n])
    #     #if abs(new_result - res) <= abs(result - res):
    #     #    result = new_result
    #     #else:
    #     #    break
    #     result = find_res()
    #     print(result)
    #lam[n] -= dlt
    #print("\nlam = ", lam[n], "\n")
    # if N == 0:
    #     lam[n] -= dlt
    #     aa = ritz(ta, tb, aa, lam, n, e)
    #     new_result = find_res()
    #     while abs(new_result - res) < abs(result - res):
    #         result = new_result
    #         print(result)
    #         lam[n] -= dlt
    #         aa = ritz(ta, tb, aa, lam, n, e)
    #         new_result = find_res()

    aa = ritz(ta, tb, aa, lam, n, e)
    result = find_res()
    while abs(result-res) > dlt*10:
        lam += dlt
        aa = ritz(ta, tb, aa, lam, n, e)
        result = find_res()
        # print(result)

    return aa, lam, result


def true_x(t):
    return 0.11 * t*t + 0.14 * t
def true_x1(t):
    return 0.22*t + 0.14


_e = 1e-5
# lamb = [_e, _e, _e, _e, _e]
lamb = _e
_a = [0.125, 0.125, 0.125, 0.125]
_ta = 0
_tb = 1
_xa = 0
_xb = .25
_res = .08333

# _a2, _a3, _a4 = _a.copy(), _a.copy(), _a.copy()
# aa2, aa3, aa4 = ritz(_ta, _tb, _a2, lamb, 2, _e), ritz(_ta, _tb, _a3, lamb, 3, _e), ritz(_ta, _tb, _a4, lamb, 4, _e)
# print(aa2, aa3, aa4)
#print(H(W(0.33, [0.039, 2], 2), Wp1(0.33, [0.039, 2], 2), 0.01))
#print(H(W(0.33, [0.039, 1], 2), Wp1(0.33, [0.039, 1], 2), 0.01))
#print(H(W(0.33, [0.039, 0.5], 2), Wp1(0.33, [0.039, 0.5], 2), 0.01))
a2, la2, res2 = find_lamb(_ta, _tb, _a, lamb, _res, 2, _e)
a3, la3, res3 = find_lamb(_ta, _tb, _a, lamb, _res, 3, _e)
a4, la4, res4 = find_lamb(_ta, _tb, _a, lamb, _res, 4, _e)

print(a2, a3, a4)
print(la2, la3, la4)
#print(H(W(0.4, [1.318, 2, 3.0], 3), Wp1(0.4, [1.318, 2, 3.0], 3), 0.01))
#print(H(W(0.4, [1.318, 2, 2.0], 3), Wp1(0.4, [1.318, 2, 2.0], 3), 0.01))
#print(H(W(0.4, [1.318, 2, 1.0], 3), Wp1(0.4, [1.318, 2, 1.0], 3), 0.01))
#print(H(W(0.4, [1.318, 2, 4.0], 3), Wp1(0.4, [1.318, 2, 4.0], 3), 0.01))

#for j in range(11):
#    x = true_x(j*.1)
#    x1 = .22*j*.1+.14
#    print("x = ", x, "y = ", H(x, x1, 0.305))

# for j in range(11):
#    x = true_x(j*.1)
#    x1 = .22*j*.1+.14
#    print("x = ", x, "y = ", H(x, x1, 0.305), "S = ", S(x, x1))

figure, axis = plt.subplots(1, 3)

t_points = []
x_points2 = []
x_points3 = []
x_points4 = []
x_true_points = []
m = 10
for i in range(m):
    t_points.append((_tb * i) / (m - 1))
    x_true_points.append(true_x(t_points[-1]))
    x_points2.append(W(t_points[-1], a2, 2))
    x_points3.append(W(t_points[-1], a3, 3))
    x_points4.append(W(t_points[-1], a4, 4))

axis[0].plot(t_points, x_true_points, color="r")
axis[0].plot(t_points, x_points2, color="b")
axis[0].set_title("n = 2")
axis[1].plot(t_points, x_true_points, color="r")
axis[1].plot(t_points, x_points3, color="b")
axis[1].set_title("n = 3")
axis[2].plot(t_points, x_true_points, color="r")
axis[2].plot(t_points, x_points4, color="b")
axis[2].set_title("n = 4")

plt.show()
