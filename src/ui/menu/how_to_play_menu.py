from __future__ import annotations

from typing import TYPE_CHECKING

from js import document

from engine.event_bus import EventBus, EventType, GameEvent


VISIBLE_CLASS = "visible"


class HowToPlayMenu:
    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:
        self.event_bus = event_bus

        self._how_to_play_menu = document.getElementById("how-to-play-menu")

        self._done_btn = document.querySelector("#how-to-play-menu .done")
        self._done_btn.onclick = lambda _: self._done_btn_onclick()

    def _done_btn_onclick(self) -> None:
        self.hide()
        self.event_bus.post(
            GameEvent(
                event_type=EventType.GAME_PAUSED,
                payload={},
            ),
        )

    def is_visible(self) -> bool:
        return self._how_to_play_menu.classList.contains(VISIBLE_CLASS)

    def make_visible(self) -> None:
        if not self.is_visible():
            self._how_to_play_menu.classList.add(VISIBLE_CLASS)

    def hide(self) -> None:
        self._how_to_play_menu.classList.remove(VISIBLE_CLASS)
