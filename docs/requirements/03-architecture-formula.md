# 03. Архитектурная формула

> **Статус:** НЕ реализовано. Requirements document.
> **Сервис:** `doge-identity-service`

---

## 4 слоя идентичности

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1 — DOGEstonia Account Layer                         │
│  Supabase Auth                                              │
│  · login / signup / session / JWT                           │
│  · email+password, magic link                               │
│  · base user identity (auth.users)                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ JWT Bearer
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2 — Human Verification Layer                         │
│  Authentigate (SaaS, SK ID Solutions)                       │
│  · Smart-ID / Mobile-ID / ID-card                           │
│  · OIDC Authorization Code Flow + PKCE S256                 │
│  · returns: personal_code + personal_code_country           │
│  · one-time only (not per-story)                            │
└──────────────────────────┬──────────────────────────────────┘
                           │ OIDC callback (code + state)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 3 — DOGEstonia Authorization Layer                   │
│  doge-identity-service (FastAPI, этот сервис)               │
│  · OAuth 2.0 Authorization Server для Custom GPT            │
│  · валидирует Supabase JWT                                  │
│  · проверяет eid_verified status                            │
│  · применяет business permissions                           │
│  · /me, /auth/eid/start, /auth/authentigate/callback          │
│  · /oauth/authorize, /oauth/token                           │
└──────────────────────────┬──────────────────────────────────┘
                           │ Bearer token (выдан identity-service)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 4 — Future Wallet Signature Layer (Post-MVP)         │
│  · story signing via wallet address                         │
│  · authorship proof on-chain                                │
│  · portable civic identity                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Компонентная таблица

| Компонент | Роль | MVP |
|-----------|------|-----|
| **Supabase Auth** | account/session layer, JWT issuer | ✅ |
| **Supabase Postgres** | хранение profiles, eid sessions, audit | ✅ |
| **Authentigate** | one-time human uniqueness verification (SaaS) | ✅ (mock в dev) |
| **doge-identity-service** | DOGEstonia authorization layer + OAuth 2.0 server | ✅ строить |
| **doge-complaints-gateway** | stories/issues pipeline, валидирует Bearer от identity-service | ✅ уже есть |
| **spa-app (React/Vite, браузер)** | dashboard, OAuth authorize UI, eID verification screen | ✅ расширять |
| **Custom GPT** | story submission interface, OAuth client | ✅ интегрировать |
| **Wallet** | cryptographic authorship (post-MVP) | ❌ |

---

## Схема взаимодействий (MVP user flows)

### Flow A: Web login + eID verification

```
User (браузер / spa-app)
  → POST supabase.auth.signInWithPassword()
  ← Supabase JWT (access_token)

User нажимает "Verify with eID"
  → POST identity-service /auth/eid/start
    (Authorization: Bearer <supabase_jwt>)
  ← { redirect_url: "https://id.authentigate.eu/authorize?..." }

User редиректит → Authentigate → eID verification
  ← Authentigate callback → identity-service /auth/authentigate/callback?code=...&state=...

identity-service:
  - exchanges code → tokens
  - generates verified_person_hash
  - applies conflict detection
  - sets profiles.eid_verified = true
  → redirects user to https://dogestonia.ee/verify?success=true
```

### Flow B: Custom GPT story submission (gateway-direct)

```
ChatGPT (Custom GPT Action)
  → redirect user to identity-service /oauth/authorize

User логинится в spa-app (email/password)
  ← identity-service выдаёт auth_code → ChatGPT
  → POST identity-service /oauth/token { code, client_id, client_secret }
  ← access_token (scope: stories:create, profile:read)

ChatGPT
  → POST doge-complaints-gateway /intake/stories
    (Authorization: Bearer <access_token>)

gateway:
  → introspection /me у identity-service: { active, sub, eid_verified }

  if eid_verified = false:
    ← 403 { error: "verification_required", verification_url: "https://dogestonia.ee/verify" }
    ChatGPT сообщает пользователю → пользователь делает eID в spa-app → возвращается → повторяет

  if eid_verified = true:
    ← story_id
    ← 200 { story_id: "...", status: "accepted" }
```

> Identity **не** принимает и **не** форвардит story HTTP-запросы. См. [09-gateway-expectations](../runtime-docs/09-gateway-expectations.md).

---

## Принцип session-binding в eID flow

```
Единственный источник истины для привязки eID к пользователю:
  eid_verification_sessions.supabase_user_id (запись создана в /auth/eid/start)

Callback НИКОГДА не использует текущую браузерную сессию.
Причина: сессия может смениться пока пользователь проходил eID.
```

---

## Deployment topology

```
Internet
  ├── spa-app (React SPA, статический хостинг)
  │     → вызывает identity-service и Supabase
  │
  ├── identity.dogestonia.ee  →  doge-identity-service (FastAPI)
  │     → Supabase (auth + postgres)
  │     → Authentigate (OIDC)
  │
  └── api.dogestonia.ee  →  doge-complaints-gateway (FastAPI)
        → Supabase (postgres)
        → (валидирует Bearer от identity-service через /validate или JWT check)
```
