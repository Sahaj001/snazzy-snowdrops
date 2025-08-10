from __future__ import annotations


class GameEvent:
    """Represents a game-wide event."""

    def __init__(self, event_type: str, payload: dict) -> None:
        self.type = event_type
        self.payload = payload


class EventBus:
    """A simple publish/subscribe queue."""

    def __init__(self) -> None:
        self._queue: list[GameEvent] = []

    def post(self, evt: GameEvent) -> None:
        """Post a new event to the queue."""
        self._queue.append(evt)

    def poll(self) -> list[GameEvent]:
        """Retrieve and clear all events in the queue."""
        events = self._queue[:]
        self._queue.clear()
        return events
