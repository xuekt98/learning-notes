"""Light -- three subclasses that match Tiger Book 4.5.1.

    AmbientLight      constant everywhere; no shadow test.
    PointLight        position-based, 1/r^2 attenuation; shadow ray in [eps, r].
    DirectionalLight  parallel rays from one direction; shadow ray in [eps, inf).

The interface follows Tiger Book 4.5.2:

    class Light
        Color illuminate(Ray ray, HitRecord hrec)

`illuminate` returns the shading contribution of THIS light to the hit
point. Shadow testing is done inside each shadow-casting light by asking
`scene.hit(shadow_ray, eps, r)` -- if anything is in the way, the light
contributes zero (per Tiger Book 4.5.3). The `scene` is passed in by the
top-level `Scene.shade_ray`, so lights don't need to know about each other.

The pre-computed irradiance uses:

    PointLight:        E = I * max(0, n . l) / r^2
    DirectionalLight:  E = color * max(0, n . l)
    AmbientLight:      E = Ia * ka            (ka is the material's ambient coeff)

and the BRDF comes from `hrec.surface.material.evaluate(l, v, n)`. The
returned value is `BRDF * E` -- the same `k * E` step the book shows.
"""

from .Color import Color
from .Vec3 import Vec3
from .Ray import Ray


# A small epsilon used to start the shadow ray slightly away from the
# shading point (Tiger Book 4.5.3, page 94: "the usual adjustment to avoid
# that problem is to test for t in [eps, r]").
SHADOW_EPS = 1e-3


class Light:
    """Abstract base class for lights."""

    def illuminate(self, scene, ray, hrec) -> Color:
        raise NotImplementedError(
            f"{type(self).__name__} must implement illuminate(scene, ray, hrec)"
        )


# ----------------------------------------------------------------------
# 4.5.1 -- AmbientLight
# ----------------------------------------------------------------------
class AmbientLight(Light):
    """Constant illumination, no direction, no shadow.

    Tiger Book 4.5.2:
        class AmbientLight, subclass of Light
            Color Ia
            Color illuminate(Ray ray, HitRecord hrec)
                Color ka = hrec.surface.material.ka
                return ka * Ia
    """

    __slots__ = ("color",)

    def __init__(self, color: Color):
        self.color = color

    def illuminate(self, scene, ray, hrec) -> Color:
        ka = hrec.surface.material.ka
        return Color(ka.x * self.color.x, ka.y * self.color.y, ka.z * self.color.z)

    def __repr__(self):
        return f"AmbientLight({self.color})"


# ----------------------------------------------------------------------
# 4.5.1 -- PointLight
# ----------------------------------------------------------------------
class PointLight(Light):
    """Position-based point light, 1/r^2 attenuation.

    Tiger Book 4.5.2:
        class PointLight, subclass of Light
            Color I
            Vec3  p
            Color illuminate(Ray ray, HitRecord hrec)
                Vec3  x = ray.evaluate(hrec.t)
                real r = |p - x|
                Vec3  l = (p - x) / r
                Vec3  n = hrec.normal
                Color E = max(0, n . l) I / r^2
                Color k = hrec.surface.material.evaluate(l, v, n)
                return k * E

    Tiger Book 4.5.3 (added inside the same method):
        HitRecord srec = scene.hit(Ray(x, l), eps, r)
        if srec.t < inf: return 0   # in shadow
    """

    __slots__ = ("position", "intensity")

    def __init__(self, position: Vec3, intensity: Color):
        self.position = position
        self.intensity = intensity

    def illuminate(self, scene, ray, hrec) -> Color:
        x = ray.evaluate(hrec.t)
        to_light = self.position - x
        r = to_light.length
        if r <= 0:
            return Color(0, 0, 0)
        l = to_light / r  # unit vector toward the light

        # 4.5.3 shadow test
        shadow_ray = Ray(x, l)
        srec = scene.hit(shadow_ray, SHADOW_EPS, r)
        if srec is not None:
            return Color(0, 0, 0)

        # 4.5.2 irradiance + BRDF
        n_dot_l = max(0.0, hrec.n.dot(l))
        atten = 1.0 / (r * r)
        v = -ray.d  # view direction (Tiger Book 4.5.1)
        k = hrec.surface.material.evaluate(l, v, hrec.n)
        return Color(
            k.x * self.intensity.x * n_dot_l * atten,
            k.y * self.intensity.y * n_dot_l * atten,
            k.z * self.intensity.z * n_dot_l * atten,
        )

    def __repr__(self):
        return f"PointLight(pos={self.position}, I={self.intensity})"


# ----------------------------------------------------------------------
# 4.5.1 -- DirectionalLight
# ----------------------------------------------------------------------
class DirectionalLight(Light):
    """Parallel rays from a fixed direction (e.g. sunlight).

    The `direction` argument is the direction the LIGHT IS TRAVELLING
    (away from the source). The unit vector TOWARD the light is `-direction`.

    Shadow test interval is [eps, inf) -- per Tiger Book 4.5.3 page 95:
    "The shadow test for directional lights is similar but uses t1 = inf."
    """

    __slots__ = ("direction", "color")

    def __init__(self, direction: Vec3, color: Color):
        self.direction = direction.normalized()
        self.color = color

    def illuminate(self, scene, ray, hrec) -> Color:
        # l points TOWARD the light, so flip the light's travel direction.
        l = -self.direction

        # 4.5.3 shadow test, t1 = infinity
        x = ray.evaluate(hrec.t)
        shadow_ray = Ray(x, l)
        srec = scene.hit(shadow_ray, SHADOW_EPS, float("inf"))
        if srec is not None:
            return Color(0, 0, 0)

        # 4.5.2 irradiance + BRDF (no attenuation -- distance is infinite)
        n_dot_l = max(0.0, hrec.n.dot(l))
        v = -ray.d
        k = hrec.surface.material.evaluate(l, v, hrec.n)
        return Color(
            k.x * self.color.x * n_dot_l,
            k.y * self.color.y * n_dot_l,
            k.z * self.color.z * n_dot_l,
        )

    def __repr__(self):
        return f"DirectionalLight(dir={self.direction}, color={self.color})"
