from typing import Self

from js import document, performance

from engine.state import DelayState, PauseState
from menu.settings_menu import SettingsMenu

VISIBLE_CLASS = "visible"


class MainMenu:
    _initialized = False
    _instance = None

    def __init__(self) -> None:
        if not self._initialized:
            self._main_menu = document.getElementById("main-menu")

            self._continue_btn = document.querySelector("#main-menu .continue")
            self._new_game_btn = document.querySelector("#main-menu .new-game")
            self._settings_btn = document.querySelector("#main-menu .settings")

            self._continue_btn.onclick = lambda _: self._continue_btn_onclick()
            self._new_game_btn.onclick = lambda _: self._new_game_btn_onclick()
            self._settings_btn.onclick = lambda _: self._settings_btn_onclick()

            self._initialized = True

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def _continue_btn_onclick(self) -> None:
        self.hide()
        PauseState.unpause()

    def _new_game_btn_onclick(self) -> None:
        self.hide()
        PauseState.unpause()
        DelayState.set_delay(performance.now())
        # more stuff to be done here

    def _settings_btn_onclick(self) -> None:
        self.hide()
        SettingsMenu().make_visible(self)

    def is_visible(self) -> bool:
        return self._main_menu.classList.contains(VISIBLE_CLASS)

    def make_visible(self) -> None:
        if not self.is_visible():
            self._main_menu.classList.add(VISIBLE_CLASS)

    def hide(self) -> None:
        self._main_menu.classList.remove(VISIBLE_CLASS)
