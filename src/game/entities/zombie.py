import random
from enum import Enum
from typing import TYPE_CHECKING

from engine.interfaces import Behaviour
from game.entities.entity import Entity
from models import Direction, Pos, SpriteRegistry

if TYPE_CHECKING:
    from game import World


class ZombieState(Enum):
    WALKING_UP = "walking_up"
    WALKING_DOWN = "walking_down"
    WALKING_LEFT = "walking_left"
    WALKING_RIGHT = "walking_right"

    @classmethod
    def random(cls) -> "ZombieState":
        """Return a random walking state."""
        return random.choice(list(cls))

    def direction(self) -> Direction:
        """Return the direction associated with this state."""
        if self == ZombieState.WALKING_UP:
            return Direction.UP
        if self == ZombieState.WALKING_DOWN:
            return Direction.DOWN
        if self == ZombieState.WALKING_LEFT:
            return Direction.LEFT
        if self == ZombieState.WALKING_RIGHT:
            return Direction.RIGHT
        return Direction.LEFT


class Zombie(Entity):
    def __init__(
        self,
        zombie_id: str,
        pos: Pos,
        behaviour: Behaviour,
        sprite_registry: SpriteRegistry | None = None,
    ) -> None:
        super().__init__(zombie_id, pos, behaviour, sprite_registry)
        self.hp = 10
        self.state = ZombieState.WALKING_DOWN
        self.step_size = 1
        self.chasing = False

    def update(self, **kwargs: int) -> None:
        """Update the zombie's state and position."""
        world = kwargs.get("world")
        if self.chasing:
            self.chase(world, kwargs.get("target_pos", self.pos))
        else:
            self.wander(world)

        # Update frame index for animation
        self.update_frame_idx()

    def wander(self, world: "World") -> None:
        """Move the zombie in a random direction."""
        while True:
            dx, dy = self.state.direction().value
            next_x = self.pos.x + dx * self.step_size
            next_y = self.pos.y + dy * self.step_size
            if not world.is_passable(next_x, next_y):
                # If the next position is not passable, change direction
                self.state = ZombieState.random()
                continue

            self.pos.x = next_x
            self.pos.y = next_y
            break

    def chase(self, _world: "World", target_pos: Pos) -> None:
        """Move towards the target position."""
        if self.pos.x < target_pos.x:
            self.pos.x += self.step_size
        elif self.pos.x > target_pos.x:
            self.pos.x -= self.step_size

        if self.pos.y < target_pos.y:
            self.pos.y += self.step_size
        elif self.pos.y > target_pos.y:
            self.pos.y -= self.step_size

    def update_frame_idx(self) -> None:
        """Update the frame index for the zombie's sprite animation."""
        if self.sprite_registry:
            sprite = self.sprite_registry.get(self.state.value)
            print(f"Updating frame index for {self.state.value} with sprite: {sprite}")
            if sprite:
                self.frame_idx = (self.frame_idx + 1) % self.sprite_registry.get(
                    self.state.value,
                ).frame_count
        else:
            self.frame_idx = 0
