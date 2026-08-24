"""Scene -- the top-level object a ray tracer iterates over.

A Scene bundles:

  * a Surface (the geometry; usually a SurfaceGroup)
  * a list of Lights
  * a background color for rays that miss everything
  * max_depth (Tiger Book 4.5.4) to bound the mirror-reflection recursion

Tiger Book 4.5.2 shade-ray pseudocode (extended with 4.5.4 reflection):

    function shade-ray(Ray ray, real t0, real t1, int depth)
        if depth >= MAX_DEPTH: return 0
        HitRecord rec = scene.hit(ray, t0, t1)
        if rec.t < inf then
            Color c = 0
            for light in scene.lights do
                c = c + light.illuminate(ray, rec)
            # Tiger Book 4.5.4: mirror reflection (recursive call)
            km = rec.surface.material.km
            if km > 0 and depth < MAX_DEPTH:
                Vec3 r = d - 2(d . n) n
                c = c + km * shade-ray(Ray(rec.p, r), eps, inf, depth + 1)
            return c
        else
            return background-color
"""

from .Color import Color
from .Ray import Ray
from .Surface import Surface


DEFAULT_MAX_DEPTH = 5
SHADOW_EPS = 1e-3  # both shadow rays and reflection rays start at this
                    # t0 to avoid self-intersection.


class Scene:
    __slots__ = ("surface", "lights", "background", "max_depth")

    def __init__(self, surface: Surface, lights,
                 background: Color = None, max_depth: int = DEFAULT_MAX_DEPTH):
        self.surface = surface
        self.lights = list(lights)
        self.background = background if background is not None else Color(0, 0, 0)
        self.max_depth = max_depth

    # ---- expose hit() so lights can do shadow rays against the same geometry
    def hit(self, ray: Ray, t0: float, t1: float):
        return self.surface.hit(ray, t0, t1)

    # ---- Tiger Book 4.5.2 shade-ray() + 4.5.4 mirror recursion ----
    def shade_ray(self, ray: Ray,
                  t0: float = SHADOW_EPS,
                  t1: float = float("inf"),
                  depth: int = 0) -> Color:
        # Tiger Book 4.5.4: "The recursive call may never terminate... This
        # can be fixed by adding a maximum recursion depth."
        if depth >= self.max_depth:
            return Color(0, 0, 0)

        rec = self.surface.hit(ray, t0, t1)
        if rec is None:
            return self.background

        # ----- direct lighting (4.5.2) -----
        c = Color(0, 0, 0)
        for light in self.lights:
            contribution = light.illuminate(self, ray, rec)
            c = Color(c.x + contribution.x,
                      c.y + contribution.y,
                      c.z + contribution.z)

        # ----- mirror reflection (4.5.4) -----
        km = rec.surface.material.km
        if km.x > 0.0 or km.y > 0.0 or km.z > 0.0:
            # r = d - 2 (d . n) n   (Tiger Book Eq. 4.3)
            # Note: in our convention n has been flipped to face the camera
            # (front_face=True) so d . n < 0 and -2(d . n) > 0 -- r points
            # back toward the viewer side. With a back-face hit, the same
            # formula still gives a sensible reflection vector.
            two_dn = 2.0 * ray.d.dot(rec.n)
            r = ray.d - rec.n * two_dn
            reflected = self.shade_ray(
                Ray(ray.evaluate(rec.t), r),
                SHADOW_EPS, float("inf"), depth + 1,
            )
            c = Color(
                c.x + km.x * reflected.x,
                c.y + km.y * reflected.y,
                c.z + km.z * reflected.z,
            )

        return c

    def __repr__(self):
        return (
            f"Scene({len(self.lights)} lights, bg={self.background}, "
            f"max_depth={self.max_depth})"
        )
