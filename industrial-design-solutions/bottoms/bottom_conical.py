import math


class BottomConical:
    def __init__(self):
        # D - millimeters
        self.D = [400, 500, 600, 700, 800, 900,
                  1000, 1200, 1400, 1600, 1800,
                  2000, 2200, 2400, 2500, 2600, 2800,
                  3000, 3200, 3400, 3600, 3800,
                  4000, 4500, 5000, 5600, 6300]
        self.Alpha = [30, 45, 60]

    def get_params(self, user_data):
        prm = self.__calculate(user_data)
        return prm

    def get_data(self):
        return [self.D, self.Alpha]

    def __calculate(self, user_data):
        Pr = user_data.P
        Dk = user_data.D
        sig = user_data.sig
        c = user_data.c
        alpha = user_data.alpha
        phi = user_data.phi

        skr = (Pr*Dk)/(2*sig*phi-Pr) * (1/math.cos(alpha))
        sk = skr + c
        return sk
