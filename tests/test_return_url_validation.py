from __future__ import annotations

import pytest

from core.security.return_url import (
    InvalidReturnUrlError,
    normalize_return_url,
    parse_allowed_return_urls,
    validate_return_url,
)


def test_parse_allowed_return_urls_comma_separated() -> None:
    raw = "https://dogestonia.ee/verify, https://app.example/callback"
    assert parse_allowed_return_urls(raw) == frozenset(
        {"https://dogestonia.ee/verify", "https://app.example/callback"}
    )


def test_validate_return_url_accepts_allowlisted() -> None:
    allowed = parse_allowed_return_urls("https://dogestonia.ee/verify")
    validate_return_url("https://dogestonia.ee/verify", allowed)


def test_validate_return_url_rejects_foreign_domain() -> None:
    allowed = parse_allowed_return_urls("https://dogestonia.ee/verify")
    with pytest.raises(InvalidReturnUrlError, match="not in allowlist"):
        validate_return_url("https://evil.example/phish", allowed)


def test_validate_return_url_ignores_query_string_for_match() -> None:
    allowed = parse_allowed_return_urls("https://dogestonia.ee/verify")
    validate_return_url("https://dogestonia.ee/verify?context=foo", allowed)


def test_validate_return_url_none_is_allowed() -> None:
    validate_return_url(None, frozenset())


def test_normalize_return_url_rejects_missing_host() -> None:
    with pytest.raises(InvalidReturnUrlError):
        normalize_return_url("/relative-only")
