from __future__ import annotations

from typing import Mapping


def resolve_idempotency_key(headers: Mapping[str, str]) -> str | None:
    for key, value in headers.items():
        if key.lower() == "idempotency-key":
            stripped = value.strip()
            return stripped if stripped else None
    return None
