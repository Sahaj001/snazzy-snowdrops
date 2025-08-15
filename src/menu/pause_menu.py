from typing import Self

from js import document

from engine.state import PauseState
from menu.main_menu import MainMenu
from menu.settings_menu import SettingsMenu

VISIBLE_CLASS = "visible"


class PauseMenu:
    _initialized = False
    _instance = None

    def __init__(self) -> None:
        if not self._initialized:
            self._pause_menu = document.getElementById("pause-menu")

            self._continue_btn = document.querySelector("#pause-menu .continue")
            self._main_menu_btn = document.querySelector("#pause-menu .main-menu-btn")
            self._settings_btn = document.querySelector("#pause-menu .settings")

            self._continue_btn.onclick = lambda _: self._continue_btn_onclick()
            self._main_menu_btn.onclick = lambda _: self._main_menu_btn_onclick()
            self._settings_btn.onclick = lambda _: self._settings_btn_onclick()

            self._initialized = True

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def _continue_btn_onclick(self) -> None:
        self.hide()
        PauseState.unpause()

    def _main_menu_btn_onclick(self) -> None:
        self.hide()
        MainMenu().make_visible()

    def _settings_btn_onclick(self) -> None:
        self.hide()
        SettingsMenu().make_visible(self)

    def is_visible(self) -> bool:
        return self._pause_menu.classList.contains(VISIBLE_CLASS)

    def make_visible(self) -> None:
        if not self.is_visible():
            self._pause_menu.classList.add(VISIBLE_CLASS)

    def hide(self) -> None:
        self._pause_menu.classList.remove(VISIBLE_CLASS)
