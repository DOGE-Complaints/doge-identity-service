## Task workspace — `task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Audit source: [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) (F1)
- Follow-up (не reopen pkg-000008): [`task-ids-06-01-t03-audit-f1-asgi-import-time-config-isolation`](../../../../EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-01-conftest-autouse-fixtures/task-ids-06-01-t03-audit-f1-asgi-import-time-config-isolation/README.md) 🟢 Done — lazy `app` закрыт; остаётся cwd `.env` merge при `delenv`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000010`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F1  
---

## Task: fix — dotenv cwd test isolation (F1)

### Цель
Восстановить контракт `test_access_app_with_incomplete_supabase_env_raises_config_error`: при `delenv(SUPABASE_SERVICE_ROLE)` доступ к `asgi_app.app` должен поднимать `ConfigError`, даже если в cwd есть `.env` с service role.

### Почему это важно
Offline-сюита локально **199 passed / 1 failed**; индекс и acceptance t06 ссылаются на зелёную сюиту при фактическом падении F1. В CI без `.env` тест проходит — слабая изоляция маскируется в dev.

### Факты из кода
1. [`tests/test_asgi_import_config_isolation.py:28-41`](../../../../../../../tests/test_asgi_import_config_isolation.py) — ожидает `ConfigError` при доступе к `asgi_mod.app`; падает `DID NOT RAISE`.
2. [`src/core/config/providers.py:10-15`](../../../../../../../src/core/config/providers.py) — `merge_dotenv_from_cwd(source, priority=priority)` подмешивает cwd `.env` для ключей, отсутствующих в `os.environ`.
3. [`src/core/config/schema.py:107-108`](../../../../../../../src/core/config/schema.py) — `ConfigError` при `supabase` без непустого `SUPABASE_SERVICE_ROLE`.
4. [`src/core/api/asgi_app.py:346-354`](../../../../../../../src/core/api/asgi_app.py) — lazy `_default_production_app()` / `__getattr__("app")` (IDS-06 F1 закрыт на import-time).
5. [`tests/conftest.py`](../../../../../../../tests/conftest.py) — `_block_dotenv_leakage` не защищает, когда тест сам удаляет переменную из env.

### Gap / Проблема
Тест удаляет `SUPABASE_SERVICE_ROLE` из process env → ключ «отсутствует» → значение подтягивается из cwd `.env` → `provide_app_config()` успешен → регрессия offline-сюиты (не дефект `/me`).

### AC/DoD
- [x] (P0) `test_access_app_with_incomplete_supabase_env_raises_config_error` — PASS при наличии cwd `.env` с `SUPABASE_SERVICE_ROLE`.
- [x] (P0) `pytest -m "not live_integration" -q` — 0 failed (200 passed ожидаемо).
- [x] (P1) Решение задокументировано в BULLRUN-PHASE-LOG (изоляция теста vs переопределение merge — один выбранный путь).
- [x] (P1) Не ломать `make serve` / uvicorn entry `core.api.asgi_app:app`.

### Где менять код
- `doge-identity-service/tests/test_asgi_import_config_isolation.py` (предпочтительно: изоляция от cwd `.env`)
- опционально: `doge-identity-service/tests/conftest.py`, `src/core/config/env_file.py`

### Out of scope
- Изменение логики `handle_me` / AUTHCORE-01 runtime.
- Reopen EPIC-IDS-06 pkg-000008 или lazy `app` (уже Done).

### План выполнения
1. Выбрать путь: monkeypatch/chdir для теста **или** явный `env=` в `provide_app_config` в тесте **или** doc-only (только если инвариант меняется — с обоснованием).
2. Реализовать; прогнать изолированный тест и полную offline-сюиту.
3. BULLRUN-PHASE-LOG + sync gap row в индексе.

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_asgi_import_config_isolation.py::test_access_app_with_incomplete_supabase_env_raises_config_error -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
