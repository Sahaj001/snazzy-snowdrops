from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Optional
from ui.inventory import InventoryOverlay

if TYPE_CHECKING:
    from models import ObjectTile
    from ui import DialogBox

    from .position import Pos
    from .sprite import Sprite


class DrawCmdType(Enum):
    """Types of draw commands for the RenderSystem."""

    SPRITE = "sprite"
    TILE = "tile"
    COLLISION = "collision"
    TEXT = "text"
    DIALOG = "dialog"
    INVENTORY_OVERLAY = "inventory_overlay"


@dataclass
class DrawCmd:
    """Represents a single draw instruction for the RenderSystem.

    This decouples rendering from game logic.
    """

    position: "Pos"
    type: DrawCmdType = DrawCmdType.SPRITE
    sprite: Optional["Sprite"] = None
    frame_idx: int = 0
    dialog: Optional["DialogBox"] = None
    tile_gid: int = 0  # For tile rendering
    collision_box: Optional["ObjectTile"] = None
    inventory_overlay: InventoryOverlay | None = None
    text: str | None = None
    layer: int = 0  # Rendering order (higher = drawn later, on top)
    rotation: float = 0.0  # Rotation in degrees
    scale: float = 1.0  # Scale multiplier
    opacity: float = 1.0  # Transparency (1.0 = fully opaque)
