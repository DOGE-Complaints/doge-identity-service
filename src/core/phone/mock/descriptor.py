from __future__ import annotations

from core.phone.base import SmsSenderPort
from core.phone.descriptor import SmsProviderDescriptor
from core.phone.mock.mock_sender import MockSmsSender
from core.phone.runtime import SmsProviderRuntime
from core.phone.config_spec import SmsProviderConfigSpec, noop_provider_settings_loader

MOCK_SMS_CONFIG_SPEC = SmsProviderConfigSpec(
    required=(),
    optional_defaults={},
    loader=noop_provider_settings_loader,
)


def _build_mock_sms_sender(_runtime: SmsProviderRuntime) -> SmsSenderPort:
    return MockSmsSender()


MOCK_SMS_DESCRIPTOR = SmsProviderDescriptor(
    name="mock",
    config_spec=MOCK_SMS_CONFIG_SPEC,
    build=_build_mock_sms_sender,
)
