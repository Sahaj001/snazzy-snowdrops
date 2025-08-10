from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from game.entities.entity import Entity
    from game.entities.player import Player
    from models.position import Pos


class Tile:
    """Represents a single tile in the world."""

    def __init__(self, sprite_id: str, *, z: int = 0, passable: bool = False) -> None:
        self.sprite_id = sprite_id
        self.passable = passable
        self.z = z


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
        """Find all entities within `radius` of the given position."""
        result = []
        r2 = radius * radius
        for e in self.entities:
            dx = e.pos.x - pos.x
            dy = e.pos.y - pos.y
            if dx * dx + dy * dy <= r2:
                result.append(e)
        return result

    def is_passable(self, x: int, y: int) -> bool:
        """Check if a location is passable in the tile map."""
        return self.tiles.is_passable(x, y)

    def update(self, dt: float, event_bus: EventBus) -> None:
        """Update all entities in the world."""
        events = event_bus.poll()

        for event in events:
            if event.type == "input":
                self._handle_input(event.payload)

        for e in self.entities:
            e.update(self, dt)

    def _handle_input(self, payload: dict) -> None:
        print("payload", payload)
        key = payload["key"]
        etype = payload["type"]

        player = self.players[0] if self.players else None
        if not player:
            return

        if etype == "keydown":
            if key == "ArrowUp":
                player.move(0, -1)
            elif key == "ArrowDown":
                player.move(0, 1)
            elif key == "ArrowLeft":
                player.move(-1, 0)
            elif key == "ArrowRight":
                player.move(1, 0)

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
