from __future__ import annotations

import hmac

from core.security.hashing import hash_secret


def verify_client_secret(
    client_secret: str,
    *,
    expected_hash: str,
    key: str,
) -> bool:
    actual_hash = hash_secret(client_secret, key=key)
    return hmac.compare_digest(expected_hash, actual_hash)
