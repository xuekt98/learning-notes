"""Chapter 5 demo -- Blinn-Phong specular on TWO balls (Fig 4.17 style).

Tiger Book Eq. 5.6:

  Lr = ( R/pi + ks * max(0, n . h)^p ) E    (Blinn-Phong)

where h = (l + v) / |l + v| is the half-vector.

Scene layout (matches Fig 4.17):
  * Two balls (red on the LEFT, blue on the RIGHT) sitting at the
    center of a small bounded tabletop.
  * Warm + cool directional lights (gives each ball a two-tone tint)
  * Small ambient so the shadows aren't pitch black.
  * Camera: 3/4 view from above-front, close enough to see specular.

Two side-by-side panels:
  Left  -- pure Lambertian (ks = 0): smooth gradient, no highlight
  Right -- Blinn-Phong (ks > 0): same scene + visible specular spot
          on each ball where n bisects l and v.
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
# Geometry -- two balls at the center of a bounded tabletop
# ------------------------------------------------------------------
red_ball  = Sphere(Vec3(-0.75, 0.55, 0.0), 0.55)
blue_ball = Sphere(Vec3( 0.75, 0.55, 0.0), 0.55)

# 4x4 tabletop, two triangles, CCW from above so outward normal is +y.
table_a = Triangle(Vec3(-2.0, 0.0, -2.0), Vec3( 2.0, 0.0, -2.0),
                  Vec3( 2.0, 0.0,  2.0))
table_b = Triangle(Vec3(-2.0, 0.0, -2.0), Vec3( 2.0, 0.0,  2.0),
                  Vec3(-2.0, 0.0,  2.0))


# ------------------------------------------------------------------
# Lights -- warm + cool directional pair (Fig 4.17 style)
# ------------------------------------------------------------------
# Two point lights at upper corners of the scene (1/r^2 falloff,
# shadow ray tested against [eps, r] -- see PointLight.illuminate()).
warm    = PointLight(Vec3( 2.0, 2.5, 1.5), color(7.0, 6.4, 5.0))
cool    = PointLight(Vec3(-2.0, 2.5, 1.5), color(2.5, 3.5, 7.0))
ambient = AmbientLight(color(0.55, 0.55, 0.55))


# ------------------------------------------------------------------
# Camera + view -- close 3/4 view, similar to Fig 4.17
# ------------------------------------------------------------------
cam  = Camera.from_lookat(Vec3(0.0, 1.2, 2.4), Vec3(0.0, 0.5, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-1.1, r=1.1, b=-0.5, t=1.1, nx=400, ny=300,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Materials
# ------------------------------------------------------------------
gray_table = Lambertian(color(0.85, 0.85, 0.85), ka=0.20)
table_a.material = gray_table
table_b.material = gray_table

# Pure Lambertian -- no specular (Chapter 4 look).
red_matte  = Lambertian(color(0.85, 0.20, 0.20), ka=0.60)
blue_matte = Lambertian(color(0.20, 0.40, 0.90), ka=0.60)

# Blinn-Phong -- same diffuse + white specular (Chapter 5 highlight).
red_shiny  = Lambertian(color(0.85, 0.20, 0.20), ka=0.60,
                        ks=color(1.0, 1.0, 1.0), p=50.0)
blue_shiny = Lambertian(color(0.20, 0.40, 0.90), ka=0.60,
                        ks=color(1.0, 1.0, 1.0), p=50.0)


# ------------------------------------------------------------------
# Render -- two panels
# ------------------------------------------------------------------
def render(red_mat, blue_mat):
    red_ball.material  = red_mat
    blue_ball.material = blue_mat
    scene = Scene(SurfaceGroup([red_ball, blue_ball, table_a, table_b]),
                  [ambient, warm, cool],
                  background=color(0.10, 0.10, 0.12), max_depth=1)
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
    ((red_matte,  blue_matte),  "Pure Lambertian (ks = 0)"),
    ((red_shiny,  blue_shiny),  "Blinn-Phong (ks = 1.0, p = 50)"),
]

panels = []
for (r_mat, b_mat), label in configs:
    print(f"  rendering: {label}")
    panels.append((render(r_mat, b_mat), label))


# ------------------------------------------------------------------
# Side-by-side
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
    img = Image.fromarray(np.flipud(buf * 255).astype(np.uint8), mode="RGB")
    x = k * (PANEL_W + GAP)
    draw.text((x + 8, 6), label, fill="black", font=font)
    out.paste(img, (x, HEADER))

out_path = os.path.join(HERE, "demo_ch5_phong.png")
out.save(out_path)
print(f"\nSaved {out_path}")
print()
print("What you should see (matches Fig 4.17's scene layout):")
print("  * Two balls (red on left, blue on right) on a centered tabletop.")
print("  * Left  panel -- pure Lambertian: smooth gradients, no highlight.")
print("  * Right panel -- Blinn-Phong: same gradients + a WHITE specular")
print("               spot on each ball, where the half-vector h bisects")
print("               the light and view directions.")
print()
print("Try changing p in red_shiny/blue_shiny to see how the Phong")
print("exponent sharpens or softens the highlight:")
print("  p = 10   -- soft 'eggshell' (broad)")
print("  p = 50   -- mild gloss")
print("  p = 200  -- glossy")
print("  p = 1000 -- tight, almost mirror-like")
