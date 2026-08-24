"""Sphere -- ray-sphere intersection (Tiger Book, Section 4.4.1).

A sphere with center c and radius R is the implicit surface

    (p - c) . (p - c) - R^2 = 0.

Substituting the ray p(t) = e + t*d and expanding gives the quadratic

    A t^2 + B t + C = 0

with
    A = d . d
    B = 2 (oc . d),     where oc = e - c
    C = oc . oc - R^2

The discriminant D = (oc.d)^2 - A*C tells us how many real solutions there
are:
    D < 0:  no intersection (miss)
    D = 0:  tangent (one grazing hit)
    D > 0:  two intersections; the smaller root is the entry hit, the larger
            root is the exit hit.

For a search restricted to [t0, t1], we pick the smallest root that lies
inside the interval. The book recommends checking the discriminant FIRST
(Tiger Book 4.4.1, page 87) so we can early-out on a miss.

The unit outward normal at the hit point p is n = (p - c) / R. We flip
that normal so it always points AGAINST the ray direction (i.e. toward
the camera). Shading code (Section 4.5) is then free to assume `n` faces
the viewer; `hit.front_face` records which side was actually hit.
"""

import math

from .Vec3 import Vec3
from .Ray import Ray
from .Surface import Surface
from .HitRecord import HitRecord


class Sphere(Surface):
    __slots__ = ("center", "radius", "material")

    def __init__(self, center: Vec3, radius: float, material=None):
        self.center = center
        self.radius = float(radius)
        # Tiger Book 4.5.2: "Each surface stores a reference to its material."
        # The light's illuminate() reads it via hrec.surface.material.
        self.material = material

    def hit(self, ray: Ray, t0: float, t1: float):
        # oc = e - c  (origin to center)
        oc = ray.o - self.center
        a = ray.d.dot(ray.d)
        b_half = oc.dot(ray.d)
        c = oc.dot(oc) - self.radius * self.radius

        # Check discriminant first (Tiger Book 4.4.1, page 87).
        disc = b_half * b_half - a * c
        if disc < 0:
            return None
        sqrt_disc = math.sqrt(disc)

        # Smaller root first (entry hit).
        t = (-b_half - sqrt_disc) / a
        if not (t0 <= t <= t1):
            # Larger root (exit hit; only valid if the ray started inside).
            t = (-b_half + sqrt_disc) / a
            if not (t0 <= t <= t1):
                return None

        p = ray.evaluate(t)
        outward_n = (p - self.center) / self.radius
        # Ray going against the outward normal => front face. (If the ray
        # hits the inside of the sphere, the outward normal points the
        # same way as the ray, so we flip it for shading.)
        front_face = ray.d.dot(outward_n) < 0
        n = outward_n if front_face else -outward_n

        return HitRecord(t, p, n, front_face, surface=self)

    def __repr__(self):
        return f"Sphere(c={self.center}, r={self.radius})"
