from __future__ import annotations

from core.security.hashing import hash_secret


def test_hash_secret_imports() -> None:
    assert callable(hash_secret)


def test_hash_secret_is_deterministic_hmac_sha256_hex() -> None:
    digest_a = hash_secret("demo", key="demo-key")
    digest_b = hash_secret("demo", key="demo-key")
    assert digest_a == digest_b
    assert len(digest_a) == 64
    assert all(ch in "0123456789abcdef" for ch in digest_a)
