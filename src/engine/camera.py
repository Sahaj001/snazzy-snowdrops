from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.position import Pos


class Camera:
    """Defines the viewport over the world.

    x,y -> pixel
    screen_w, screen_h -> pixel
    """

    def __init__(self, x: int, y: int, screen_w: int, screen_h: int) -> None:
        self.x = x
        self.y = y
        self.screen_w = screen_w
        self.screen_h = screen_h

    def world_to_screen(self, x: int, y: int) -> tuple[int, int]:
        """Convert world coordinates to screen coordinates."""
        return x - self.x, y - self.y

    def center_on(self, pos: Pos) -> None:
        """Center the camera on a given world position."""
        self.x = pos.x - self.screen_w // 2
        self.y = pos.y - self.screen_h // 2
