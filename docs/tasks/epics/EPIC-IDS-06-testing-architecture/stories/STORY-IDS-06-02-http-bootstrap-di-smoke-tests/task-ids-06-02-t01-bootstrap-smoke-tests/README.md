## Task workspace — `task-ids-06-02-t01-bootstrap-smoke-tests`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 2  
**Story:** [`../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md`](../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md)  
---

## Task: tests — bootstrap smoke module

### Цель
Создать `tests/test_bootstrap_smoke.py` с 6 тестами из epic §6 Story 2 Outputs L157–163.

### Почему это важно
Проверяет импорты core-слоёв и fail-fast config до HTTP/DI smoke (epic Story 2).

### Факты из кода
1. [`tests/test_bootstrap_smoke.py`](../../../../../../../tests/test_bootstrap_smoke.py) — **отсутствует**.
2. [`tests/test_config_schema.py`](../../../../../../../tests/test_config_schema.py) — частичное пересечение config tests; epic требует отдельный модуль per §5 L54.
3. Epic Outputs L158–163 — список test functions.

### Gap
`test_bootstrap_smoke.py` отсутствует.

### AC/DoD
- [x] (P0) `test_core_imports` — импорты `core.config`, `core.api.asgi_app`, `core.api.dependencies`, `core.domain.contracts`, `core.providers.base`, `core.security.hashing`.
- [x] (P0) `test_app_config_from_env` — `DB_BACKEND=in_memory`, `EID_PROVIDER=mock` → `AppConfig.db_backend == "in_memory"`.
- [x] (P0) `test_config_fail_fast_on_invalid_backend` — `DB_BACKEND=postgres` → `ConfigError`.
- [x] (P0) `test_config_fail_fast_on_pilot_without_secrets` — `APP_PROFILE=pilot` без `OAUTH_ACCESS_TOKEN_SECRET` → `ConfigError`.
- [x] (P0) `test_config_fail_fast_on_pilot_empty_eid_secret` — `APP_PROFILE=pilot`, `DOGESTONIA_EID_SECRET=""` → `ConfigError`.
- [x] (P0) `test_config_fail_fast_on_unknown_eid_provider` — `EID_PROVIDER=xyz` → `ConfigError`.

### Где менять код
- `doge-identity-service/tests/test_bootstrap_smoke.py` (новый)

### Out of scope
- HTTP transport smoke — [`task-ids-06-02-t02-http-transport-smoke-tests`](../task-ids-06-02-t02-http-transport-smoke-tests/README.md)
- Story 2 acceptance — t05

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_bootstrap_smoke.py -v
```
