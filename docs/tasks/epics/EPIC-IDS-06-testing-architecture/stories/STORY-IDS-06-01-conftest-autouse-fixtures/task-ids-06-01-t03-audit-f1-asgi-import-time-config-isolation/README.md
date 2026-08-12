## Task workspace — `task-ids-06-01-t03-audit-f1-asgi-import-time-config-isolation`

- Story: [`../STORY-IDS-06-01-conftest-autouse-fixtures.md`](../STORY-IDS-06-01-conftest-autouse-fixtures.md)
- Audit source: [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) (F1)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_06_audit_2026_06_02`  
**Decision Ref:** [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) §F1  
---

## Task: fix — import-time config isolation (F1)

### Цель
Устранить крэш collection при неполных Supabase creds в process env: module-level `provide_app_config()` / `create_app()` в `asgi_app` выполняется до autouse `_block_dotenv_leakage`.

### Почему это важно
Epic §8 verification cmd#3 не исполним; при `DB_BACKEND=supabase` + неполный env вся коллекция падает на import, хотя per-test изоляция env корректна.

### Факты из кода
1. [`src/core/api/asgi_app.py:346-347`](../../../../../../../src/core/api/asgi_app.py) — `_config = provide_app_config(); app = create_app(_config)` на уровне модуля.
2. [`tests/conftest.py:12`](../../../../../../../tests/conftest.py) — импорт `core.api.asgi_app` при collection (до autouse-фикстур).
3. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) — `ConfigError` при `DB_BACKEND=supabase` без `SUPABASE_SERVICE_ROLE`.
4. [`../../../../../../analysis/epic-ids-06-audit-2026-06-02.md`](../../../../../../analysis/epic-ids-06-audit-2026-06-02.md) — команда #4: collection fail без service_role.

### Gap / Проблема
Autouse `_block_dotenv_leakage` не покрывает import-time оценку конфига; заявление AC S1 «in_memory при .env с supabase» верно только при полных creds, иначе — fail collection.

### AC/DoD
- [x] (P0) `DB_BACKEND=supabase SUPABASE_URL=https://prod.local pytest tests/test_bootstrap_smoke.py --collect-only` — без `ConfigError` на import (lazy `app` в `asgi_app.py`).
- [x] (P0) `pytest -m "not live_integration" -q` — 196 passed (2026-06-02).
- [x] (P1) `tests/test_asgi_import_config_isolation.py` — import/collection contract.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py` (lazy app factory — предпочтительно по audit)
- опционально: `doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/EPIC-IDS-06-testing-architecture.md` §8 (если doc-only путь)
- опционально: `doge-identity-service/tests/` — контракт import/collection

### Out of scope
- Переписывание live Supabase integration (Story 3).
- Изменение логики `provide_service_factory` / DI singleton.

### План выполнения
1. Выбрать путь: lazy init в `asgi_app` **или** doc-align §8 cmd#3 (не оба без обоснования).
2. Реализовать выбранный путь; не ломать `make serve` / uvicorn entry (`app` export).
3. Прогнать audit verify cmd#4 и полный offline suite.

### Проверка
```bash
cd doge-identity-service
DB_BACKEND=supabase SUPABASE_URL=https://prod.local .venv/bin/python -m pytest tests/test_bootstrap_smoke.py --collect-only -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
