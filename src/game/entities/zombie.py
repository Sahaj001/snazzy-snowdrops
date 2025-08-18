import random
import time
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
    now = time.time()

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
        self.chasing = True
        self.prev_state = ZombieState.WALKING_DOWN
        self.take_damage_to_player = False
        self.now = time.time()

    def take_damage(self, target_pos: Pos):
        return ((self.pos.x - target_pos.x) ** 2 + (self.pos.y - target_pos.y) ** 2) ** (1/2)

    def update(self, **kwargs: int) -> None:
        """Update the zombie's state and position."""
        world = kwargs.get("world")
        if time.time() - self.now >= 1:
            print(self.take_damage(kwargs.get("target_pos", self.pos)))
            if self.take_damage(kwargs.get("target_pos", self.pos)) < 2:
                self.take_damage_to_player = True
            else:
                self.take_damage_to_player = False
        if self.chasing:
            self.chase(world, kwargs.get("target_pos", self.pos))
        else:
            self.wander(world)

        # Update frame index for animation
        self.update_frame_idx()

    def wander(self, world: "World") -> None:
        """Move the zombie in a random direction."""
        curr_state = self.state
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
        self.state = curr_state

    def chase(self, world: "World", target_pos: Pos) -> None:
        """Move towards the target position with seamless directional movement."""
        dx, dy = self.prev_state.direction().value
        next_x = self.pos.x + dx * self.step_size
        next_y = self.pos.y + dy * self.step_size

        # Check if continuing in previous direction moves toward target and is passable
        moving_toward_target = False
        if (
            (self.prev_state == ZombieState.WALKING_RIGHT and self.pos.x < target_pos.x)
            or (self.prev_state == ZombieState.WALKING_LEFT and self.pos.x > target_pos.x)
            or (self.prev_state == ZombieState.WALKING_DOWN and self.pos.y < target_pos.y)
            or (self.prev_state == ZombieState.WALKING_UP and self.pos.y > target_pos.y)
        ):
            moving_toward_target = True

        if moving_toward_target and world.is_passable(next_x, next_y):
            self.pos.x = next_x
            self.pos.y = next_y
            self.state = self.prev_state
            return 

        # If can't continue in previous direction, find new possible moves
        possible_moves = []

        if self.pos.x < target_pos.x:
            next_x = self.pos.x + self.step_size
            if world.is_passable(next_x, self.pos.y):
                possible_moves.append(("x", self.step_size, ZombieState.WALKING_RIGHT))
        elif self.pos.x > target_pos.x:
            next_x = self.pos.x - self.step_size
            if world.is_passable(next_x, self.pos.y):
                possible_moves.append(("x", -self.step_size, ZombieState.WALKING_LEFT))

        if self.pos.y < target_pos.y:
            next_y = self.pos.y + self.step_size
            if world.is_passable(self.pos.x, next_y):
                possible_moves.append(("y", self.step_size, ZombieState.WALKING_DOWN))
        elif self.pos.y > target_pos.y:
            next_y = self.pos.y - self.step_size
            if world.is_passable(self.pos.x, next_y):
                possible_moves.append(("y", -self.step_size, ZombieState.WALKING_UP))

        # If there are possible moves toward target, randomly choose one
        if possible_moves:
            axis, movement, new_state = random.choice(possible_moves)
            if axis == "x":
                self.pos.x += movement
            else:
                self.pos.y += movement
            self.prev_state = self.state
            self.state = new_state
        # If no direct path to target is passable, fall back to wandering behavior
        else:
            self.prev_state = self.state
            self.state = ZombieState.random()
            

        

    def update_frame_idx(self) -> None:
        """Update the frame index for the zombie's sprite animation."""
        if self.sprite_registry:
            sprite = self.sprite_registry.get(self.state.value)
            if sprite:
                self.frame_idx = (self.frame_idx + 1) % self.sprite_registry.get(
                    self.state.value,
                ).frame_count
        else:
            self.frame_idx = 0
