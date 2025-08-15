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
    zoom: int

    def world_to_screen(self, wx: int, wy: int) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        sx = int((wx - self.x) * self.zoom)
        sy = int((wy - self.y) * self.zoom)
        return sx, sy

    def screen_to_world(self, sx: int, sy: int) -> tuple[int, int]:
        """Convert screen coordinates to world coordinates for click event."""
        wx = sx / self.zoom + self.x
        wy = sy / self.zoom + self.y
        return wx, wy

    def center_on(self, pos: Pos) -> None:
        """Center the camera on a given world position."""
        half_w_world = (self.screen_w / self.zoom) * 0.5
        half_h_world = (self.screen_h / self.zoom) * 0.5
        self.x = pos.x - half_w_world
        self.y = pos.y - half_h_world
        self.x, self.y = self.clamp(self.x, self.y)

    def clamp(self, x: int, y: int) -> tuple[int, int]:
        """Clamp the camera position to ensure it doesn't go out of bounds."""
        max_x = max(0.0, self.world_max_x - self.screen_w / self.zoom)
        max_y = max(0.0, self.world_max_y - self.screen_h / self.zoom)
        clamped_x = min(max(0.0, x), max_x)
        clamped_y = min(max(0.0, y), max_y)
        return clamped_x, clamped_y
