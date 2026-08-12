## Task workspace — `task-ids-10-10-t04-pilot-file-provider-fail-fast`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: [`task-ids-10-10-t03-file-descriptor-registry-runtime`](../task-ids-10-10-t03-file-descriptor-registry-runtime/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) Scope §«Demo-only fail-fast»; Story AC #5  
---

## Task: implement — pilot + `SMS_PROVIDER=file` → `ConfigError`

### Цель
Anti-leak: при `APP_PROFILE=pilot` и `SMS_PROVIDER=file` → `ConfigError` (plaintext OTP on disk forbidden in pilot).

### Почему это важно
File sink writes plaintext OTP to disk; pilot/demo profile must fail-fast per security paradigm.

### Факты из кода
1. SMS provider validation: [`schema.py:170-178`](../../../../../../../src/core/config/schema.py) — registered names only.
2. Pilot block (mock guard exists): [`schema.py:180-195`](../../../../../../../src/core/config/schema.py) — **no file guard yet**.
3. Active provider validate hook: [`schema.py:116-119`](../../../../../../../src/core/config/schema.py).

### Gap / Проблема
`APP_PROFILE=pilot` + `SMS_PROVIDER=file` loads without error — OTP would leak to disk in pilot.

### AC/DoD
- [x] (P0) `APP_PROFILE=pilot` + `SMS_PROVIDER=file` → `ConfigError` with clear message.
- [x] (P0) Non-pilot profiles + `file` still allowed (dev).
- [x] (P1) Story AC #5 — verified in t06 tests.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`

### Out of scope
- Sender / registry changes (t01–t03)
- `.env.example` warning text (t05)

### Проверка
```bash
cd doge-identity-service
grep -n "pilot.*file\|file.*pilot" src/core/config/schema.py
python3 -m pytest tests/test_phone_config_schema.py -q -k pilot
```
