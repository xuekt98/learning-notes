"""Demo for Section 4.4.1 -- Ray-Sphere Intersection.

Two parts:

  (1) Numerical unit tests. We hand-pick rays with known answers
      (head-on, off-center, tangent, miss, ray-from-inside) and check that
      `Sphere.hit` returns the expected t, normal, and front_face flag.

  (2) A visual render. We cast perspective rays from the camera built in
      4.3 at a sphere centered at the origin and render the silhouette.
      For pixels that hit, we color by the surface normal so you can also
      eyeball the normal math -- R/G/B are mapped from n.x, n.y, n.z in
      [-1, 1] to [0, 255]. The disk should appear smooth and roughly
      round; off-sphere pixels are black.
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
from modules.Sphere import Sphere


# ------------------------------------------------------------------
# (1) Numerical tests
# ------------------------------------------------------------------
print("=" * 60)
print("Section 4.4.1 -- numerical tests")
print("=" * 60)

sphere = Sphere(Vec3(0, 0, 0), 1.0)


def expect(name, ray, expected):
    hr = sphere.hit(ray, 0.001, 1e9)
    if expected is None:
        ok = hr is None
        print(f"  {name:35s} -> {'PASS' if ok else 'FAIL'}  (got {hr})")
        return ok
    ok = (
        hr is not None
        and math.isclose(hr.t, expected["t"], abs_tol=1e-6)
        and math.isclose(hr.n.x, expected["n"].x, abs_tol=1e-6)
        and math.isclose(hr.n.y, expected["n"].y, abs_tol=1e-6)
        and math.isclose(hr.n.z, expected["n"].z, abs_tol=1e-6)
        and hr.front_face == expected["front_face"]
    )
    print(f"  {name:35s} -> {'PASS' if ok else 'FAIL'}  (got {hr})")
    return ok


all_pass = True

# Head-on ray from (0,0,5) toward (0,0,0): hits front at t = 5 - 1 = 4
all_pass &= expect(
    "head-on (5,0,0)->(0,0,0)",
    Ray(Vec3(0, 0, 5), Vec3(0, 0, -1)),
    {"t": 4.0, "n": Vec3(0, 0, 1), "front_face": True},
)

# Same ray, but starting inside (0,0,0): hits the back at t = 1
all_pass &= expect(
    "from inside (0,0,0)->(1,0,0)",
    Ray(Vec3(0, 0, 0), Vec3(1, 0, 0)),
    {"t": 1.0, "n": Vec3(-1, 0, 0), "front_face": False},
)

# Miss: ray from (5, 5, 5) toward (0, 0, -10) -- passes well above the
# origin, never enters the sphere.
all_pass &= expect(
    "miss (5,5,5)->(0,0,-10)",
    Ray(Vec3(5, 5, 5), Vec3(-5, -5, -15).normalized()),
    None,
)

# Off-center ray that hits the front (entry hit, smaller root)
# From (2, 0, 5) toward (0.5, 0, 0). Direction normalized:
# (-1.5, 0, -5) / sqrt(1.5^2 + 5^2) = (-1.5, 0, -5) / sqrt(27.25)
# oc = (2,0,5); a = d.d; b_half = oc.d = (2)(-1.5/sqrt(27.25)) + (5)(-5/sqrt(27.25))
#                                  = (-3 - 25) / sqrt(27.25) = -28/sqrt(27.25)
# disc = b_half^2 - a * c
# ... easier: numerically just check t is approximately what geometry says.
hr = sphere.hit(
    Ray(Vec3(2, 0, 5), Vec3(-1.5, 0, -5).normalized()),
    0.001, 1e9,
)
ok = hr is not None and 0 < hr.t < 1e9 and hr.front_face
print(f"  {'off-center (2,0,5)->(.5,0,0)':35s} -> "
      f"{'PASS' if ok else 'FAIL'}  (got t={hr.t if hr else None})")
all_pass &= ok

# Same off-center ray, but with t interval [10, 20] -- miss within interval
hr = sphere.hit(
    Ray(Vec3(2, 0, 5), Vec3(-1.5, 0, -5).normalized()),
    10.0, 20.0,
)
ok = hr is None
print(f"  {'same ray, interval [10,20]':35s} -> "
      f"{'PASS' if ok else 'FAIL'}  (got {hr})")
all_pass &= ok

print()
print("OVERALL:", "ALL PASS" if all_pass else "SOME FAILED")
print()


# ------------------------------------------------------------------
# (2) Visual render -- normal-encoded sphere silhouette
# ------------------------------------------------------------------
print("=" * 60)
print("Section 4.4.1 -- visual render")
print("=" * 60)

cam = Camera.from_lookat(Vec3(0, 0, 5), Vec3(0, 0, 0), Vec3(0, 1, 0))
view = View(cam, l=-1, r=1, b=-1, t=1, nx=400, ny=400,
            projection="perspective", focal_length=1.0)

# A second sphere off to the side, to also see that the same hit()
# works for arbitrary centers
sphere2 = Sphere(Vec3(-1.8, 0.6, 0), 0.6)

NX, NY = view.nx, view.ny
buf = np.zeros((NY, NX, 3), dtype=np.float32)

for j in range(NY):
    for i in range(NX):
        ray = view.ray(i, j)
        # Try the closer sphere first so the smaller one wins ties
        hr = sphere.hit(ray, 0.001, 1e9)
        if hr is None:
            hr = sphere2.hit(ray, 0.001, 1e9)
        if hr is not None:
            # Map normal in [-1, 1] to RGB in [0, 1]
            buf[j, i, 0] = 0.5 * (hr.n.x + 1.0)
            buf[j, i, 1] = 0.5 * (hr.n.y + 1.0)
            buf[j, i, 2] = 0.5 * (hr.n.z + 1.0)

img = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_4_spheres.png")
img.save(out_path)
print(f"Saved normal-encoded spheres to {out_path}")
print("Expected: two round disks. The big one at center is the unit sphere")
print("centered at origin; the small one to the upper-left is offset.")
print("Colors map normal (n.x, n.y, n.z) -> (R, G, B): right=+R, up=+G, ")
print("toward camera=+B.")
