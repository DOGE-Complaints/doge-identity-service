from __future__ import annotations

ALLOWED_REQUESTED_ACTIONS: frozenset[str] = frozenset({"eid:verify", "stories:submit"})
VERIFY_REQUIRED_ACTIONS: frozenset[str] = frozenset({"stories:submit"})


def normalize_requested_action(value: str | None) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    if trimmed not in ALLOWED_REQUESTED_ACTIONS:
        raise ValueError(trimmed)
    return trimmed


def normalize_return_context(value: str | None) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    return trimmed or None


def action_requires_phone_verification(requested_action: str | None) -> bool:
    return requested_action in VERIFY_REQUIRED_ACTIONS
