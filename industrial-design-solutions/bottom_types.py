from enum import Enum


class BottomTypes(str, Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    FLAT = "плоское"
    SPHERICAL = "сферическое"
    CONICAL = "коническое"
