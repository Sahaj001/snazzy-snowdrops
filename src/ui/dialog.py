from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DialogBox:
    """Represents a dialog box with text and options."""

    text: str
    options: list[str]  # ["Yes", "No"]
    selected_index: int = 0
    callback: Callable[[str], None] = None
