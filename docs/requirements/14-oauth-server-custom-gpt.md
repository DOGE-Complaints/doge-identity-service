# 14. OAuth 2.0 Server — Custom GPT Authorization

> **Статус:** НЕ реализовано. Spec для `src/core/oauth/authorization_server.py`, `token_service.py`, `client_store.py`.
> **Предусловие:** Файл 09 (Supabase JWT validation) реализован.
> **Связь:** Custom GPT использует эти endpoints для получения access_token. Файл 15 (story auth) валидирует этот токен.

---

## Принцип (из ADR-IDS-002)

doge-identity-service реализует OAuth 2.0 Authorization Code Flow как Authorization Server.  
ChatGPT (Custom GPT) — OAuth client.  
Пользователь логинится через spa-app — credentials никогда не идут через ChatGPT.

```
ChatGPT → redirect → /oauth/authorize (identity-service)
/oauth/authorize → redirect → spa-app /login (пользователь вводит email/password)
spa-app → POST supabase login → supabase_jwt
spa-app → POST identity-service /oauth/authorize/complete (с supabase_jwt)
identity-service → redirect → ChatGPT callback?code=<auth_code>
ChatGPT → POST /oauth/token { code, client_id, client_secret }
identity-service → { access_token, token_type, expires_in }
ChatGPT → Authorization: Bearer <access_token> в каждом запросе
```

---

## Registered OAuth Client (ChatGPT)

```python
# src/core/oauth/client_store.py
# MVP: статическая конфигурация из env vars

REGISTERED_CLIENTS = {
    "openai-custom-gpt": OAuthClient(
        client_id=config.gpt_oauth_client_id,           # "openai-custom-gpt"
        client_secret_hash=hash(config.gpt_oauth_client_secret),
        redirect_uri=config.gpt_oauth_redirect_uri,     # "https://oauth.pstmn.io/v1/callback"
        allowed_scopes={"stories:create", "stories:draft", "profile:read"},
        grant_types={"authorization_code"},
    )
}
```

Post-MVP: clients хранятся в DB для динамической регистрации.

---

## GET /oauth/authorize

**Назначение:** Начало OAuth 2.0 Authorization Code Flow. ChatGPT редиректит сюда пользователя.

### Query params

```
response_type=code          (required, only "code" supported)
client_id=openai-custom-gpt (required)
redirect_uri=<callback>     (required, must match registered)
scope=stories:create        (optional, space-separated)
state=<csrf_token>          (required, client-generated)
code_challenge=<pkce>       (optional but recommended)
code_challenge_method=S256  (optional)
```

### Алгоритм

```
1. Validate client_id — exists in REGISTERED_CLIENTS?
   → Если нет: 400 { error: "invalid_client" }

2. Validate redirect_uri — matches registered?
   → Если нет: 400 { error: "invalid_redirect_uri" }
   (NOTE: return error directly, не через redirect — redirect_uri не trusted)

3. Validate response_type == "code"
   → Если нет: redirect back { error: "unsupported_response_type" }

4. Validate scope — subset of allowed_scopes?
   → Если нет: redirect back { error: "invalid_scope" }

5. Store authorization_request:
   {
     client_id, redirect_uri, scope, state,
     code_challenge, code_challenge_method,
     request_id (UUID), expires_at: now() + 5min
   }

6. Redirect user to spa-app login page:
   https://dogestonia.ee/login?oauth_request_id=<request_id>
   (spa-app показывает login form; после логина POST обратно на identity-service)
```

### Как spa-app завершает авторизацию

После успешного логина через Supabase:
```
POST /oauth/authorize/complete
Authorization: Bearer <supabase_jwt>
Body: { "oauth_request_id": "<request_id>" }
```

Identity-service:
1. Validates Supabase JWT → `supabase_user_id`
2. Resolves `oauth_request_id` → `authorization_request`
3. Generates `authorization_code` (UUID, single-use, TTL: `OAUTH_AUTHORIZATION_CODE_TTL_S`)
4. Stores: `{ code → (supabase_user_id, client_id, scope, code_challenge) }`
5. Redirects to `redirect_uri?code=<auth_code>&state=<original_state>`

---

## POST /oauth/token

**Назначение:** Обмен authorization_code на access_token.

### Request (form-encoded)

```
grant_type=authorization_code
code=<authorization_code>
redirect_uri=<must match original>
client_id=openai-custom-gpt
client_secret=<GPT_OAUTH_CLIENT_SECRET>
code_verifier=<pkce_verifier>  (if PKCE was used)
```

### Алгоритм

```
1. Authenticate client: validate client_id + client_secret
   → Если неверно: 401 { error: "invalid_client" }

2. Resolve authorization_code:
   - Найти по code
   - Проверить client_id совпадает
   - Проверить code не истёк (TTL)
   - Проверить code не использовался (single-use)
   → Если не найден/истёк/использован: 400 { error: "invalid_grant" }

3. Validate redirect_uri — matches original?
   → Если нет: 400 { error: "invalid_grant" }

4. Validate PKCE (если code_challenge был задан):
   base64url(sha256(code_verifier)) == code_challenge
   → Если нет: 400 { error: "invalid_grant" }

5. Mark code as consumed (single-use enforcement)

6. Issue access_token:
   - type: JWT signed with OAUTH_ACCESS_TOKEN_SECRET
   - TTL: OAUTH_ACCESS_TOKEN_TTL_S (default 3600s)
   - claims: { sub: supabase_user_id, scope, iss, exp, iat, jti }

7. Return token response
```

### Response

```json
HTTP 200
Content-Type: application/json

{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "stories:create stories:draft profile:read"
}
```

**Не возвращаем `refresh_token` в MVP.** ChatGPT повторяет Authorization Code Flow при истечении.

---

## Access Token Format (JWT)

```json
{
  "iss": "https://identity.dogestonia.ee",
  "sub": "<supabase_user_id>",
  "aud": "doge-identity-service",
  "exp": 1748376000,
  "iat": 1748372400,
  "jti": "<uuid>",
  "scope": "stories:create stories:draft profile:read",
  "token_type": "oauth_access"
}
```

Подпись: `HS256` с `OAUTH_ACCESS_TOKEN_SECRET`.

**Token НЕ содержит:**
```
eid_verified      — проверяется динамически при каждом запросе
verified_person_hash
personal_code
email
```

---

## Валидация access_token в endpoint handlers

```python
# src/core/oauth/token_service.py

def validate_oauth_access_token(token: str, *, config: AppConfig) -> OAuthClaims:
    """
    Validates OAuth access_token issued by doge-identity-service.
    Returns OAuthClaims with supabase_user_id and scope.
    Raises TokenValidationError if invalid/expired.
    """
    ...

@dataclass(frozen=True)
class OAuthClaims:
    supabase_user_id: str
    scope: frozenset[str]  # {"stories:create", "stories:draft", "profile:read"}
    jti: str               # for revocation (post-MVP)
```

---

## Scope Model

| Scope | Разрешает |
|-------|---------|
| `profile:read` | GET /me |
| `stories:draft` | POST /story-drafts (no eID required) |
| `stories:create` | POST /stories, POST /gpt/actions/submit-story (eID required) |

Scope `stories:create` в токене ≠ разрешение без eID. При запросе submit-story backend дополнительно проверяет `profiles.eid_verified`.

---

## Ошибки OAuth (RFC 6749 формат)

```json
HTTP 400
{
  "error": "invalid_grant",
  "error_description": "Authorization code expired or already used."
}
```

Стандартные коды: `invalid_client`, `invalid_grant`, `invalid_request`, `unsupported_grant_type`, `invalid_scope`.

---

## Acceptance Criteria

- [ ] `GET /oauth/authorize?response_type=code&client_id=openai-custom-gpt&...` → redirect к spa-app login
- [ ] `GET /oauth/authorize` с незарегистрированным `client_id` → 400 `invalid_client`
- [ ] `GET /oauth/authorize` с неверным `redirect_uri` → 400 `invalid_redirect_uri` (не redirect!)
- [ ] `POST /oauth/authorize/complete` с валидным Supabase JWT → authorization_code выдан, redirect к ChatGPT
- [ ] `POST /oauth/token` с валидным code → `access_token` в ответе
- [ ] `POST /oauth/token` с использованным code → 400 `invalid_grant`
- [ ] `POST /oauth/token` с истёкшим code → 400 `invalid_grant`
- [ ] `POST /oauth/token` с неверным `client_secret` → 401 `invalid_client`
- [ ] Выданный `access_token` валидируется в `validate_oauth_access_token()`
- [ ] `access_token` не содержит `eid_verified`, `verified_person_hash`, `personal_code`
