## Task workspace — `task-ids-03-02-t05-audit-di-2-create-app-dual-config-note`

- Story: [`../STORY-IDS-03-02-build-api-dependencies-singleton-lifespan.md`](../STORY-IDS-03-02-build-api-dependencies-singleton-lifespan.md)
- Audit source: [`../../../../../../analysis/epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) (DI-2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_03_audit_2026_05_28`  
---

## Task: docs — NOTE в `create_app` о dual-config паттерне

### Цель
Закрыть gap DI-2: задокументировать, что `create_app(config)` использует переданный `config` только для CORS, а DI-контейнер читает конфиг через `build_api_dependencies()` → `provide_app_config()` из `os.environ`.

### Почему это важно (риск)
Разработчик EPIC-IDS-04 может ожидать `get_api_dependencies().config == config` из `create_app(config)`; без документации — footgun при расхождении env и аргумента.

### Факты из кода
1. [`epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) DI-2 §Story 2.
2. [`src/core/api/asgi_app.py:59–76`](../../../../../../../src/core/api/asgi_app.py): `create_app(config)` — CORS из `config.cors_allowed_origins`; `_clear_api_dependencies_cache()` при сборке.
3. [`src/core/api/asgi_app.py:80–85`](../../../../../../../src/core/api/asgi_app.py): `_lifespan` → `get_api_dependencies()` → env-driven config.
4. [`tests/conftest.py`](../../../../../../../tests/conftest.py): тесты синхронизируют env через `monkeypatch.setenv` (audit L127).

### Gap / Проблема
Dual-config не задокументирован в runtime-коде; поведение корректно в тестах, но неочевидно для интеграции EPIC-IDS-04.

### AC/DoD
- [x] (P0) В `create_app` добавлен NOTE/docstring: `config` — только для CORSMiddleware; DI читает `provide_app_config()` из env (см. audit L131–137).
- [x] (P0) Упомянуть паттерн тестов: `monkeypatch.setenv` + `provide_app_config()` (ссылка на conftest).
- [x] (P1) Поведение runtime **не** меняется (только комментарий/docstring).

### Acceptance
- [acceptance-verification-task-ids-03-02-t05-audit-di-2-create-app-dual-config-note.md](./acceptance-verification-task-ids-03-02-t05-audit-di-2-create-app-dual-config-note.md) — PASS

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py` — `create_app`

### Out of scope
- Объединение config paths (отдельный epic/refactor)
- Изменения `build_api_dependencies`, `provide_app_config`

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/ -q -m "not live_integration"
```
