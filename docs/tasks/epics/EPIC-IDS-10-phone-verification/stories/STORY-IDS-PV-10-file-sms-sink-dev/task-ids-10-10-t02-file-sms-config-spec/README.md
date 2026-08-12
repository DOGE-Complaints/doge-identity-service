## Task workspace — `task-ids-10-10-t02-file-sms-config-spec`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: [`task-ids-10-10-t01-file-sms-sender-core`](../task-ids-10-10-t01-file-sms-sender-core/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) Scope §«Provider-owned config»; Story AC #1 (partial)  
---

## Task: implement — `file/config.py` + `SmsProviderConfigSpec`

### Цель
Provider-owned config для file SMS: `FILE_SMS_OUTBOX_DIR` optional, default `var/sms-outbox`.

### Почему это важно
Outbox path consumed by `FileSmsSender`; без config-spec `SMS_PROVIDER=file` не пройдёт provider-owned validation (PV-02 pattern).

### Факты из кода
1. Config spec pattern: [`config_spec.py`](../../../../../../../src/core/phone/config_spec.py).
2. Telnyx precedent: [`telnyx/config.py`](../../../../../../../src/core/phone/telnyx/config.py) (PV-06 t01).
3. Mock descriptor (no required config): [`mock/descriptor.py:9-24`](../../../../../../../src/core/phone/mock/descriptor.py).

### Gap / Проблема
Нет `file/config.py`; outbox dir hardcoded or missing.

### AC/DoD
- [x] (P0) `FileSmsSettings` (or equivalent) with `outbox_dir` from `FILE_SMS_OUTBOX_DIR`.
- [x] (P0) Default `var/sms-outbox` (relative to cwd) when env unset.
- [x] (P0) `SmsProviderConfigSpec` — **no required** fields (optional outbox only).
- [x] (P1) Story AC #1 (partial) — config wires into sender factory (t03).

### Где менять код
- `doge-identity-service/src/core/phone/file/config.py` (new)

### Out of scope
- Descriptor / registry (t03)
- Schema pilot guard (t04)
- `.env.example` (t05)

### Проверка
```bash
cd doge-identity-service
grep -n "FILE_SMS_OUTBOX_DIR\|outbox" src/core/phone/file/config.py
```
