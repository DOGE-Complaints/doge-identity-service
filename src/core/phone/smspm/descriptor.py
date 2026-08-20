from __future__ import annotations

from core.phone.base import SmsSenderPort
from core.phone.descriptor import SmsProviderDescriptor
from core.phone.runtime import SmsProviderRuntime
from core.phone.smspm.config import SMSPM_SMS_CONFIG_SPEC, SmspmSettings
from core.phone.smspm.sender import SmspmSmsSender


def _build_smspm_sms_sender(runtime: SmsProviderRuntime) -> SmsSenderPort:
    settings = runtime.settings.get("smspm")
    if not isinstance(settings, SmspmSettings):
        raise RuntimeError("SMSPM settings are not loaded in SMS provider runtime")
    if runtime.http_client is None:
        raise RuntimeError("SMSPM SMS provider requires an HTTP client in runtime")
    return SmspmSmsSender(settings=settings, http_client=runtime.http_client)


SMSPM_SMS_DESCRIPTOR = SmsProviderDescriptor(
    name="smspm",
    config_spec=SMSPM_SMS_CONFIG_SPEC,
    build=_build_smspm_sms_sender,
)
