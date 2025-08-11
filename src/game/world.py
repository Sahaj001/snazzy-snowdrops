from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from models.position import Pos

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from game.entities.entity import Entity
    from game.entities.player import Player


@dataclass
class Tile:
    """Represents a single tile in the world."""

    sprite_id: str
    z: int = 0
    passable: bool = False


class TileMap:
    """Grid of tiles that makes up the world terrain."""

    def __init__(self, width: int, height: int, tile_size: int) -> None:
        self.width = width
        self.height = height
        self.tile_size = tile_size
        # 2D array: tiles[y][x]
        self.tiles: list[list[Tile | None]] = [[None for _ in range(width)] for _ in range(height)]

    def get(self, x: int, y: int) -> Tile | None:
        """Get the tile at given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def set(self, x: int, y: int, tile: Tile) -> None:
        """Set the tile at given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile

    def is_passable(self, x: int, y: int) -> bool:
        """Check if a tile can be walked on."""
        tile = self.get(x, y)
        return tile.passable if tile else False


class World:
    """The game world, containing all entities and the tile map."""

    def __init__(self, tiles: TileMap) -> None:
        self.players: list[Player] = []
        self.entities: list[Entity] = []
        self.tiles = tiles

    def find_near(self, pos: Pos, radius: int) -> list[Entity]:
        """Find all entities within `radius` of the given position using Chebyshev distance."""
        result = []
        for e in self.entities:
            dx = abs(e.pos.x - pos.x)
            dy = abs(e.pos.y - pos.y)
            distance = max(dx, dy)
            if distance <= radius:
                result.append(e)
        return result

    def is_passable(self, x: int, y: int) -> bool:
        """Check if a location is passable in the tile map."""
        # First check if the tile itself is passable
        if not self.tiles.is_passable(x, y):
            return False

        # Then check if any entity at this position blocks movement
        for entity in self.entities:
            if (
                entity.pos.x == x
                and entity.pos.y == y
                and hasattr(entity, "behaviour")
                and entity.behaviour
                and (entity.behaviour, "passable")
                and not entity.behaviour.passable
            ):
                return False

        return True

    def update(self, dt: float, event_bus: EventBus) -> None:
        """Update all entities in the world."""
        events = event_bus.get_events()

        for event in events:
            if event.event_type == "input":
                self._handle_input(event.payload, event_bus)

        for e in self.entities:
            e.update(self, dt)

    def _handle_input(self, payload: dict, event_bus: EventBus) -> None:
        """Handle input events like clicks or key presses."""
        print("_handle_input payload", payload)
        etype = payload["type"]
        if etype == "key":
            self._handle_key_event(payload)
        elif etype == "click":
            self._handle_click_event(payload, event_bus)
        else:
            print(f"Unhandled input event type: {etype}")

    def _check_if_click_on_entity(
        self,
        x: int,
        y: int,
        entities: list[Entity],
    ) -> Entity | None:
        """Check if a click event intersects with any entity."""
        for entity in entities:
            if entity.pos.x == x and entity.pos.y == y:
                return entity
        return None

    def _handle_click_event(self, payload: dict, event_bus: EventBus) -> None:
        """Handle click events to interact with entities."""
        screen_x, screen_y = payload["position"]
        # Convert screen coordinates to tile coordinates

        tile_x, tile_y = (
            screen_x // self.tiles.tile_size,
            screen_y // self.tiles.tile_size,
        )

        player_pos = self.players[0].pos if self.players else Pos(0, 0, 0)
        entities_in_scope = self.find_near(player_pos, 1)
        clicked_entity = self._check_if_click_on_entity(
            tile_x,
            tile_y,
            entities_in_scope,
        )
        print(f"Clicked entity: {clicked_entity}")

        if clicked_entity and hasattr(clicked_entity, "interact"):
            clicked_entity.interact(
                self.players[0] if self.players else None,
                event_bus,
            )

    def _handle_key_event(self, payload: dict) -> None:
        key = payload["key"]

        player = self.players[0] if self.players else None
        if not player:
            return

        if key == "ArrowUp":
            player.move(0, -1, self)
        elif key == "ArrowDown":
            player.move(0, 1, self)
        elif key == "ArrowLeft":
            player.move(-1, 0, self)
        elif key == "ArrowRight":
            player.move(1, 0, self)

    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the world."""
        self.entities.append(entity)

    def remove_entity(self, entity: Entity) -> None:
        """Remove an entity from the world."""
        if entity in self.entities:
            self.entities.remove(entity)

    def add_player(self, player: Player) -> None:
        """Add a player to the world."""
        self.players.append(player)
        self.add_entity(player)

    def remove_player(self, player: Player) -> None:
        """Remove a player from the world."""
        if player in self.players:
            self.players.remove(player)
            self.remove_entity(player)

    def get_player(self) -> Player | None:
        """Get the first player in the world."""
        return self.players[0] if self.players else None
