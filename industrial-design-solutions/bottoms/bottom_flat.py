import math


class BottomFlat:
    def __init__(self):
        # D - millimeters
        self.D = [400, 500, 600, 700, 800, 900,
                  1000, 1200, 1400, 1600, 1800,
                  2000, 2200, 2400, 2500, 2600, 2800,
                  3000, 3200, 3400, 3600, 3800,
                  4000, 4500, 5000, 5600]
        self.K = [0.53, 0.5, 0.45, 0.41, 0.38]

    def get_params(self, user_data):
        prm = self.__calculate(user_data)
        return prm

    def get_data(self):
        return [self.D, self.K]

    def __calculate(self, user_data):
        K = user_data.K
        Pr = user_data.P
        Dr = user_data.D
        sig = user_data.sig
        c = user_data.c
        phi = user_data.phi

        sr = K*Dr*math.sqrt(Pr/(sig*phi))
        s = sr + c
        if (s-c)/Dr <= 0.11:
            return s
        else:
            Kp = 22/(1 + (math.sqrt(1+(6*(s-c))/Dr)**2))
            s = s*Kp
            return s
