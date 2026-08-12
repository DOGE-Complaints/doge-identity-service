## Task workspace — `task-ids-11-01-t02-rfc6749-errors-scope-validation-client-secret`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Prerequisite: t01 (store contracts)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) Scope bullets `client_secret`, RFC 6749 errors, scope model; Story AC #2, #3, #7  
---

## Task: implement — RFC 6749 errors, scope validation, client_secret

### Цель
Ввести канон ошибок OAuth (`{error, error_description}`), валидацию scope-модели и включить проверку `client_secret` в prod-path token exchange.

### Почему это важно
Gap SEC-1: [`repositories.py:466-467`](../../../../../../../src/core/infrastructure/repositories.py) делает `del client_secret` — prod-path не защищён. Scope и ошибки должны соответствовать [req-14 §Scope Model](../../../../../requirements/14-oauth-server-custom-gpt.md).

### Факты из кода
1. [`repositories.py:466-467`](../../../../../../../src/core/infrastructure/repositories.py) — `client_secret` intentionally skipped.
2. [`repositories.py:405-427`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryOAuthClientStore.from_config` + client scopes.
3. [`schema.py:44-49,211-216`](../../../../../../../src/core/config/schema.py) — `OAUTH_*`, `GPT_OAUTH_*` env.
4. PKCE S256 уже в `InMemoryOAuthTokenService` — ошибки `invalid_grant` нужно отдавать в RFC формате.

### Gap / Проблема
Нет модуля oauth errors/scope; `client_secret` не валидируется; `invalid_grant` и прочие ошибки не унифицированы.

### AC/DoD
- [x] (P0) `src/core/oauth/errors.py` — RFC 6749 response helper (`error`, `error_description`).
- [x] (P0) `src/core/oauth/scope.py` — validate `profile:read` / `stories:draft` / `stories:create` against client allowed scopes.
- [x] (P0) `InMemoryOAuthTokenService.exchange_code_for_token` — verify `client_secret` when provided (reject mismatch).
- [x] (P0) Token errors: expired/reused code → `invalid_grant` in RFC format.
- [x] (P1) Unit tests: bad secret, bad scope, error JSON shape.

### Где менять код
- `doge-identity-service/src/core/oauth/` (new: `errors.py`, `scope.py`)
- `doge-identity-service/src/core/infrastructure/repositories.py` (`issue_access_token`, `InMemoryOAuthClientStore`)
- `doge-identity-service/tests/` (unit tests for errors/scope/secret)

### Out of scope
- HTTP route wiring (t03–t04)
- Introspection (OAUTH-02)
- Supabase persistence (OAUTH-03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
