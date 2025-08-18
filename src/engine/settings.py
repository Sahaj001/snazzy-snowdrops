from engine.event_bus import EventBus, EventType
from engine.sound_system import SoundSystem
from engine.state import GameState
from ui.menu import MainMenu, SettingsMenu, HowToPlayMenu
from ui.inventory import InventoryState


class Settings:
    """Represents the game settings."""

    def __init__(self, event_bus: EventBus, sound_system: SoundSystem) -> None:
        self.game_state = GameState.PAUSED
        self.main_menu = MainMenu(event_bus=event_bus)
        self.settings_menu = SettingsMenu(event_bus=event_bus, sound_sys=sound_system)
        self.how_to_play_menu = HowToPlayMenu(event_bus=event_bus)

    def update(self, event_bus: EventBus) -> None:
        """Update the settings based on game events."""
        for event in event_bus.get_events():
            if event.event_type == EventType.GAME_PAUSED:
                self.game_state = GameState.PAUSED
                self.main_menu.make_visible()
                self.main_menu.enable_continue()
                InventoryState.update_inventory(self.game_state)
                event.consume()
            elif event.event_type == EventType.GAME_RESUMED:
                self.game_state = GameState.RESUMED
                self.main_menu.hide()
                self.settings_menu.hide()
                InventoryState.update_inventory(self.game_state)
                event.consume()
            elif event.event_type == EventType.NEW_GAME:
                self.game_state = GameState.RESUMED
                self.main_menu.make_visible()
                self.main_menu.disable_continue()
                event.consume()
            elif event.event_type == EventType.OPEN_SETTINGS:
                self.game_state = GameState.PAUSED
                self.settings_menu.make_visible()
                event.consume()
            elif event.event_type == EventType.OPEN_HELP:
                self.game_state = GameState.PAUSED
                self.how_to_play_menu.make_visible()
                event.consume()
