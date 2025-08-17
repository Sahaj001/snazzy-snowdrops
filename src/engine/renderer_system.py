from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import EventType, GameEvent
from models.draw_cmd import DrawCmd, DrawCmdType
from models.position import Pos
from ui import DialogBox, StatusBar, InventoryOverlay

if TYPE_CHECKING:
    from engine.camera import Camera
    from engine.event_bus import EventBus
    from game.world import World
    from view.view_bridge import ViewBridge


class RenderSystem:
    """Builds a draw queue and sends it to the view."""

    def __init__(
        self,
        view_bridge: ViewBridge,
        camera: Camera,
        inventory_overlay: InventoryOverlay
    ) -> None:
        self.view_bridge = view_bridge
        self.camera = camera
        self.active_dialog: DialogBox | None = None
        self.status_bar = StatusBar()
        self.inventory_overlay: InventoryOverlay = inventory_overlay

    def build_draw_queue(
        self,
        world: World,
        camera: Camera,
    ) -> list[DrawCmd]:
        """Generate a list of draw commands based on the current world state."""
        draw_commands = []
        draw_commands.extend(self._build_world_draw_commands(world, camera))
        draw_commands.extend(
            self._build_ui_draw_commands(
                world,
            ),
        )
        return draw_commands

    def _build_ui_draw_commands(
        self,
        world: World,
    ) -> list[DrawCmd]:
        draw_commands = []
        if self.active_dialog:
            dialog_position = Pos(
                world.tile_map.width * world.tile_map.tile_size / 2,
                world.tile_map.height * world.tile_map.tile_size / 2,
                0,
            )
            draw_commands.append(
                DrawCmd(
                    type=DrawCmdType.DIALOG,
                    dialog=self.active_dialog,
                    position=dialog_position,
                    scale=self.camera.zoom,
                ),
            )

        if self.inventory_overlay:
            draw_commands.append(
                DrawCmd(
                    type=DrawCmdType.INVENTORY_OVERLAY,
                    position=None,  # Position is handled by the InventoryOverlay class
                    inventory_overlay=self.inventory_overlay,
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
        tile_map = world.tile_map
        tile_size_pixels = tile_map.tile_size  # pixels

        start_tile_x = max(int(camera.x // tile_size_pixels), 0)
        start_tile_y = max(int(camera.y // tile_size_pixels), 0)

        end_tile_x = min(
            int((camera.x + camera.screen_w / camera.zoom) // tile_size_pixels),
            tile_map.width,
        )
        end_tile_y = min(
            int((camera.y + camera.screen_h / camera.zoom) // tile_size_pixels),
            tile_map.height,
        )

        for y in range(start_tile_y, end_tile_y + 1):
            for x in range(start_tile_x, end_tile_x + 1):
                tiles = tile_map.get(x, y)
                if tiles:
                    for tile in tiles:
                        world_x = x * tile_size_pixels
                        world_y = y * tile_size_pixels

                        screen_x, screen_y = camera.world_to_screen(world_x, world_y)

                        draw_commands.append(
                            DrawCmd(
                                type=DrawCmdType.TILE,
                                tile_gid=tile.gid,
                                position=Pos(screen_x, screen_y, tile.z),
                                layer=tile.z,
                                scale=self.camera.zoom,
                            ),
                        )

        # 2. Draw collision boxes
        for box in tile_map.collision_boxes:
            if camera.x <= box.x < camera.x + camera.screen_w and camera.y <= box.y < camera.y + camera.screen_h:
                screen_x, screen_y = camera.world_to_screen(box.x, box.y)
                draw_commands.append(
                    DrawCmd(
                        type=DrawCmdType.COLLISION,
                        position=Pos(screen_x, screen_y, 0),
                        collision_box=box,
                        scale=self.camera.zoom,
                    ),
                )

        # 3. Draw entities (players, NPCs, items, etc.)
        for entity in world.entities:
            # Get sprite for this entity type
            sprite = entity.sprite_registry.get(entity.state.value) if hasattr(entity, "sprite_registry") else None
            if not sprite:
                print(f"Sprite not found for entity: {entity} {entity.state}")
                continue

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
                        layer=entity.pos.z,
                        scale=self.camera.zoom,
                        frame_idx=(entity.frame_idx if hasattr(entity, "frame_idx") else 0),
                    ),
                )

        # Sort by layer for proper rendering order (lower layers first)
        draw_commands.sort(key=lambda cmd: cmd.layer)

        return draw_commands

    def flush_to_view(self, cmds: list[DrawCmd]) -> None:
        """Send the draw commands to the view for rendering."""
        self.view_bridge.draw(cmds)

    def update(self, now: float, event_bus: EventBus, world: World) -> None:
        """Update the renderer state, e.g., handle UI overlays."""
        # Handle any events related to rendering, e.g., UI updates
        events = event_bus.get_events()
        for event in events:
            if event.event_type == EventType.ASK_DIALOG:
                self._handle_ask_dialog_event(event)
            elif event.event_type == EventType.CLOSE_DIALOG:
                # Handle closing dialog events if needed
                if self.active_dialog:
                    print(f"Closing dialog: {self.active_dialog.text}")
                    self.active_dialog = None
                event.consume()
            elif event.event_type == EventType.INVENTORY_TOGGLE:
                if self.inventory_overlay.active:
                    print("Toggling inventory overlay off")
                    self.inventory_overlay.active = False
                elif not self.inventory_overlay.active:
                    print("Toggling inventory overlay on")
                    self.inventory_overlay.active = True
                event.consume()

        # update ui components like status bar
        if self.status_bar:
            player = world.get_current_player()
            self.status_bar.update(
                hp=player.hp,
                intelligence=player.intelligence,
                fatigue=player.fatigue,
                ticks=now,
                events=events,
            )

            self.status_bar.update_ui()

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
