from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass
class InputEvent:
    """Represents a single user input event."""

    input_type: InputType
    key: str | None = None
    position: tuple[int, int] | None = None


class InputType(Enum):
    """Defines the type of input events."""

    KEYDOWN = "keydown"
    KEYUP = "keyup"
    CLICK = "click"


class InputSystem:
    """Manages input events."""

    def __init__(
        self,
    ) -> None:
        self._events: list[InputEvent] = []

    def consume_events(self) -> list[InputEvent]:
        """Return and clear the current input events."""
        events = self._events[:]
        self._events.clear()
        return events

    def push_event(self, event: InputEvent) -> None:
        """Add a new input event to the queue."""
        self._events.append(event)
