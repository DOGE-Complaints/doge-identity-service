"""Minimal `.env` parsing for operator DX (no python-dotenv dependency)."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, MutableMapping


def merge_dotenv_from_path(
    path: Path,
    target: MutableMapping[str, str],
    *,
    priority: Mapping[str, str],
) -> None:
    """Fill *target* with KEY=value from *path* only for keys absent in *priority*."""
    if not path.is_file():
        return
    fixed = frozenset(priority.keys())
    text = path.read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in fixed:
            continue
        value = value.strip().strip('"').strip("'")
        target[key] = value


def merge_dotenv_from_cwd(
    target: MutableMapping[str, str],
    *,
    priority: Mapping[str, str],
) -> None:
    merge_dotenv_from_path(Path.cwd() / ".env", target, priority=priority)


def _parse_dotenv_file(path: Path) -> dict[str, str]:
    """Parse `.env` file into a dict without applying priority rules."""
    parsed: dict[str, str] = {}
    if not path.is_file():
        return parsed
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        parsed[key] = value.strip().strip('"').strip("'")
    return parsed
