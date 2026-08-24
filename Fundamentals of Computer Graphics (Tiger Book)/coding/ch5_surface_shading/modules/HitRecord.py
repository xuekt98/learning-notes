"""HitRecord -- the data returned by a successful ray-surface intersection.

Tiger Book 4.4.3 defines the minimum required fields:

    class HitRecord
        Surface  | surface that was hit
        real     | t         | coordinate of hit point along the ray
        Vec3     | n         | surface normal at the hit point
        ...

We follow that minimum, plus the convenience fields `p` (the hit point in
3D) and `front_face` (True if the ray hit the front of the surface, False
if it hit the back). Shading code in 4.5 assumes `n` always points toward
the camera, so we flip the outward normal at construction time.
"""

from .Vec3 import Vec3


class HitRecord:
    __slots__ = ("t", "p", "n", "front_face", "surface")

    def __init__(self, t: float, p: Vec3, n: Vec3, front_face: bool,
                 surface: "Surface | None" = None):
        self.t = t
        self.p = p
        self.n = n
        self.front_face = front_face
        self.surface = surface

    def __repr__(self):
        return (
            f"HitRecord(t={self.t:.4f}, p={self.p}, n={self.n}, "
            f"front_face={self.front_face})"
        )
