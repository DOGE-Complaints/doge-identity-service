# Acceptance verification — task-ids-14-02-t03-smspm-descriptor-wire

- **Gate:** PASS
- **Wave:** pkg-000047
- **Story:** STORY-IDS-SMSPM-02-sms-sender
- **Date:** 2026-08-20T10:27:17Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `build` returns `SmspmSmsSender(settings=…, http_client=runtime.http_client)` | PASS | [`descriptor.py:10-16`](../../../../../../../src/core/phone/smspm/descriptor.py) |
| Missing http_client → RuntimeError | PASS | [`descriptor.py:14-15`](../../../../../../../src/core/phone/smspm/descriptor.py) |
| `SmspmSmsStub` removed | PASS | no `SmspmSmsStub` in `src/` (rg 0 `.py`) |
| Do not change `_needs_sms_http_client` allow-list | PASS | [`runtime_factory.py:14-15`](../../../../../../../src/core/phone/runtime_factory.py) still `not in {"mock", "file"}` |
