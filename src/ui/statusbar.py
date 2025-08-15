from dataclasses import dataclass

from js import document


@dataclass
class StatusBar:
    """Represents the player's status bar displaying health, intelligence, and fatigue."""

    hp: int = 100
    max_hp: int = 100
    intelligence: int = 0
    max_intelligence: int = 100
    fatigue: int = 0
    max_fatigue: int = 100
    ticks: int = 0  # in-game ticks

    def update(
        self,
        hp: int,
        intelligence: int,
        fatigue: int,
        ticks: int | None = None,
    ) -> None:
        self.hp = hp
        self.intelligence = intelligence
        self.fatigue = fatigue
        if ticks is not None:
            self.ticks = ticks

    def update_ui(self) -> None:
        """Update the UI elements for the status bar."""

        def set_stat_py(selector: str, value: int):
            bar = document.querySelector(selector)
            if not bar:
                return
            bar.style.setProperty("--val", str(value))
            bar.querySelector(".track").setAttribute("aria-valuenow", str(value))
            bar.querySelector(".val").textContent = f"{value}%"

        set_stat_py("#hud .bar:nth-child(1)", self.hp)
        set_stat_py("#hud .bar:nth-child(2)", self.intelligence)
        set_stat_py("#hud .bar:nth-child(3)", self.fatigue)

        timer_element = document.querySelector("#game-timer .val")
        if timer_element:
            timer_element.textContent = format_game_time(self.ticks)


def format_game_time(ticks: float) -> str:
    """Convert game ticks to a formatted time string (HH:MM:SS)."""
    seconds = ticks // 1000
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
