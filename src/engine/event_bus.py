from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Types of events that can be posted to the EventBus."""

    # input events
    MOUSE_CLICK = "click"
    PLAYER_MOVED = "player_moved"
    INPUT = "input"

    # dialog events
    ASK_DIALOG = "ask_dialog"
    CLOSE_DIALOG = "close_dialog"

    # interaction events
    FRUIT_PICKED = "fruit_picked"

    # game events
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"
    NEW_GAME = "new_game"
    OPEN_SETTINGS = "open_settings"
    OPEN_HELP = "open_help"

    #inventory events
    INVENTORY_CHANGE = "inventory_change"


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

    def clear(self, force: bool = False) -> None:
        """Clear the event queue."""
        # only clear events that are consumed
        self._queue = [evt for evt in self._queue if not evt.is_consumed or force]
