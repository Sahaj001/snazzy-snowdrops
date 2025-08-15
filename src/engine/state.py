class PauseState:
    _paused = False

    @classmethod
    def pause(cls) -> None:
        cls._paused = True

    @classmethod
    def unpause(cls) -> None:
        cls._paused = False

    @classmethod
    def is_paused(cls) -> bool:
        return cls._paused

    def __new__(cls) -> None:
        msg = f"{cls.__name__} can't be instantiated"
        raise TypeError(msg)


class DelayState:
    _delay = 0

    @classmethod
    def accum_delay(cls, dtime: float) -> None:
        cls._delay += dtime

    @classmethod
    def set_delay(cls, delay: float) -> None:
        cls._delay = delay

    @classmethod
    def get_delay(cls) -> float:
        return cls._delay