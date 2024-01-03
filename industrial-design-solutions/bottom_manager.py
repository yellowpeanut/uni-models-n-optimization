

class BottomManager:
    def __init__(self):
        pass

    @staticmethod
    def get(bottom_type):
        from bottom_types import BottomTypes
        from bottoms.bottom_flat import BottomFlat
        from bottoms.bottom_spherical import BottomSpherical
        from bottoms.bottom_conical import BottomConical

        if bottom_type == BottomTypes.FLAT:
            return BottomFlat()
        elif bottom_type == BottomTypes.SPHERICAL:
            return BottomSpherical()
        elif bottom_type == BottomTypes.CONICAL:
            return BottomConical()
        else:
            return None
