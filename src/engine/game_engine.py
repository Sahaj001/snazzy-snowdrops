from __future__ import annotations

from typing import TYPE_CHECKING

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
    ) -> None:
        self.world = world
        self.renderer = renderer
        self.input = input_sys
        self.event_bus = event_bus

    def tick(self, dt: float) -> None:
        """Advance the game state by dt seconds."""
        self.world.update(dt)

    def render(self) -> None:
        """Render the current game state."""
        cmds = self.renderer.build_draw_queue(self.world, self.renderer.camera)
        self.renderer.flush_to_view(cmds)

    def spawn(self, e: Entity) -> None:
        """Add an entity to the world."""
        self.world.add_entity(e)
