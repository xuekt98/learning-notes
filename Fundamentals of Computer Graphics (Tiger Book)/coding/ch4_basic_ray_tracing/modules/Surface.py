"""Surface -- abstract base class for anything a ray can intersect.

Tiger Book 4.4.3:
    class Surface
        HitRecord hit(Ray r, real t0, real t1)

"Anything that a ray can intersect, including groups of surfaces or
efficiency structures (Section 12.3) should be a subclass of Surface.
The ray-tracing program would then have one reference to a Surface for
the whole model, and new types of objects and efficiency structures can
be added transparently."

In Python, `hit()` returns a HitRecord on success and None on miss. We
also expose a Python-friendly alias `intersect` that maps to the same
method, since `surface.intersect(ray, t0, t1)` reads more naturally.
"""

from .Ray import Ray
from .HitRecord import HitRecord


class Surface:
    """Abstract base for ray-intersectable surfaces."""

    def hit(self, ray: Ray, t0: float, t1: float):
        """Return a HitRecord if the ray hits this surface within [t0, t1],
        otherwise return None.

        Subclasses MUST override this method.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement hit(ray, t0, t1)"
        )

    # Alias -- `surface.intersect(ray, t0, t1)` reads more naturally
    intersect = hit
