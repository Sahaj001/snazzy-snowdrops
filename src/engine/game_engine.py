from __future__ import annotations

from typing import TYPE_CHECKING

from engine.event_bus import GameEvent
from engine.input_system import InputType
from engine.sound_system import SoundSystem

if TYPE_CHECKING:
    from engine.event_bus import EventBus
    from engine.input_system import InputSystem
    from engine.renderer_system import RenderSystem
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

    def tick(self, dt: float) -> None:
        """Advance the game state by dt seconds."""
        input_events = self.input.consume_events()

        for event in input_events:
            print(f"Processing input event: {event}")
            if event.input_type == InputType.CLICK:
                self.event_bus.post(
                    GameEvent("input", {"type": "click", "position": event.position}),
                )
            elif event.input_type in (InputType.KEYDOWN, InputType.KEYUP):
                # Handle key events
                print(f"Key event: {event.input_type} {event.key}")
                self.event_bus.post(
                    GameEvent("input", {"type": "key", "key": event.key}),
                )

        self.world.update(dt, self.event_bus)
        self.render()

    def render(self) -> None:
        """Render the current game state."""
        cmds = self.renderer.build_draw_queue(self.world, self.renderer.camera)
        self.renderer.flush_to_view(cmds)

    def spawn(self, e: Entity) -> None:
        """Add an entity to the world."""
        self.world.add_entity(e)
