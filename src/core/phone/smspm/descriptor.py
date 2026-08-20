from __future__ import annotations

from dataclasses import dataclass

from core.phone.base import SmsErrorCode, SmsSenderError, SmsSenderPort, SmsSendResult
from core.phone.descriptor import SmsProviderDescriptor
from core.phone.runtime import SmsProviderRuntime
from core.phone.smspm.config import SMSPM_SMS_CONFIG_SPEC, SmspmSettings


@dataclass(frozen=True)
class SmspmSmsStub:
    """Placeholder sender until STORY-IDS-SMSPM-02 implements HTTP POST."""

    @property
    def provider_name(self) -> str:
        return "smspm"

    def send(self, *, to_e164: str, text: str) -> SmsSendResult:
        raise SmsSenderError(
            "SMSPM HTTP send is not implemented (STORY-IDS-SMSPM-02)",
            code=SmsErrorCode.PROVIDER_UNAVAILABLE,
        )


def _build_smspm_sms_sender(runtime: SmsProviderRuntime) -> SmsSenderPort:
    settings = runtime.settings.get("smspm")
    if not isinstance(settings, SmspmSettings):
        raise RuntimeError("SMSPM settings are not loaded in SMS provider runtime")
    return SmspmSmsStub()


SMSPM_SMS_DESCRIPTOR = SmsProviderDescriptor(
    name="smspm",
    config_spec=SMSPM_SMS_CONFIG_SPEC,
    build=_build_smspm_sms_sender,
)
