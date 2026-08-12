## Task workspace — `task-ids-01-04-t01-makefile-targets`

- Story: [`../STORY-IDS-01-04-makefile-railway-env-example.md`](../STORY-IDS-01-04-makefile-railway-env-example.md)
- Decision Ref: [`../../../../../../requirements/06-technical-scaffold.md`](../../../../../../requirements/06-technical-scaffold.md) §Шаг 4; эпик §Story 4 (audit M-2 check-env vars)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000001`  
---

## Task: implement — Makefile serve dev check-env test

### Цель
Makefile с `set -a && . ./.env`, uvicorn `--app-dir src`, port `${PORT:-8100}`, targets `test` / `test-live` с markers.

### Факты из кода
1. Эпик §Story 4: `check-env` печатает `APP_PROFILE`, `PORT`, `SUPABASE_URL`, `SUPABASE_JWT_SECRET`, `AUTHENTIGATE_ISSUER`, `EID_PROVIDER`.
2. Impl-epic Task 4.1 — структура gateway Makefile, port 8100.
3. `make serve` до EPIC-IDS-02: **ожидаемый** `ImportError` для `core.api.asgi_app` — не failure этой задачи.

### Gap / Проблема
Операторы запускают uvicorn без загрузки `.env` → неверный `db_backend` в логах.

### AC/DoD
- [x] (P0) Targets: `serve`, `dev`, `check-env`, `test`, `test-live` (см. эпик §Story 4).
- [x] (P0) `serve`/`dev`: host `127.0.0.1`, port `${PORT:-8100}`, `.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app`.
- [x] (P0) `test`: `pytest -m "not live_integration"`; `test-live`: `-m live_integration`.
- [x] (P0) `make check-env` exit 0 с identity-vars (значения могут быть `<not set>` в demo).

### Где менять код
- `doge-identity-service/Makefile`

### Out of scope
- `railpack.json` (T02)
- Реализация `asgi_app` (EPIC-IDS-02)

### Команды проверки
```bash
cd doge-identity-service && make check-env
```
