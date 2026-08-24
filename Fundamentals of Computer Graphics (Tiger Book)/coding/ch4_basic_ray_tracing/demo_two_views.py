"""Demo for Section 4.3 -- side-by-side comparison of the two views.

We draw a side view of the camera setup (looking along +x at the y-z plane)
twice: once for the orthographic view (4.3.1) and once for the perspective
view (4.3.2). Both use the SAME camera frame, SAME image rectangle
l=r=b=t=1, and a 7x7 pixel grid. We then plot 7 sample rays that have
u_img = 0 and v_img sweeping from -1 (bottom) to +1 (top).

What you should see:
  * Orthographic: all 7 rays are parallel horizontal lines that start on
    the image plane (which sits AT the eye) and travel in the -w direction
    into the scene.
  * Perspective: all 7 rays share an origin at the eye (red dot) and fan
    out, converging to the image plane (which sits one focal length IN
    FRONT OF the eye) and continuing into the scene.

That visual difference -- "parallel arrows" vs "fan from a point" -- is
the entire geometric distinction between 4.3.1 and 4.3.2.
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


# ------------------------------------------------------------------
# Geometry of the demo: a camera looking down -z from (0, 0, 5)
# ------------------------------------------------------------------
EYE = Vec3(0, 0, 5)
TARGET = Vec3(0, 0, 0)
UP = Vec3(0, 1, 0)

CAM = Camera.from_lookat(EYE, TARGET, UP)

# Side-view world bounds (we look along +x at the y-z plane)
Y_MIN, Y_MAX = -2.2, 2.2
Z_MIN, Z_MAX = -1.5, 6.5

# Canvas geometry (per panel)
PANEL_W, PANEL_H = 520, 460
MARGIN = 50


def world_to_pixel(y, z, panel_h=PANEL_H):
    px = (z - Z_MIN) / (Z_MAX - Z_MIN) * (PANEL_W - 2 * MARGIN) + MARGIN
    py = (Y_MAX - y) / (Y_MAX - Y_MIN) * (panel_h - 2 * MARGIN) + MARGIN
    return px, py


# ------------------------------------------------------------------
# Panel rendering
# ------------------------------------------------------------------
def render_panel(view: View, title: str, formula: str) -> Image.Image:
    img = Image.new("RGB", (PANEL_W, PANEL_H), "white")
    draw = ImageDraw.Draw(img)

    # ----- header text
    try:
        font_big = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", 18)
        font_small = ImageFont.truetype(
            "/System/Library/Fonts/Helvetica.ttc", 12)
        font_mono = ImageFont.truetype(
            "/System/Library/Fonts/Courier.ttc", 13)
    except OSError:
        font_big = font_small = font_mono = ImageFont.load_default()

    draw.text((MARGIN, 8), title, fill="black", font=font_big)
    draw.text((MARGIN, 32), formula, fill="#444", font=font_mono)
    draw.text((MARGIN, 50),
              "side view of the y-z plane, u_img = 0, "
              "v_img sweeps from -1 (bottom) to +1 (top)",
              fill="#666", font=font_small)

    # ----- axes (light gray)
    px_x0, py_x0 = world_to_pixel(Y_MIN, Z_MIN)
    px_x1, py_x1 = world_to_pixel(Y_MAX, Z_MAX)
    px_y0, py_y0 = world_to_pixel(0, Z_MIN)
    px_y1, py_y1 = world_to_pixel(0, Z_MAX)
    # y axis (vertical at z=0)
    draw.line([(px_y1, py_y0), (px_y1, py_y1)], fill="#ddd", width=1)
    draw.text((px_y1 + 4, py_y0 - 12), "+y", fill="#999", font=font_small)
    # z axis (horizontal at y=0)
    draw.line([(px_x0, py_x0), (px_x1, py_x1)], fill="#ddd", width=1)
    draw.text((px_x1 - 14, py_x1 + 4), "+z", fill="#999", font=font_small)

    # ----- image plane (vertical line) -- at the right place for each view
    plane_z = view.image_plane_z.z
    px_plane, _ = world_to_pixel(0, plane_z)
    py_top, _ = world_to_pixel(1.0, plane_z)
    py_bot, _ = world_to_pixel(-1.0, plane_z)
    draw.line([(px_plane, py_top), (px_plane, py_bot)], fill="black", width=2)
    draw.text((px_plane - 70, py_top - 16),
              f"image plane (z={plane_z:.1f})",
              fill="black", font=font_small)

    # ----- eye dot (perspective only)
    if view.projection == "perspective":
        eye_px, eye_py = world_to_pixel(EYE.y, EYE.z)
        r = 6
        draw.ellipse(
            [(eye_px - r, eye_py - r), (eye_px + r, eye_py + r)],
            fill="#cc0000", outline="#cc0000",
        )
        draw.text((eye_px + 10, eye_py - 8), "eye (e)", fill="#cc0000",
                  font=font_small)

    # ----- sample rays: u_img = 0, v_img varies
    n_samples = 7
    # rainbow colormap (low v_img = blue, high v_img = red)
    cmap = [
        (66, 133, 244),    # blue   -> v_img = -1
        (52, 168, 83),     # cyan
        (251, 188, 4),     # yellow
        (251, 188, 4),     # yellow
        (251, 188, 4),
        (234, 67, 53),     # red    -> v_img = +1
        (234, 67, 53),
    ][:n_samples]
    # simpler: use a proper 7-stop gradient
    stops = np.linspace(0, 1, n_samples)
    cmap = [
        tuple(int(c) for c in (66 + (234 - 66) * t,
                                133 + (67 - 133) * t,
                                244 + (53 - 244) * t))
        for t in stops
    ]

    i_center = view.nx // 2  # u_img = 0
    for k in range(n_samples):
        j = int(round(k * (view.ny - 1) / (n_samples - 1)))
        ray = view.ray(i_center, j)

        # trace from ray origin to origin + t_max * d
        t_max = 3.0
        end = ray.o + t_max * ray.d

        p0 = world_to_pixel(ray.o.y, ray.o.z)
        p1 = world_to_pixel(end.y, end.z)
        color = cmap[k]
        draw.line([p0, p1], fill=color, width=2)

        # arrow head
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        norm = (dx ** 2 + dy ** 2) ** 0.5 or 1.0
        # perpendicular for arrow wings
        wx = -dy / norm * 6
        wy = dx / norm * 6
        head = [(p1[0], p1[1]),
                (p1[0] - dx / norm * 10 + wx, p1[1] - dy / norm * 10 + wy),
                (p1[0] - dx / norm * 10 - wx, p1[1] - dy / norm * 10 - wy)]
        draw.polygon(head, fill=color)

    # ----- legend
    legend_x = MARGIN
    legend_y = PANEL_H - 40
    draw.text((legend_x, legend_y - 18), "rays, v_img = -1 (bottom) ... +1 (top)",
              fill="#444", font=font_small)
    bar_w = 200
    for k in range(n_samples):
        x0 = legend_x + int(k * bar_w / n_samples)
        x1 = legend_x + int((k + 1) * bar_w / n_samples)
        draw.rectangle([(x0, legend_y), (x1, legend_y + 10)], fill=cmap[k])
    draw.text((legend_x, legend_y + 14), "v_img",
              fill="#444", font=font_small)

    return img


# ------------------------------------------------------------------
# Build the two views
# ------------------------------------------------------------------
ortho = View(CAM, l=-1, r=1, b=-1, t=1, nx=7, ny=7,
             projection="orthographic")
persp = View(CAM, l=-1, r=1, b=-1, t=1, nx=7, ny=7,
             projection="perspective", focal_length=1.0)

ortho_panel = render_panel(
    ortho,
    title="Orthographic view (4.3.1)",
    formula="ray.o = e + u_img*u + v_img*v    ray.d = -w",
)
persp_panel = render_panel(
    persp,
    title="Perspective view (4.3.2)",
    formula="ray.o = e    ray.d = -focal*w + u_img*u + v_img*v",
)

# ----- stack them side by side
GAP = 20
combined = Image.new(
    "RGB",
    (PANEL_W * 2 + GAP, PANEL_H + 40),
    "white",
)
combined.paste(ortho_panel, (0, 30))
combined.paste(persp_panel, (PANEL_W + GAP, 30))

# top header
draw_top = ImageDraw.Draw(combined)
try:
    font_top = ImageFont.truetype(
        "/System/Library/Fonts/Helvetica.ttc", 14)
except OSError:
    font_top = ImageFont.load_default()
draw_top.text(
    (MARGIN, 8),
    "Tiger Book §4.3 -- two views of the same camera frame",
    fill="black", font=font_top,
)

out_path = os.path.join(HERE, "demo_two_views.png")
combined.save(out_path)
print(f"Saved comparison image to {out_path}")
print()
print("Same camera (e=(0,0,5), looking at origin), same 7x7 viewport l=r=b=t=1.")
print("Orthographic rays (left):  parallel, all start on image plane at z=5.")
print("Perspective rays (right):  share origin at eye, fan through the image")
print("                           plane at z=4 (= eye_z - focal_length).")
