"""Reproduction of Tiger Book Figure 4.17.

Source: Tiger Book 4.5.4, page 95 (PDF page 112).
Caption: "A simple scene rendered with shading, shadows, and mirror
         reflection. Both the floor and the blue sphere have nonzero
         mirror reflection coefficients."

Scene: green sphere on the LEFT, blue/purple sphere on the RIGHT, both
sitting at the center of a small square mirror floor. Both spheres have
mirror reflection (km > 0), the floor is a full mirror (km ~ 1).

This demo also instruments every surface.hit() call so we can report
how much tracing the render actually does.
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
# Materials
# ------------------------------------------------------------------
floor_mat = Lambertian(color(0.55, 0.55, 0.55), ka=0.10,
                       km=color(0.90, 0.90, 0.90))   # near-full mirror floor
green_mat = Lambertian(color(0.20, 0.75, 0.35), ka=0.20,
                       km=color(0.55, 0.65, 0.55))
blue_mat  = Lambertian(color(0.35, 0.25, 0.85), ka=0.20,
                       km=color(0.55, 0.45, 0.75))


# ------------------------------------------------------------------
# Geometry
# ------------------------------------------------------------------
green_ball = Sphere(Vec3(-0.75, 0.50, 0.0), 0.50, material=green_mat)
blue_ball  = Sphere(Vec3( 0.75, 0.50, 0.0), 0.50, material=blue_mat)

# Mirror floor -- a SQUARE made of two triangles, centered at origin.
floor_a = Triangle(Vec3(-3.0, 0.0, -3.0), Vec3( 3.0, 0.0, -3.0),
                  Vec3( 3.0, 0.0,  3.0), material=floor_mat)
floor_b = Triangle(Vec3(-3.0, 0.0, -3.0), Vec3( 3.0, 0.0,  3.0),
                  Vec3(-3.0, 0.0,  3.0), material=floor_mat)
geometry = SurfaceGroup([green_ball, blue_ball, floor_a, floor_b])


# ------------------------------------------------------------------
# Lights
# ------------------------------------------------------------------
warm    = DirectionalLight(Vec3(-0.6, -1.0, -0.4).normalized(),
                            color(0.50, 0.46, 0.36))
cool    = DirectionalLight(Vec3( 0.6, -1.0, -0.4).normalized(),
                            color(0.28, 0.34, 0.55))
ambient = AmbientLight(color(0.28, 0.28, 0.28))


# ------------------------------------------------------------------
# Camera + view
# ------------------------------------------------------------------
cam  = Camera.from_lookat(Vec3(0.0, 1.2, 2.4), Vec3(0.0, 0.5, 0.0), Vec3(0, 1, 0))
view = View(cam, l=-1.1, r=1.1, b=-0.5, t=1.1, nx=400, ny=300,
            projection="perspective", focal_length=1.0)


# ------------------------------------------------------------------
# Tracing-instrumented render
# ------------------------------------------------------------------
# Wrap every surface so every hit() bumps a counter.
class _HitCount:
    __slots__ = ("_s",)
    def __init__(self, s): self._s = s
    def hit(self, *a, **kw):
        stats["surface_hit_calls"][0] += 1
        return self._s.hit(*a, **kw)
    def __getattr__(self, n): return getattr(self._s, n)


NX, NY = view.nx, view.ny
stats = {
    "shade_ray_calls": 0,
    "shade_ray_depths": [],
    "surface_hit_calls": [0],   # wrapped in list so the wrapper can mutate it
}

# Build a wrapped geometry (light points still hit the original via
# Scene.surface; we patch at the Scene level below).
_wrapped_geometry = SurfaceGroup([_HitCount(s) for s in geometry.surfaces])

# We can't add fields to Scene, but we CAN swap `surface` on this single
# instance by replacing it in the class __dict__. Since Scene uses
# __slots__, attributes are class-level read-only. The cleanest path:
# temporarily swap in the wrapped group before rendering, restore after.

scene = Scene(_wrapped_geometry, [ambient, warm, cool],
              background=color(0.20, 0.20, 0.22), max_depth=5)

# Monkey-patch shade_ray on the Scene class to count its calls (and
# record recursion depth).  This is invasive but Pythonic for stats.
_orig_shade_ray = Scene.shade_ray

def _counting_shade_ray(self, ray, t0=1e-3, t1=float("inf"), depth=0):
    stats["shade_ray_calls"] += 1
    stats["shade_ray_depths"].append(depth)
    return _orig_shade_ray(self, ray, t0, t1, depth)

Scene.shade_ray = _counting_shade_ray

buf = np.zeros((NY, NX, 3), dtype=np.float32)
for j in range(NY):
    for i in range(NX):
        ray = view.ray(i, j)
        c = scene.shade_ray(ray)
        cc = clamp01(c)
        buf[j, i, 0] = cc.x
        buf[j, i, 1] = cc.y
        buf[j, i, 2] = cc.z

# Restore the original shade_ray so we don't pollute the module.
Scene.shade_ray = _orig_shade_ray


out = Image.fromarray(np.flipud(buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_5_fig_4_17.png")
out.save(out_path)
print(f"Saved {out_path}")
print()
print("=" * 60)
print("Tracing stats for this render:")
print("=" * 60)
print(f"  pixels rendered                : {NX*NY:>10,}")
print(f"  scene.shade_ray() calls         : {stats['shade_ray_calls']:>10,}")
print(f"  surface.hit() calls             : {stats['surface_hit_calls'][0]:>10,}")
print(f"    of which primary hits         : {NX*NY:>10,}  (one per pixel)")
print(f"    of which shadow + reflection : {stats['surface_hit_calls'][0] - NX*NY:>10,}")
print()
depths = stats["shade_ray_depths"]
print(f"  shade_ray recursion-depth distribution:")
from collections import Counter
for d, count in sorted(Counter(depths).items()):
    pct = 100 * count / len(depths)
    print(f"    depth {d:>2} : {count:>10,} pixels  ({pct:>5.1f}%)")
print()
print(f"  Per-pixel averages:")
print(f"    shade_ray() calls / pixel  : {stats['shade_ray_calls'] / (NX*NY):.3f}")
print(f"    surface.hit() calls / pixel: {stats['surface_hit_calls'][0] / (NX*NY):.2f}")
print()
print("Theory (max_depth=5):")
print("  Per pixel: 1 primary + N=3 shadows + reflection max_depth times")
print("  Per surface.hit() call: 4 surfaces checked (2 spheres + 2 floor tris)")
print("  So per pixel: (1 + 3 + 1*max_depth) * 4 = up to 40 hit() calls")
