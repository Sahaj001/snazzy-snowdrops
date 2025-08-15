from __future__ import annotations

from typing import TYPE_CHECKING, Self

from js import document

if TYPE_CHECKING:
    from engine.sound_system import SoundSystem
    from menu.main_menu import MainMenu
    from menu.pause_menu import PauseMenu

VISIBLE_CLASS = "visible"


class SettingsMenu:
    _initialized = False
    _instance = None

    _ref: MainMenu | PauseMenu

    def __init__(self, sound_sys: SoundSystem | None = None) -> None:
        if not self._initialized:
            assert sound_sys is not None  # noqa: S101
            self._sound_sys = sound_sys

            self._settings_menu = document.getElementById("settings-menu")

            self._done_btn = document.querySelector("#settings-menu .done")

            self._done_btn.onclick = lambda _: self._done_btn_onclick()

            self._master_vol_slider = document.querySelector("#settings-menu #master")
            self._sfx_vol_slider = document.querySelector("#settings-menu #sound-effects")
            self._bgm_vol_slider = document.querySelector("#settings-menu #bg-music")

            self._master_vol_slider.onchange = lambda _: self._master_vol_slider_onchange()
            self._sfx_vol_slider.onchange = lambda _: self._sfx_vol_slider_onchange()
            self._bgm_vol_slider.onchange = lambda _: self._bgm_vol_slider_onchange()

            self._master_vol_slider.value = self._sound_sys.get_master_vol() * 100
            self._sfx_vol_slider.value = self._sound_sys.get_sfx_vol() * 100
            self._bgm_vol_slider.value = self._sound_sys.get_bgm_vol() * 100

            self._initialized = True

    def __new__(cls, sound_sys: SoundSystem | None = None) -> Self:  # noqa: ARG004
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def _done_btn_onclick(self) -> None:
        self.hide()
        self._ref.make_visible()

    def _master_vol_slider_onchange(self) -> None:
        self._sound_sys.set_master_vol(int(self._master_vol_slider.value) / 100)

    def _sfx_vol_slider_onchange(self) -> None:
        self._sound_sys.set_sfx_vol(int(self._sfx_vol_slider.value) / 100)

    def _bgm_vol_slider_onchange(self) -> None:
        self._sound_sys.set_bgm_vol(int(self._bgm_vol_slider.value) / 100)

    def is_visible(self) -> bool:
        return self._settings_menu.classList.contains(VISIBLE_CLASS)

    def make_visible(self, ref: MainMenu | PauseMenu) -> None:
        self._ref = ref

        if not self.is_visible():
            self._settings_menu.classList.add(VISIBLE_CLASS)

    def hide(self) -> None:
        self._settings_menu.classList.remove(VISIBLE_CLASS)