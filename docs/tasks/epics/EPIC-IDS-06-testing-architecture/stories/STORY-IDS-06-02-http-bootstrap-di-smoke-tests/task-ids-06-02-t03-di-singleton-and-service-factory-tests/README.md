## Task workspace — `task-ids-06-02-t03-di-singleton-and-service-factory-tests`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 2  
**Story:** [`../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md`](../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md)  
---

## Task: tests — DI singleton and service factory modules

### Цель
Создать `tests/test_di_singleton.py` (L173–176) и `tests/test_di_service_factory.py` (L177–180) per epic §6 Story 2.

### Почему это важно
Singleton DI должен сбрасываться между тестами; factory после EPIC-IDS-05 не фолбэчит на InMemory без creds (epic L179).

### Факты из кода
1. [`tests/test_di_singleton.py`](../../../../../../../tests/test_di_singleton.py) — **отсутствует** (deferred EPIC-IDS-03).
2. [`tests/test_di_service_factory.py`](../../../../../../../tests/test_di_service_factory.py) — **отсутствует**; overlap [`tests/test_service_factory.py`](../../../../../../../tests/test_service_factory.py).
3. [`src/core/infrastructure/providers.py`](../../../../../../../src/core/infrastructure/providers.py) — `provide_service_factory` supabase branch (EPIC-IDS-05 done).
4. Epic L179 — **после EPIC-IDS-05** тест `raises ValueError without supabase creds`, не fallback.

### Gap
Epic Outputs L173–180 не реализованы под каноническими именами файлов.

### AC/DoD
- [x] (P0) `test_di_singleton.py`: `test_singleton_is_same_object`, `test_clear_cache_allows_recreation`, `test_health_uses_singleton`.
- [x] (P0) `test_di_service_factory.py`: `test_factory_for_in_memory`.
- [x] (P0) `test_factory_raises_without_supabase_creds` (post-IDS-05; epic L179) — `DB_BACKEND=supabase` без creds → `ValueError`.
- [x] (P0) `test_factory_returns_same_instance_for_same_repository_call`.

### Где менять код
- `doge-identity-service/tests/test_di_singleton.py` (новый)
- `doge-identity-service/tests/test_di_service_factory.py` (новый)

### Out of scope
- eID registry / JWT validator — t04
- Live Supabase — Story 3

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_di_singleton.py tests/test_di_service_factory.py -v
```
