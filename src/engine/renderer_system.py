from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import EventType, GameEvent
from models.draw_cmd import DrawCmd, DrawCmdType
from models.position import Pos
from models.sprite import Sprite, SpriteType
from ui.dialog import DialogBox

if TYPE_CHECKING:
    from engine.camera import Camera
    from engine.event_bus import EventBus
    from game.world import World
    from view.view_bridge import ViewBridge


class SpriteRegistry:
    """Stores and retrieves sprite data."""

    def __init__(self) -> None:
        self._sprites: dict[str, Sprite] = {}

    def get(self, sprite_id: str) -> Sprite:
        """Retrieve a sprite by its ID."""
        return self._sprites.get(sprite_id, None)

    def load_from_json(self, _path: str) -> None:
        """Load sprite metadata from a JSON file."""
        # mock loading from json with some basic sprites like player and path
        sprite_size = 50
        self._sprites["player"] = Sprite(
            type=SpriteType.SPRITE,
            image_path="assets/sprites/player.png",
            size=(sprite_size, sprite_size),
        )
        self._sprites["wall"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/wall.png",
            size=(sprite_size, sprite_size),
        )
        self._sprites["fruit"] = Sprite(
            type=SpriteType.EDIBLE,
            image_path="assets/sprites/fruit.png",
            size=(sprite_size, sprite_size),
        )
        self._sprites["grass"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/path.png",
            size=(sprite_size, sprite_size),
        )
        self._sprites["tree"] = Sprite(
            type=SpriteType.TILE,
            image_path="assets/sprites/tree.png",
            size=(sprite_size, sprite_size),
        )
        self._sprites["player_info"] = Sprite(
            type=SpriteType.SPRITE,
            image_path="assets/sprites/fruit.png",
            size=(sprite_size, sprite_size),
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
        self.ui_overlays = {}  # overlay_id / sprite_id -> expiry_time
        self.active_dialog: DialogBox | None = None

    def build_draw_queue(
        self,
        world: World,
        camera: Camera,
        now: float,
    ) -> list[DrawCmd]:
        """Generate a list of draw commands based on the current world state."""
        draw_commands = []
        draw_commands.extend(self._build_world_draw_commands(world, camera))
        draw_commands.extend(self._build_ui_draw_commands(world, now))
        return draw_commands

    def _build_ui_draw_commands(self, world: World, now: float) -> list[DrawCmd]:
        draw_commands = []
        tile_size = world.tiles.tile_size
        for overlay_id, expiry_time in self.ui_overlays.items():
            if expiry_time > now and overlay_id == "player_info":
                player = world.get_current_player()
                player_pos = player.pos
                hud_position = Pos(
                    (player_pos.x - 1) * tile_size,
                    player_pos.y * tile_size,
                    0,
                )

                draw_commands.append(
                    DrawCmd(
                        type=DrawCmdType.TEXT,
                        text=player.get_hud_info(),
                        position=hud_position,
                    ),
                )

        if self.active_dialog:
            dialog_position = Pos(
                world.tiles.width * tile_size / 2,
                world.tiles.height * tile_size / 2,
                0,
            )
            draw_commands.append(
                DrawCmd(
                    type=DrawCmdType.DIALOG,
                    dialog=self.active_dialog,
                    position=dialog_position,
                ),
            )

        return draw_commands

    def _build_world_draw_commands(
        self,
        world: World,
        camera: Camera,
    ) -> list[DrawCmd]:
        """Generate a list of draw commands based on the current world state."""
        draw_commands = []

        # 1. Draw tiles from the tile map
        tile_map = world.tiles
        tile_size_pixels = tile_map.tile_size  # pixels

        start_tile_x = max(camera.x // tile_size_pixels, 0)
        start_tile_y = max(camera.y // tile_size_pixels, 0)

        end_tile_x = min(
            (camera.x + camera.screen_w) // tile_size_pixels,
            tile_map.width,
        )
        end_tile_y = min(
            (camera.y + camera.screen_h) // tile_size_pixels,
            tile_map.height,
        )

        for y in range(start_tile_y, end_tile_y + 1):
            for x in range(start_tile_x, end_tile_x + 1):
                tile = tile_map.get(x, y)
                if tile:
                    sprite = self.sprites.get(tile.sprite_id)

                    world_x = x * tile_size_pixels
                    world_y = y * tile_size_pixels

                    screen_x, screen_y = camera.world_to_screen(world_x, world_y)

                    # Create draw command
                    draw_commands.append(
                        DrawCmd(
                            type=DrawCmdType.SPRITE,
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

                world_pos_x, world_pos_y = entity.pos.x, entity.pos.y
                if (
                    camera.x <= world_pos_x < camera.x + camera.screen_w
                    and camera.y <= world_pos_y < camera.y + camera.screen_h
                ):
                    screen_x, screen_y = camera.world_to_screen(
                        world_pos_x,
                        world_pos_y,
                    )

                    draw_commands.append(
                        DrawCmd(
                            type=DrawCmdType.SPRITE,
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

    def add_ui_overlay(self, overlay_id: str, expiry_time: float) -> None:
        """Add a UI overlay that will expire after a certain time."""
        self.ui_overlays[overlay_id] = expiry_time

    def update(self, now: float, event_bus: EventBus) -> None:
        """Update the renderer state, e.g., handle UI overlays."""
        expired = [k for k, expiry in self.ui_overlays.items() if now > expiry]
        for k in expired:
            del self.ui_overlays[k]

        # Handle any events related to rendering, e.g., UI updates
        events = event_bus.get_events()
        for event in events:
            if event.event_type == EventType.UI_UPDATE:
                self._handle_ui_update_event(event, now)
            elif event.event_type == EventType.ASK_DIALOG:
                self._handle_ask_dialog_event(event)
            elif event.event_type == EventType.DIALOG_INPUT:
                self._handle_dialog_input_event(event)

    def _handle_ui_update_event(self, event: GameEvent, now: float) -> None:
        """Handle UI update events."""
        overlay_id = event.payload.get("overlay_id")
        expiry_time = event.payload.get("expiry_time", now + 5000)
        self.ui_overlays[overlay_id] = expiry_time
        print(f"UI overlay '{overlay_id}' added with expiry time {expiry_time}.")
        event.consume()

    def _handle_ask_dialog_event(self, event: GameEvent) -> None:
        """Handle dialog events."""
        dialog = event.payload.get("dialog")
        callback = event.payload.get("callback", None)
        options = event.payload.get("options", [])
        selected_index = event.payload.get("selected_index", 0)
        self.active_dialog = DialogBox(
            text=dialog,
            options=options,
            selected_index=selected_index,
            callback=callback,
        )
        event.consume()

    def _handle_dialog_input_event(self, event: GameEvent) -> None:
        """Handle dialog input events."""
        if self.active_dialog:
            key = event.payload.get("key")
            if key == "ArrowLeft":
                self.active_dialog.selected_index = max(
                    0,
                    self.active_dialog.selected_index - 1,
                )
            elif key == "ArrowRight":
                self.active_dialog.selected_index = min(
                    len(self.active_dialog.options) - 1,
                    self.active_dialog.selected_index + 1,
                )
            elif key == "Enter":
                if self.active_dialog.callback:
                    self.active_dialog.callback(
                        self.active_dialog.options[self.active_dialog.selected_index],
                    )
                self.active_dialog = None
            elif key == "Escape":
                self.active_dialog = None
        event.consume()
