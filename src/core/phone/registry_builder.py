from __future__ import annotations

from core.phone.descriptor import SmsProviderDescriptor
from core.phone.file.descriptor import FILE_SMS_DESCRIPTOR
from core.phone.mock.descriptor import MOCK_SMS_DESCRIPTOR
from core.phone.smspm.descriptor import SMSPM_SMS_DESCRIPTOR
from core.phone.telnyx.descriptor import TELNYX_SMS_DESCRIPTOR
from core.phone.registry import SmsSenderRegistry
from core.phone.runtime import SmsProviderRuntime

ALL_SMS_PROVIDER_DESCRIPTORS: tuple[SmsProviderDescriptor, ...] = (
    MOCK_SMS_DESCRIPTOR,
    FILE_SMS_DESCRIPTOR,
    TELNYX_SMS_DESCRIPTOR,
    SMSPM_SMS_DESCRIPTOR,
)

_DESCRIPTOR_BY_NAME = {descriptor.name: descriptor for descriptor in ALL_SMS_PROVIDER_DESCRIPTORS}


def registered_sms_provider_names() -> frozenset[str]:
    return frozenset(_DESCRIPTOR_BY_NAME)


def get_sms_provider_descriptor(name: str) -> SmsProviderDescriptor | None:
    return _DESCRIPTOR_BY_NAME.get(name)


def build_sms_registry(runtime: SmsProviderRuntime) -> SmsSenderRegistry:
    active_name = runtime.config.sms_provider
    names_to_register = {"mock"}
    if active_name != "mock":
        names_to_register.add(active_name)

    providers = {}
    for name in names_to_register:
        descriptor = _DESCRIPTOR_BY_NAME.get(name)
        if descriptor is None:
            continue
        providers[name] = descriptor.build(runtime)

    return SmsSenderRegistry(providers)
