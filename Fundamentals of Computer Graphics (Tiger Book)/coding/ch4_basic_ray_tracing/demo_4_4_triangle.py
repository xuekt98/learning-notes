"""Demo for Section 4.4.2 -- Ray-Triangle Intersection.

  (1) Numerical unit tests. We hand-pick rays with known answers
      (head-on, parallel to triangle, miss, edge, behind) and check that
      Triangle.hit returns the expected t, beta, gamma, front_face.

  (2) Visual render. We cast perspective rays at a tetrahedron made of
      4 triangles. Each face's normal is constant, so the rendered image
      should show 2-3 cleanly separated colored regions (the visible faces)
      against a black background, with no spurious pixels.
"""

import os
import sys
import math

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from modules.Vec3 import Vec3
from modules.Ray import Ray
from modules.Camera import Camera
from modules.View import View
from modules.Triangle import Triangle


# ------------------------------------------------------------------
# (1) Numerical tests
# ------------------------------------------------------------------
print("=" * 60)
print("Section 4.4.2 -- numerical tests")
print("=" * 60)

# A single equilateral-ish triangle in the z=0 plane, pointing +z.
A = Vec3(-1.0, -1.0, 0.0)
B = Vec3( 1.0, -1.0, 0.0)
C = Vec3( 0.0,  1.0, 0.0)
tri = Triangle(A, B, C)

all_pass = True

def expect(name, ray, expected):
    hr = tri.hit(ray, 0.001, 1e9)
    if expected is None:
        ok = hr is None
        print(f"  {name:38s} -> {'PASS' if ok else 'FAIL'}  (got {hr})")
        return ok
    ok = (
        hr is not None
        and math.isclose(hr.t, expected["t"], abs_tol=1e-5)
        and math.isclose(hr.n.x, expected["n"].x, abs_tol=1e-5)
        and math.isclose(hr.n.y, expected["n"].y, abs_tol=1e-5)
        and math.isclose(hr.n.z, expected["n"].z, abs_tol=1e-5)
        and hr.front_face == expected["front_face"]
    )
    print(f"  {name:38s} -> {'PASS' if ok else 'FAIL'}  (got {hr})")
    return ok

# 1) Head-on ray through centroid (0, -1/3, 0). t = 5 - 0 = 5 (triangle at z=0,
#    ray from (0, 0, 5) along -z), beta = gamma = 1/3.
all_pass &= expect(
    "head-on through centroid (0,0,5)->(0,0,0)",
    Ray(Vec3(0.0, -1.0 / 3.0, 5.0), Vec3(0.0, 0.0, -1.0)),
    {"t": 5.0, "n": Vec3(0.0, 0.0, 1.0), "front_face": True},
)

# 2) Head-on through vertex A (-1,-1,0). beta = 1, gamma = 0.
all_pass &= expect(
    "head-on through vertex A (-1,-1,0)",
    Ray(Vec3(-1.0, -1.0, 5.0), Vec3(0.0, 0.0, -1.0)),
    {"t": 5.0, "n": Vec3(0.0, 0.0, 1.0), "front_face": True},
)

# 3) Ray hitting edge AB. Midpoint of AB is (0, -1, 0). beta = 1/2, gamma = 0.
all_pass &= expect(
    "hits edge AB at midpoint",
    Ray(Vec3(0.0, -1.0, 5.0), Vec3(0.0, 0.0, -1.0)),
    {"t": 5.0, "n": Vec3(0.0, 0.0, 1.0), "front_face": True},
)

# 4) Miss outside triangle (e.g. y = -2)
all_pass &= expect(
    "miss at y=-2",
    Ray(Vec3(0.0, -2.0, 5.0), Vec3(0.0, 0.0, -1.0)),
    None,
)

# 5) Parallel to triangle: d has zero z. Should not hit (no unique solution).
all_pass &= expect(
    "parallel to triangle (d=(-1,0,0))",
    Ray(Vec3(0.0, -1.0 / 3.0, 5.0), Vec3(-1.0, 0.0, 0.0)),
    None,
)

# 6) Behind the camera (origin behind eye along -z). Same as head-on but
#    the eye is on the +z side, ray heads +z (away from triangle).
all_pass &= expect(
    "behind camera (5,0,0)->(6,0,0)",
    Ray(Vec3(5.0, -1.0 / 3.0, 5.0), Vec3(1.0, 0.0, 0.0)),
    None,
)

# 7) Ray hits the BACK of the triangle (from -z side, going +z). It still
#    registers a hit, but front_face = False and the normal is flipped.
all_pass &= expect(
    "hits back side (0,0,-5)->(0,0,0)",
    Ray(Vec3(0.0, -1.0 / 3.0, -5.0), Vec3(0.0, 0.0, 1.0)),
    {"t": 5.0, "n": Vec3(0.0, 0.0, -1.0), "front_face": False},
)

# 8) t interval filter: same ray that hits (in unbounded interval), but
#    interval [10, 20] excludes it. Build inline (different t0/t1 args).
hr = tri.hit(
    Ray(Vec3(0.0, -1.0 / 3.0, 5.0), Vec3(0.0, 0.0, -1.0)),
    10.0, 20.0,
)
ok8 = hr is None
print(f"  {"interval [10,20] excludes a real hit":38s} -> "
      f"{"PASS" if ok8 else "FAIL"}  (got {hr})")
all_pass &= ok8

print()
print("OVERALL:", "ALL PASS" if all_pass else "SOME FAILED")
print()


# ------------------------------------------------------------------
# (2) Visual render -- tetrahedron with normal-encoded colors
# ------------------------------------------------------------------
print("=" * 60)
print("Section 4.4.2 -- visual render")
print("=" * 60)

# Vertices of a regular tetrahedron centered at origin, "radius" 1.
v0 = Vec3( 1.0,  1.0,  1.0)
v1 = Vec3( 1.0, -1.0, -1.0)
v2 = Vec3(-1.0,  1.0, -1.0)
v3 = Vec3(-1.0, -1.0,  1.0)

# 4 triangular faces. The vertex order below gives outward normals (all
# right-hand-rule consistent).
F0 = Triangle(v0, v1, v2)   # normal = (+, +, -)/sqrt(3)
F1 = Triangle(v0, v3, v1)   # normal = (+, -, +)/sqrt(3)
F2 = Triangle(v0, v2, v3)   # normal = (-, +, +)/sqrt(3)
F3 = Triangle(v1, v3, v2)   # normal = (-, -, -)/sqrt(3)

faces = [F0, F1, F2, F3]
print("Face normals:")
for k, f in enumerate(faces):
    print(f"  F{k}: {f.normal}")

cam = Camera.from_lookat(Vec3(0, 0, 5), Vec3(0, 0, 0), Vec3(0, 1, 0))
view = View(cam, l=-1.5, r=1.5, b=-1.5, t=1.5, nx=400, ny=400,
            projection="perspective", focal_length=1.0)

NX, NY = view.nx, view.ny
buf = np.zeros((NY, NX, 3), dtype=np.float32)

# Aggregate "world": pick the CLOSEST hit among all faces.
# (Not yet implemented as a SurfaceList class -- just a manual loop here.)
for j in range(NY):
    for i in range(NX):
        ray = view.ray(i, j)
        best = None
        for face in faces:
            hr = face.hit(ray, 0.001, 1e9)
            if hr is None:
                continue
            if best is None or hr.t < best.t:
                best = hr
        if best is not None:
            buf[j, i, 0] = 0.5 * (best.n.x + 1.0)
            buf[j, i, 1] = 0.5 * (best.n.y + 1.0)
            buf[j, i, 2] = 0.5 * (best.n.z + 1.0)

img = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_4_tetrahedron.png")
img.save(out_path)
print(f"\nSaved normal-encoded tetrahedron to {out_path}")
print("Expected: 2-3 cleanly separated colored triangular regions (the faces")
print("facing the camera) on a black background. Each region's color matches")
print("its face's outward normal mapped to RGB.")
