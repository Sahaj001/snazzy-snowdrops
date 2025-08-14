from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import EventType
from models import Pos, TileMap
from models.direction import Direction

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from game.entities.entity import Entity
    from game.entities.player import Player


class World:
    """The game world, containing all entities and the tile map."""

    def __init__(
        self,
        tile_map: TileMap,
    ) -> None:
        self.players: list[Player] = []
        self.entities: list[Entity] = []
        self.tile_map = tile_map

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
        if not self.tile_map.is_passable(
            x // self.tile_map.tile_size,
            y // self.tile_map.tile_size,
        ):
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

        # If all checks pass, the location is considered passable
        for box in self.tile_map.collision_boxes:
            # print all the conditions for debugging
            print(
                f"Checking collision box: {box.id} at ({box.x}, {box.y}) "
                f"with size ({box.width}, {box.height}) for point ({x}, {y})",
            )
            if box.x <= x < box.x + box.width and box.y <= y < box.y + box.height:
                return box.passable

        return True

    def update(self, dt: float, event_bus: EventBus) -> None:
        """Update all entities in the world."""
        events = event_bus.get_events()

        for event in events:
            if event.event_type == EventType.INPUT:
                self._handle_input(event.payload, event_bus)
                event.consume()
            elif event.event_type == EventType.FRUIT_PICKED:
                self._handle_fruit_picked(event.payload)
                event.consume()

        for e in self.entities:
            e.update(self, dt)

    def _handle_fruit_picked(self, payload: dict) -> None:
        """Handle fruit picked events."""
        fruit_id = payload.get("fruit_id")
        fruit = self.get_entity_by_id(fruit_id)
        if fruit:
            self.remove_entity(fruit)

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
        tile_x: int,
        tile_y: int,
        entities: list[Entity],
    ) -> Entity | None:
        """Check if a click event intersects with any entity."""
        clickable_entities = []
        for entity in entities:
            entity_world_x, entity_world_y = entity.pos.x, entity.pos.y
            # check if click happens between pos +- tile_size
            if (
                entity_world_x <= tile_x < entity_world_x + self.tile_map.tile_size
                and entity_world_y <= tile_y < entity_world_y + self.tile_map.tile_size
            ):
                clickable_entities.append(entity)

        clickable_entities.sort(key=lambda e: e.pos.z, reverse=True)
        return clickable_entities[0] if clickable_entities else None

    def _handle_click_event(self, payload: dict, event_bus: EventBus) -> None:
        """Handle click events to interact with entities."""
        world_x, world_y = payload["position"]

        player_pos = self.players[0].pos if self.players else Pos(0, 0, 0)
        entities_in_scope = self.find_near(player_pos, self.tile_map.tile_size)
        clicked_entity = self._check_if_click_on_entity(
            world_x,
            world_y,
            entities_in_scope,
        )
        print(f"Clicked entity: {clicked_entity}")

        if clicked_entity and hasattr(clicked_entity, "interact"):
            clicked_entity.interact(
                self.players[0] if self.players else None,
                event_bus,
            )

    def _handle_key_event(self, payload: dict) -> None:
        """Handle key events for player movement."""
        key = payload["key"]

        player = self.players[0] if self.players else None
        if not player:
            return

        if key == "ArrowUp":
            player.move(Direction.UP, self)
        elif key == "ArrowDown":
            player.move(Direction.DOWN, self)
        elif key == "ArrowLeft":
            player.move(Direction.LEFT, self)
        elif key == "ArrowRight":
            player.move(Direction.RIGHT, self)

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

    def get_current_player(self) -> Player | None:
        """Get the first player in the world."""
        return self.players[0] if self.players else None

    def get_entity_by_id(self, entity_id: str) -> Entity | None:
        """Get an entity by its ID."""
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None
