from modules.Coordinate import Coordinate

class Ray:
    def __init__(self, origion, direction):
        self.origin = origin
        self.direction = direction

    def evaluate(self, t):
        return self.origin + t * self.direction