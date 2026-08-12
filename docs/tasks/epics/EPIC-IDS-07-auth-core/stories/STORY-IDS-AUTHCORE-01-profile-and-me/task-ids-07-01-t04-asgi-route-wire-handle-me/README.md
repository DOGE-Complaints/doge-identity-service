## Task workspace — `task-ids-07-01-t04-asgi-route-wire-handle-me`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Prerequisite: [`../task-ids-07-01-t02-handle-me-handler/README.md`](../task-ids-07-01-t02-handle-me-handler/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000009`  
**Skill declared:** python-pro  
---

## Task: implement — wire `/me` route to `handle_me`

### Цель
Маршрут `GET /me` вызывает `handle_me`, а не `handle_me_stub`.

### Почему это важно
Без wiring handler не достигается из HTTP (story «Точки в коде» — [`asgi_app.py:159-169`](../../../../../../../src/core/api/asgi_app.py)).

### Факты из кода
1. [`asgi_app.py:159-169`](../../../../../../../src/core/api/asgi_app.py) — `me()` → `handle_me_stub`.
2. [`asgi_app.py:18`](../../../../../../../src/core/api/asgi_app.py) — import `handle_me_stub`.
3. [`security.py:65-70`](../../../../../../../src/core/api/security.py) — `Depends(get_current_user)` уже на маршруте.

### Gap / Проблема
HTTP layer всё ещё на stub 501.

### AC/DoD
- [x] (P0) `asgi_app.me` вызывает `handle_me` с `deps`, `current_user`, `trace_id`.
- [x] (P0) Import `handle_me` из `core.api.handlers`; `handle_me_stub` не используется маршрутом `/me`.
- [x] (P1) `make serve` / uvicorn entry без регрессии.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- Handler logic — t02/t03
- Smoke tests — t05

### Проверка
```bash
cd doge-identity-service
grep -n "handle_me" src/core/api/asgi_app.py
```
