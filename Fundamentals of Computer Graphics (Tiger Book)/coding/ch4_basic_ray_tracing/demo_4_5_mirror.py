"""Demo for Section 4.5.4 -- Mirror Reflection.

Tiger Book 4.5.4:

    r = d - 2(d . n) n                                 (Eq. 4.3)
    color = c + km * shade-ray(Ray(p, r), eps, inf)

We render two side-by-side panels of the SAME scene, just swapping the
material on the right-hand sphere from Lambertian (no km) to Lambertian
with km = white (full mirror). The left sphere is always matte red, so
you can directly see what changes when the right sphere becomes a mirror.

Camera looks down at the scene from the upper-right, lights come from the
upper-front so the visible (camera-facing) sides of both spheres are lit.
The mirror sphere reflects the surrounding ground + sky into a compressed
view of the environment on its surface.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from modules.Vec3 import Vec3
from modules.Ray import Ray
from modules.Camera import Camera
from modules.View import View
from modules.Color import Color, color, clamp01
from modules.Material import Lambertian
from modules.Sphere import Sphere
from modules.Triangle import Triangle
from modules.SurfaceGroup import SurfaceGroup
from modules.Light import AmbientLight, PointLight, DirectionalLight
from modules.Scene import Scene


# ------------------------------------------------------------------
# Scene
# ------------------------------------------------------------------
red_lambertian   = Lambertian(color(0.85, 0.20, 0.20), ka=0.40)
white_lambertian = Lambertian(color(0.80, 0.80, 0.80), ka=0.40)
mirror_white     = Lambertian(color(0.00, 0.00, 0.00), ka=0.05,
                              km=color(0.95, 0.95, 0.95))

# Two side-by-side spheres. The right one's material is swapped per panel.
red_ball   = Sphere(Vec3(-1.2, 0.55, 0.0), 0.55, material=red_lambertian)
right_ball = Sphere(Vec3( 1.2, 0.55, 0.0), 0.55, material=red_lambertian)

# Large white ground.
ground = Triangle(
    Vec3(-15.0, 0.0, -15.0),
    Vec3( 15.0, 0.0,  15.0),
    Vec3(-15.0, 0.0,  15.0),
    material=white_lambertian,
)

# ---- lights (placed so the camera-facing sides of both spheres are lit) ----
ambient    = AmbientLight(color(0.40, 0.40, 0.40))
# Direction travels down-back-left, so the light source is upper-FRONT-right,
# which lights the +x-facing sides of both spheres (i.e. what the camera sees).
directional = DirectionalLight(Vec3(-0.6, -1.0, -0.4).normalized(),
                               color(1.40, 1.40, 1.40))
point      = PointLight(Vec3(3.0, 3.0, 3.0), color(1.60, 1.60, 1.60))

# ---- camera / view: 3/4 view from upper-right ----
cam = Camera.from_lookat(Vec3(3.0, 1.4, 3.0), Vec3(0.0, 0.55, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-2.0, r=2.0, b=-1.0, t=1.8, nx=300, ny=300,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------
def render(right_material):
    right_ball.material = right_material
    geometry = SurfaceGroup([red_ball, right_ball, ground])
    scene = Scene(geometry, [ambient, directional, point],
                 background=color(0.05, 0.07, 0.12), max_depth=5)
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
    return buf


configs = [
    (red_lambertian, "Lambertian (km = 0)"),
    (mirror_white,   "Mirror (km = 0.95)"),
]

panels = []
for mat, label in configs:
    print(f"  rendering: {label}")
    panels.append((render(mat), label))


# ------------------------------------------------------------------
# Side-by-side grid
# ------------------------------------------------------------------
PANEL_W, PANEL_H = view.nx, view.ny
HEADER = 32
GAP = 10
W = PANEL_W * 2 + GAP
H = PANEL_H + HEADER

out = Image.new("RGB", (W, H), "white")
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 17)
except OSError:
    font = ImageFont.load_default()

draw = ImageDraw.Draw(out)
for k, (buf, label) in enumerate(panels):
    img = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
    x = k * (PANEL_W + GAP)
    draw.text((x + 8, 6), label, fill="black", font=font)
    out.paste(img, (x, HEADER))

out_path = os.path.join(HERE, "demo_4_5_mirror.png")
out.save(out_path)
print(f"\nSaved {out_path}")
print()
print("Left = matte red ball (Lambertian, no km).")
print("Right = mirror ball (Lambertian with km=0.95, no diffuse).")
print()
print("Look at the right ball in each panel:")
print("  * Left:  matte red, shading gradient from the directional light.")
print("  * Right: mirror -- the visible hemisphere reflects the surrounding")
print("           environment (ground + sky + the red ball on the left).")
print("           You'll see a bright 'horizon' where the white ground")
print("           reflection meets the dark sky reflection.")
print()
print("Per Tiger Book 4.5.4 the recursion is bounded by Scene.max_depth = 5.")
