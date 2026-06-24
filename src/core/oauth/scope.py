from __future__ import annotations

CANONICAL_OAUTH_SCOPES: frozenset[str] = frozenset(
    {"profile:read", "stories:draft", "stories:create"}
)


def parse_scope_param(scope: str | None) -> list[str]:
    if not scope or not scope.strip():
        return sorted(CANONICAL_OAUTH_SCOPES)
    return [part for part in scope.split() if part]


def validate_requested_scopes(
    requested: list[str],
    *,
    allowed_scopes: list[str],
) -> list[str]:
    unknown = [scope for scope in requested if scope not in CANONICAL_OAUTH_SCOPES]
    if unknown:
        raise ValueError("invalid_scope")
    allowed = set(allowed_scopes)
    disallowed = [scope for scope in requested if scope not in allowed]
    if disallowed:
        raise ValueError("invalid_scope")
    return requested
