# 11. eID Verification Flow

> ⏸️ **eID отложен (2026-06-24):** реальные eID-провайдеры (Authentigate/eID-Easy) — descriptor-заглушки (STORY-IDS-EID-02); активный гейт верификации — ТЕЛЕФОН (см. новый `19-phone-verification-flow.md`). Код eID ушёл вперёд этого спека (descriptor/registry-рефактор; redirect-маркеры `?eid_status=verified`/`?eid_status=error&eid_error=` вместо `?context=`/`?error=`). См. full-audit.

> **Статус:** НЕ реализовано. Spec для `/auth/eid/start`, `/auth/eid/callback`, `verification_session_store.py`.
> **Предусловие:** Файл 08 (миграции) + файл 09 (JWT validation) + файл 12 (Authentigate client) реализованы.
> **Связь:** Файл 12 (OIDC client) — внешний вызов к Authentigate. Файл 13 (hash + conflict) — финальный шаг callback.

---

## Общая схема

```
User (в браузере / spa-app)
  │
  ▼
POST /auth/eid/start
  Authorization: Bearer <supabase_jwt>
  Body: { return_context, return_url, requested_action }
  │
  │  Backend: создаёт verification session
  │           генерирует state, nonce, code_verifier
  │           строит Authentigate authorize URL
  │
  ▼
Response: { redirect_url, expires_at }
  │
  │  spa-app: window.location.href = redirect_url
  │
  ▼
Authentigate (Smart-ID / Mobile-ID / ID-card)
  │
  │  После успешной верификации:
  │  GET /auth/eid/callback?code=...&state=...
  │
  ▼
Backend callback:
  - validates state
  - resolves session → gets supabase_user_id
  - exchanges code for tokens (Authentigate)
  - validates ID token
  - generates verified_person_hash
  - applies conflict detection (transaction)
  - marks profile eid_verified=true
  - marks session consumed
  - redirects user to return_url
```

---

## POST /auth/eid/start

**Auth required:** yes (Supabase JWT).

### Request body

```json
{
  "return_context": "dashboard_verification",
  "return_url": "https://dogestonia.ee/verify",
  "requested_action": "eid:verify"
}
```

| Поле | Type | Required | Описание |
|------|------|---------|---------|
| `return_context` | string | No | `dashboard_verification` \| `story_submission` \| `custom_gpt_submit` |
| `return_url` | string | No | URL для редиректа после верификации. MUST быть в allowlist. |
| `requested_action` | string | No | `eid:verify` \| `stories:submit` |

### Алгоритм

```
1. Validate Supabase JWT → supabase_user_id
2. Check: profile.eid_verified == true?
   → Если да: return 200 { "status": "already_verified" }
3. Validate return_url against allowlist (P-006)
   → Если невалиден: return 400 { "error": "invalid_return_url" }
4. Generate OIDC parameters:
   - state = secrets.token_urlsafe(32)         — CSRF token
   - nonce = secrets.token_urlsafe(16)         — OIDC nonce
   - code_verifier = secrets.token_urlsafe(48) — PKCE verifier (min 43 chars)
   - code_challenge = base64url(sha256(code_verifier))  — PKCE S256
5. Encrypt code_verifier:
   - code_verifier_encrypted = aes_gcm_encrypt(code_verifier, CODE_VERIFIER_ENCRYPTION_KEY)
   - code_verifier_hash = sha256(code_verifier)  — для audit/debug, не для token exchange
6. INSERT eid_verification_sessions:
   {
     supabase_user_id: from JWT,
     state, nonce, code_verifier_encrypted, code_verifier_hash,
     return_context, return_url (validated), requested_action,
     status: 'started',
     expires_at: now() + 10 minutes
   }
7. Build Authentigate authorize URL:
   {AUTHENTIGATE_ISSUER}/authorize
     ?response_type=code
     &client_id={AUTHENTIGATE_CLIENT_ID}
     &redirect_uri={AUTHENTIGATE_REDIRECT_URI}
     &scope={AUTHENTIGATE_SCOPES}
     &state={state}
     &nonce={nonce}
     &code_challenge={code_challenge}
     &code_challenge_method=S256
8. Log audit event: eid_verification_started
9. Return: { redirect_url, expires_at }
```

### Response (успех)

```json
HTTP 200
{
  "redirect_url": "https://id.authentigate.eu/authorize?...",
  "expires_at": "2026-05-25T14:40:00Z"
}
```

### Errors

| Error code | HTTP | Условие |
|-----------|------|---------|
| `authentication_required` | 401 | Нет/невалидный JWT |
| `already_verified` | 200 | `eid_verified` уже `true` |
| `invalid_return_url` | 400 | return_url не в allowlist |

### Rate limit

`5 requests / 10 minutes / user` (BE-SEC-003).
При превышении: `429 { "error": "rate_limit_exceeded" }`.

---

## Return URL Allowlist

```python
ALLOWED_RETURN_URLS = [
    "https://dogestonia.ee/verify",
    "https://dogestonia.ee/dashboard/verify",
]

ALLOWED_QUERY_PARAM_KEYS = {"context", "error", "draft_id"}
```

Валидация: сравнивать scheme + host + path без query params. Query params обрабатываются отдельно.

---

## GET /auth/eid/callback

**Auth required:** нет (вызывается Authentigate, не браузерной сессией пользователя).

### Query params

```
code=<authorization_code>
state=<csrf_token>
error=<error_code>        (опционально, при отказе пользователя)
error_description=<text>  (опционально)
```

### Алгоритм (10 шагов)

```
1. Check if error param present:
   → Если да: find session by state, mark failed, redirect to error URL

2. Validate state:
   a. SELECT session FROM eid_verification_sessions WHERE state = $state
   b. Если не найден → 400 { error: "invalid_or_consumed_state" }

3. Validate session status:
   - Если status != 'started' → reject: invalid_or_consumed_state
   
4. Validate session expiration:
   - Если expires_at < now():
     UPDATE status = 'expired'
     → redirect to error URL: ?error=eid_session_expired

5. Extract supabase_user_id from session:
   - НЕ из браузерной сессии! Только из session.supabase_user_id.

6. Decrypt code_verifier:
   code_verifier = aes_gcm_decrypt(session.code_verifier_encrypted, KEY)

7. Exchange code for tokens (Authentigate):
   POST {AUTHENTIGATE_ISSUER}/token
     grant_type=authorization_code
     code=<code>
     redirect_uri=<AUTHENTIGATE_REDIRECT_URI>
     client_id=<CLIENT_ID>
     client_secret=<CLIENT_SECRET>
     code_verifier=<code_verifier>   ← из шага 6, не из hash!
   
   Если ошибка:
     UPDATE session.status = 'failed'
     Log: eid_verification_failed
     → redirect to error URL

8. Validate ID token (файл 12 — authentigate_client.py):
   - Verify signature (JWKS от Authentigate)
   - Verify iss, aud, exp, nonce
   - Extract: personal_code, personal_code_country

9. Generate verified_person_hash + Conflict detection (файл 13):
   - hash = HMAC_SHA256(PEPPER, f"{country}:{personal_code}")
   - BEGIN TRANSACTION
   - SELECT profile WHERE verified_person_hash = hash
   - Apply conflict logic (Case A/B/C)
   - COMMIT или ROLLBACK

10. On success:
    - UPDATE session.status = 'consumed'
    - Log: eid_verification_success
    - Redirect to: session.return_url + "?context=<return_context>"
    
    Allowed query params on redirect: only those in ALLOWED_QUERY_PARAM_KEYS
```

### Redirect URLs (успех/ошибка)

```
Успех:  https://dogestonia.ee/verify?context=dashboard_verification
Ошибка: https://dogestonia.ee/verify?error=identity_already_linked
Ошибка: https://dogestonia.ee/verify?error=eid_session_expired
Ошибка: https://dogestonia.ee/verify?error=eid_verification_failed
```

Если `return_url` не задан или не в allowlist — редиректить на `https://dogestonia.ee/verify` (дефолт).

---

## Session State Machine (полная)

```
                  ┌─────────┐
                  │ started │
                  └────┬────┘
        ┌───────────┬──┴──────────┐
        ▼           ▼             ▼
  ┌──────────┐  ┌────────┐  ┌─────────┐
  │ consumed │  │ failed │  │ expired │
  └──────────┘  └────────┘  └─────────┘

Переходы:
started → consumed  : callback успешно обработан
started → failed    : ошибка token exchange или ID token validation
started → expired   : expires_at < now() при попытке использования
                      ИЛИ background cleanup job
```

**Правила одноразовости:**
- `state` уникален (UNIQUE constraint в DB).
- Повторное использование state: SESSION NOT FOUND (или статус != 'started') → `invalid_or_consumed_state`.

---

## Acceptance Criteria

- [ ] `POST /auth/eid/start` без JWT → 401
- [ ] `POST /auth/eid/start` для уже верифицированного → 200 `already_verified`
- [ ] `POST /auth/eid/start` с return_url не в allowlist → 400 `invalid_return_url`
- [ ] `POST /auth/eid/start` успешно → создаёт запись в `eid_verification_sessions`, возвращает redirect_url
- [ ] `GET /auth/eid/callback` с невалидным state → 400/redirect с `invalid_or_consumed_state`
- [ ] `GET /auth/eid/callback` с истёкшей сессией → redirect с `eid_session_expired`
- [ ] `GET /auth/eid/callback` успешный flow → `profiles.eid_verified=true`, сессия `consumed`
- [ ] `GET /auth/eid/callback` НЕ использует текущую браузерную сессию (session binding rule)
- [ ] После callback: `code_verifier_encrypted` в сессии остаётся, но статус `consumed` — повторный вызов rejected
