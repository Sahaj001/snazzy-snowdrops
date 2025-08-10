from __future__ import annotations

from typing import TYPE_CHECKING

from models.draw_cmd import DrawCmd
from models.position import Pos
from models.sprite import Sprite, SpriteType

if TYPE_CHECKING:
    from engine.camera import Camera
    from game.world import World
    from view.view_bridge import ViewBridge


class SpriteRegistry:
    """Stores and retrieves sprite data."""

    def __init__(self) -> None:
        self._sprites: dict[str, Sprite] = {}

    def get(self, sprite_id: str) -> Sprite:
        """Retrieve a sprite by its ID."""
        return self._sprites[sprite_id]

    def load_from_json(self, _path: str) -> None:
        """Load sprite metadata from a JSON file."""
        # mock loading from json with some basic sprites like player and path
        self._sprites["player"] = Sprite(
            type=SpriteType.SPRITE,
            image_path="assets/sprites/player.png",
            size=(32, 32),
        )
        self._sprites["wall"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/path.png",
            size=(32, 32),
        )
        self._sprites["stone"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/path.png",
            size=(32, 32),
        )
        self._sprites["grass"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/path.png",
            size=(32, 32),
        )
        self._sprites["tree"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/path.png",
            size=(32, 32),
        )


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

    def build_draw_queue(self, world: World, _camera: Camera) -> list[DrawCmd]:
        """Generate a list of draw commands based on the current world state."""
        draw_commands = []

        # 1. Draw tiles from the tile map
        tile_map = world.tiles
        tile_size = tile_map.tile_size

        # Draw all tiles (no camera culling for now)
        for y in range(tile_map.height):
            for x in range(tile_map.width):
                tile = tile_map.get(x, y)
                if tile:
                    # Get the sprite for this tile type
                    sprite = self.sprites.get(tile.sprite_id)

                    # Calculate screen position directly from tile coordinates
                    screen_x = x * tile_size
                    screen_y = y * tile_size

                    # Create draw command
                    draw_commands.append(
                        DrawCmd(
                            sprite=sprite,
                            position=Pos(screen_x, screen_y, tile.z),
                            layer=tile.z,
                        ),
                    )

        # 2. Draw entities (players, NPCs, items, etc.)
        for entity in world.entities:
            # Get sprite for this entity type
            sprite_id = entity.sprite_id if hasattr(entity, "sprite_id") else entity.__class__.__name__.lower()

            try:
                sprite = self.sprites.get(sprite_id)

                # Calculate screen position directly from entity position
                screen_x = entity.pos.x * tile_size
                screen_y = entity.pos.y * tile_size

                draw_commands.append(
                    DrawCmd(
                        sprite=sprite,
                        position=Pos(screen_x, screen_y, entity.pos.z),
                        layer=entity.pos.z + 10,  # Entities above tiles
                    ),
                )
            except KeyError:
                # Skip entities without sprites
                print(f"Warning: No sprite found for entity type '{sprite_id}'")
                continue

        # Sort by layer for proper rendering order (lower layers first)
        draw_commands.sort(key=lambda cmd: cmd.layer)

        return draw_commands

    def flush_to_view(self, cmds: list[DrawCmd]) -> None:
        """Send the draw commands to the view for rendering."""
        self.view_bridge.draw(cmds)
