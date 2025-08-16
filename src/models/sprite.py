from dataclasses import dataclass

from js import HTMLCanvasElement, Image, Math

from engine.interfaces import Drawable
from models import DrawCmd


@dataclass
class Sprite(Drawable):
    """Represents a sprite resource.

    Stores metadata needed for rendering and animation.
    """

    image_path: str  # Path to the sprite image file
    size: tuple[int, int]  # (width, height) in pixels
    frame_count: int = 1  # Number of animation frames
    origin: tuple[int, int] = (0, 0)  # Pivot/origin for rotation/scaling
    tint: tuple[int, int, int] | None = None  # RGB color tint (if any)
    loop: bool = False

    def is_animated(self) -> bool:
        """Return True if sprite has more than one frame."""
        return self.loop

    def draw(
        self,
        canvas: HTMLCanvasElement,
        img: Image,
        cmd: DrawCmd,
    ) -> None:
        """Draw a single sprite at a given position."""
        x, y = cmd.position.x, cmd.position.y
        w, h = self.size
        ctx = canvas.getContext("2d", alpha=True)
        ctx.save()

        ctx.translate(x + w / 2, y + h / 2)
        ctx.rotate(cmd.rotation * (Math.PI / 180))

        if self.is_animated():
            source_x = cmd.frame_idx * w
            source_y = 0
            ctx.drawImage(
                img,
                source_x,
                source_y,
                w,
                h,
                -w / 2,
                -h / 2,
                w * cmd.scale,
                h * cmd.scale,
            )
        else:
            ctx.drawImage(img, -w / 2, -h / 2, w * cmd.scale, h * cmd.scale)
        ctx.restore()


class SpriteRegistry:
    """Stores and retrieves sprite data."""

    def __init__(self) -> None:
        self._sprites: dict[str, Sprite] = {}

    def get(self, sprite_id: str) -> Sprite:
        """Retrieve a sprite by its ID."""
        return self._sprites.get(sprite_id, None)

    def add(self, state: str, sprite: Sprite) -> None:
        """Add a new sprite to the registry."""
        self._sprites[state] = sprite

    @classmethod
    def load_from_json(cls, data: dict) -> "SpriteRegistry":
        """Load sprite metadata from a JSON file."""
        sprite_registry = cls()
        for state, info in data["state"].items():
            sprite = Sprite(
                image_path=info["image_path"],
                size=(info["width"], info["height"]),
                frame_count=info["frame_count"],
                loop=info.get("loop", False),
            )
            sprite_registry.add(state, sprite)

        return sprite_registry
