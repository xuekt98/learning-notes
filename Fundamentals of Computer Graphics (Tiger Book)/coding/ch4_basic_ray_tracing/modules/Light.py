from modules.Coordinate import Coordinate

class Light:
    def __init__(self):
        return

class PointLight(Light):
    def __init__(self, position):
        super(Light).__init__()
        self.point_light_position = position