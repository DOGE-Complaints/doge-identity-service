from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from core.phone.base import SmsErrorCode, SmsSendResult, SmsSenderError

_SANITIZE_PHONE_FILENAME_RE = re.compile(r"[^+0-9]")


def _format_utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def sanitize_phone_log_basename(to_e164: str) -> str:
    return _SANITIZE_PHONE_FILENAME_RE.sub("", to_e164)


@dataclass
class FileSmsSender:
    """Dev SMS sender: appends message text to per-number log files on disk."""

    outbox_dir: Path

    @property
    def provider_name(self) -> str:
        return "file"

    def send(self, *, to_e164: str, text: str) -> SmsSendResult:
        safe_name = sanitize_phone_log_basename(to_e164)
        log_path = self.outbox_dir / f"{safe_name}.log"
        line = f"{_format_utc_iso(datetime.now(timezone.utc))}\t{text}\n"
        try:
            self.outbox_dir.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(line)
        except OSError as exc:
            raise SmsSenderError(str(exc), code=SmsErrorCode.SEND_FAILED) from exc
        return SmsSendResult(provider_message_id=f"file-{uuid.uuid4()}", accepted=True)
