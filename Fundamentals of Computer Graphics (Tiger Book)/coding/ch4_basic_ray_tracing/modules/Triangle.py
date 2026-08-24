"""Triangle -- ray-triangle intersection (Tiger Book, Section 4.4.2).

A triangle with vertices a, b, c is the parametric surface

    p(u, v) = a + u (b - a) + v (c - a),       0 <= u, 0 <= v, u + v <= 1

so a ray hits the triangle iff there exist u, v in those ranges and a t > 0
such that

    e + t d = a + u (b - a) + v (c - a).

Rearranging gives the 3x3 linear system

    t d + u (a - b) + v (a - c) = a - e

which we solve with Cramer's rule (Tiger Book, page 88). Following the book's
"compute t, then gamma, then beta" early-termination order:

    1. compute t; bail if not in [t0, t1]
    2. compute gamma; bail if gamma < 0 or gamma > 1
    3. compute beta;  bail if beta  < 0 or beta  > 1 - gamma
    4. accept the hit

Step 3's upper bound uses gamma, so gamma must be computed first. This
ordering also short-circuits the most common miss cases (rays that miss the
plane or the triangle's parametric box) before doing the last division.

The book's implementation pseudocode:

    boolean raytri(Ray r, vector3 a, vector3 b, vector3 c, interval [t0, t1])
        compute t
        if (t < t0) or (t > t1) then return false
        compute gamma
        if (gamma < 0) or (gamma > 1) then return false
        compute beta
        if (beta < 0) or (beta > 1 - gamma) then return false
        return true

NOTE: Tiger Book mentions Möller-Trumbore (1997) at the end of 4.4.2 as an
"important and efficient alternative" that computes beta, gamma, t
simultaneously. We use Cramer's rule here for direct faithfulness to the
book; switching to MT later is a one-method change.

The outward unit normal is precomputed from (b - a) x (c - a); we flip it
so shading code can assume `n` points toward the camera (same convention
as Sphere).
"""

from .Vec3 import Vec3
from .Ray import Ray
from .Surface import Surface
from .HitRecord import HitRecord


class Triangle(Surface):
    __slots__ = ("a", "b", "c", "_normal", "material")

    def __init__(self, a: Vec3, b: Vec3, c: Vec3, material=None):
        self.a = a
        self.b = b
        self.c = c
        # Tiger Book 4.5.2: "Each surface stores a reference to its material."
        self.material = material
        # Outward normal from the right-hand rule (b - a) x (c - a).
        self._normal = ((b - a).cross(c - a)).normalized()

    @property
    def normal(self):
        """The geometric (outward) unit normal, computed once at construction."""
        return self._normal

    def hit(self, ray: Ray, t0: float, t1: float):
        # ---- build the 3x3 system
        # M has columns col1 = a - b, col2 = a - c, col3 = d; unknowns are
        # (beta, gamma, t); RHS = a - e.  See the module docstring.
        col1 = self.a - self.b
        col2 = self.a - self.c
        col3 = ray.d
        rhs = self.a - ray.o

        # Determinant of M via the scalar triple product col1 . (col2 x col3).
        D = col1.dot(col2.cross(col3))
        # |D| tiny => ray parallel to the triangle's plane => no unique hit.
        if abs(D) < 1e-8:
            return None

        # ---- step 1: t (per the book's early-termination order)
        D_t = col1.dot(col2.cross(rhs))
        t = D_t / D
        if not (t0 <= t <= t1):
            return None

        # ---- step 2: gamma
        D_gamma = col1.dot(rhs.cross(col3))
        gamma = D_gamma / D
        if gamma < 0.0 or gamma > 1.0:
            return None

        # ---- step 3: beta
        D_beta = rhs.dot(col2.cross(col3))
        beta = D_beta / D
        if beta < 0.0 or beta > 1.0 - gamma:
            return None

        # ---- hit accepted
        p = ray.evaluate(t)
        outward_n = self._normal
        front_face = ray.d.dot(outward_n) < 0
        n = outward_n if front_face else -outward_n
        return HitRecord(t, p, n, front_face, surface=self)

    def __repr__(self):
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"
