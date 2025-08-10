class Event:
    def __init__(self, name, **kwargs) -> None:
        self.name = name
        self.data = kwargs


class EventManager:
    def __init__(self) -> None:
        self.listeners = {}

    def subscribe(self, event_name, callback) -> None:
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback) -> None:
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def dispatch(self, event) -> None:
        for callback in self.listeners.get(event.name, []):
            callback(event)
