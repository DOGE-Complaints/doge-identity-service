from __future__ import annotations

from core.phone.base import SmsSenderPort
from core.phone.descriptor import SmsProviderDescriptor
from core.phone.runtime import SmsProviderRuntime
from core.phone.telnyx.config import TelnyxSettings, TELNYX_SMS_CONFIG_SPEC
from core.phone.telnyx.sender import TelnyxSmsSender


def _build_telnyx_sms_sender(runtime: SmsProviderRuntime) -> SmsSenderPort:
    settings = runtime.settings.get("telnyx")
    if not isinstance(settings, TelnyxSettings):
        raise RuntimeError("Telnyx settings are not loaded in SMS provider runtime")
    if runtime.http_client is None:
        raise RuntimeError("Telnyx SMS provider requires an HTTP client in runtime")
    return TelnyxSmsSender(settings=settings, http_client=runtime.http_client)


TELNYX_SMS_DESCRIPTOR = SmsProviderDescriptor(
    name="telnyx",
    config_spec=TELNYX_SMS_CONFIG_SPEC,
    build=_build_telnyx_sms_sender,
)
