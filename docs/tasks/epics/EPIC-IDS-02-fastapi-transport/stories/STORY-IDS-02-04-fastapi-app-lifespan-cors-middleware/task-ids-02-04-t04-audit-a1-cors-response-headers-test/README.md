## Task workspace — `task-ids-02-04-t04-audit-a1-cors-response-headers-test`

- Story: [`../STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware.md`](../STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (A-1)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_02_audit_2026_05_28`  
---

## Task: tests — CORS response headers (Access-Control-Allow-Origin)

### Цель
Закрыть gap A-1: добавить HTTP-тесты, что `CORSMiddleware` отражает разрешённый `Origin` в ответе и не эхоит недопустимый origin.

### Факты из кода
1. [`audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) A-1: CORS настроен в [`asgi_app.py:72–77`](../../../../../../../src/core/api/asgi_app.py), но заголовки не проверяются.
2. [`tests/conftest.py`](../../../../../../../tests/conftest.py): `CORS_ALLOWED_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"`.
3. [`tests/test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py): `test_options_me_returns_200` и `test_options_oauth_authorize_returns_200` проверяют только status 200.

### AC/DoD
- [x] (P0) `test_cors_allowed_origin_header_present`: `GET /health` с `Origin: http://localhost:3000` → `access-control-allow-origin == http://localhost:3000`.
- [x] (P0) `test_cors_disallowed_origin_not_reflected`: `GET /health` с `Origin: http://evil.com` → header ≠ `http://evil.com`.

### Acceptance
- [acceptance-verification-task-ids-02-04-t04-audit-a1-cors-response-headers-test.md](./acceptance-verification-task-ids-02-04-t04-audit-a1-cors-response-headers-test.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_asgi_transport.py` (fixture `test_client` из `conftest.py`)

### Out of scope
- Изменения `asgi_app.py`, `CORSMiddleware`, `config.cors_allowed_origins`

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_asgi_transport.py -q -k cors
```
