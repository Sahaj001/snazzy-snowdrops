from dataclasses import dataclass
from enum import Enum

from ui.dialog import DialogBox

from .position import Pos
from .sprite import Sprite


class DrawCmdType(Enum):
    """Types of draw commands for the RenderSystem."""

    SPRITE = "sprite"
    TEXT = "text"
    DIALOG = "dialog"


@dataclass
class DrawCmd:
    """Represents a single draw instruction for the RenderSystem.

    This decouples rendering from game logic.
    """

    position: Pos
    type: DrawCmdType = DrawCmdType.SPRITE
    sprite: Sprite | None = None
    dialog: DialogBox | None = None
    text: str | None = None
    layer: int = 0  # Rendering order (higher = drawn later, on top)
    rotation: float = 0.0  # Rotation in degrees
    scale: float = 1.0  # Scale multiplier
    opacity: float = 1.0  # Transparency (1.0 = fully opaque)
