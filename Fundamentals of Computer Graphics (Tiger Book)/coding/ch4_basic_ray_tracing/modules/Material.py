"""Material -- encapsulates surface reflectance (the BRDF).

Tiger Book 4.5.2:

    class Material
        Color evaluate(Vec3 l, Vec3 v, Vec3 n)

`evaluate` returns the BRDF value at the shading point given the light
direction `l`, view direction `v`, and surface normal `n`. The light is
then responsible for multiplying by the incident irradiance (Tiger Book's
`Color k * E` step).

For the simple Lambertian (diffuse) model we implement here, the BRDF is
constant in `l`, `v`, `n` -- it's just the surface's albedo `kd / pi`.
For ray-tracer shading we drop the /pi (the book's pseudocode absorbs it
into `E` by skipping the normalization), so `evaluate` returns `kd`.
"""

from .Color import Color
from .Vec3 import Vec3


class Material:
    """Abstract base class for materials."""

    # `ka` is the ambient reflectance used by AmbientLight (Tiger Book 4.5.2).
    # Subclasses must set this attribute.
    ka: Color

    def evaluate(self, l: Vec3, v: Vec3, n: Vec3) -> Color:
        """Return the BRDF for incident light from direction `l`, viewer in
        direction `v`, surface normal `n` (all unit vectors)."""
        raise NotImplementedError(
            f"{type(self).__name__} must implement evaluate(l, v, n)"
        )


class Lambertian(Material):
    """Ideal diffuse (matte) surface, with optional mirror term.

    The diffuse BRDF is constant: f_r = kd / pi. We omit the /pi because the
    book's PointLight.illuminate pseudocode puts `n . l` (no pi) into E, so
    absorbing pi here would over-darken the result.

    `km` is the mirror (specular reflection) coefficient (Tiger Book 4.5.4).
    When km > 0, Scene.shade_ray recurses: it traces a reflected ray and
    adds `km * reflected_color` to the result. A pure mirror has
    `color = (0,0,0)` and `km = (1,1,1)` (or tinted for gold/blue mirrors).
    """

    __slots__ = ("color", "ka", "km")

    def __init__(self, color: Color, ka: float = 0.0,
                 km: Color = None):
        # `color` is the diffuse albedo kd (also reused as the ambient
        # reflectance when ka is omitted -- a common convention).
        self.color = color
        self.ka = Color(ka, ka, ka)
        # km: mirror color. None / Color(0,0,0) means no reflection.
        self.km = km if km is not None else Color(0, 0, 0)

    def evaluate(self, l: Vec3, v: Vec3, n: Vec3) -> Color:
        return self.color

    def __repr__(self):
        return f"Lambertian(color={self.color}, ka={self.ka}, km={self.km})"
