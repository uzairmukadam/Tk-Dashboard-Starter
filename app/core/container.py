class Container:
    def __init__(self):
        self._services = {}

    def register(self, name, instance):
        """Register a service by name."""
        self._services[name] = instance

    def resolve(self, name):
        """Resolve a service by name. Raises KeyError if not found."""
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered in the container.")
        return self._services[name]

    def get(self, name):
        """Alias for resolve(). Resolve a service by name."""
        return self.resolve(name)

    def has(self, name) -> bool:
        """Check whether a service is registered."""
        return name in self._services
