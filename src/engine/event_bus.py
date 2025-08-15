from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Types of events that can be posted to the EventBus."""

    INPUT = "input"
    UI_UPDATE = "ui_update"
    ASK_DIALOG = "ask_dialog"
    DIALOG_INPUT = "dialog_input"
    FRUIT_PICKED = "fruit_picked"
    INVENTORY_TOGGLE = "inventory_toggle"


@dataclass
class GameEvent:
    """Represents a game-wide event."""

    event_type: EventType
    payload: dict
    is_consumed: bool = False

    def consume(self) -> None:
        """Mark the event as consumed."""
        self.is_consumed = True


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
        # only clear events that are consumed
        self._queue = [evt for evt in self._queue if not evt.is_consumed]
