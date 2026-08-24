"""View -- a high-level wrapper that bundles a Camera with a viewport and a
projection mode. This is the object a ray tracer actually iterates over:

    view = View(camera, l=-1, r=1, b=-1, t=1, nx=400, ny=400,
                projection="perspective", focal_length=1.0)
    for j in range(view.ny):
        for i in range(view.nx):
            ray = view.ray(i, j)        # Ray for pixel (i, j)
            color = trace(ray)          # whatever your tracer returns

The two projection modes correspond to Section 4.3.1 (orthographic) and
Section 4.3.2 (perspective) of Tiger Book.
"""

import numpy as np

from .Camera import Camera
from .Ray import Ray
from .Vec3 import Vec3


class View:
    PROJECTIONS = ("perspective", "orthographic")

    __slots__ = (
        "camera",
        "l", "r", "b", "t",
        "nx", "ny",
        "projection",
        "focal_length",
        "oblique_projection_dir",
    )

    def __init__(
        self,
        camera: Camera,
        l: float, r: float, b: float, t: float,
        nx: int, ny: int,
        projection: str = "perspective",
        focal_length: float = None,
        oblique_projection_dir: Vec3 = None,
    ):
        if projection not in self.PROJECTIONS:
            raise ValueError(
                f"projection must be one of {self.PROJECTIONS}, got {projection!r}"
            )
        if projection == "perspective" and focal_length is None:
            raise ValueError("Perspective views require `focal_length`.")

        self.camera = camera
        self.l, self.r, self.b, self.t = l, r, b, t
        self.nx, self.ny = nx, ny
        self.projection = projection
        self.focal_length = focal_length
        self.oblique_projection_dir = oblique_projection_dir

    # ---- a few derived quantities, useful in shading code ----
    @property
    def aspect(self):
        return (self.r - self.l) / (self.t - self.b)

    @property
    def image_plane_z(self):
        """For perspective, the image plane sits `focal_length` in front of the
        eye along -w (i.e. between the eye and the scene). For orthographic,
        the image plane sits AT the eye."""
        if self.projection == "perspective":
            return self.camera.e + (-self.camera.w) * self.focal_length
        return self.camera.e

    # ---- the one method a tracer calls ----
    def ray(self, i: int, j: int) -> Ray:
        if self.projection == "orthographic":
            return self.camera.orthographic_ray(
                i, j, self.nx, self.ny,
                self.l, self.r, self.b, self.t,
                projection_dir=self.oblique_projection_dir,
            )
        return self.camera.perspective_ray(
            i, j, self.nx, self.ny,
            self.l, self.r, self.b, self.t,
            self.focal_length,
            projection_dir=self.oblique_projection_dir,
        )

    # ---- batch generation ----
    def generate_rays(self):
        """Return a (ny, nx) numpy array of Ray objects, indexed by [j, i]."""
        out = np.empty((self.ny, self.nx), dtype=object)
        for j in range(self.ny):
            for i in range(self.nx):
                out[j, i] = self.ray(i, j)
        return out

    def __repr__(self):
        kind = self.projection
        if self.oblique_projection_dir is not None:
            kind += " (oblique)"
        return (
            f"View({kind}, "
            f"viewport=({self.l},{self.r},{self.b},{self.t}), "
            f"resolution={self.nx}x{self.ny}, "
            f"focal={self.focal_length})"
        )
