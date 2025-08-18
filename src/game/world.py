from __future__ import annotations

import copy
from typing import TYPE_CHECKING

from engine.event_bus import EventType, GameEvent
from game import Player
from models import Pos, TileMap
from game.inventory import Inventory, Item
from ui.inventory import InventoryOverlay

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from game import Zombie
    from game.entities.entity import Entity


class World:
    """The game world, containing all entities and the tile map."""

    def __init__(
        self,
        player: Player,
        entities: list[Entity],
        zombies: list[Zombie],
        tile_map: TileMap,
        inventory: Inventory
    ) -> None:
        self.players = []
        self.entities = []
        self.zombies = []

        self.inventory: Inventory = inventory
        self.inventory_ui: InventoryOverlay = InventoryOverlay(self.inventory)

        self.add_player(player)
        for entity in entities:
            self.add_entity(entity)
        for zombie in zombies:
            self.zombies.append(zombie)
            self.add_entity(zombie)

        self.tile_map = tile_map
        # create a deep copy of the original state of the world
        self._original_tile_map = copy.deepcopy(tile_map)
        self._original_entities = copy.deepcopy(self.entities)

    def reset_world(self) -> None:
        """Reset the world to its original state."""
        self.tile_map = copy.deepcopy(self._original_tile_map)
        self.entities = copy.deepcopy(self._original_entities)
        self.players = []
        for player in self._original_entities:
            if isinstance(player, Player):
                self.add_player(player)

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
            # player has width and height
            # check rectangle collision
            player_width, player_height = (
                self.tile_map.tile_size,
                self.tile_map.tile_size,
            )

            def rects_overlap(r1: tuple, r2: tuple) -> bool:
                x1, y1, w1, h1 = r1
                x2, y2, w2, h2 = r2
                return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

            if rects_overlap(
                (box.x, box.y, box.width, box.height),
                (x, y, player_width, player_height),
            ):
                return box.passable

        return True

    def update(self, dt: float, event_bus: EventBus) -> None:
        """Update all entities in the world."""
        events = event_bus.get_events()

        for event in events:
            if event.event_type == EventType.NEW_GAME:
                self.reset_world()
                event.consume()
                event_bus.clear(force=True)
                event_bus.post(
                    GameEvent(
                        event_type=EventType.GAME_RESUMED,
                        payload={},
                    ),
                )
                return
            if event.event_type == EventType.MOUSE_CLICK and not event.is_consumed:
                self._handle_click_event(event.payload, event_bus)
                event.consume()
            if event.event_type == EventType.INPUT:
                print("Input event received:", event.payload)
                self._handle_key_event(event.payload, event_bus)
                event.consume()
            elif event.event_type == EventType.INVENTORY_CHANGE:
                self._handle_inventory_change(event.payload)
                event.consume()
        for e in self.entities:
            e.update(
                time_delta=dt,
                events=events,
                world=self,
                target_pos=self.get_current_player().pos,
            )


    def _handle_inventory_change(self, payload: dict) -> None:
        """Handle inventory change events."""
        action_type = payload["action"]
        object_name = payload["object_name"]
        item_id = payload.get("item_id")

        if action_type == "add":
            item = Item(item_id, object_name, stackable=False)
            self.inventory.add(item)
        elif action_type == "remove":
            item = Item(item_id, object_name)
            self.inventory.remove(item)

        self.inventory_ui.items = self.inventory.return_all_items()

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
    
    def _handle_key_event(self, payload: dict, event_bus: EventBus) -> None:
        key = payload["key"]
        print("Key pressed:", key)

    def _handle_click_event(self, payload: dict, event_bus: EventBus) -> None:
        """Handle click events to interact with entities."""
        world_x, world_y = payload["position"]

        player_pos = self.players[0].pos if self.players else Pos(0, 0, 0)
        entities_in_scope = self.find_near(player_pos, self.tile_map.tile_size)
        clicked_entity = self.check_if_click_on_entity(
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
