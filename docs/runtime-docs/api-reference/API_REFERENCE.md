# DOGE Identity Service API Reference

## 1. Overview

This reference describes the runtime API surface for `doge-identity-service` with explicit state separation:

- **As-is**: behavior implemented in `FastAPI` transport routes ([`src/core/api/asgi_app.py`](../../../src/core/api/asgi_app.py)) backed by handler functions ([`src/core/api/handlers.py`](../../../src/core/api/handlers.py), [`src/core/oauth/handlers.py`](../../../src/core/oauth/handlers.py)).
- **Deferred**: eID provider routes exist but run against a **mock** provider — real eID (Authentigate) is post-MVP.

The canonical machine-readable contract is:

- [`docs/runtime-docs/api-reference/openapi.yaml`](./openapi.yaml)

Narrative companion (not per-endpoint): [`01-api.md`](../01-api.md); security model: [`04-security.md`](../04-security.md); gateway coupling: [`09-gateway-expectations.md`](../09-gateway-expectations.md).

## 2. Runtime Boundary

Current runtime is **ASGI/FastAPI-driven** under [`asgi_app.py`](../../../src/core/api/asgi_app.py) (`create_app`). Routes registered (verified 2026-07-10):

| Route | Line | Domain |
|-------|------|--------|
| `GET /health` | [asgi_app.py:287](../../../src/core/api/asgi_app.py) | Ops |
| `GET /ready` | [:294](../../../src/core/api/asgi_app.py) | Ops |
| `GET /me` | [:301](../../../src/core/api/asgi_app.py) | Identity/session |
| `POST /auth/eid/start` | [:313](../../../src/core/api/asgi_app.py) | eID (deferred/mock) |
| `GET /auth/{provider}/callback` | [:333](../../../src/core/api/asgi_app.py) | eID (deferred/mock) |
| `POST /auth/phone/request` | [:359](../../../src/core/api/asgi_app.py) | Phone verification |
| `POST /auth/phone/confirm` | [:377](../../../src/core/api/asgi_app.py) | Phone verification |
| `POST /webhooks/telnyx/messaging` | [:395](../../../src/core/api/asgi_app.py) | SMS delivery webhook |
| `GET /oauth/authorize` | [:410](../../../src/core/api/asgi_app.py) | OAuth server |
| `POST /oauth/authorize/complete` | [:422](../../../src/core/api/asgi_app.py) | OAuth server |
| `POST /oauth/token` | [:439](../../../src/core/api/asgi_app.py) | OAuth server |
| `POST /oauth/introspect` | [:447](../../../src/core/api/asgi_app.py) | OAuth server |

**CORS**: `allow_origins` from `CORS_ALLOWED_ORIGINS`; `allow_methods=[GET,POST,OPTIONS]`; `allow_headers=[authorization, content-type, x-trace-id]` ([asgi_app.py:204-207](../../../src/core/api/asgi_app.py)).

**Servers** (illustrative): local `http://127.0.0.1:8100`; deployed `https://<identity-app>.up.railway.app` (substitute your Railway domain).

## 3. Authentication Model

| Scheme | Where | Implementation |
|--------|-------|----------------|
| **Supabase JWT** (`Authorization: Bearer <supabase_access_token>`) | `/me`, `/auth/phone/*` | JWKS/ES256 validation via `SupabaseJwtValidatorImpl` ([`supabase_validator.py`](../../../src/core/auth/supabase_validator.py), SEC-06 JWKS-only); `get_current_user` ([`security.py`](../../../src/core/api/security.py)) |
| **OAuth access token** (`Bearer`) | issued by `/oauth/token`; accepted alongside Supabase JWT by `CompositeBearerTokenAuth` | self-signed HS256 on `OAUTH_ACCESS_TOKEN_SECRET` ([`access_token_jwt.py`](../../../src/core/oauth/access_token_jwt.py)) |
| **Service token** (`X-Service-Token` or `Bearer <SERVICE_API_TOKEN>`) | `/oauth/introspect` | `require_service_token` ([`security.py`](../../../src/core/api/security.py)) |
| **Telnyx Ed25519 signature** | `/webhooks/telnyx/messaging` | `verify_telnyx_webhook_signature` ([`telnyx/webhook_signature.py`](../../../src/core/phone/telnyx/webhook_signature.py)); requires `TELNYX_WEBHOOK_PUBLIC_KEY` |
| **None (public)** | `/health`, `/ready` | — |

Missing/invalid Bearer on protected routes → **401**. In **pilot** profile, config fails fast when critical secrets are unset ([`schema.py`](../../../src/core/config/schema.py)).

## 4. Envelope and Error Contract

Implemented in [`envelope.py`](../../../src/core/api/envelope.py):

- **Success**: `{ "data": { … } }`
- **Error**: `{ "error": { "code", "message", "trace_id"? } }`
- **Rate limit**: `{ "error": { "code": "rate_limit_exceeded", "message", "retry_after", "trace_id"? } }`

> ⚠️ **Two error shapes coexist:** most routes use the envelope above. The **OAuth verify-gate** (`/oauth/authorize/complete`) returns a **flat** body `{ "error": "verification_required", "reason", "verify_url" }` with HTTP **403** ([`verification_required.py`](../../../src/core/oauth/verification_required.py)) — this is a deliberate contract for GPT Actions (OAUTH-04), not the standard envelope.

---

## 5. Ops

### `GET /health`
- **As-is**: [asgi_app.py:287](../../../src/core/api/asgi_app.py) → `handle_health` ([handlers.py:41](../../../src/core/api/handlers.py))
- **Auth**: none · **Purpose**: liveness (Railway healthcheck path)
- **Response** `200`: `{ "data": { "status": "ok", "trace_id": "…" } }`

### `GET /ready`
- **As-is**: [asgi_app.py:294](../../../src/core/api/asgi_app.py) → `handle_readiness` ([handlers.py:47-53](../../../src/core/api/handlers.py))
- **Auth**: none · **Purpose**: readiness (DB/deps probe)
- **Response** `200` ready / `503` degraded: `{ "data": { "status": "ready" | "degraded", … } }`

---

## 6. Identity / session

### `GET /me`
- **As-is**: [asgi_app.py:301](../../../src/core/api/asgi_app.py) → `handle_me` ([handlers.py:73-88](../../../src/core/api/handlers.py)); payload [`me_response.py`](../../../src/core/api/me_response.py)
- **Auth**: Supabase JWT (Bearer) · **Purpose**: current user profile + verification flags from JWT + profile store
- **No auto-provision**: missing profile → `200` with `eid_verified=false` and profile fields `null` (no DB write); `created_at=null`, `account_status="active"`
- **Account fields (AUTHCORE-02 / CAB-02):** `created_at` — ISO-8601 from `profiles.created_at` or `null` (**семантика D-CAB-2:** момент создания профиля / первой верификации, **не** дата регистрации в Supabase Auth; UI-label «Account Created» может быть неточным); `account_status` — enum in contract, **MVP always `"active"`** (no migration)
- **Email fields (ONB-01 / D-CAB-3):** `email` — из JWT claim (`null`, если claim отсутствует); для **OAuth/GPT** access-токенов Identity структурно отдаёт `email: null` ([`security.py`](../../../src/core/api/security.py) OAuth path). `email_verified` — **всегда `true`** для валидного токена (политика «токен ⇒ подтверждён»; корректно только при включённом Supabase **Confirm email** — [`supabase-project-setup.md` §2a](../../runbook/supabase-project-setup.md)). ⚠️ Не трактовать `email_verified: true` как «есть подтверждённый адрес» без проверки `email != null` (OAuth/GPT: `email:null` + `email_verified:true` — принятый дизайн).
- **Response** `200`:

```json
{
  "data": {
    "supabase_user_id": "…", "role": "authenticated",
    "email": "user@example.com", "email_verified": true,
    "eid_verified": false, "display_name": null, "avatar_url": null,
    "eid_provider": null, "eid_method": null, "eid_country": null, "eid_verified_at": null,
    "phone_verified": false, "phone_provider": null, "phone_dial_prefix": null, "phone_verified_at": null,
    "created_at": null,
    "account_status": "active"
  }
}
```
- **Errors**: `401` missing/invalid token.

---

## 7. Phone verification

Core owns the OTP (generation, `code_hash`, TTL, attempts, cooldown — [`otp_engine.py`](../../../src/core/phone/otp_engine.py)); the SMS provider only delivers text. Rules: 6 digits · TTL 5 min · 5 attempts · resend cooldown 60 s.

### `POST /auth/phone/request`
- **As-is**: [asgi_app.py:359](../../../src/core/api/asgi_app.py) → `handle_phone_request` ([handlers.py:494-534](../../../src/core/api/handlers.py))
- **Auth**: Supabase JWT (Bearer) · rate-limited (SEC-01/01b) · **Purpose**: create OTP session + send SMS via active provider (`SMS_PROVIDER`)
- **Request**: `{ "phone": "+37255555555" }` (normalized to E.164; prefix allowlist `PHONE_ALLOWED_DIAL_PREFIXES`)
- **Response** `200`: `{ "data": { "sent": true, "expires_at": "…Z" } }` — **OTP code is never in the response/logs**
- **Errors**: `400` (`INVALID_PHONE`, `COUNTRY_NOT_ALLOWED`), `429` rate limit (`retry_after`), `503` provider unavailable.

### `POST /auth/phone/confirm`
- **As-is**: [asgi_app.py:377](../../../src/core/api/asgi_app.py) → `handle_phone_confirm` ([handlers.py:537-635](../../../src/core/api/handlers.py))
- **Auth**: Supabase JWT (Bearer) · **Purpose**: verify submitted code, set `phone_verified`
- **Request**: `{ "phone": "+37255555555", "code": "123456" }`
- **Response** `200`: `{ "data": { "status": "verified" } }` ([handlers.py:635](../../../src/core/api/handlers.py))
- **Errors**: `400` (`CODE_MISMATCH`, `CODE_EXPIRED`, `TOO_MANY_ATTEMPTS`, `invalid_or_consumed_state`), `409` `profile_conflict` (number already linked to another account, dedup P1).

---

## 8. OAuth server (Custom GPT Actions)

RFC-style OAuth 2.0 with PKCE S256; issues self-signed access tokens. Canon for GPT user-scoped auth (D-6). Durable handshake/codes when `DB_BACKEND=supabase` (OAUTH-03).

### `GET /oauth/authorize`
- **As-is**: [asgi_app.py:410](../../../src/core/api/asgi_app.py) → `handle_oauth_authorize` ([oauth/handlers.py](../../../src/core/oauth/handlers.py))
- **Purpose**: start authorization; redirects user to spa login (`build_spa_oauth_login_url`, [`spa_login.py`](../../../src/core/oauth/spa_login.py))

### `POST /oauth/authorize/complete`
- **As-is**: [asgi_app.py:422](../../../src/core/api/asgi_app.py) → `handle_oauth_authorize_complete` ([oauth/handlers.py](../../../src/core/oauth/handlers.py))
- **Purpose**: complete authorization after login; issues authorization code
- **Verify-gate (OAUTH-04)**: when `requested_action=stories:submit` and `phone_verified=false` → **403** flat body `{ "error": "verification_required", "reason": "…", "verify_url": "…" }` ([verification_required.py](../../../src/core/oauth/verification_required.py))

### `POST /oauth/token`
- **As-is**: [asgi_app.py:439](../../../src/core/api/asgi_app.py) → `handle_oauth_token` ([oauth/handlers.py:179-197](../../../src/core/oauth/handlers.py))
- **Purpose**: exchange authorization code (PKCE S256, `client_secret` verified) for access token
- **Response** `200`: `{ "access_token": "…", "token_type": "Bearer", "expires_in": <OAUTH_ACCESS_TOKEN_TTL_S> }`

### `POST /oauth/introspect`
- **As-is**: [asgi_app.py:447](../../../src/core/api/asgi_app.py) → `handle_oauth_introspect` ([oauth/introspection.py:9-31](../../../src/core/oauth/introspection.py))
- **Auth**: service token · **Purpose**: RFC 7662-style introspection (D-6 canon for GPT Actions / lazy phone-gate)
- **Response** always `200`: active → `{ "active": true, "sub": "…", "phone_verified": <bool> }`; inactive → `{ "active": false }`

---

## 9. eID (deferred — mock provider)

eID (Authentigate) is **post-MVP**; routes run against a **mock** provider (`EID_PROVIDER=mock`). Documented for completeness; not part of MVP phone-verification path.

### `POST /auth/eid/start`
- **As-is**: [asgi_app.py:313](../../../src/core/api/asgi_app.py) → eID start handler · **Auth**: Supabase JWT · **Status**: deferred/mock

### `GET /auth/{provider}/callback`
- **As-is**: [asgi_app.py:333](../../../src/core/api/asgi_app.py) → `handle_eid_callback` ([handlers.py](../../../src/core/api/handlers.py)) · **Status**: deferred/mock; redirects to `return_url` with outcome

---

## 10. SMS delivery webhook (Telnyx, PV-07)

### `POST /webhooks/telnyx/messaging`
- **As-is**: [asgi_app.py:395](../../../src/core/api/asgi_app.py) → `handle_telnyx_messaging_webhook` ([handlers.py:653](../../../src/core/api/handlers.py))
- **Auth**: **none by header** — verified via **Ed25519 signature** (Telnyx public key). **Public route** (Telnyx calls it externally).
- **Purpose**: ingest delivery-status events (`message.sent` / `message.delivered` / `message.finalized`) → update session delivery status ([`telnyx/delivery_ingest.py`](../../../src/core/phone/telnyx/delivery_ingest.py))
- **Config gate**: if `TELNYX_WEBHOOK_PUBLIC_KEY` is **unset** → **503 `CONFIG_ERROR`** ([handlers.py:660-667](../../../src/core/api/handlers.py)); invalid signature → rejected (audit-logged `invalid_signature`).
- **URI to configure in Telnyx Messaging Profile → Inbound → Webhook URL**: `https://<identity-app>.up.railway.app/webhooks/telnyx/messaging`

---

## 11. Change log
- 2026-07-10: initial reference created (12 routes, verified vs `asgi_app.py`); mirrors gateway [`api-reference`](../../../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md) structure.
