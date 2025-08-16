from __future__ import annotations

from js import Audio


class SoundSystem:
    def __init__(self, bgm_map: dict, sfx_map: dict) -> None:
        self._master_vol = 1
        self._bgm_vol = 1
        self._sfx_vol = 1

        self._cur_bgm_audio: dict = {}
        self._cur_sfx_audio: dict = {}

        self._bgm_map = bgm_map
        self._sfx_map = sfx_map

        self._bgm = Audio.new()
        self._bgm.loop = True

        self._sfx = Audio.new()

    def _get_apparent_bgm_vol(self, vol: float) -> float:
        return self._master_vol * self._bgm_vol * vol

    def _get_apparent_sfx_vol(self, vol: float) -> float:
        return self._master_vol * self._sfx_vol * vol

    def get_master_vol(self) -> float:
        return self._master_vol

    def get_bgm_vol(self) -> float:
        return self._bgm_vol

    def get_sfx_vol(self) -> float:
        return self._sfx_vol

    def set_master_vol(self, vol: float) -> None:
        self._master_vol = vol

        self._bgm.volume = self._get_apparent_bgm_vol(
            self._cur_bgm_audio.get("volume", 0),
        )
        self._sfx.volume = self._get_apparent_sfx_vol(
            self._cur_sfx_audio.get("volume", 0),
        )

    def set_bgm_vol(self, vol: float) -> None:
        self._bgm_vol = vol
        self._bgm.volume = self._get_apparent_bgm_vol(
            self._cur_bgm_audio.get("volume", 0),
        )

    def set_sfx_vol(self, vol: float) -> None:
        self._sfx_vol = vol
        self._sfx.volume = self._get_apparent_sfx_vol(
            self._cur_sfx_audio.get("volume", 0),
        )

    def play_bgm(self, audio: str) -> None:
        """Play background music.

        params:
            audio: str - background music to play, i.e. "boss", "normal", etc.
        """
        self._cur_bgm_audio = self._bgm_map.get(audio)  # type: ignore

        if self._cur_bgm_audio:
            self._bgm.volume = self._get_apparent_bgm_vol(self._cur_bgm_audio["volume"])
            self._bgm.src = self._cur_bgm_audio["path"]
            self._bgm.play()

    def play_sfx(self, audio: str) -> None:
        """Play sound effect.

        params:
            audio: str - sound effect to play depending on event, i.e. "hit", "walk", "eat, etc.
        """
        self._cur_sfx_audio = self._sfx_map.get(audio)  # type: ignore

        if self._cur_sfx_audio:
            self._sfx.volume = self._get_apparent_sfx_vol(self._cur_sfx_audio["volume"])
            self._sfx.src = self._cur_sfx_audio["path"]
            self._sfx.play()
