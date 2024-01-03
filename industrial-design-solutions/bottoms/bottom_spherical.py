import math


class BottomSpherical:
    def __init__(self):
        # D - millimeters
        self.D = [400, 450, 500, 600, 700, 800, 900,
                  1000, 1100, 1200, 1400, 1600, 1800,
                  2000, 2200, 2400, 2600, 2800, 3000]
        self.K = [0.58, 0.72]

    def get_params(self, user_data):
        prm = self.__calculate(user_data)
        return prm

    def get_data(self):
        return [self.D, self.K]

    def __calculate(self, user_data):
        Ks = user_data.K
        Pr = user_data.P
        R = user_data.D
        sig = user_data.sig
        c = user_data.c
        phi = user_data.phi

        sr = (Ks*Pr*R)/(phi*sig)
        s = sr + c
        if (s-c)/R <= 0.1:
            return s
        else:
            return None
