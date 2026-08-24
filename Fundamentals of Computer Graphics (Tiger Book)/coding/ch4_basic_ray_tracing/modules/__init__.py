"""modules -- reusable 3D math primitives for the Tiger Book code experiments."""
from .Vec3 import Vec3
from .Ray import Ray
from .Camera import Camera
from .View import View
from .Color import Color, color, clamp01, to_srgb_bytes
from .HitRecord import HitRecord
from .Surface import Surface
from .Material import Material, Lambertian
from .Sphere import Sphere
from .Triangle import Triangle
from .SurfaceGroup import SurfaceGroup
from .Light import Light, AmbientLight, PointLight, DirectionalLight
from .Scene import Scene

__all__ = [
    "Vec3", "Ray", "Camera", "View",
    "Color", "color", "clamp01", "to_srgb_bytes",
    "HitRecord", "Surface",
    "Material", "Lambertian",
    "Sphere", "Triangle", "SurfaceGroup",
    "Light", "AmbientLight", "PointLight", "DirectionalLight",
    "Scene",
]
