"""SurfaceGroup -- a group of surfaces that can be intersected as one.

Tiger Book 4.4.4:

    class Group, subclass of Surface
        list-of-Surface surfaces
        HitRecord hit(Ray ray, real t0, real t1)
            HitRecord closest_hit(∞)
            for surf in surfaces:
                rec = surf.hit(ray, t0, t1)
                if rec.t < ∞:
                    closest_hit = rec
                    t1 = t              # shrink: only look CLOSER than this
            return closest_hit

The `t1 = t` line is the crucial optimization. Instead of computing every
hit and then picking the closest, the search interval shrinks as soon as a
candidate is found, so subsequent surfaces only get hit-tested in [t0, t].
This is what makes "intersect the world" O(surfaces) in the average case
(rather than O(surfaces log surfaces) if we sorted all hits).

A miss is represented here by `None` rather than the book's `t = ∞`; the
algorithm logic is unchanged.
"""

from typing import Iterable, Optional

from .Ray import Ray
from .HitRecord import HitRecord
from .Surface import Surface


class SurfaceGroup(Surface):
    """A Group of surfaces (Tiger Book 4.4.4)."""

    __slots__ = ("surfaces",)

    def __init__(self, surfaces: Optional[Iterable[Surface]] = None):
        self.surfaces = list(surfaces) if surfaces is not None else []

    def add(self, surface: Surface) -> "SurfaceGroup":
        """Append a surface. Returns self so calls can be chained."""
        self.surfaces.append(surface)
        return self

    def hit(self, ray: Ray, t0: float, t1: float):
        closest_hit = None
        # Note: t1 is REBOUND here so each subsequent call only checks for
        # hits strictly closer than the best one found so far.
        for surface in self.surfaces:
            hr = surface.hit(ray, t0, t1)
            if hr is not None:
                closest_hit = hr
                t1 = hr.t
        return closest_hit

    def __len__(self):
        return len(self.surfaces)

    def __iter__(self):
        return iter(self.surfaces)

    def __getitem__(self, index):
        return self.surfaces[index]

    def __repr__(self):
        return f"SurfaceGroup({len(self.surfaces)} surfaces)"
