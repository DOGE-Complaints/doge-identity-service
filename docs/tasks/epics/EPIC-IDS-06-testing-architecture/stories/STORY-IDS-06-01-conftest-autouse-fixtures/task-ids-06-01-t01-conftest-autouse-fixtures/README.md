## Task workspace — `task-ids-06-01-t01-conftest-autouse-fixtures`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 1  
**Story:** [`../STORY-IDS-06-01-conftest-autouse-fixtures.md`](../STORY-IDS-06-01-conftest-autouse-fixtures.md)  
---

## Task: implement — conftest autouse fixtures

### Цель
Реализовать в `tests/conftest.py` три механизма из epic §6 Story 1 Outputs (L79–143): `_block_dotenv_leakage`, `_pytest_session_logging`, `pytest_collection_modifyitems` (auto `live_integration` для `tests/integration/supabase/`).

### Почему это важно
`_block_dotenv_leakage` — главный механизм изоляции; без него unit-тесты могут попасть в реальный Supabase (epic §6 Story 1 Why, L75).

### Факты из кода
1. [`tests/conftest.py`](../../../../../../../tests/conftest.py) L1–28 — есть `test_client` + `_TEST_ENV`, **нет** autouse `_block_dotenv_leakage` / `_pytest_session_logging` / `pytest_collection_modifyitems`.
2. Epic Outputs L80–143 — эталонная структура фикстур и env vars.
3. [`pyproject.toml`](../../../../../../../pyproject.toml) L35–37 — marker `live_integration` уже зарегистрирован (предусловие EPIC-IDS-01, epic L46).
4. Pattern — [`docs/tech-requirements/impl-epic-06-testing-architecture.md`](../../../../../../../docs/tech-requirements/impl-epic-06-testing-architecture.md) §Story 1.

### Gap
Epic §6 Story 1 Outputs L79–143 не реализованы в `tests/conftest.py`.

### AC/DoD
- [x] (P0) `_block_dotenv_leakage` с `autouse=True` перезаписывает identity-env vars per epic L92–131.
- [x] (P0) `_pytest_session_logging` вызывает `configure_logging` (epic L133–135).
- [x] (P0) `pytest_collection_modifyitems` маркирует `/tests/integration/supabase/` как `live_integration` (epic L137–142).
- [x] (P1) Top-level imports: `base64`, `os`, `pytest`, `configure_logging` (epic L82–88).

### Где менять код
- `doge-identity-service/tests/conftest.py`

### Out of scope
- Story 1 verbatim acceptance — [`task-ids-06-01-t02-story1-acceptance-verification`](../task-ids-06-01-t02-story1-acceptance-verification/README.md)
- Offline smoke test modules — Story 2
- `mock_oidc` tests — epic §9 Open Questions L314

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/ --collect-only -q 2>&1 | head -20
```
