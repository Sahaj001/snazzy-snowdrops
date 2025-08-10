from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.view_bridge import ViewBridge


class InputEvent:
    """Represents a single user input event."""

    def __init__(self, input_type: str, key: str) -> None:
        self.type = input_type  # e.g., "keydown", "keyup"
        self.key = key


class InputSystem:
    """Manages input events."""

    def __init__(self, view_bridge: ViewBridge) -> None:
        self.view_bridge = view_bridge
        self._events: list[InputEvent] = []

    def consume_events(self) -> list[InputEvent]:
        """Return and clear the current input events."""
        events = self._events[:]
        self._events.clear()
        return events

    def push_event(self, event: InputEvent) -> None:
        """Add a new input event to the queue."""
        self._events.append(event)
