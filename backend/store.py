import time
from collections import deque

class DataStore:
    def __init__(self):
        self._data = {}
        self._expirations = {}
        self._tombstones = deque(maxlen=100)

    def stats(self) -> dict:
        return {
            "total_keys": len(self._data),
            "active_ttls": len(self._expirations),
            "tombstone_count": len(self._tombstones)
        }
        
    def keys(self) -> list:
        active_keys = []
        for k in list(self._data.keys()):
            if self.exists(k):
                active_keys.append(k)
        return active_keys

    def _archive_to_tombstone(self, key: str, value: str, reason: str):
        self._tombstones.append({
            "key": key,
            "value": value,
            "reason": reason,
            "timestamp": time.time()
        })

    def set(self, key: str, value: str, ex_seconds: int = None):
        self._data[key] = value
        if ex_seconds is not None:
            self._expirations[key] = time.time() + ex_seconds
        else:
            self._expirations.pop(key, None) 

    def get(self, key: str) -> str | None:
        if key in self._expirations:
            if time.time() > self._expirations[key]:
                val = self._data.pop(key, None)
                self._expirations.pop(key, None)
                if val is not None:
                    self._archive_to_tombstone(key, val, "expired")
                return None
                
        return self._data.get(key)

    def delete(self, key: str) -> int:
        self.get(key) 
        
        if key in self._data:
            val = self._data.pop(key)
            self._expirations.pop(key, None)
            self._archive_to_tombstone(key, val, "deleted")
            return 1
        return 0

    def exists(self, key: str) -> int:
        self.get(key) 
        return 1 if key in self._data else 0

    def restore_latest(self) -> str | None:
        if not self._tombstones:
            return None
        
        record = self._tombstones.pop()
        self.set(record["key"], record["value"]) 
        return record["key"]