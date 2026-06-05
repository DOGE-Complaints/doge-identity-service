"""Return URL allowlist validation (req-11 P-006)."""

from __future__ import annotations

from urllib.parse import urlparse


class InvalidReturnUrlError(ValueError):
    code: str = "invalid_return_url"


def parse_allowed_return_urls(raw: str) -> frozenset[str]:
    if not raw.strip():
        return frozenset()
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


def normalize_return_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise InvalidReturnUrlError(f"invalid return_url: {url!r}")
    path = parsed.path or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def validate_return_url(return_url: str | None, allowed: frozenset[str]) -> None:
    if return_url is None or not return_url.strip():
        return
    if not allowed:
        raise InvalidReturnUrlError("return_url not in allowlist: allowlist is empty")
    normalized = normalize_return_url(return_url)
    allowed_normalized = {normalize_return_url(entry) for entry in allowed}
    if normalized not in allowed_normalized:
        raise InvalidReturnUrlError(f"return_url not in allowlist: {return_url!r}")
