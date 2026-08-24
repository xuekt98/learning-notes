"""Demo for Section 4.3: Computing Viewing Rays.

We build a camera that looks from (0, 0, 5) toward the origin with up = +y,
then:

  1. Print a handful of orthographic and perspective rays (corners + center)
     to sanity-check the formulas against the book (4.3.1, 4.3.2).

  2. Render a 400x400 image where each pixel's color encodes the absolute
     components of the perspective ray direction (R = |du|, G = |dv|, B = |dw|).
     This gives an immediate visual fingerprint: pixels near the image-plane
     center go straight along -w (mostly blue), pixels to the right skew +u
     (more red), pixels at the top skew +v (more green). If you see a smooth
     radial gradient centered in the image, your camera frame is right.
"""

import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from modules.Vec3 import Vec3
from modules.Camera import Camera


NX = NY = 400
# image rectangle l, r, b, t (centered, 1:1 aspect)
L, R, B, T = -1.0, 1.0, -1.0, 1.0
FOCAL = 1.0  # image-plane distance

# camera: eye at (0, 0, 5), looking at origin, up = +y
cam = Camera.from_lookat(
    eye=Vec3(0, 0, 5),
    target=Vec3(0, 0, 0),
    up=Vec3(0, 1, 0),
)

print("Camera frame (e, u, v, w):")
print(f"  e = {cam.e}")
print(f"  u = {cam.u}")
print(f"  v = {cam.v}")
print(f"  w = {cam.w}")
print()


# ---- (1) Print a few sample rays for both projection modes ----
def show(label, ray):
    o = ray.o.as_tuple()
    d = ray.d.as_tuple()
    print(f"{label:>22}  o=({o[0]:+.3f},{o[1]:+.3f},{o[2]:+.3f})  "
        f"d=({d[0]:+.3f},{d[1]:+.3f},{d[2]:+.3f})")


print("Orthographic rays (4.3.1, all share d = -w):")
for label, (i, j) in {
    "center (i=200,j=200)": (200, 200),
    "top-left (i=0,j=0)": (0, 0),
    "top-right (i=399,j=0)": (399, 0),
    "bottom-left (i=0,j=399)": (0, 399),
    "bottom-right (i=399,j=399)": (399, 399),
}.items():
    show(label, cam.orthographic_ray(i, j, NX, NY, L, R, B, T))

print("\nPerspective rays (4.3.2, all share o = e):")
for label, (i, j) in {
    "center (i=200,j=200)": (200, 200),
    "top-left (i=0,j=0)": (0, 0),
    "top-right (i=399,j=0)": (399, 0),
    "bottom-left (i=0,j=399)": (0, 399),
    "bottom-right (i=399,j=399)": (399, 399),
}.items():
    show(label, cam.perspective_ray(i, j, NX, NY, L, R, B, T, FOCAL))


# ---- (2) Render direction-encoded image ----
buf = np.zeros((NY, NX, 3), dtype=np.float32)
j_grid, i_grid = np.meshgrid(np.arange(NY), np.arange(NX), indexing="ij")
# collapse into one flat loop (kept readable without numpy micro-optimization)
for j in range(NY):
    for i in range(NX):
        ray = cam.perspective_ray(i, j, NX, NY, L, R, B, T, FOCAL)
        d = ray.d
        buf[j, i, 0] = abs(d.x)
        buf[j, i, 1] = abs(d.y)
        buf[j, i, 2] = abs(d.z)

# normalize so the brightest channel is 1 (purely a visualization aid)
m = buf.max()
if m > 0:
    buf /= m

img = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_3_direction.png")
img.save(out_path)
print(f"\nSaved direction-encoded PNG to {out_path}")
print("Expected look: blue at the center (rays go mostly -w),")
print("red on the right (rays skew +u), green at the top (rays skew +v).")
