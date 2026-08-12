## Task workspace — `task-ids-05-02-t03-story2-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 2  
**Story:** [`../STORY-IDS-05-02-supabase-repositories-identity-set.md`](../STORY-IDS-05-02-supabase-repositories-identity-set.md)  
---

## Task: tests — Story 2 acceptance verification

### Цель
Добавить pytest с mock httpx для verbatim AC Story 2 (epic L113–119).

### Почему это важно
Репозитории — тонкие PostgREST-обёртки; unit-тесты с mock фиксируют URL/body/conflict/JSONB без live Supabase.

### Факты из кода
1. Story 2 AC — [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) L113–119.
2. [`tests/test_inmemory_repositories.py`](../../../../../../../tests/test_inmemory_repositories.py) — reference behavior for conflict/session (InMemory).
3. `tests/test_db_supabase_repositories.py` — **отсутствует**.

### Gap
Нет pytest для Supabase repository AC L113–119.

### AC/DoD
- [x] (P0) `SupabaseProfileRepository(db).get_by_supabase_user_id("u1")` — GET с `eq.u1&limit=1`; пустой результат → `None`.
- [x] (P0) `SupabaseProfileRepository(db).attach_eid_verification(...)` с уже занятым `verified_person_hash` → доменная ошибка conflict (не bare httpx exception).
- [x] (P0) `SupabaseVerificationSessionStore.create(session)` — body содержит `provider`, `provider_session_data` (даже пустой `{}`).
- [x] (P0) `SupabaseEIDAuditLogRepository.log_event(event)` идемпотентен на app-уровне: повторный вызов с тем же event объектом не падает (audit append-only).
- [x] (P0) `SupabaseHealthRepository(db).ping()` делегирует на `db.healthcheck()`; `isinstance(SupabaseHealthRepository(db), HealthRepository)` — True (runtime Protocol check из EPIC-IDS-04).
- [x] (P0) JSONB поля при чтении — всегда `dict` (или `list`), никогда `str`.

### Где менять код
- `doge-identity-service/tests/test_db_supabase_repositories.py` (новый)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_db_supabase_repositories.py -v
```
