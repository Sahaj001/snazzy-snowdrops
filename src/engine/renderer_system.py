from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.camera import Camera
    from game.world import World
    from models.draw_cmd import DrawCmd
    from models.sprite import Sprite
    from view.view_bridge import ViewBridge


class SpriteRegistry:
    """Stores and retrieves sprite data."""

    def __init__(self) -> None:
        self._sprites: dict[str, Sprite] = {}

    def get(self, sprite_id: str) -> Sprite:
        """Retrieve a sprite by its ID."""
        return self._sprites[sprite_id]

    def load_from_json(self, path: str) -> None:
        """Load sprite metadata from a JSON file."""


class RenderSystem:
    """Builds a draw queue and sends it to the view."""

    def __init__(
        self,
        sprites: SpriteRegistry,
        view_bridge: ViewBridge,
        camera: Camera,
    ) -> None:
        self.sprites = sprites
        self.view_bridge = view_bridge
        self.camera = camera

    def build_draw_queue(self, _world: World, _camera: Camera) -> list[DrawCmd]:
        """Generate a list of draw commands based on the current world state."""
        # Generate DrawCmd objects from world state
        return []

    def flush_to_view(self, cmds: list[DrawCmd]) -> None:
        """Send the draw commands to the view for rendering."""
        self.view_bridge.draw(cmds)
