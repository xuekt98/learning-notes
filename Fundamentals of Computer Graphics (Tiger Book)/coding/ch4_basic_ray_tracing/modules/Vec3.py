"""Vec3 -- the 3D vector used throughout Tiger Book (Chapter 2 + Chapter 4).

Tiger Book assumes a `Vec3` class that "supports the usual arithmetic
operations" (4.3, page 83). This is a minimal implementation: arithmetic,
dot, length, normalize, component-wise multiply, and cross product.
"""


class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # ---------- arithmetic ----------
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, s):
        # supports scalar * Vec3 and Vec3 * scalar (component-wise if both are Vec3)
        if isinstance(s, Vec3):
            return Vec3(self.x * s.x, self.y * s.y, self.z * s.z)
        return Vec3(self.x * s, self.y * s, self.z * s)

    def __rmul__(self, s):
        return self.__mul__(s)

    def __truediv__(self, s):
        return Vec3(self.x / s, self.y / s, self.z / s)

    # ---------- geometry ----------
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    @property
    def length_squared(self):
        return self.dot(self)

    @property
    def length(self):
        return self.length_squared ** 0.5

    def normalized(self):
        length = self.length
        if length == 0.0:
            raise ValueError("Cannot normalize a zero vector")
        return self / length

    # ---------- helpers ----------
    def as_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return (
            isinstance(other, Vec3)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )
