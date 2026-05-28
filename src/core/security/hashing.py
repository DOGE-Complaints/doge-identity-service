"""Security hashing helpers."""

from __future__ import annotations

import hashlib
import hmac


def hash_secret(plaintext: str, *, key: str) -> str:
    """Create deterministic HMAC hash for secret values."""
    return hmac.new(key.encode("utf-8"), plaintext.encode("utf-8"), hashlib.sha256).hexdigest()
