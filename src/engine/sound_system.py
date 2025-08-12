from __future__ import annotations

from js import Audio


class SoundSystem:
    def __init__(self, bgm_map: dict, sfx_map: dict) -> None:
        self._bgm_map = bgm_map
        self._sfx_map = sfx_map

        self._bgm = Audio.new()
        self._bgm.loop = True

        self._sfx = Audio.new()

    def play_bgm(self, audio: str) -> None:
        """Play background music.

        params:
            audio: str - background music to play, i.e. "boss", "normal", etc.
        """
        audio_file = self._bgm_map.get(audio)
        if audio_file:
            self._bgm.volume = audio_file["volume"]
            self._bgm.src = audio_file["path"]
            self._bgm.play()

    def play_sfx(self, audio: str) -> None:
        """Play sound effect.

        params:
            audio: str - sound effect to play depending on event, i.e. "hit", "walk", "eat, etc.
        """
        audio_file = self._sfx_map.get(audio)
        if audio_file:
            self._sfx.volume = audio_file["volume"]
            self._sfx.src = audio_file["path"]
            self._sfx.play()
