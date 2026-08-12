## Task workspace — `task-ids-09-01-t02-asgi-eid-start-wire-body`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Prerequisite: [`../task-ids-09-01-t01-handle-auth-eid-start-orchestration/README.md`](../task-ids-09-01-t01-handle-auth-eid-start-orchestration/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000015`  
**Skill declared:** python-pro  
---

## Task: implement — ASGI wire `POST /auth/eid/start` + JSON body

### Цель
В [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) парсить JSON body (`return_url`, `return_context`, `requested_action`); route вызывает handler из t01 (не stub).

### Почему это важно
Story Scope: start + флаг через `return_context`/`requested_action`; AC #1 через transport.

### Факты из кода
1. [`asgi_app.py:181-195`](../../../../../../../src/core/api/asgi_app.py) — route вызывает `handle_auth_eid_start_stub`, `return_url` только из query via `_return_url_from_request`.
2. [`tests/test_asgi_transport.py:77-107`](../../../../../../../tests/test_asgi_transport.py) — transport stubs для start (ожидают 501 → обновить в t05).
3. [`handlers.py:70-92`](../../../../../../../src/core/api/handlers.py) — текущий stub entry point.

### Gap / Проблема
Route wired на stub; JSON body для `return_context`/`requested_action` не парсится.

### AC/DoD
- [x] (P0) `POST /auth/eid/start` вызывает реальный handler t01 с `current_user` из JWT.
- [x] (P0) Body JSON: минимум `return_url`; опционально `return_context`, `requested_action` прокинуты в handler (story Scope).
- [x] (P0) Envelope-ответ с redirect URL при success (AC #1).
- [x] (P1) Обратная совместимость: `return_url` из query если body пуст.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- Handler orchestration logic — t01
- Mock callback route — t03
- eideasy/authentigate callbacks — EID-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_asgi_transport.py -k eid_start
```
