## Task workspace — `task-ids-06-05-t01-smoke-conftest-and-local-server-tests`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 5  
**Story:** [`../STORY-IDS-06-05-live-server-smoke.md`](../STORY-IDS-06-05-live-server-smoke.md)  
---

## Task: tests — smoke conftest and local server smoke module

### Цель
Реализовать `tests/smoke/conftest.py` и `tests/smoke/test_local_server_smoke.py` per epic §6 Story 5 Outputs L257–266; обеспечить исключение smoke из default `pytest tests/ -q` (AC L269).

### Почему это важно
Быстрая проверка после `make serve` / deploy через `IDENTITY_URL` (port 8100).

### Факты из кода
1. [`tests/smoke/.gitkeep`](../../../../../../../tests/smoke/.gitkeep) — нет реализации.
2. [`pyproject.toml`](../../../../../../../pyproject.toml) L32 — `testpaths = ["tests"]` (smoke сейчас **внутри** tree; нужна настройка exclusion per epic L269).
3. Epic L260 — `identity_url` fixture default `http://localhost:8100`.

### Gap
Smoke layer отсутствует; exclusion из default run не проверен.

### AC/DoD
- [x] (P0) `tests/smoke/conftest.py`: marker `smoke`, `identity_url` session fixture.
- [x] (P0) `test_health`, `test_ready`, `test_me_without_auth`, `test_options_me`, `test_options_oauth_authorize` per epic L262–266.
- [x] (P1) Smoke **не** собираются при `pytest tests/ -q` (pyproject `testpaths` / `norecursedirs` / marker filter — per epic L269).

### Где менять код
- `doge-identity-service/tests/smoke/conftest.py` (новый)
- `doge-identity-service/tests/smoke/test_local_server_smoke.py` (новый)
- `doge-identity-service/pyproject.toml` (при необходимости exclusion)

### Out of scope
- Story 5 acceptance — t02
- Production auto-run — epic §9 L315

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/ -q --collect-only 2>&1 | grep -c smoke || true
# expect 0 smoke items in default collection
```
