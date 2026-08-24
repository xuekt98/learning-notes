"""Demo for Section 4.5.1 -- three types of lights.

We build one scene: a red sphere sitting on a light-gray ground plane. We
then render it four times -- once per light configuration -- and stitch
the result into a 2x2 grid so you can compare at a glance:

  top-left     : AmbientLight only
  top-right    : DirectionalLight only
  bottom-left  : PointLight only
  bottom-right : all three combined

This makes the role of each light type obvious:

  * Ambient        -> uniform base color, no shape, no shadow.
  * Directional    -> Lambertian gradient (n . l), sphere casts a shadow.
  * Point          -> Lambertian gradient + 1/r^2 falloff + tight shadow.

The 4.5.2 Light.illurface contract and / 4.5.3 shadow ray are wired up
exactly as the book specifies -- see modules/Light.py.
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
from modules.Color import Color, color, clamp01
from modules.Material import Lambertian
from modules.Sphere import Sphere
from modules.Triangle import Triangle
from modules.SurfaceGroup import SurfaceGroup
from modules.Light import AmbientLight, PointLight, DirectionalLight
from modules.Scene import Scene


# ------------------------------------------------------------------
# Scene: a red sphere on a light-gray ground plane
# ------------------------------------------------------------------
red_mat   = Lambertian(color(0.85, 0.25, 0.25), ka=0.50)
white_mat = Lambertian(color(0.80, 0.80, 0.80), ka=0.50)

sphere = Sphere(Vec3(0.0, 0.55, 0.0), 0.5, material=red_mat)
# Big ground triangle. CCW vertex order from above so its normal points +y.
# Large ground triangle (30x30), CCW from above so the normal points +y.
ground = Triangle(
    Vec3(-15.0,  0.0, -15.0),
    Vec3( 15.0,  0.0,  15.0),
    Vec3(-15.0,  0.0,  15.0),
    material=white_mat,
)
geometry = SurfaceGroup([sphere, ground])

# ---- lights ----
ambient_only = AmbientLight(color(0.40, 0.40, 0.40))
directional  = DirectionalLight(Vec3(0.8, -1.0, -0.3).normalized(),
                                color(1.50, 1.50, 1.50))
point        = PointLight(Vec3(1.5, 2.5, 1.5), color(2.50, 2.50, 2.50))

# ------------------------------------------------------------------
# Camera + View
# ------------------------------------------------------------------
cam = Camera.from_lookat(Vec3(3.5, 1.2, 2.5), Vec3(0.0, 0.5, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-2.0, r=2.0, b=-1.0, t=2.0, nx=300, ny=300,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Render one panel
# ------------------------------------------------------------------
def render(lights):
    scene = Scene(geometry, lights, background=color(0.05, 0.05, 0.10))
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


# ------------------------------------------------------------------
# Build the 2x2 grid
# ------------------------------------------------------------------
configs = [
    ([ambient_only],             "AmbientLight only"),
    ([directional],              "DirectionalLight only"),
    ([point],                    "PointLight only"),
    ([ambient_only, directional, point], "All three combined"),
]

panels = []
for lights, label in configs:
    print(f"  rendering: {label}")
    panels.append((render(lights), label))


GAP = 12
PANEL_W, PANEL_H = view.nx, view.ny
HEADER = 30
W = PANEL_W * 2 + GAP
H = (PANEL_H + HEADER) * 2 + GAP

out = Image.new("RGB", (W, H), "white")
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
except OSError:
    font = ImageFont.load_default()

draw = ImageDraw.Draw(out)
positions = [
    (0, 0),
    (PANEL_W + GAP, 0),
    (0, PANEL_H + HEADER + GAP),
    (PANEL_W + GAP, PANEL_H + HEADER + GAP),
]
for (buf, label), (x, y) in zip(panels, positions):
    img = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
    draw.text((x + 6, y + 6), label, fill="black", font=font)
    out.paste(img, (x, y + HEADER))

out_path = os.path.join(HERE, "demo_4_5_lights.png")
out.save(out_path)
print(f"\nSaved {out_path}")
print()
print("What you should see:")
print("  * Top-left (Ambient only): uniform base color, no shading, no shadow.")
print("  * Top-right (Directional): Lambertian gradient on the sphere,")
print("          plus a parallel-edged shadow on the ground.")
print("  * Bottom-left (Point): Lambertian gradient + 1/r^2 falloff + tight")
print("          shadow that follows the sphere's silhouette.")
print("  * Bottom-right (All three): the 'full' image; ambient fills in the")
print("          shadow areas, point light adds the warm spot, directional")
print("          gives the global gradient.")
