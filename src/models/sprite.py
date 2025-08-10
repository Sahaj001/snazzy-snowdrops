from dataclasses import dataclass


@dataclass
class Sprite:
    """Represents a sprite resource.

    Stores metadata needed for rendering and animation.
    """

    image_path: str  # Path to the sprite image file
    size: tuple[int, int]  # (width, height) in pixels
    frame_count: int = 1  # Number of animation frames
    frame_time: float = 0.1  # Time per frame in seconds
    loop: bool = True  # Whether the animation loops
    origin: tuple[int, int] = (0, 0)  # Pivot/origin for rotation/scaling
    tint: tuple[int, int, int] | None = None  # RGB color tint (if any)

    def is_animated(self) -> bool:
        """Return True if sprite has more than one frame."""
        return self.frame_count > 1
