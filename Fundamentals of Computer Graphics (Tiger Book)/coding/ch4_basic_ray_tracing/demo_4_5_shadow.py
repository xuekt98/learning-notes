"""Demo for Section 4.5.3 -- Shadows.

This scene contains NO mirror reflection (km = 0 on every surface);
it's a pure Lambertian demo whose purpose is to show that PointLight
and DirectionalLight already cast shadow rays (4.5.3 algorithm in
modules/Light.py). The shadow check is:

    HitRecord srec = scene.hit(Ray(x, l), eps, r)        # PointLight
    if srec.t < inf: return 0                           # in shadow
    (or use [eps, inf) for DirectionalLight)

Scene: a CYAN tetrahedron on the left, a PURPLE sphere on the right,
both sitting on a light-gray ground. A single directional light from
upper-back-left casts long shadows that clearly outline each object's
silhouette. An ambient light fills the shadows with a tiny bit of color
so they're not pitch black.
"""

import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from modules.Vec3 import Vec3
from modules.Camera import Camera
from modules.View import View
from modules.Color import color, clamp01
from modules.Material import Lambertian
from modules.Sphere import Sphere
from modules.Triangle import Triangle
from modules.SurfaceGroup import SurfaceGroup
from modules.Light import AmbientLight, DirectionalLight
from modules.Scene import Scene


# ------------------------------------------------------------------
# Materials -- NO mirror (km = 0) on any of them.
# ------------------------------------------------------------------
ground_mat  = Lambertian(color(0.85, 0.85, 0.85), ka=0.20)
cyan_mat    = Lambertian(color(0.20, 0.85, 0.85), ka=0.20)   # cyan tetrahedron
purple_mat  = Lambertian(color(0.70, 0.30, 0.90), ka=0.20)   # purple sphere


# ------------------------------------------------------------------
# Geometry
# ------------------------------------------------------------------
purple_sphere = Sphere(Vec3(1.2, 0.65, 0.0), 0.65, material=purple_mat)

# Cyan tetrahedron -- cube-corner vertices scaled to edge ~1.2.
SCALE = 0.55
v0 = Vec3( 1.0 * SCALE,  1.0 * SCALE,  1.0 * SCALE)
v1 = Vec3( 1.0 * SCALE, -1.0 * SCALE, -1.0 * SCALE)
v2 = Vec3(-1.0 * SCALE,  1.0 * SCALE, -1.0 * SCALE)
v3 = Vec3(-1.0 * SCALE, -1.0 * SCALE,  1.0 * SCALE)
TET_OFFSET = Vec3(-1.2, 0.65, 0.0)
v0 = v0 + TET_OFFSET
v1 = v1 + TET_OFFSET
v2 = v2 + TET_OFFSET
v3 = v3 + TET_OFFSET
# Face vertex orders verified in demo_4_4_triangle.py (outward normals).
F0 = Triangle(v0, v1, v2, material=cyan_mat)
F1 = Triangle(v0, v3, v1, material=cyan_mat)
F2 = Triangle(v0, v2, v3, material=cyan_mat)
F3 = Triangle(v1, v3, v2, material=cyan_mat)
tetrahedron = SurfaceGroup([F0, F1, F2, F3])

ground = Triangle(
    Vec3(-15.0, 0.0, -15.0),
    Vec3( 15.0, 0.0,  15.0),
    Vec3(-15.0, 0.0,  15.0),
    material=ground_mat,
)

geometry = SurfaceGroup([purple_sphere, tetrahedron, ground])


# ------------------------------------------------------------------
# Lights
# ------------------------------------------------------------------
# Strong directional from upper-back-LEFT so both objects cast long,
# visible shadows onto the ground in front toward the camera.
directional = DirectionalLight(Vec3(-0.8, -1.0, 1.0).normalized(),
                               color(0.95, 0.95, 0.95))
ambient     = AmbientLight(color(0.35, 0.35, 0.35))    # light fill so shadows aren't pitch-black


# ------------------------------------------------------------------
# Camera + view: 3/4 view from above-front-right
# ------------------------------------------------------------------
cam = Camera.from_lookat(Vec3(1.5, 1.6, 4.0), Vec3(0.0, 0.5, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-2.0, r=2.0, b=-1.0, t=1.6, nx=400, ny=400,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------
scene = Scene(geometry, [ambient, directional],
              background=color(0.10, 0.10, 0.15), max_depth=1)

NX, NY = view.nx, view.ny
buf = np.zeros((NY, NX, 3), dtype=np.float32)
for j in range(NY):
    for i in range(NX):
        ray = view.ray(i, j)
        c = scene.shade_ray(ray)
        cc = clamp01(c)
        buf[j, i, 0] = cc.x
        buf[j, i, 1] = cc.y
        buf[j, i, 2] = cc.z

out = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_5_shadow.png")
out.save(out_path)
print(f"Saved {out_path}")
print()
print("What's in the image:")
print("  * Cyan tetrahedron on the LEFT, purple sphere on the RIGHT.")
print("  * Both cast clear shadows on the light-gray ground -- the")
print("    shadows are the umbra shape of each object, projected along")
print("    the directional light's ray direction.")
print("  * The tetrahedron's shadow is a roughly diamond/quadrilateral")
print("    shape (the silhouette of a tetrahedron viewed from above).")
print("  * The sphere's shadow is an ellipse.")
print("  * AmbientLight fills the shadow region so it's not pitch black.")
print()
print("The shadow check inside each shadow-casting light is exactly")
print("Tiger Book 4.5.3 page 94: scene.hit(Ray(x, l), eps, r) and bail")
print("if anything is hit. See modules/Light.py for the implementation.")
