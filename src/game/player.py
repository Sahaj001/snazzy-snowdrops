# src/game/player.py
from src.event_system import register_listener


class Player:
    def __init__(self) -> None:
        self.x, self.y = 100, 100
        register_listener("keydown", self.on_keydown)

    def on_keydown(self, key) -> None:
        if key == "ArrowUp":
            self.y -= 5
        elif key == "ArrowDown":
            self.y += 5
        elif key == "ArrowLeft":
            self.x -= 5
        elif key == "ArrowRight":
            self.x += 5
        print(f"Player moved to ({self.x}, {self.y})")
