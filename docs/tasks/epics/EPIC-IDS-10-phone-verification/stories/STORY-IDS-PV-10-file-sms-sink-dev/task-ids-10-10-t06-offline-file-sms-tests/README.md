## Task workspace — `task-ids-10-10-t06-offline-file-sms-tests`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: [`task-ids-10-10-t01-file-sms-sender-core`](../task-ids-10-10-t01-file-sms-sender-core/README.md) … [`task-ids-10-10-t05-dev-hygiene-gitignore-env-example`](../task-ids-10-10-t05-dev-hygiene-gitignore-env-example/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) Scope §«Тесты (offline)»; Story AC #1–#6, #8  
---

## Task: tests — offline file SMS provider coverage

### Цель
Offline tests: append semantics, multi-number files, sanitize, pilot+file ConfigError, e2e `POST /auth/phone/request`, no httpx for file.

### Почему это важно
Story gate requires pytest evidence for all sender/registry/security behaviours before t07 acceptance.

### Факты из кода
1. Phone request handler: [`handlers.py:494,504`](../../../../../../../src/core/api/handlers.py).
2. Existing phone test patterns: `tests/test_phone_*`.
3. Config schema tests: `tests/test_phone_config_schema.py`.

### Gap / Проблема
No tests for `file` provider behaviour.

### AC/DoD
- [x] (P0) Two SMS same number → 2 append lines, timestamps ascending.
- [x] (P0) Different numbers → different outbox files.
- [x] (P0) Filename sanitize — only `+` and digits; no path traversal.
- [x] (P0) `APP_PROFILE=pilot` + `SMS_PROVIDER=file` → `ConfigError`.
- [x] (P0) E2e `POST /auth/phone/request` with `SMS_PROVIDER=file` creates log line with OTP text.
- [x] (P0) `file` provider does not create `httpx.Client`.
- [x] (P1) Story AC #1–#6, #8.

### Где менять код
- `doge-identity-service/tests/test_phone_file_sms_sender.py` (new, or extend existing `test_phone_*`)

### Out of scope
- Story gate doc sync (t07)
- Changes to mock/telnyx senders

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_file_sms_sender.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
