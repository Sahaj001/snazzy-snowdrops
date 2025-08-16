from js import document, performance

from engine.event_bus import EventBus, EventType, GameEvent
from engine.state import DelayState

VISIBLE_CLASS = "visible"


class MainMenu:
    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self._main_menu = document.getElementById("main-menu")

        self._continue_btn = document.querySelector("#main-menu .continue")
        self._new_game_btn = document.querySelector("#main-menu .new-game")
        self._settings_btn = document.querySelector("#main-menu .settings")

        self._continue_btn.onclick = lambda _: self._continue_btn_onclick()
        self._new_game_btn.onclick = lambda _: self._new_game_btn_onclick()
        self._settings_btn.onclick = lambda _: self._settings_btn_onclick()

    def _continue_btn_onclick(self) -> None:
        self.hide()
        self.event_bus.post(
            GameEvent(
                event_type=EventType.GAME_RESUMED,
                payload={},
            ),
        )

    def _new_game_btn_onclick(self) -> None:
        self.hide()
        DelayState.set_delay(performance.now())
        # more stuff to be done here
        self.event_bus.post(
            GameEvent(
                event_type=EventType.NEW_GAME,
                payload={},
            ),
        )

    def _settings_btn_onclick(self) -> None:
        self.hide()
        self.event_bus.post(
            GameEvent(
                event_type=EventType.OPEN_SETTINGS,
                payload={},
            ),
        )

    def is_visible(self) -> bool:
        return self._main_menu.classList.contains(VISIBLE_CLASS)

    def make_visible(self) -> None:
        if not self.is_visible():
            self._main_menu.classList.add(VISIBLE_CLASS)

    def disable_continue(self) -> None:
        """Disable the continue button."""
        if self._continue_btn:
            self._continue_btn.disabled = True

    def enable_continue(self) -> None:
        """Enable the continue button."""
        if self._continue_btn:
            self._continue_btn.disabled = False

    def hide(self) -> None:
        self._main_menu.classList.remove(VISIBLE_CLASS)
