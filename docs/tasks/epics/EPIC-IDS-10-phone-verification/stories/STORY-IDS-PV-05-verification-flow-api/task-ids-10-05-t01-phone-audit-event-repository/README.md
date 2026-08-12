## Task workspace — `task-ids-10-05-t01-phone-audit-event-repository`

- Story: [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md)
- Prerequisite: STORY-IDS-PV-01..04 Done

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** todo  
**Wave:** `pkg-000026`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) Scope bullet 4; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §5  
---

## Task: implement — `PhoneAuditEvent` and in-memory audit repository

### Цель
Добавить phone audit domain (отдельный от eID) — Story Scope §аудит; foundation для handlers t03/t04.

### Почему это важно
Story AC #4: все события в аудите без PII; handlers логируют request/confirm шаги.

### Факты из кода
1. eID образец: [`EIDAuditEvent`](../../../../../../../src/core/domain/models.py:91-102), [`EIDAuditLogRepository`](../../../../../../../src/core/domain/contracts.py:91-100).
2. `_log_eid_audit` pattern: [`handlers.py:85-113`](../../../../../../../src/core/api/handlers.py).
3. `PhoneAuditEvent` / `PhoneAuditLogRepository` **отсутствуют** (grep → 0).
4. `InMemoryEIDAuditLogRepository`: [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — mirror for phone.

### Gap / Проблема
Phone flow has no audit trail; cannot satisfy AC#4.

### AC/DoD
- [ ] (P0) `PhoneAuditEvent` frozen dataclass (mirror eID fields: `id`, `supabase_user_id`, `event_type`, `provider`, `success`, `failure_reason`, `request_id`, `created_at`; no raw phone/code in any field).
- [ ] (P0) `PhoneAuditLogRepository` protocol: `log_event`, `list_events` (mirror eID).
- [ ] (P0) `InMemoryPhoneAuditLogRepository` in `repositories.py`.
- [ ] (P1) `_log_phone_audit(deps, ...)` helper in `handlers.py` (stub callable from t03/t04) OR dedicated `phone_audit.py` module imported by handlers.
- [ ] (P1) Story AC #4: `failure_reason` uses `SmsErrorCode` values only, never E.164 or OTP plaintext.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/domain/contracts.py`
- `doge-identity-service/src/core/infrastructure/repositories.py`
- `doge-identity-service/src/core/api/handlers.py` (or `src/core/phone/audit.py`)

### Out of scope
- Supabase `phone_audit_events` migration — defer (offline in-memory sufficient for story AC)
- Handler orchestration — t03, t04
- DI wiring — t02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.domain.models import PhoneAuditEvent; from core.infrastructure.repositories import InMemoryPhoneAuditLogRepository; print(PhoneAuditEvent, InMemoryPhoneAuditLogRepository)"
```
