# Handbook переменных окружения — doge-identity-service

> **Назначение:** операторский мануал — что означает каждая группа env, как сгенерировать секреты, куда их класть, чем local отличается от Railway/pilot.
> **SSOT в коде:** [`schema.py`](../../src/core/config/schema.py) (`load_config_from_env`, `pilot_required`).
> **Шаблон:** [`.env.example`](../../.env.example).

---

## 0. Handbook за 2 минуты

### Локально без секретов (demo)

```bash
cd doge-identity-service
cp .env.example .env
make serve    # http://127.0.0.1:8100
```

Профиль `demo` + `DB_BACKEND=in_memory` — сервис стартует без Supabase и без секретов ([`providers.py`](../../src/core/config/providers.py)).

### Локально с Supabase

См. пошагово: [`supabase-project-setup.md`](./supabase-project-setup.md).

### Railway pilot (чеклист)

В **Railway Variables** сервиса identity задайте:

| Переменная | Обязательна |
|------------|-------------|
| `APP_PROFILE` | `pilot` |
| `DB_BACKEND` | `supabase` |
| `SMS_PROVIDER` | `mock` (не `file`) |
| `API_BASE_URL` | публичный URL identity |
| `SUPABASE_URL` | из Supabase Dashboard |
| `SUPABASE_SERVICE_ROLE` | из Supabase Dashboard |
| `DATABASE_URL` | Postgres connection string |
| `DOGESTONIA_EID_SECRET` | сгенерировать (§3) |
| `EID_SESSION_ENC_KEY` | сгенерировать (§3) |
| `OAUTH_ACCESS_TOKEN_SECRET` | сгенерировать (§3) |
| `GPT_OAUTH_CLIENT_SECRET` | сгенерировать (§3) |
| `SERVICE_API_TOKEN` | сгенерировать (§3) |
| `CORS_ALLOWED_ORIGINS` | origin spa (см. [`cors-allowed-origins.md`](./cors-allowed-origins.md)) |

`PORT` Railway задаёт сам — **не переопределять**.

Без любой из `pilot_required` переменных сервис **не стартует** (`ConfigError` на boot).

---

## 1. Куда класть значения

| Место | Что класть | Никогда |
|-------|------------|---------|
| **Локально** | `doge-identity-service/.env` (копия `.env.example`) | не коммитить в git |
| **Railway** | Variables сервиса **identity** | не в репозиторий |
| **ChatGPT Actions** | Bearer = `GPT_ACTIONS_BEARER_SECRET` на **gateway** (= `SERVICE_API_TOKEN` gateway) | не путать с identity |
| **ChatGPT OAuth** (дверь B) | Client ID / Secret / Redirect в настройках OAuth Custom GPT | только когда включаете OAuth |

Секреты identity **не** кладутся в spa-app, gateway или GPT UI репозиторий.

---

## 2. Публичное vs приватное

### Важно: «парный» ≠ публичный + приватный ключ

В OAuth client credentials **нет** пары RSA-ключей (как у TLS). Есть:

- **`GPT_OAUTH_CLIENT_ID`** — «логин» клиента (идентификатор, не секрет). Дефолт: `openai-custom-gpt`. **Не генерируется** — просто строка в env.
- **`GPT_OAUTH_CLIENT_SECRET`** — «пароль» клиента. **Генерируется одна** случайная строка (§3).

Слово **«парный»** в этой доке значит: **одно и то же секретное значение кладётся в два места** (identity env + ChatGPT OAuth Client Secret), а не что нужны два разных ключа.

### Типы переменных

| Тип | Примеры | Где хранить | Local vs prod |
|-----|---------|-------------|---------------|
| **Идентификатор** (не секрет) | `GPT_OAUTH_CLIENT_ID` | identity env + ChatGPT OAuth Client ID | можно одинаковый |
| **Секрет сервера** (приватный, одно место) | `OAUTH_ACCESS_TOKEN_SECRET`, `DOGESTONIA_EID_SECRET`, `EID_SESSION_ENC_KEY`, `SERVICE_API_TOKEN`, `SUPABASE_SERVICE_ROLE` | только identity env | **разные** значения на среду |
| **Секрет в двух местах** (одно значение, два хранилища) | `GPT_OAUTH_CLIENT_SECRET` | identity env **и** ChatGPT OAuth Client Secret | одно значение на среду |
| **Константа** | `GPT_OAUTH_REDIRECT_URI` | identity env + ChatGPT OAuth | одинакова везде (`https://oauth.pstmn.io/v1/callback`) |
| **URL** (не секрет, но разный по среде) | `API_BASE_URL`, `CORS_ALLOWED_ORIGINS`, `AUTHENTIGATE_REDIRECT_URI` | identity env | local ≠ prod |

**Правило:** приватные секреты prod **не копируйте** в local `.env`. Supabase prod и dev — **разные проекты** (CI test — третий, см. `.env.example` §CI).

**Не путать:**

- `SERVICE_API_TOKEN` на **identity** ≠ `SERVICE_API_TOKEN` на **gateway** (разные сервисы, **разные** сгенерированные значения).
- `GPT_OAUTH_CLIENT_SECRET` (identity OAuth) ≠ `GPT_ACTIONS_BEARER_SECRET` (gateway Actions Bearer).
- `GPT_OAUTH_CLIENT_SECRET` ≠ `OAUTH_ACCESS_TOKEN_SECRET` (разные роли — пароль клиента vs ключ подписи JWT).

---

## 3. Команды генерации секретов

Copy-paste. Выполните **отдельно** для local dev и для prod — значения должны отличаться.

```bash
# DOGESTONIA_EID_SECRET — HMAC для verified_person_hash / subject_hash (32 bytes, base64)
python3 -c "import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"

# EID_SESSION_ENC_KEY — Fernet-ключ для шифрования session secrets (см. session_secret.py)
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# OAUTH_ACCESS_TOKEN_SECRET — HMAC для подписи OAuth access-token JWT (32 bytes, base64)
python3 -c "import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"

# GPT_OAUTH_CLIENT_SECRET — пароль OAuth-клиента ChatGPT (случайная строка)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# SERVICE_API_TOKEN — сервисный токен для POST /oauth/introspect (случайная строка)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Не генерируются** — берутся из Supabase Dashboard:

- `SUPABASE_URL` — Settings → API → Project URL
- `SUPABASE_SERVICE_ROLE` — Settings → API → `service_role` key (secret)
- `DATABASE_URL` — Settings → Database → connection string

---

## 4. Local vs Production

| Переменная | Local demo | Local + Supabase | Railway pilot |
|------------|------------|------------------|---------------|
| `APP_PROFILE` | `demo` | `demo` или `pilot` | `pilot` |
| `API_BASE_URL` | `http://localhost:8100` | `http://localhost:8100` | `https://doge-identity-service-….up.railway.app` |
| `DB_BACKEND` | `in_memory` | `supabase` | `supabase` |
| `SMS_PROVIDER` | `mock` | `mock` | `mock` (**не** `file`) |
| `CORS_ALLOWED_ORIGINS` | `*` или `http://localhost:5173,…` | как demo | origin spa (не `*`) |
| Секреты `pilot_required` | не нужны в demo | нужны если `pilot` | все обязательны |
| `PORT` | `8100` | `8100` | не трогать |

В `demo` без `EID_SESSION_ENC_KEY` подставляется встроенный demo-дефолт ([`schema.py:19-20,199-200`](../../src/core/config/schema.py)) — **только для local demo**, не для pilot.

---

## 5. OAuth 2.0 Server и GPT

Identity реализует OAuth 2.0 Authorization Server для Custom GPT ([`handlers.py`](../../src/core/oauth/handlers.py), эндпоинты в [`asgi_app.py`](../../src/core/api/asgi_app.py)).

Подробная схема «две двери»: [`spa-app/docs/runtime-docs/gpt-oauth-and-story-submit-flow.md`](../../../spa-app/docs/runtime-docs/gpt-oauth-and-story-submit-flow.md).

### Дверь A — stash + redirect (основной сценарий сейчас)

```
ChatGPT --Bearer--> gateway POST /story-drafts
ChatGPT --redirect--> SPA /story/submit
SPA --browser--> identity /me, phone verification
SPA --browser--> gateway POST /story-drafts/{id}/submit
```

GPT Actions Bearer настраивается на **gateway** (`GPT_ACTIONS_BEARER_SECRET`), не на identity.
Переменные `GPT_OAUTH_*` в этом сценарии **не используются GPT напрямую**, но при `APP_PROFILE=pilot` **обязательны для старта** identity.

### Дверь B — GPT OAuth bridge (backend готов)

```
ChatGPT --> GET identity/oauth/authorize
identity --> redirect SPA /login?oauth_request_id=…
SPA --> POST identity/oauth/authorize/complete
identity --> redirect ChatGPT callback?code=…
ChatGPT --> POST identity/oauth/token (с client_secret)
```

Когда включаете OAuth в Custom GPT, продублируйте в его настройках:

| Поле в ChatGPT | Значение |
|----------------|----------|
| Client ID | `GPT_OAUTH_CLIENT_ID` (дефолт `openai-custom-gpt`) |
| Client Secret | тот же `GPT_OAUTH_CLIENT_SECRET`, что в identity env |
| Redirect URI | `GPT_OAUTH_REDIRECT_URI` (`https://oauth.pstmn.io/v1/callback`) |
| Authorization URL | `{API_BASE_URL}/oauth/authorize` |
| Token URL | `{API_BASE_URL}/oauth/token` |

### Переменные OAuth-блока

| Переменная | Что это | Откуда | Куда | Тип |
|------------|---------|--------|------|-----|
| `OAUTH_ACCESS_TOKEN_SECRET` | Ключ подписи access-token JWT ([`access_token_jwt.py`](../../src/core/oauth/access_token_jwt.py)) | §3 base64-команда | только identity env | приватный, **отдельный** секрет |
| `OAUTH_ACCESS_TOKEN_TTL_S` | Время жизни access token (сек), дефолт 3600 | из примера | identity env | настройка |
| `OAUTH_AUTHORIZATION_CODE_TTL_S` | Время жизни auth code (сек), дефолт 300 | из примера | identity env | настройка |
| `GPT_OAUTH_CLIENT_ID` | Идентификатор OAuth-клиента ChatGPT («логин») | дефолт `openai-custom-gpt`, не генерировать | identity env + ChatGPT OAuth **Client ID** | идентификатор (не секрет) |
| `GPT_OAUTH_CLIENT_SECRET` | Пароль клиента; ChatGPT шлёт при `POST /oauth/token` | §3 `token_urlsafe` — **одна** строка | identity env + ChatGPT OAuth **Client Secret** (то же значение) | приватный, **два места** |
| `GPT_OAUTH_REDIRECT_URI` | Callback OpenAI после авторизации | константа OpenAI | identity env + ChatGPT OAuth | константа |

**Частая ошибка:** сгенерировать одну base64-строку и положить её и в `OAUTH_ACCESS_TOKEN_SECRET`, и в `GPT_OAUTH_CLIENT_SECRET`. Нужны **два разных** значения (две команды из §3).

---

## 6. Остальные группы (кратко)

### Deployment

| Переменная | Назначение |
|------------|------------|
| `APP_PROFILE` | `demo` — мягкие дефолты; `pilot` — fail-fast на секретах |
| `API_BASE_URL` | Публичный base URL identity (OAuth redirects, ссылки в ответах) |
| `PORT` | Порт uvicorn; на Railway не переопределять |

### Supabase

См. [`supabase-project-setup.md`](./supabase-project-setup.md). `SUPABASE_SERVICE_ROLE` — **только server**, никогда в браузер.

### Identity secrets

| Переменная | Назначение |
|------------|------------|
| `DOGESTONIA_EID_SECRET` | HMAC для `verified_person_hash` / `subject_hash` |
| `EID_SESSION_ENC_KEY` | Fernet-ключ для `SessionSecretBox` ([`session_secret.py`](../../src/core/security/session_secret.py)) |

### Service trust — `SERVICE_API_TOKEN`

**Что это простыми словами:** общий «служебный пароль» между **доверенными backend-сервисами**. Identity проверяет его на `POST /oauth/introspect` — эндпоинте, где другой сервер (например gateway) спрашивает: «этот OAuth access token ещё жив? у пользователя верифицирован телефон?» ([`introspection.py`](../../src/core/oauth/introspection.py)).

Без правильного токена introspect отвечает **401** ([`security.py:108-116`](../../src/core/api/security.py)). В `APP_PROFILE=pilot` пустой `SERVICE_API_TOKEN` → сервис **не стартует** ([`schema.py:193-197`](../../src/core/config/schema.py)).

**Откуда брать:** нигде не выдаётся автоматически — **генерируете сами** (как пароль):

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Куда класть:**

| Место | Переменная | Значение |
|-------|------------|----------|
| identity `.env` / Railway Variables | `SERVICE_API_TOKEN` | сгенерированная строка |
| gateway (если снова включат вызов introspect) | отдельная env на gateway | **тот же** токен, что на identity (договорённость ops) |

Запрос к introspect ([`asgi_app.py:447-450`](../../src/core/api/asgi_app.py)):

```http
POST /oauth/introspect
Authorization: Bearer <SERVICE_API_TOKEN>
# или заголовок X-Service-Token: <SERVICE_API_TOKEN>
Content-Type: application/x-www-form-urlencoded

token=<oauth_access_token_to_check>
```

**Не путать с gateway `SERVICE_API_TOKEN`:** у gateway **свой** одноимённый токен — он защищает **другие** маршруты (stash от GPT, legacy intake). Это **другая** сгенерированная строка в Variables **другого** Railway-сервиса. Имена совпадают, значения — **нет**.

**Сейчас (дверь A):** GPT шлёт Bearer на gateway, не на identity introspect; но для pilot identity всё равно требует `SERVICE_API_TOKEN` на старте — introspect готов к двери B / server-to-server.

### CORS

См. [`cors-allowed-origins.md`](./cors-allowed-origins.md). На pilot — явный список origin spa, не `*`.

### Phone / SMS

`SMS_PROVIDER=mock` на pilot/Railway. `SMS_PROVIDER=file` **запрещён** для pilot ([`schema.py:178-181`](../../src/core/config/schema.py)).

### eID / Authentigate

Заполняются при включении реальных провайдеров (`EID_PROVIDER=authentigate` / `eideasy`). Redirect URI local vs prod — разные URL (§4).

---

## 7. Проверка после настройки

### Локально

```bash
make check-env
make serve
# в другом терминале:
curl -s http://localhost:8100/health
make smoke IDENTITY_URL=http://127.0.0.1:8100
```

### Railway

```bash
curl -s https://<identity-host>/health
make smoke IDENTITY_URL=https://<identity-host>
```

Подробнее: [`run-and-healthcheck.md`](./run-and-healthcheck.md).

CORS preflight (spa + identity):

```bash
cd spa-app
SPA_ORIGIN=https://dogestonia-spa-tallinn-demo.up.railway.app \
GATEWAY_BASE_URL=https://dogestonia-tallinn.up.railway.app \
IDENTITY_SERVICE_URL=https://doge-identity-service-tallinn-demo.up.railway.app \
  npm run verify:cors:preflight
```

---

## Связанные документы

| Документ | Когда читать |
|----------|--------------|
| [`.env.example`](../../.env.example) | шаблон для `.env` |
| [`cors-allowed-origins.md`](./cors-allowed-origins.md) | CORS и spa origin |
| [`run-and-healthcheck.md`](./run-and-healthcheck.md) | запуск и smoke |
| [`supabase-project-setup.md`](./supabase-project-setup.md) | новый Supabase проект |
| [`STORY-IDS-DEPLOY-01`](../tasks/backlog-stories/railway-deploy/STORY-IDS-DEPLOY-01-railway-deployability.md) | Railway deploy checklist |
