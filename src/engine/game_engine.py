from __future__ import annotations

from typing import TYPE_CHECKING

from js import Event, document
from pyodide.ffi import create_proxy

from engine.event_bus import EventType, GameEvent
from engine.input_system import InputType

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from engine.input_system import InputSystem
    from engine.place import PlaceSystem
    from engine.renderer_system import RenderSystem
    from engine.settings import Settings
    from engine.sound_system import SoundSystem
    from game.entities.entity import Entity
    from game.world import World


class GameEngine:
    """Main game controller tying together world, renderer, input, and events."""

    def __init__(
        self,
        world: World,
        renderer: RenderSystem,
        input_sys: InputSystem,
        event_bus: EventBus,
        sound_sys: SoundSystem,
        settings: Settings,
        place_sys: PlaceSystem,
    ) -> None:
        self.world = world
        self.renderer = renderer
        self.input = input_sys
        self.event_bus = event_bus
        self.sound_sys = sound_sys
        self.settings = settings
        self.place_sys = place_sys

        self._play_bgm_on_load_proxy = create_proxy(self._play_bgm_on_load)
        document.addEventListener("click", self._play_bgm_on_load_proxy)
        document.addEventListener("keypress", self._play_bgm_on_load_proxy)

    def tick(self, dt: float) -> None:
        """Advance the game state by dt seconds."""
        input_events = self.input.consume_events()

        for input_event in input_events:
            print(f"[Game Engine] Processing input event: {input_event}")
            if (
                input_event.input_type == InputType.CLICK
                and self.settings.game_state.is_resumed()
                and self.renderer.active_dialog is None
            ):
                # handle mouse click events only when game is resumed and no dialog is displayed
                screen_x, screen_y = input_event.position
                world_x, world_y = self.renderer.camera.screen_to_world(
                    screen_x,
                    screen_y,
                )
                if (
                    11 <= world_x // self.world.tile_map.tile_size <= 12  # noqa: PLR2004
                    and 7 <= world_y // self.world.tile_map.tile_size <= 8  # noqa: PLR2004
                ):
                    self.event_bus.post(
                        GameEvent(
                            EventType.BEGIN_PUZZLE,
                            {
                                "puzzle_kind": "sliding_tiles_puzzle",
                            },
                        ),
                    )
                    
                else:
                    self.event_bus.post(
                        GameEvent(
                            event_type=EventType.MOUSE_CLICK,
                            payload={"type": "click", "position": (world_x, world_y)},
                        ),
                    )

                self.sound_sys.play_sfx("btn-click")
            # handle keyboard events
            elif input_event.input_type in (InputType.KEYDOWN, InputType.KEYUP):
                event_type = self.get_event_type(input_event.key)

                self.event_bus.post(
                    GameEvent(
                        event_type=event_type,
                        payload={"type": "key", "key": input_event.key},
                    ),
                )

        self.settings.update(self.event_bus)
        if self.settings.game_state.is_resumed():
            self.place_sys.update()
            self.world.update(dt, self.event_bus)

    def render(self, now: float) -> None:
        """Render the current game state."""
        self.renderer.update(now, self.event_bus, self.world)
        if self.settings.game_state.is_paused():
            return
        cmds = self.renderer.build_draw_queue(
            self.world,
            self.renderer.camera,
        )
        self.renderer.flush_to_view(cmds)

    def spawn(self, e: Entity) -> None:
        """Add an entity to the world."""
        self.world.add_entity(e)

    def get_event_type(self, key: str) -> EventType | None:
        """Determine the event type based on the key pressed."""
        if key.lower() == "f" and not self.settings.game_state.is_paused():
            return EventType.PLACE_MODE_STATE_CHANGE
        if key in ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"):
            if EventType.BEGIN_PUZZLE:
                return EventType.PUZZLE_INPUT
            return EventType.PLAYER_MOVED
        if key == "Escape":
            if self.settings.game_state.is_paused():
                return EventType.GAME_RESUMED
            return EventType.GAME_PAUSED
        return None

    def _play_bgm_on_load(self, event: Event) -> None:
        if event.isTrusted:
            self.sound_sys.play_bgm("normal")

            document.removeEventListener("click", self._play_bgm_on_load_proxy)
            document.removeEventListener("keypress", self._play_bgm_on_load_proxy)
