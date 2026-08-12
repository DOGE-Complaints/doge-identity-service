## Task workspace — `task-ids-11-04-t02-oauth-authorize-relay-handlers`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: [`task-ids-11-04-t01-oauth-request-context-schema`](../task-ids-11-04-t01-oauth-request-context-schema/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) Scope §relay; Story AC #1  
---

## Task: implement — OAuth authorize relay handlers

### Цель
Пробросить `requested_action` и `return_context` через `/oauth/authorize` → persist → `/oauth/authorize/complete` (Story AC #1).

### Почему это важно
GPT передаёт контекст действия при authorize; без relay identity не знает, что пользователь хотел сделать после логина.

### Факты из кода
1. `handle_oauth_authorize` не читает контекст: [`handlers.py:22-116`](../../../../../../../src/core/oauth/handlers.py).
2. `save()` без relay-полей в том же модуле.
3. `handle_oauth_authorize_complete` — читает persisted request по `oauth_request_id`.
4. ASGI routes: [`asgi_app.py:370-416`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Query params `requested_action`/`return_context` игнорируются; persisted handshake не содержит их для complete-path.

### AC/DoD
- [ ] (P0) Story AC #1: `requested_action`/`return_context` парсятся из query на `/oauth/authorize`, валидируются, сохраняются в store.
- [ ] (P0) `/oauth/authorize/complete` читает persisted `requested_action`/`return_context` вместе с пользователем.
- [ ] (P0) Невалидный `requested_action` → RFC 6749 error (не silent ignore).
- [ ] (P1) Traceability: Story AC #1 verbatim.

### Где менять код
- `doge-identity-service/src/core/oauth/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py` (если нужна передача query)

### Out of scope
- Verify-gate при `phone_verified=false` (t03)
- `verification_required` payload (t04)
- Offline test suite (t06)

### Проверка
```bash
cd doge-identity-service
grep -n 'requested_action\|return_context' src/core/oauth/handlers.py
```
