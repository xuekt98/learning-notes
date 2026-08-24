"""Scene demo -- a sphere and a tetrahedron, both with mirror reflection.

Tiger Book 4.5.4, extended: same recursion formula and material `km`
scheme, but the scene shows TWO mirror primitives (a Sphere and a
Tetrahedron made of 4 Triangles) so you can see:

  * a curved mirror (sphere)   -- reflects a wide field of view
  * a flat-faced mirror (tetra) -- each face is a flat mirror with its
                                   own horizon line

The two mirrors use different `km` tints:
  * sphere      -> silver mirror  (km = white)
  * tetrahedron -> gold mirror    (km = warm yellow), like the book notes
    on page 96: "gold reflects yellow more efficiently than blue"

A big RED rectangle behind the camera acts as a "studio backdrop" -- the
mirrors reflect its bright color onto their visible (camera-facing)
hemispheres, so the reflection is clearly visible rather than the dim sky.

Both objects also reflect each other (mirror-on-mirror), up to
Scene.max_depth = 5.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
from modules.Light import AmbientLight, PointLight, DirectionalLight
from modules.Scene import Scene


# ------------------------------------------------------------------
# Materials
# ------------------------------------------------------------------
red_ground_mat   = Lambertian(color(0.90, 0.25, 0.25), ka=0.50)
# Silver mirror -- full reflection, no diffuse.
silver_mirror   = Lambertian(color(0, 0, 0), ka=0.02,
                             km=color(0.95, 0.95, 0.95))
# Gold mirror -- Tiger Book 4.5.4: "gold reflects yellow more efficiently
# than blue, so it shifts the colors of the objects it reflects."
gold_mirror     = Lambertian(color(0, 0, 0), ka=0.02,
                             km=color(1.00, 0.82, 0.42))
# Bright red backdrop -- the mirrors reflect this.


# ------------------------------------------------------------------
# Geometry -- sphere + tetrahedron + ground + red backdrop
# ------------------------------------------------------------------
sphere = Sphere(Vec3(-1.5, 0.75, 0.0), 0.75, material=silver_mirror)

# Regular tetrahedron (cube-corner construction).
SCALE = 0.55
v0 = Vec3( 1.0 * SCALE,  1.0 * SCALE,  1.0 * SCALE)
v1 = Vec3( 1.0 * SCALE, -1.0 * SCALE, -1.0 * SCALE)
v2 = Vec3(-1.0 * SCALE,  1.0 * SCALE, -1.0 * SCALE)
v3 = Vec3(-1.0 * SCALE, -1.0 * SCALE,  1.0 * SCALE)
TET_OFFSET = Vec3(1.5, 0.75, 0.0)
v0 = v0 + TET_OFFSET
v1 = v1 + TET_OFFSET
v2 = v2 + TET_OFFSET
v3 = v3 + TET_OFFSET
# Each face gets the gold mirror material.
F0 = Triangle(v0, v1, v2, material=gold_mirror)
F1 = Triangle(v0, v3, v1, material=gold_mirror)
F2 = Triangle(v0, v2, v3, material=gold_mirror)
F3 = Triangle(v1, v3, v2, material=gold_mirror)
tetrahedron = SurfaceGroup([F0, F1, F2, F3])

# White ground.
ground = Triangle(
    Vec3(-15.0, 0.0, -15.0),
    Vec3( 15.0, 0.0,  15.0),
    Vec3(-15.0, 0.0,  15.0),
    material=red_ground_mat,
)

geometry = SurfaceGroup([sphere, tetrahedron, ground])


# ------------------------------------------------------------------
# Lights
# ------------------------------------------------------------------
ambient     = AmbientLight(color(0.40, 0.40, 0.40))
# Light source is upper-FRONT-right (direction travels down-back-left),
# so it lights the +x-facing sides of both mirrors.
directional = DirectionalLight(Vec3(-0.6, -1.0, -0.4).normalized(),
                               color(1.60, 1.60, 1.60))
point       = PointLight(Vec3(2.0, 3.0, 2.0), color(1.40, 1.40, 1.40))


# ------------------------------------------------------------------
# Camera + view
# ------------------------------------------------------------------
cam = Camera.from_lookat(Vec3(3.0, 0.5, 3.0), Vec3(0.0, 0.75, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-1.3, r=1.3, b=-0.5, t=1.4, nx=400, ny=400,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------
scene = Scene(geometry, [ambient, directional, point],
              background=color(0.05, 0.07, 0.12), max_depth=5)

NX, NY = view.nx, view.ny
print(f"Rendering {NX}x{NY} with max_depth={scene.max_depth} ...")
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
out_path = os.path.join(HERE, "demo_4_5_mirror_scene.png")
out.save(out_path)
print(f"Saved {out_path}")
print()
print("What's in the image:")
print("  * Silver mirror sphere on the LEFT")
print("  * Gold mirror tetrahedron on the RIGHT (4 flat faces, each its")
print("    own little mirror)")
print("  * White ground at y = 0")
print("  * Big red backdrop wall at x = 8 -- the mirrors reflect this")
print()
print("Look for:")
print("  * RED reflection on both mirrors' visible hemispheres (from the")
print("    back wall)")
print("  * The gold tetrahedron's red reflection is tinted yellow (gold)")
print("  * The silver sphere's red reflection is neutral")
print("  * A 'horizon line' where the white ground reflection meets the")
print("    red wall reflection (on the sphere) or where the gold/dark sky")
print("    split happens (on each tetrahedron face)")
print("  * Mirror-on-mirror: the sphere also reflects the tetrahedron,")
print("    and vice versa, up to Scene.max_depth = 5 bounces.")
