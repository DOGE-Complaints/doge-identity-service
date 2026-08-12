## Task workspace — `task-ids-11-04-t03-oauth-verify-gate-phone-branch`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: [`task-ids-11-04-t02-oauth-authorize-relay-handlers`](../task-ids-11-04-t02-oauth-authorize-relay-handlers/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) Scope §«не верифицирован → verify»; Story AC #2  
---

## Task: implement — OAuth verify-gate phone branch

### Цель
При `requested_action` требующем verify и `phone_verified=false` — сигнал «нужен verify» без выдачи authorization code (Story AC #2).

### Почему это важно
Подача истории из GPT требует phone verify; пользователь после логина не должен получить code, пока не пройдёт PV-05.

### Факты из кода
1. `phone_verified` в профиле: [`me_response.py`](../../../../../../../src/core/api/me_response.py), [`introspection.py:23-31`](../../../../../../../src/core/oauth/introspection.py).
2. `handle_oauth_authorize_complete` — точка гейта после Supabase login.
3. SPA login redirect: [`spa_login.py`](../../../../../../../src/core/oauth/spa_login.py).
4. Phone flow готов: PV-05 ✅.

### Gap / Проблема
Complete-path всегда выдаёт code при валидном JWT, не проверяя `phone_verified` для verify-requiring actions.

### AC/DoD
- [ ] (P0) Story AC #2: при action требующем verify + `phone_verified=false` — **no** authorization code.
- [ ] (P0) Сигнал verify-need: redirect/marker к verify-странице с `return_context`.
- [ ] (P0) `phone_verified` из `profile_repository`, не из JWT claims.
- [ ] (P1) Расширить `spa_login.py` или sibling для verify redirect URL с `return_context`.

### Где менять код
- `doge-identity-service/src/core/oauth/handlers.py` (`handle_oauth_authorize_complete`)
- `doge-identity-service/src/core/oauth/spa_login.py`

### Out of scope
- Канонический `verification_required` JSON module (t04)
- HTTP 403 mapping (t05)
- Gateway enforcement

### Проверка
```bash
cd doge-identity-service
grep -n 'phone_verified' src/core/oauth/handlers.py
```
