"""Ray -- the basic 3D ray primitive from Tiger Book, Section 4.3.

A ray is described by an origin `o` and a propagation direction `d`. The
set of points on the ray is the 3D parametric line

    p(t) = o + t * d,    t in R.

Tiger Book uses t < 0 for points "behind" the eye, and t > 0 in front of it.
The closest object intersected by the ray is found by picking the smallest
positive t that satisfies the surface equation (Section 4.4).
"""

from .Vec3 import Vec3


class Ray:
    __slots__ = ("o", "d")

    def __init__(self, origin: Vec3, direction: Vec3):
        # Tiger Book names the fields `o` and `d` (Section 4.3, page 83).
        self.o = origin
        self.d = direction

    def evaluate(self, t):
        """Return the 3D point at parameter t along the ray.

        Equivalent to the book pseudocode `return o + t*d`.
        """
        return self.o + t * self.d

    def point_at(self, t):
        """Alias for `evaluate`, in case you prefer the Shirley naming."""
        return self.evaluate(t)

    def __repr__(self):
        return f"Ray(o={self.o}, d={self.d})"
