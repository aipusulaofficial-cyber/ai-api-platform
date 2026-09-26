import time
from threading import RLock


class SharedWindowLimiter:
    """Thread-safe limiter boundary for an injectable shared backend."""

    def __init__(self, limit: int, window_s: float = 60.0):
        if limit < 1 or window_s <= 0:
            raise ValueError("invalid limiter configuration")
        self.limit = limit
        self.window_s = window_s
        self._lock = RLock()
        self._hits: dict[str, list[float]] = {}

    def allow(self, key: str, now: float | None = None) -> bool:
        if not key:
            raise ValueError("key required")
        current = time.monotonic() if now is None else now
        with self._lock:
            hits = [t for t in self._hits.get(key, []) if current - t < self.window_s]
            if len(hits) >= self.limit:
                self._hits[key] = hits
                return False
            hits.append(current)
            self._hits[key] = hits
            return True
