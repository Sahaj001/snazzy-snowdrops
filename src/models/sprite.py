from dataclasses import dataclass
from enum import Enum

from js import HTMLCanvasElement, Image, Math

from engine.interfaces import Drawable
from models.position import Pos


class SpriteType(Enum):
    """Enumeration of different sprite rendering types."""

    SPRITE = "sprite"  # Image-based sprite
    RECT = "rect"  # Rectangle/square
    CIRCLE = "circle"  # Circle/ellipse
    TEXT = "text"  # Text rendering
    LINE = "line"  # Line drawing
    POLYGON = "polygon"  # Custom polygon
    TILE = "tile"  # Tile sprite (for tilemaps)
    EDIBLE = "edible"  # Edible entities


@dataclass
class Sprite(Drawable):
    """Represents a sprite resource.

    Stores metadata needed for rendering and animation.
    """

    image_path: str  # Path to the sprite image file
    type: SpriteType
    size: tuple[int, int]  # (width, height) in pixels
    frame_count: int = 1  # Number of animation frames
    frame_time: float = 0.1  # Time per frame in seconds
    loop: bool = True  # Whether the animation loops
    origin: tuple[int, int] = (0, 0)  # Pivot/origin for rotation/scaling
    tint: tuple[int, int, int] | None = None  # RGB color tint (if any)

    def is_animated(self) -> bool:
        """Return True if sprite has more than one frame."""
        return self.frame_count > 1

    def draw(
        self,
        canvas: HTMLCanvasElement,
        img: Image,
        position: Pos,
        rotation: float = 0,
    ) -> None:
        """Draw a single sprite at a given position."""
        x, y = position.x, position.y
        w, h = self.size
        ctx = canvas.getContext("2d", alpha=True)
        ctx.save()
        ctx.translate(x + w / 2, y + h / 2)
        ctx.rotate(rotation * (Math.PI / 180))
        ctx.drawImage(img, -w / 2, -h / 2, w, h)
        ctx.restore()
