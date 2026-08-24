"""Material -- encapsulates surface reflectance (the BRDF).

Tiger Book 5.2 -- the basic shading model for Chapter 5:

  Lr = (R/pi + ks * max(0, n . h)^p) E        (Eq. 5.6)

Where:
  * R     -- diffuse reflectance (we absorb R/pi into the "color" attribute
             for simplicity, matching Tiger Book's Chapter 4 simplification)
  * ks    -- specular coefficient (colored separately for RGB)
  * p     -- Phong exponent; higher p = sharper, more mirror-like highlight
  * n     -- surface normal at the shading point
  * h     -- the half-vector h = (l + v) / |l + v| (Blinn-Phong, p.102)
  * E     -- irradiance from the light source (provided by the Light)
  * Lr    -- reflected radiance that the eye sees

When p is small, the highlight is broad and soft; when p is large,
the highlight is tight and mirror-like. Tiger Book's sidebar suggests:
   p = 10    -- "eggshell"
   p = 100   -- mildly shiny
   p = 1000  -- really glossy
   p = 10000 -- nearly mirror-like

For the "no specular" case (Chapter 4's pure Lambertian), pass
ks = Color(0, 0, 0) (or leave it as the default) and the material
reduces to Lr = (R/pi) E.
"""

from .Color import Color
from .Vec3 import Vec3


class Material:
    """Abstract base class for materials."""

    # `ka` is the ambient reflectance used by AmbientLight (5.3).
    # Subclasses must set this attribute.
    ka: Color

    def evaluate(self, l: Vec3, v: Vec3, n: Vec3) -> Color:
        """Return the BRDF (k) for the given shading inputs.

        The Light multiplies this BRDF by the irradiance E to get Lr.

        l: unit vector from shading point toward the light
        v: unit vector from shading point toward the viewer
        n: unit surface normal at the shading point
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement evaluate(l, v, n)"
        )


class Lambertian(Material):
    """Ideal diffuse (matte) surface, with optional Blinn-Phong specular.

    The Lambertian BRDF is constant: f_r = R/pi. We omit the /pi because
    the Light.illuminate() pseudocode puts `n . l` (no pi) into E, so
    absorbing pi here would over-darken the result.

    With ks > 0 the material also reflects a Blinn-Phong specular term
    (Tiger Book 5.2.2 / Eq. 5.6). Pass ks = Color(0, 0, 0) to disable
    specular, recovering the pure Lambertian behavior from Chapter 4.
    """

    __slots__ = ("color", "ka", "km", "ks", "p")

    def __init__(self, color: Color, ka: float = 0.0,
                 ks: Color = None, p: float = 10.0):
        # `color` is the diffuse albedo (R/pi absorbed).
        self.color = color
        self.ka = Color(ka, ka, ka)
        # km: mirror (specular reflection) coefficient. Carried over from
        # Chapter 4's 4.5.4 mirror reflection -- default to no mirror so the
        # Chapter 5 demos that don't care about mirror reflection just work.
        self.km = Color(0, 0, 0)
        # ks: specular coefficient (colored). Default = no specular.
        self.ks = ks if ks is not None else Color(0, 0, 0)
        # p: Phong exponent. Tiger Book says 10 = eggshell, 1000 = glossy.
        self.p = p

    def evaluate(self, l: Vec3, v: Vec3, n: Vec3) -> Color:
        # Diffuse (constant) BRDF
        brdf = self.color

        # Specular (Blinn-Phong): ks * max(0, n . h)^p
        if self.ks.x > 0.0 or self.ks.y > 0.0 or self.ks.z > 0.0:
            h = (l + v)
            h_len = h.length
            if h_len > 0:
                h = h / h_len
                n_dot_h = n.dot(h)
                if n_dot_h > 0:
                    spec_strength = n_dot_h ** self.p
                    brdf = Color(
                        brdf.x + self.ks.x * spec_strength,
                        brdf.y + self.ks.y * spec_strength,
                        brdf.z + self.ks.z * spec_strength,
                    )
        return brdf

    def __repr__(self):
        return f"Lambertian(color={self.color}, ka={self.ka}, ks={self.ks}, p={self.p}, km={self.km})"
