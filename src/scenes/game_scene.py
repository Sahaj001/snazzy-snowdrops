class GameScene:
    def __init__(self, event_manager) -> None:
        self.event_manager = event_manager

    def start(self) -> None:
        print("Game scene started")
        self.event_manager.subscribe("keydown", self.on_key)

    def update(self) -> None:
        pass  # game logic here

    def render(self) -> None:
        pass  # draw to canvas here

    def on_key(self, event) -> None:
        print(f"Key pressed: {event.data['key']}")
