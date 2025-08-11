from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GameEvent:
    """Represents a game-wide event."""

    event_type: str
    payload: dict


class EventBus:
    """A simple publish/subscribe queue."""

    def __init__(self) -> None:
        self._queue: list[GameEvent] = []

    def post(self, evt: GameEvent) -> None:
        """Post a new event to the queue."""
        self._queue.append(evt)

    def get_events(self) -> list[GameEvent]:
        """Retrieve and clear all events in the queue."""
        return list(self._queue)

    def clear(self) -> None:
        """Clear the event queue."""
        self._queue.clear()
