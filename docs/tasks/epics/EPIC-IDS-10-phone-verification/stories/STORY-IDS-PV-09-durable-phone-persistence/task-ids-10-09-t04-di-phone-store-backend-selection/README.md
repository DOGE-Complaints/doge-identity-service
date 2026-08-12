## Task workspace — `task-ids-10-09-t04-di-phone-store-backend-selection`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: [`task-ids-10-09-t02-supabase-phone-verification-session-store`](../task-ids-10-09-t02-supabase-phone-verification-session-store/README.md); [`task-ids-10-09-t03-supabase-phone-audit-log-repository`](../task-ids-10-09-t03-supabase-phone-audit-log-repository/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) Scope §«DI-переключатель по backend»; Story AC #4  
---

## Task: implement — DI phone store backend selection

### Цель
Ветвить phone session store и audit repo по `DB_BACKEND` в `providers.py` — по образцу OAuth [`providers.py:91-103`](../../../../../../../src/core/infrastructure/providers.py).

### Почему это важно
Сегодня phone stores подключены **безусловно** in-memory ([`providers.py:121-122`](../../../../../../../src/core/infrastructure/providers.py)); без DI switch durable path недоступен при `DB_BACKEND=supabase`.

### Факты из кода
1. Unconditional in-memory DI: [`providers.py:121-122`](../../../../../../../src/core/infrastructure/providers.py) — `InMemoryPhoneVerificationSessionStore()` / `InMemoryPhoneAuditLogRepository()`.
2. OAuth DI precedent: [`providers.py:91-103`](../../../../../../../src/core/infrastructure/providers.py) — `db_backend=="supabase"` → Supabase* ; else InMemory*.
3. Supabase stores from t02/t03 in [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py).

### Gap / Проблема
Phone stores не ветвятся по backend; always in-memory.

### AC/DoD
- [x] (P0) `DB_BACKEND=supabase` → `SupabasePhoneVerificationSessionStore` + `SupabasePhoneAuditLogRepository`.
- [x] (P0) `DB_BACKEND=in_memory` → прежние `InMemoryPhoneVerificationSessionStore` / `InMemoryPhoneAuditLogRepository` (unchanged behavior).
- [x] (P0) Existing offline tests remain green on in-memory path.
- [x] (P1) Traceability: Story AC #4.

### Где менять код
- `doge-identity-service/src/core/infrastructure/providers.py` (lines ~121-122 area)

### Out of scope
- Store implementations (t02, t03)
- Bootstrap (t05)
- Rate-limiting (SEC-01)
- Access-token statelessness (OAuth)

### Проверка
```bash
cd doge-identity-service
grep -A5 'PhoneVerificationSessionStore\|PhoneAuditLogRepository' src/core/infrastructure/providers.py
python3 -m pytest -m "not live_integration" -q
```
