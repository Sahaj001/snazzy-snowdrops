from engine import state
from engine.event_bus import EventBus, EventType
from engine.input_system import InputSystem
from game.entities.fruit import Fruit
from game.world import World
from models.position import Pos
from models.sprite import SpriteRegistry
from models.tile import TileMap

class PlaceSystem:
    def __init__(
        self,
        input_sys: InputSystem,
        event_bus: EventBus,
        tile_map: TileMap,
        world: World,
        fruit_registry: SpriteRegistry,
    ) -> None:
        self.event_bus = event_bus
        self.input = input_sys
        self.tile_map = tile_map
        self.tile_size = tile_map.tile_size
        self.world = world
        self.fruit_registry = fruit_registry

    def update(self) -> None:
        """Update Place Mode and throw stuff if clicks are recieved."""
        events = self.event_bus.get_events()

        for event in events:
            if event.event_type == EventType.PLACE_MODE_STATE_CHANGE:
                if state.PlaceMode.is_enabled():
                    state.PlaceMode.disable()
                    print("Place Mode disabled")
                else:
                    state.PlaceMode.enable()
                    print("Place Mode enabled")
                event.consume()
            if event.event_type == EventType.MOUSE_CLICK and state.PlaceMode.is_enabled():
                pos = event.payload["position"]
                print(f"trying to place fruit at {pos}")
                self._place(*pos)
                event.consume()

    def _place(self, x: int, y: int) -> None:
        fruit_pos = Pos(
            x=(x // self.tile_size) * self.tile_size,
            y=(y // self.tile_size) * self.tile_size,
            z=1,
        )

        if not self.world.inventory.has_fruit():
            print("No fruit in inventory, cannot place.")
            return

        if self._is_placeable(fruit_pos):
            fruit = Fruit(
                fruit_id=f"fruit_t_{x}_{y}",
                pos=fruit_pos,
                behaviour=None,
                sprite_registry=self.fruit_registry,
            )
            self.world.add_entity(fruit)

            self.world.inventory.remove_fruit(self.world)

            print(f"placed {fruit.id} at {fruit_pos}")

    def _is_placeable(self, fruit_pos: Pos) -> bool:
        print(f"Checking if placeable at {fruit_pos}")
        player_pos = self.world.get_current_player().pos

        if (
            abs(fruit_pos.x - player_pos.x) <= self.tile_size * 2
            and abs(fruit_pos.y - player_pos.y) <= self.tile_size * 2
            and self._is_altar(fruit_pos)
        ):
            entities_in_scope = self.world.find_near(fruit_pos, self.tile_size)
            clicked_entity = self.world._check_if_click_on_entity(fruit_pos.x, fruit_pos.y, entities_in_scope)
            print(f"Clicked entity: {clicked_entity}")

            if clicked_entity is None:
                return True
        return False

    def _is_altar(self, fruit_pos: Pos) -> bool:
        for tile in self.tile_map.altars:
            if (
                tile[0] // self.tile_size == fruit_pos.x // self.tile_size
                and tile[1] // self.tile_size == fruit_pos.y // self.tile_size
            ):
                return True

        return False
