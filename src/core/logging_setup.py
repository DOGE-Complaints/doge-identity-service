from __future__ import annotations

import logging
import sys
from pathlib import Path


def configure_logging(
    log_level: str,
    log_format: str = "text",
    log_debug_dir: str | None = None,
) -> None:
    level = getattr(logging, log_level.upper(), logging.INFO)
    if log_format == "json":
        fmt = (
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"name": "%(name)s", "msg": %(message)s}'
        )
    else:
        fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(
        level=level,
        format=fmt,
        stream=sys.stdout,
        force=True,
    )
    if log_debug_dir:
        Path(log_debug_dir).mkdir(parents=True, exist_ok=True)


def log_runtime_exception(
    exc: Exception,
    *,
    trace_id: str | None,
    path: str,
) -> None:
    logger = logging.getLogger("core.runtime")
    logger.error(
        "unhandled_exception path=%s trace_id=%s exc=%r",
        path,
        trace_id,
        exc,
    )
