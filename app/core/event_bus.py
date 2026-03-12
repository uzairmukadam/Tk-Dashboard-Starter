class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_name, callback):
        """Subscribe a callback to an event."""
        self._subscribers.setdefault(event_name, []).append(callback)

    def unsubscribe(self, event_name, callback):
        """Remove a previously registered callback from an event."""
        listeners = self._subscribers.get(event_name, [])
        if callback in listeners:
            listeners.remove(callback)

    def publish(self, event_name, data=None):
        """Publish an event to all subscribers."""
        for callback in list(self._subscribers.get(event_name, [])):
            callback(data)

    def clear(self, event_name):
        """Remove all subscribers for a given event."""
        self._subscribers.pop(event_name, None)
