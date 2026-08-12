## Task workspace — `task-ids-04-02-t03-story2-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 2  
**Story:** [`../STORY-IDS-04-02-inmemory-repositories.md`](../STORY-IDS-04-02-inmemory-repositories.md)  
---

## Task: tests — Story 2 acceptance verification

### Цель
Добавить pytest-покрытие verbatim AC Story 2 (epic L201–206): runtime Protocol checks, unique `verified_person_hash`, unknown state → `None`, `hash_secret` import, отсутствие httpx/joserfc/fastapi в infrastructure repos.

### Почему это важно
InMemory — единственный backend для тестов до EPIC-IDS-05; AC фиксируют поведение state machine и conflict detection (req-13).

### Факты из кода
1. Story 2 AC — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L201–206.
2. [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — **отсутствует** (t02).
3. [`src/core/security/hashing.py`](../../../../../../../src/core/security/hashing.py) — существует.
4. [`tests/`](../../../../../../../tests/) — нет `test_inmemory_repositories.py`.

### Gap
Нет автоматических тестов AC L201–206.

### AC/DoD
- [ ] (P0) `isinstance(InMemoryProfileRepository(), ProfileRepository)` — True (runtime Protocol check).
- [ ] (P0) `InMemoryProfileRepository().attach_eid_verification(user_id="u1", ..., verified_person_hash="h")` + повторный вызов с тем же `hash` для другого `user_id` → `RuntimeError` (имитация unique index).
- [ ] (P0) `InMemoryVerificationSessionStore().get_by_state("unknown")` → `None`.
- [ ] (P0) `from core.security.hashing import hash_secret` — импортируется без ошибок; unit-тест на детерминизм (опционально, одна строка).
- [ ] (P0) Все InMemory классы зависят только от stdlib + `core.security.hashing` (нет httpx, joserfc, fastapi импортов).

### Где менять код
- `doge-identity-service/tests/test_inmemory_repositories.py` (новый)

### Out of scope
- Реализация repositories — t02
- Factory integration — Story 3–6
- `tests/test_di_service_factory.py` — EPIC-IDS-06

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_inmemory_repositories.py -v
```
