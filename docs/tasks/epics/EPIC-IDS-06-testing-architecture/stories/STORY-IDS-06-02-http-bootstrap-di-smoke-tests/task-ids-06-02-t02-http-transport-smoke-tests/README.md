## Task workspace — `task-ids-06-02-t02-http-transport-smoke-tests`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 2  
**Story:** [`../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md`](../STORY-IDS-06-02-http-bootstrap-di-smoke-tests.md)  
---

## Task: tests — HTTP transport smoke module

### Цель
Создать `tests/test_http_transport_smoke.py` per epic §6 Story 2 Outputs L164–172: autouse `_reset_deps`, health/ready/me/CORS/trace_id, 14 routes check.

### Почему это важно
HTTP-слой через ASGITransport без реального сервера; `_clear_api_dependencies_cache()` обязателен (epic Story 2 Why L154).

### Факты из кода
1. [`tests/test_http_transport_smoke.py`](../../../../../../../tests/test_http_transport_smoke.py) — **отсутствует**.
2. [`tests/test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py) — частичный overlap; P3: migrate/consolidate в epic-имя файла, не менять AC.
3. [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — `_clear_api_dependencies_cache()` для autouse fixture.

### Gap
Epic §5 L55 / Story 2 Outputs L164–172 не реализованы.

### AC/DoD
- [x] (P0) autouse `_reset_deps` — `_clear_api_dependencies_cache()` до и после теста.
- [x] (P0) `test_health_returns_200` — `data.status == "ok"`.
- [x] (P0) `test_ready_returns_status` — `db_backend == "in_memory"`, `db_ready is True`.
- [x] (P0) `test_me_without_auth_returns_401` — `code == "AUTHENTICATION_REQUIRED"`.
- [x] (P0) `test_me_with_stub_bearer_returns_501` — `code == "NOT_IMPLEMENTED"`.
- [x] (P0) `test_options_me_cors_preflight` — `status_code == 200`.
- [x] (P0) `test_trace_id_propagation` — `x-trace-id: custom` в envelope.
- [x] (P0) `test_all_identity_routes_registered` — 14 paths из EPIC-IDS-02 Story 5 в `app.routes`.

### Где менять код
- `doge-identity-service/tests/test_http_transport_smoke.py` (новый)

### Out of scope
- DI singleton tests — t03
- Удаление `test_asgi_transport.py` — отдельное решение P3 после green suite

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_http_transport_smoke.py -v
```
