# Acceptance verification — task-ids-14-02-t02-smspm-error-mapping

- **Gate:** PASS
- **Wave:** pkg-000047
- **Story:** STORY-IDS-SMSPM-02-sms-sender
- **Date:** 2026-08-20T10:27:17Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| 401 → `SEND_FAILED` | PASS | [`errors.py:30-32`](../../../../../../../src/core/phone/smspm/errors.py) |
| invalid phone string → `INVALID_PHONE` | PASS | [`errors.py:33-35`](../../../../../../../src/core/phone/smspm/errors.py) |
| 5xx / timeout → `PROVIDER_UNAVAILABLE` | PASS | [`errors.py:27-29,52-54`](../../../../../../../src/core/phone/smspm/errors.py) |
| else `SEND_FAILED` / `UNKNOWN` (D-02-2) | PASS | [`errors.py:36-41`](../../../../../../../src/core/phone/smspm/errors.py) |
| Logs must not include hash/token/OTP/full MSISDN (D-02-7) | PASS | [`errors.py:43-48`](../../../../../../../src/core/phone/smspm/errors.py) labels `http_401`/`invalid_phone`/…; exception message generic |
