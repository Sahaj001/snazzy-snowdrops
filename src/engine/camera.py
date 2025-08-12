from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.position import Pos


@dataclass
class Camera:
    """Defines the viewport over the world.

    x,y -> pixel
    screen_w, screen_h -> pixel
    """

    x: int
    y: int
    screen_w: int
    screen_h: int
    world_max_x: int
    world_max_y: int

    def world_to_screen(self, x: int, y: int) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        return x - self.x, y - self.y

    def screen_to_world(self, x: int, y: int) -> tuple[int, int]:
        """Convert screen coordinates to world coordinates."""
        return x + self.x, y + self.y

    def center_on(self, pos: Pos) -> None:
        """Center the camera on a given world position."""
        self.x = max(0, pos.x - self.screen_w // 2)
        self.y = max(0, pos.y - self.screen_h // 2)

        self.x, self.y = self.clamp(self.x, self.y)

    def clamp(self, x: int, y: int) -> tuple[int, int]:
        """Clamp the camera position to ensure it doesn't go out of bounds."""
        clamped_x = max(0, min(x, self.world_max_x - self.screen_w))
        clamped_y = max(0, min(y, self.world_max_y - self.screen_h))
        return clamped_x, clamped_y
