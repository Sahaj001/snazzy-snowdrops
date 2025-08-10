from dataclasses import dataclass

from .position import Pos
from .sprite import Sprite


@dataclass
class DrawCmd:
    """Represents a single draw instruction for the RenderSystem.

    This decouples rendering from game logic.
    """

    sprite: Sprite  # What to draw (sprite asset)
    position: Pos  # Where to draw it in world coordinates
    layer: int = 0  # Rendering order (higher = drawn later, on top)
    rotation: float = 0.0  # Rotation in degrees
    scale: float = 1.0  # Scale multiplier
    opacity: float = 1.0  # Transparency (1.0 = fully opaque)
