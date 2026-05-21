import threading

class IntelligenceHub:
    """
    Centralized Intelligence Hub for Omni-Prophet V20.
    Stores and shares data between physics, statistical, and outcome models.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(IntelligenceHub, cls).__new__(cls)
                cls._instance._data = {}
        return cls._instance

    def set(self, key, value, game_id=None):
        """Set a value in the hub, optionally scoped by game_id."""
        if game_id:
            if game_id not in self._data:
                self._data[game_id] = {}
            self._data[game_id][key] = value
        else:
            self._data[key] = value

    def get(self, key, default=None, game_id=None):
        """Get a value from the hub."""
        if game_id:
            return self._data.get(game_id, {}).get(key, default)
        return self._data.get(key, default)

    def clear(self, game_id=None):
        """Clear data for a game or the entire hub."""
        if game_id:
            if game_id in self._data:
                del self._data[game_id]
        else:
            self._data = {}

# Singleton instance for easy access
HUB = IntelligenceHub()
