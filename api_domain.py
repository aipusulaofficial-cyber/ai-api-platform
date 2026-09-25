"""API governance primitives: version validation and deterministic token-bucket throttling."""
from dataclasses import dataclass
import time


@dataclass(frozen=True)
class ApiRequest:
    request_id: str
    version: str
    key: str


class TokenBucket:
    def __init__(self, capacity: int, refill_per_s: float) -> None:
        if capacity <= 0 or refill_per_s < 0:
            raise ValueError("invalid token bucket configuration")
        self.capacity = capacity
        self.tokens = float(capacity)
        self.rate = refill_per_s
        self.last: float | None = None

    def consume(self, cost: int = 1, now: float | None = None) -> bool:
        if cost < 1:
            raise ValueError("cost must be positive")
        current = time.monotonic() if now is None else now
        if self.last is None:
            self.last = current
        else:
            elapsed = current - self.last
            if elapsed < 0:
                raise ValueError("time must be monotonic")
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last = current
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True


def validate_version(version: str) -> None:
    if version not in {"v1", "v2"}:
        raise ValueError("unsupported api version")
