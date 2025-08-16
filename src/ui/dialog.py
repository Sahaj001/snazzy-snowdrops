from collections.abc import Callable

from js import document


class DialogBox:
    """Represents a dialog box with text and options."""

    def __init__(
        self,
        text: str,
        options: list[str],
        selected_index: int = 0,
        callback: Callable[[str], None] | None = None,
    ) -> None:
        self.text = text
        self.options = options
        self.selected_index = selected_index
        self.callback = callback

    def update(
        self,
    ) -> None:
        """Update the dialog box state."""
        dialog_message = document.querySelector(".dialog-message")
        if dialog_message:
            dialog_message.textContent = self.text

        dialog_options = document.querySelectorAll(".dialog-btn")
        for i, option in enumerate(dialog_options):
            if i < len(self.options):
                option.textContent = self.options[i]
                option.style.display = "inline-block"
                option.value = self.options[i]

                def make_click_handler(option_value: str):
                    return lambda _event: self._on_option_click(option_value)

                option.onclick = make_click_handler(self.options[i])
            else:
                option.style.display = "none"

        dialog = document.getElementById("dialog")
        if dialog:
            dialog.style.display = "flex"

    def _on_option_click(self, value: str) -> None:
        """Handle option click events."""
        if self.callback:
            self.callback(value)
        dialog = document.getElementById("dialog")
        if dialog:
            dialog.style.display = "none"
