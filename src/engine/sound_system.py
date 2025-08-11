from __future__ import annotations

import json

from js import Audio


class SoundSystem:
    _initialized = False

    def __init__(self) -> None:
        if not self._initialized:
            with open("/assets/audio/bgm.json") as bgm_json:
                self._bgm_map = json.load(bgm_json)

            with open("/assets/audio/bgm.json") as sfx_json:
                self._sfx_map = json.load(sfx_json)

            self._bgm = Audio.new()
            self._bgm.loop = True

            self._sfx = Audio.new()

            self._initialized = True

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

    def __new__(cls) -> SoundSystem:  # noqa: PYI034
        """Singleton pattern: class can only have one instance,
        so multiple audios don't start playing out of nowhere.
        """  # noqa: D205
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance
