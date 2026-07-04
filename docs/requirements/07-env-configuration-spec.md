# 07. Спецификация переменных окружения

> ⚠️ **Частично устарело (2026-06-24):** не отражает eID-Easy, phone-верификацию, NODE_ID, DB_BACKEND, SERVICE_API_TOKEN — фактический SSOT конфига = `src/core/config/schema.py`.

> **Статус:** НЕ реализовано. Spec для `src/core/config/schema.py` и `example.env`.
> **Связь:** Файл 06 (scaffold) → реализует `load_config_from_env`. Файл 12 (Authentigate) → использует AUTHENTIGATE_*. Файл 14 (OAuth server) → использует OAUTH_* и GPT_OAUTH_*.

---

## Полный список переменных

### Deployment

| Переменная | Required | Default | Описание |
|-----------|---------|---------|---------|
| `APP_PROFILE` | No | `demo` | Профиль деплоя: `demo` \| `pilot`. В `pilot` — строгая валидация секретов. |
| `PORT` | No | `8100` | Порт uvicorn |
| `API_BASE_URL` | Yes | — | Базовый URL сервиса. Production: `https://identity.dogestonia.ee` |
| `LOG_LEVEL` | No | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `LOG_FORMAT` | No | `text` | `text` \| `json`. В production рекомендуется `json`. |
| `REQUEST_TIMEOUT_S` | No | `15` | Таймаут исходящих HTTP-запросов к Supabase PostgREST (секунды). Не применяется к OIDC/eID Easy — см. `OIDC_REQUEST_TIMEOUT_S`. |
| `OIDC_REQUEST_TIMEOUT_S` | No | `10` | Таймаут HTTP-запросов к OIDC-провайдерам: Authentigate discovery/JWKS, eID Easy `/token` (секунды). |

### Supabase

| Переменная | Required | Default | Описание |
|-----------|---------|---------|---------|
| `SUPABASE_URL` | Yes (pilot) | — | Project URL. Dashboard → Settings → API → Project URL. **Обязателен для JWKS validation** (`{URL}/auth/v1/.well-known/jwks.json`). |
| `SUPABASE_SERVICE_ROLE` | Yes (pilot) | — | Service role key. Только server-side. Никогда в браузер. |
| `DATABASE_URL` | Yes (если psycopg) | — | `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres` |

> **Примечание:** `SUPABASE_ANON_KEY` (anon key для клиентского SDK) намеренно опущен — identity-service server-side всегда работает через `SUPABASE_SERVICE_ROLE`. Anon key используется только во фронтенд-приложениях, которые конфигурируются отдельно.

**Примечание про JWT validation (SEC-06):** Supabase Cloud подписывает access tokens асимметрично (ES256). Identity-service проверяет подпись **только через JWKS** по `SUPABASE_URL`. `SUPABASE_JWT_SECRET` удалён.

### Authentigate OIDC

| Переменная | Required | Default | Описание |
|-----------|---------|---------|---------|
| `AUTHENTIGATE_ISSUER` | Yes | — | Issuer URL. Demo: `https://oidc.demo.sk.ee`. Production: `https://id.authentigate.eu`. Для dev mock: `http://localhost:8080` |
| `AUTHENTIGATE_CLIENT_ID` | Yes | — | Client ID от SK ID Solutions |
| `AUTHENTIGATE_CLIENT_SECRET` | Yes | — | Client secret от SK ID Solutions |
| `AUTHENTIGATE_REDIRECT_URI` | Yes | — | Callback URL. Local: `http://localhost:8100/auth/authentigate/callback`. Production: `https://identity.dogestonia.ee/auth/authentigate/callback` |
| `AUTHENTIGATE_SCOPES` | No | `openid personal_code personal_code_country` | OIDC scopes. НЕ добавлять `given_name`, `family_name`, `birthdate` (privacy) |

### Identity Secrets

| Переменная | Required | Default | Описание |
|-----------|---------|---------|---------|
| `DOGESTONIA_EID_SECRET` | Yes (pilot) | — | HMAC-SHA256 ключ для генерации `verified_person_hash` / `subject_hash`. Минимум 32 байта, крипто-случайный. Никогда не логировать. См. `ADR-IDS-008` (пересмотр 2026-05-27). Поле AppConfig: `eid_secret`. |
| `CODE_VERIFIER_ENCRYPTION_KEY` | Yes (pilot) | — | AES-256-GCM ключ для шифрования `code_verifier_encrypted` в DB. Base64-encoded 32 байта. |

### OAuth 2.0 Server (для Custom GPT)

| Переменная | Required | Default | Описание |
|-----------|---------|---------|---------|
| `OAUTH_ACCESS_TOKEN_SECRET` | Yes (pilot) | — | HMAC-SHA256 ключ для подписи access tokens выданных identity-service. Минимум 32 байта. |
| `OAUTH_ACCESS_TOKEN_TTL_S` | No | `3600` | TTL access token в секундах. Default: 1 час. |
| `OAUTH_AUTHORIZATION_CODE_TTL_S` | No | `300` | TTL authorization code в секундах. Default: 5 минут. |
| `GPT_OAUTH_CLIENT_ID` | Yes (pilot) | `openai-custom-gpt` | OAuth client_id для ChatGPT |
| `GPT_OAUTH_CLIENT_SECRET` | Yes (pilot) | — | OAuth client_secret для ChatGPT |
| `GPT_OAUTH_REDIRECT_URI` | Yes | — | ChatGPT callback URI. Production: `https://oauth.pstmn.io/v1/callback` (OpenAI standard). |

### Security & CORS

| Переменная | Required | Default | Описание |
|-----------|---------|---------|---------|
| `CORS_ALLOWED_ORIGINS` | No | `*` (demo) | Comma-separated список разрешённых origins. Production: `https://dogestonia.ee,https://chat.openai.com` |
| `ALLOWED_RETURN_URLS` | No | захардкожен | Allowlist return_url для /auth/eid/start. В demo — hardcoded list. В pilot — из env override. |

---

## `example.env`

```env
# =============================================================================
# doge-identity-service — example environment
# Copy to `.env` locally. Do not commit real secrets.
# =============================================================================

# --- Deployment ---
APP_PROFILE=demo
PORT=8100
API_BASE_URL=http://localhost:8100
LOG_LEVEL=INFO
LOG_FORMAT=text
REQUEST_TIMEOUT_S=15
OIDC_REQUEST_TIMEOUT_S=10

# --- Supabase ---
# Project URL: Supabase Dashboard → Settings → API → Project URL
SUPABASE_URL=

# Service role key (server only, never in browser)
SUPABASE_SERVICE_ROLE=

# Direct Postgres connection (for psycopg)
# postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
DATABASE_URL=

# --- Authentigate OIDC ---
# Demo environment (use mock-oauth2-server for local dev):
#   docker run -p 8080:8080 ghcr.io/navikt/mock-oauth2-server:latest
# Demo: AUTHENTIGATE_ISSUER=https://oidc.demo.sk.ee
# Production: AUTHENTIGATE_ISSUER=https://id.authentigate.eu
AUTHENTIGATE_ISSUER=http://localhost:8080

# Get from SK ID Solutions: sales@skidsolutions.eu
AUTHENTIGATE_CLIENT_ID=
AUTHENTIGATE_CLIENT_SECRET=
AUTHENTIGATE_REDIRECT_URI=http://localhost:8100/auth/authentigate/callback
AUTHENTIGATE_SCOPES=openid personal_code personal_code_country

# --- Identity Secrets ---
# HMAC secret for verified_person_hash / subject_hash (see ADR-IDS-008, пересмотр 2026-05-27):
# python3 -c "import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
DOGESTONIA_EID_SECRET=

# AES-256-GCM key for code_verifier_encrypted (32 bytes, base64)
CODE_VERIFIER_ENCRYPTION_KEY=

# --- OAuth 2.0 Server ---
OAUTH_ACCESS_TOKEN_SECRET=
OAUTH_ACCESS_TOKEN_TTL_S=3600
OAUTH_AUTHORIZATION_CODE_TTL_S=300

# ChatGPT OAuth client
GPT_OAUTH_CLIENT_ID=openai-custom-gpt
GPT_OAUTH_CLIENT_SECRET=
GPT_OAUTH_REDIRECT_URI=https://oauth.pstmn.io/v1/callback

# --- CORS ---
# Production: CORS_ALLOWED_ORIGINS=https://dogestonia.ee,https://chat.openai.com
CORS_ALLOWED_ORIGINS=*
```

---

## Генерация секретов (команды)

```bash
# DOGESTONIA_EID_SECRET
python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"

# CODE_VERIFIER_ENCRYPTION_KEY (AES-256 = 32 bytes)
python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"

# OAUTH_ACCESS_TOKEN_SECRET
python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"

# GPT_OAUTH_CLIENT_SECRET
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Валидация конфигурации при старте

Паттерн из complaints-gateway: при `APP_PROFILE=pilot` ряд переменных становятся обязательными.

| Переменная | demo | pilot |
|-----------|------|-------|
| `SUPABASE_URL` | optional | required |
| `SUPABASE_SERVICE_ROLE` | optional | required |
| `DATABASE_URL` | optional | required |
| `DOGESTONIA_EID_SECRET` | optional | required |
| `CODE_VERIFIER_ENCRYPTION_KEY` | optional | required |
| `OAUTH_ACCESS_TOKEN_SECRET` | optional | required |
| `GPT_OAUTH_CLIENT_SECRET` | optional | required |

В demo режиме сервис может стартовать без Supabase и Authentigate (для разработки scaffold).
