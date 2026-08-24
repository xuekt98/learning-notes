"""Color -- RGB color helpers built on top of Vec3.

Tiger Book's shading code uses `Color` as a 3-tuple with component-wise
arithmetic. We just alias `Color = Vec3` and add a couple of convenience
functions (clamp to [0, 1], gamma-correct sRGB output).
"""

from .Vec3 import Vec3

# Type alias. Color and Vec3 are interchangeable; for colors we conventionally
# read .x as R, .y as G, .z as B.
Color = Vec3


def color(r: float, g: float, b: float) -> Color:
    """Build a Color from explicit R/G/B components."""
    return Color(r, g, b)


def clamp01(c: Color) -> Color:
    """Clamp each channel to [0, 1]. Used when writing to an 8-bit image."""
    return Color(
        max(0.0, min(1.0, c.x)),
        max(0.0, min(1.0, c.y)),
        max(0.0, min(1.0, c.z)),
    )


def to_srgb_bytes(c: Color) -> tuple:
    """Clamp + convert a linear-RGB Color to 8-bit sRGB (no gamma correction;
    linear is fine for a basic ray tracer -- Chapter 14 adds proper gamma)."""
    clamped = clamp01(c)
    return (
        int(round(255 * clamped.x)),
        int(round(255 * clamped.y)),
        int(round(255 * clamped.z)),
    )
