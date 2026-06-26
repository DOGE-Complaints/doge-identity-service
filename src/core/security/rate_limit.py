from __future__ import annotations

import threading
from dataclasses import dataclass
from time import monotonic

from core.security.rate_limit_config import RateLimitRule


class RateLimitExceeded(Exception):
    def __init__(self, retry_after_s: int) -> None:
        self.retry_after_s = retry_after_s
        super().__init__(f"rate limit exceeded; retry after {retry_after_s}s")


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    retry_after_s: int


class InMemoryRateLimiter:
    """MVP sliding-window counter (in-process; spec 16 demo path)."""

    def __init__(self) -> None:
        self._hits: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def check(self, key: str, rule: RateLimitRule) -> RateLimitResult:
        now = monotonic()
        window_start = now - rule.window_s
        with self._lock:
            timestamps = self._hits.setdefault(key, [])
            timestamps[:] = [t for t in timestamps if t > window_start]
            if len(timestamps) >= rule.requests:
                oldest = min(timestamps)
                retry_after = max(1, int(oldest + rule.window_s - now) + 1)
                return RateLimitResult(allowed=False, retry_after_s=retry_after)
            timestamps.append(now)
            return RateLimitResult(allowed=True, retry_after_s=0)
