## Task workspace — `task-ids-11-02-t04-oauth-introspect-route`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Prerequisite: t02 (service gate), t03 (handler)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000030`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) Scope §endpoint; Story AC #1, #2  
---

## Task: implement — POST /oauth/introspect route

### Цель
Зарегистрировать `POST /oauth/introspect`: сервисный токен на входе (dependency t02), пользовательский token в теле (form/JSON, RFC 7662-подобно), ответ из handler t03.

### Почему это важно
Backlog «Точки в коде» указывает отсутствие `/oauth/introspect`; gateway ожидает dedicated introspection endpoint.

### Факты из кода
1. [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — OAuth routes at `:368-403`; no introspect.
2. Existing OAuth routes pattern: `handle_oauth_token`, JSON/form parsing helpers in same file.
3. [`09-gateway-expectations.md:32`](../../../../../../../runtime-docs/09-gateway-expectations.md) — `/oauth/introspect` отсутствует.

### Gap / Проблема
Endpoint не экспонирован наружу.

### AC/DoD
- [x] (P0) `POST /oauth/introspect` registered and reachable.
- [x] (P0) Service token required before handler runs (Story AC #2).
- [x] (P0) User token in request body → introspection JSON response.
- [x] (P1) Route excluded from user-Bearer-only paths if applicable.
- [x] (P1) Traceability: Story AC #1, #2.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/src/core/api/dependencies.py` (route deps)

### Out of scope
- Handler implementation (t03)
- Config (t01)
- Runtime-docs update (post-P3 audit if needed)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q -k introspect
```
