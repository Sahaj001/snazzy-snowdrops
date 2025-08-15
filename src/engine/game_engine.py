from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import EventType, GameEvent
from engine.input_system import InputType
from engine.state import PauseState
from menu.pause_menu import PauseMenu

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from engine.input_system import InputSystem
    from engine.renderer_system import RenderSystem
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
    ) -> None:
        self.world = world
        self.renderer = renderer
        self.input = input_sys
        self.event_bus = event_bus
        self.sound_sys = sound_sys

        self.sound_sys.play_bgm("normal")

    def tick(self, dt: float) -> None:
        """Advance the game state by dt seconds."""
        input_events = self.input.consume_events()

        for input_event in input_events:
            print(f"[Game Engine] Processing input event: {input_event}")
            if input_event.input_type == InputType.CLICK:
                screen_x, screen_y = input_event.position
                world_x, world_y = self.renderer.camera.screen_to_world(
                    screen_x,
                    screen_y,
                )
                self.event_bus.post(
                    GameEvent(
                        event_type=EventType.MOUSE_CLICK,
                        payload={"type": "click", "position": (world_x, world_y)},
                    ),
                )

                self.sound_sys.play_sfx("btn-click")
            elif input_event.input_type in (InputType.KEYDOWN, InputType.KEYUP):
                event_type = (
                    EventType.DIALOG_INPUT
                    if self.renderer.active_dialog
                    else EventType.PLAYER_MOVED
                )
                if input_event.key == "Escape":
                    PauseMenu().make_visible()
                    PauseState.pause()
                event_type = EventType.DIALOG_INPUT if self.renderer.active_dialog else EventType.PLAYER_MOVED
                self.event_bus.post(
                    GameEvent(
                        event_type=event_type,
                        payload={"type": "key", "key": input_event.key},
                    ),
                )

        self.world.update(dt, self.event_bus)

    def render(self, now: float) -> None:
        """Render the current game state."""
        self.renderer.update(now, self.event_bus)
        cmds = self.renderer.build_draw_queue(self.world, self.renderer.camera, now)
        self.renderer.flush_to_view(cmds)

    def spawn(self, e: Entity) -> None:
        """Add an entity to the world."""
        self.world.add_entity(e)
