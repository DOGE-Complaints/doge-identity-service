from __future__ import annotations

from pathlib import Path

from core.phone.base import SmsSenderPort
from core.phone.descriptor import SmsProviderDescriptor
from core.phone.file.config import FILE_SMS_CONFIG_SPEC, FileSmsSettings
from core.phone.file.file_sender import FileSmsSender
from core.phone.runtime import SmsProviderRuntime


def _build_file_sms_sender(runtime: SmsProviderRuntime) -> SmsSenderPort:
    settings = runtime.settings.get("file")
    if not isinstance(settings, FileSmsSettings):
        raise RuntimeError("File SMS settings are not loaded in SMS provider runtime")
    return FileSmsSender(outbox_dir=Path(settings.outbox_dir))


FILE_SMS_DESCRIPTOR = SmsProviderDescriptor(
    name="file",
    config_spec=FILE_SMS_CONFIG_SPEC,
    build=_build_file_sms_sender,
)
