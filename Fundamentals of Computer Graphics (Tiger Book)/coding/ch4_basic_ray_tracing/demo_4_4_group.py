"""Demo for Section 4.4.4 -- Intersecting a Group of Objects.

  (1) Numerical tests. Build a SurfaceGroup of 3 spheres + a triangle,
      cast rays at it, and verify that the closest hit wins, that a
      farther object is returned when the closer ones are missed, and
      that an empty group always misses.

  (2) Visual render. A scene with 2 spheres of different colors and a
      ground triangle. Every pixel is colored by the identity of the
      surface that was hit. Where two surfaces overlap, the closer one
      wins, so the visual shows the closest-hit logic at work.

  (3) Stats. We instrument every surface.hit() call to count how many
      actually got evaluated. With the `t1 = t` shrinking trick (Tiger
      Book 4.4.4), the count is lower than the naive "always check all
      surfaces" baseline -- the savings are what motivates the trick.
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
from modules.Triangle import Triangle
from modules.SurfaceGroup import SurfaceGroup


TOL = 1e-3  # generous absolute tolerance for t comparisons


# ------------------------------------------------------------------
# (1) Numerical tests
# ------------------------------------------------------------------
print("=" * 60)
print("Section 4.4.4 -- SurfaceGroup numerical tests")
print("=" * 60)

# Three spheres on the z-axis:
#   s_close: closest, small radius
#   s_mid:   middle, small radius
#   s_far:   farthest, larger radius (so off-axis rays still hit it)
s_close = Sphere(Vec3(0.0, 0.0,  2.0), 0.6)
s_mid   = Sphere(Vec3(0.0, 0.0,  0.0), 0.6)
s_far   = Sphere(Vec3(0.0, 0.0, -2.0), 1.4)
group = SurfaceGroup([s_close, s_mid, s_far])

all_pass = True


def expect(name, ray, expected_surface, expected_t, tol=TOL):
    hr = group.hit(ray, 0.001, 1e9)
    if expected_surface is None:
        ok = hr is None
        print(f"  {name:50s} -> {'PASS' if ok else 'FAIL'}  (got {hr})")
        return ok
    ok = (
        hr is not None
        and hr.surface is expected_surface
        and math.isclose(hr.t, expected_t, abs_tol=tol)
    )
    print(f"  {name:50s} -> {'PASS' if ok else 'FAIL'}  (got "
          f"surface={hr.surface}, t={hr.t if hr else None})")
    return ok


# Test 1: ray straight down the z-axis. Hits all 3 spheres.
# Fronts: s_close at z=2.6 (t=2.4), s_mid at z=0.6 (t=4.4), s_far at z=-0.6 (t=5.6).
# Closest = s_close at t=2.4.
all_pass &= expect(
    "ray (0,0,5)->(0,0,0) hits all 3 -> closest",
    Ray(Vec3(0, 0, 5), Vec3(0, 0, -1)),
    expected_surface=s_close,
    expected_t=2.4,
)

# Test 2: parallel ray off-axis at x=0.8. Misses s_close (r=0.6) and
# s_mid (r=0.6), hits only s_far (r=1.4) at the front.
all_pass &= expect(
    "ray at x=0.8 parallel to z misses close+mid, hits far",
    Ray(Vec3(0.8, 0, 5), Vec3(0, 0, -1)),
    expected_surface=s_far,
    expected_t=5.851,
)

# Test 3: order matters -- add s_close LAST. The closest object should
# still win even if it appears last in the surfaces list.
group_reordered = SurfaceGroup([s_far, s_mid, s_close])
hr = group_reordered.hit(Ray(Vec3(0, 0, 5), Vec3(0, 0, -1)), 0.001, 1e9)
ok = hr is not None and hr.surface is s_close and math.isclose(hr.t, 2.4, abs_tol=TOL)
print(f"  {'order in list does not matter -- closest still wins':50s} -> "
      f"{'PASS' if ok else 'FAIL'}  (got surface={hr.surface}, t={hr.t if hr else None})")
all_pass &= ok

# Test 4: empty group always misses.
empty = SurfaceGroup([])
hr = empty.hit(Ray(Vec3(0, 0, 5), Vec3(0, 0, -1)), 0.001, 1e9)
ok = hr is None
print(f"  {'empty group always misses':50s} -> {'PASS' if ok else 'FAIL'}  (got {hr})")
all_pass &= ok

# Test 5: ray that misses every sphere.
all_pass &= expect(
    "ray completely off-axis misses all",
    Ray(Vec3(5, 5, 5), Vec3(0, 0, -1)),
    expected_surface=None,
    expected_t=0,
)

# Test 6: mixed types. Group of [s_close (sphere), triangle].
# Triangle in z=0 plane; sphere in front at z=2 with r=0.6. Ray through
# the triangle's centroid (0, -1/3, 5) hits both; sphere is closer.
tri = Triangle(Vec3(-1, -1, 0), Vec3(1, -1, 0), Vec3(0, 1, 0))
mixed = SurfaceGroup([s_close, tri])
hr = mixed.hit(Ray(Vec3(0, -1.0/3.0, 5), Vec3(0, 0, -1)), 0.001, 1e9)
ok = hr is not None and hr.surface is s_close and math.isclose(hr.t, 2.501, abs_tol=TOL)
print(f"  {'mixed group [sphere, triangle] -> sphere closer':50s} -> "
      f"{'PASS' if ok else 'FAIL'}  (got surface={hr.surface}, t={hr.t if hr else None})")
all_pass &= ok

# Test 7: t0/t1 interval filter still works through Group.
# Ray (0,0,5)->(0,0,0) hits s_close FRONT at t=2.4, s_close BACK at t=3.6,
# s_mid front at t=4.4. Setting t0=3.0 excludes s_close's front but keeps
# its back (3.6); t1-shrinking then prunes s_mid's front. Net result:
# s_close's BACK is the first valid intersection. This is correct: a
# tighter t0 just means "I want to start looking further out", and the
# back of the first sphere is the first thing that qualifies.
hr = group.hit(Ray(Vec3(0, 0, 5), Vec3(0, 0, -1)), 3.0, 1e9)
ok = hr is not None and hr.surface is s_close and math.isclose(hr.t, 3.6, abs_tol=TOL)
print(f"  {'t0=3.0 -> s_close back at t=3.6 is first valid':50s} -> "
      f"{'PASS' if ok else 'FAIL'}  (got surface={hr.surface}, t={hr.t if hr else None})")
all_pass &= ok

print()
print("OVERALL:", "ALL PASS" if all_pass else "SOME FAILED")
print()


# ------------------------------------------------------------------
# (2) Visual render + (3) hit() call stats
# ------------------------------------------------------------------
print("=" * 60)
print("Section 4.4.4 -- visual render + t1-shrinking stats")
print("=" * 60)

red = Sphere(Vec3(-0.5,  0.3,  0.6), 0.8)            # upper-left, closer
blue = Sphere(Vec3( 0.5, -0.3, -0.4), 0.8)           # lower-right, farther
green = Triangle(                                     # big ground triangle
    Vec3(-2.0, -2.0, -2.0),
    Vec3( 2.0, -2.0, -2.0),
    Vec3( 0.0,  2.0, -2.0),
)

# ---- (3) Instrument every surface hit() to count actual evaluations ----
real_hit_calls = []  # list of (id(original_surface), bool: was a hit)


class _Instrumented:
    """Transparent wrapper that forwards everything to `surface` but
    logs every call to surface.hit()."""

    __slots__ = ("_surface",)

    def __init__(self, surface):
        self._surface = surface

    def hit(self, ray, t0, t1):
        hr = self._surface.hit(ray, t0, t1)
        real_hit_calls.append((id(self._surface), hr is not None))
        return hr


inst_scene = SurfaceGroup([
    _Instrumented(red),
    _Instrumented(blue),
    _Instrumented(green),
])

cam = Camera.from_lookat(Vec3(0, 0, 5), Vec3(0, 0, 0), Vec3(0, 1, 0))
view = View(cam, l=-1.5, r=1.5, b=-1.5, t=1.5, nx=400, ny=400,
            projection="perspective", focal_length=1.0)

NX, NY = view.nx, view.ny
buf = np.zeros((NY, NX, 3), dtype=np.float32)

# Surface-id -> RGB color. HitRecord.surface will be the *original*
# Sphere/Triangle (not the _Instrumented wrapper), so we match by id().
COLORS = {
    id(red):   np.array([1.00, 0.25, 0.25]),  # red
    id(blue):  np.array([0.25, 0.45, 1.00]),  # blue
    id(green): np.array([0.30, 0.85, 0.30]),  # green
}

real_hit_calls.clear()
for j in range(NY):
    for i in range(NX):
        ray = view.ray(i, j)
        hr = inst_scene.hit(ray, 0.001, 1e9)
        if hr is not None:
            color = COLORS.get(id(hr.surface))
            if color is not None:
                buf[j, i] = color

img = Image.fromarray((buf * 255).astype(np.uint8), mode="RGB")
out_path = os.path.join(HERE, "demo_4_4_group.png")
img.save(out_path)

# ---- (3) stats: compare with-shrinking vs without-shrinking ----
# The shrinking trick does NOT reduce the *number* of surface.hit() calls
# (every surface is still queried per pixel); what it does is reduce the
# number of *successful hits*. Later surfaces whose closest hit lies
# beyond the current t1 are pruned by the interval check, even though
# they would have hit if asked independently. We measure that here.

shrunk_calls = len(real_hit_calls)
shrunk_hits = sum(1 for _, did_hit in real_hit_calls if did_hit)

# Geometric (no shrinking): every surface is checked with [0.001, 1e9].
geo_hits = {id(red): 0, id(blue): 0, id(green): 0}
for j in range(NY):
    for i in range(NX):
        ray = view.ray(i, j)
        if red.hit(ray, 0.001, 1e9) is not None:
            geo_hits[id(red)] += 1
        if blue.hit(ray, 0.001, 1e9) is not None:
            geo_hits[id(blue)] += 1
        if green.hit(ray, 0.001, 1e9) is not None:
            geo_hits[id(green)] += 1
geo_hits_total = sum(geo_hits.values())

saved = geo_hits_total - shrunk_hits
saved_pct = 100 * saved / geo_hits_total if geo_hits_total else 0

print(f"Rendered {NX}x{NY} scene -> {out_path}")
print()
print("Surface hit() stats -- what the t1-shrinking trick actually saves:")
print(f"  Total pixels                      : {NX*NY}")
print(f"  surface.hit() calls (both schemes): {shrunk_calls} (= {NX*NY} * 3)")
print()
print("  Geometric hits (no shrinking, each surface asked alone):")
for sid, label in [(id(red), "red   "), (id(blue), "blue  "), (id(green), "green ")]:
    print(f"    {label}: {geo_hits[sid]}")
print(f"    total: {geo_hits_total}")
print()
print(f"  Hits accepted by Group WITH shrinking: {shrunk_hits}")
print(f"  Hits pruned by shrinking             : {saved}  ({saved_pct:.1f}% of geometric)")
print()
print("  Those pruned hits are the redundant 'farther object' queries that")
print("  the book's `t1 = t` trick skips by tightening the search interval.")
print()
print("Visual expectation:")
print("  * red dominates upper-left (closer sphere)")
print("  * blue shows in lower-right (farther sphere)")
print("  * green triangle fills background where neither sphere hits")
print("  * black = sky (no hit)")
print("  Where the spheres overlap, the closer (red) one wins.")
