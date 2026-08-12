## Task workspace — `task-ids-12-03-t01-phone-audit-event-ip-ua-model-fields`

- Story: [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- Prerequisite: STORY-IDS-SEC-01 🟢 (request IP pattern in rate-limit layer)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000037`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) Scope §модель данных; Story AC #3  
---

## Task: implement — PhoneAuditEvent ip_hash / user_agent_hash model fields

### Цель
Добавить поля `ip_hash` / `user_agent_hash` в `PhoneAuditEvent`, согласованные с `EIDAuditEvent` — Story Scope §модель данных, AC #3.

### Почему это важно
Phone-аудит сейчас не может нести hash-поля; без модели wiring (t03–t04) не сохранит IP/UA.

### Факты из кода
1. `PhoneAuditEvent` без hash-полей — [`models.py:93-101`](../../../../../../../src/core/domain/models.py).
2. `EIDAuditEvent` уже имеет `ip_hash` / `user_agent_hash` — [`models.py:114-115`](../../../../../../../src/core/domain/models.py).
3. In-memory repo принимает `PhoneAuditEvent` as-is — [`repositories.py:364-366`](../../../../../../../src/core/infrastructure/repositories.py).
4. Contract `PhoneAuditLogRepository.log_event` — [`contracts.py:98`](../../../../../../../src/core/domain/contracts.py).

### Gap / Проблема
Модель phone-аудита не содержит полей под IP/UA hash.

### AC/DoD
- [ ] (P0) `PhoneAuditEvent` dataclass: `ip_hash: str | None`, `user_agent_hash: str | None` (имена как у eID).
- [ ] (P0) Все конструкторы `PhoneAuditEvent(...)` в коде обновлены (default `None` до wiring t04).
- [ ] (P1) Поля согласованы с PV-09 durable shape (имена колонок — out of scope миграции).
- [ ] (P1) Traceability: Story AC #3.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/api/handlers.py` (`_log_phone_audit` call sites — minimal defaults)
- При необходимости: `repositories.py`, тестовые фабрики

### Out of scope
- Supabase `phone_audit_events` migration (PV-09)
- Hash computation (t02)
- eID wiring (t03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.domain.models import PhoneAuditEvent; import dataclasses; f={x.name for x in dataclasses.fields(PhoneAuditEvent)}; assert 'ip_hash' in f and 'user_agent_hash' in f"
.venv/bin/python -m pytest -m "not live_integration" -q --tb=no -x
```
