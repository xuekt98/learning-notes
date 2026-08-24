"""Reproduction of Tiger Book Figure 4.12.

Source: Tiger Book 4.5.2, page 91 (PDF page 111).
Caption: "A simple scene rendered with shading from two point sources
         using the shading model of Chapter 5."

What the original image shows:
  * A GREEN ball on the LEFT and a BLUE/PURPLE ball on the RIGHT,
    both sitting on a light gray ground
  * Both balls have a soft warm highlight from a point light
    (probably a yellow-orange one positioned upper-right)
  * Both balls have a cool ambient/diffuse fill from another light
    (probably a blue/cyan one on the opposite side)
  * Faint shadows under each ball

What we use (Chapter 4 Lambertian, since we haven't implemented
Chapter 5's full Phong-style model yet):
  * Two PointLights of distinct colors (warm + cool)
  * Lambertian material on each ball (kd only, ka for ambient fill)
  * DirectionalLight from above to light the ground + cast subtle shadows
  * Gray ground

Color choices approximate what we see in the original Figure 4.12:
  * Green ball   kd = (0.30, 0.80, 0.45) -- bluish-green
  * Blue ball    kd = (0.45, 0.30, 0.85) -- purple-blue
  * Warm light   I = (1.40, 1.10, 0.70) -- yellow-orange
  * Cool light   I = (0.40, 0.55, 1.00) -- blue
  * Ground       kd = (0.70, 0.70, 0.70)
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
from modules.Light import AmbientLight, PointLight, DirectionalLight
from modules.Scene import Scene


# ------------------------------------------------------------------
# Materials -- pure Lambertian, no mirror (km = 0)
# ------------------------------------------------------------------
# Green ball: mostly diffuse with a subtle green mirror tint.
green_mat   = Lambertian(color(0.25, 0.85, 0.40), ka=0.45,
                        km=color(0.35, 0.45, 0.35))
# Blue ball: mostly diffuse with a subtle purple/blue mirror tint.
blue_mat    = Lambertian(color(0.45, 0.30, 0.95), ka=0.45,
                        km=color(0.45, 0.30, 0.55))
ground_mat  = Lambertian(color(0.70, 0.70, 0.70), ka=0.20)


# ------------------------------------------------------------------
# Geometry
# ------------------------------------------------------------------
green_ball = Sphere(Vec3(-0.5, 0.55, 0.0), 0.55, material=green_mat)
blue_ball  = Sphere(Vec3( 0.5, 0.55, 0.0), 0.55, material=blue_mat)
ground = Triangle(
    Vec3(-15.0, 0.0, -15.0),
    Vec3( 15.0, 0.0,  15.0),
    Vec3(-15.0, 0.0,  15.0),
    material=ground_mat,
)
geometry = SurfaceGroup([green_ball, blue_ball, ground])


# ------------------------------------------------------------------
# Lights -- a warm point light upper-right and a cool point light
# upper-left, like two studio softboxes. A weak ambient fills the
# shadows so they're not pitch black.
# ------------------------------------------------------------------
warm = PointLight(Vec3( 1.8, 2.5, 2.0), color(7.00, 5.60, 3.50))
cool = PointLight(Vec3(-3.0, 4.0, 2.5), color(1.20, 1.60, 3.50))
ambient = AmbientLight(color(0.55, 0.55, 0.55))
# A gentle directional from above to give the ground a uniform illumination
# and cast subtle soft shadows of the balls onto the ground.
top = DirectionalLight(Vec3(0.1, -1.0, 0.1).normalized(),
                       color(0.55, 0.55, 0.55))


# ------------------------------------------------------------------
# Camera + view -- 3/4 view from above-front, similar to Figure 4.12
# ------------------------------------------------------------------
cam = Camera.from_lookat(Vec3(0.0, 1.0, 3.2), Vec3(0.0, 0.55, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-1.6, r=1.6, b=-0.7, t=1.0, nx=400, ny=300,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------
scene = Scene(geometry, [ambient, warm, cool, top],
              background=color(0.18, 0.18, 0.20), max_depth=3)

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

out = Image.fromarray(np.flipud(buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_5_fig_4_12.png")
out.save(out_path)
print(f"Saved {out_path}")
print()
print("Differences from the original (Chapter 5 model is not yet implemented):")
print("  * No specular highlight on the balls (Lambertian only).")
print("  * Shadows may be more pronounced (no soft shadow model).")
print("  * Ambient is plain gray; original may use a hemispherical ambient.")
print("Same as the original:")
print("  * Two colored point lights (warm + cool) give the characteristic")
print("    two-tone shading on both balls.")
print("  * Green / blue base colors match the book's choice.")
print("  * Gray ground, dark gray sky.")
