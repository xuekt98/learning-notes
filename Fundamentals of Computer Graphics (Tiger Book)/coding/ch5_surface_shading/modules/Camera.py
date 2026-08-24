"""Camera -- viewing ray generation from Tiger Book, Section 4.3.

The camera is described by an orthonormal frame {e, u, v, w} where
  - e is the eye / viewpoint,
  - u points rightward (image-plane right),
  - v points upward (image-plane up),
  - w points backward (away from the view direction, i.e. w = -view_dir).

The image rectangle in the (u, v) plane is given by l, r, b, t (left, right,
bottom, top edges) measured from e. A pixel at raster position (i, j) maps to
the image-plane coordinate

    u_img = l + (r - l) * (i + 0.5) / nx         (Eq. 4.1)
    v_img = b + (t - b) * (j + 0.5) / ny

Standard orthographic   (4.3.1): o = e + u_img*u + v_img*v,  d = -w
Standard perspective    (4.3.2): o = e,                        d = -focal*w + u_img*u + v_img*v

Oblique variants (4.3 sidebar + 4.3.2 trailing paragraph): pass
`projection_dir` (anything other than None) to replace -w. The image-plane
normal w is still used to construct u and v; only the projection direction
itself is decoupled, which is how "cavalier" / "cabinet" oblique projections
work in practice.
"""

from .Vec3 import Vec3
from .Ray import Ray


class Camera:
    __slots__ = ("e", "u", "v", "w")

    def __init__(self, e: Vec3, u: Vec3, v: Vec3, w: Vec3):
        # Caller is responsible for passing an orthonormal (u, v, w).
        # Use `Camera.from_lookat` for a convenient builder.
        self.e = e
        self.u = u
        self.v = v
        self.w = w

    @classmethod
    def from_lookat(cls, eye: Vec3, target: Vec3, up: Vec3) -> "Camera":
        """Build the camera frame from an eye point, a look-at target, and an
        up vector (Section 2.4.7 orthonormal-basis-from-two-vectors recipe).

        Conventions (Tiger Book 4.3):
            w points opposite to the view direction, so w = normalize(eye - target).
        """
        w = (eye - target).normalized()
        u = up.cross(w).normalized()
        v = w.cross(u)
        return cls(eye, u, v, w)

    # ---- shared helper: map raster (i, j) to image-plane (u_img, v_img) ----
    @staticmethod
    def _image_uv(i, j, nx, ny, l, r, b, t):
        u_img = l + (r - l) * (i + 0.5) / nx
        v_img = b + (t - b) * (j + 0.5) / ny
        return u_img, v_img

    def _projection_dir(self, projection_dir):
        return -self.w if projection_dir is None else projection_dir.normalized()

    # ---------- 4.3.1 Orthographic Views ----------
    def orthographic_ray(self, i, j, nx, ny, l, r, b, t,
                         projection_dir=None) -> Ray:
        """Section 4.3.1. By default the projection direction is -w. Pass a
        different `projection_dir` to make an oblique orthographic view."""
        u_img, v_img = self._image_uv(i, j, nx, ny, l, r, b, t)
        origin = self.e + u_img * self.u + v_img * self.v
        direction = self._projection_dir(projection_dir)
        return Ray(origin, direction)

    # ---------- 4.3.2 Perspective Views ----------
    def perspective_ray(self, i, j, nx, ny, l, r, b, t, focal_length,
                        projection_dir=None) -> Ray:
        """Section 4.3.2. By default the projection direction is -w. Pass a
        different `projection_dir` to make an oblique perspective view."""
        u_img, v_img = self._image_uv(i, j, nx, ny, l, r, b, t)
        origin = self.e  # all rays share the viewpoint
        pdir = self._projection_dir(projection_dir)
        direction = (pdir * focal_length + u_img * self.u + v_img * self.v).normalized()
        return Ray(origin, direction)
