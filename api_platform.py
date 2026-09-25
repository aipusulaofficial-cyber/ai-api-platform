"""Versioned AI API contract with authentication and deterministic throttling."""

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class APIRequest:
    api_key: str
    version: str
    payload: dict


class APIError(Exception):
    pass


class APIService:
    def __init__(self, keys, limit=10, window=60):
        self.keys = set(keys)
        self.limit = limit
        self.window = window
        self.hits = {}

    def handle(self, r, now=None):
        if r.api_key not in self.keys:
            raise APIError("unauthorized")
        if r.version not in {"v1"}:
            raise APIError("unsupported api version")
        now = time.monotonic() if now is None else now
        q = [x for x in self.hits.get(r.api_key, []) if now - x < self.window]
        if len(q) >= self.limit:
            raise APIError("rate limit")
        q.append(now)
        self.hits[r.api_key] = q
        return {"version": r.version, "status": "accepted"}
