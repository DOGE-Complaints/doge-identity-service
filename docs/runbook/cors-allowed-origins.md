# CORS_ALLOWED_ORIGINS — runbook

> **Назначение:** что такое CORS в контексте identity, как настроить локально и на Railway, как проверить.
> **Код:** [`asgi_app.py`](../../src/core/api/asgi_app.py) (`CORSMiddleware`), [`schema.py`](../../src/core/config/schema.py) (`cors_allowed_origins`), [`spa_login.py`](../../src/core/oauth/spa_login.py) (OAuth redirect base).

---

## Простыми словами

**CORS** (Cross-Origin Resource Sharing) — правило браузера: если JavaScript на странице `https://spa.example.com` хочет вызвать API на **другом** адресе (`https://identity.example.com`), браузер сначала спрашивает identity: «можно ли этому сайту читать ответ?».

`CORS_ALLOWED_ORIGINS` — **белый список адресов фронтенда**, с которых identity разрешает такие запросы.

Это **не** замена авторизации:

- CORS решает, **может ли браузер вообще прочитать ответ** с другого домена.
- `Authorization: Bearer …` решает, **кто пользователь** (`/me` без токена → **401** — это норма).

Если origin spa **не** в списке, браузер заблокирует ответ (в DevTools — CORS error), даже если identity вернул бы 200/401.

---

## Как identity использует переменную

### 1. CORS middleware (основное)

При старте [`create_app`](../../src/core/api/asgi_app.py) читает `CORS_ALLOWED_ORIGINS` из env → `AppConfig.cors_allowed_origins` и регистрирует:

| Параметр | Значение в коде |
|----------|-----------------|
| `allow_origins` | список после `split(",")` (пробелы обрезаются) |
| `allow_methods` | `GET`, `POST`, `OPTIONS` |
| `allow_headers` | `authorization`, `content-type`, `x-trace-id` |

На **каждый** запрос с заголовком `Origin` identity, если origin в списке, добавляет в ответ `Access-Control-Allow-Origin: <тот же origin>`.

Для **preflight** (`OPTIONS` перед `GET /me` с `Authorization`) spa-скрипт [`verify-cors-preflight.mjs`](../../../spa-app/scripts/verify-cors-preflight.mjs) проверяет именно `OPTIONS /me`.

### 2. OAuth redirect на spa (вторичное)

[`resolve_spa_login_base_url`](../../src/core/oauth/spa_login.py) берёт **первый** origin из списка (не `*`) и строит:

- `/login?oauth_request_id=…`
- `/verify?context=…`

Поэтому **первым** в списке на проде ставьте origin **основного spa**, не ChatGPT.

### Дефолт в коде

[`schema.py`](../../src/core/config/schema.py): если переменная не задана → `*`.

`*` удобно для локальной разработки, но на **pilot/Railway** рекомендуется явный список доменов ([DEPLOY-01](../tasks/backlog-stories/railway-deploy/STORY-IDS-DEPLOY-01-railway-deployability.md)).

---

## Что писать в значении

**Формат:** через запятую, **без пробелов** (или с пробелами — код их обрежет).

**Origin** = только `схема + хост + порт`, **без** пути и без завершающего `/`:

| Правильно | Неправильно |
|-----------|-------------|
| `https://dogestonia-spa-tallinn-demo.up.railway.app` | `https://…/login` |
| `http://localhost:5173` | `http://localhost:5173/` (обычно ок после strip, но лучше без slash) |
| `http://127.0.0.1:4173` | `*` вместе с конкретными URL (достаточно одного `*`) |

`localhost` и `127.0.0.1` — **разные** origin для браузера; если ходите с обоих — укажите оба.

---

## Локальная разработка

Типичный стек: spa (`npm run dev` → **5173**) + identity (`make serve` → **8100**).

В `doge-identity-service/.env`:

```bash
# Vite dev (основной)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Если тестируете production-бандл spa через preview:
# CORS_ALLOWED_ORIGINS=http://localhost:4173,http://127.0.0.1:4173

# Или для быстрых экспериментов (открыто всем origin — только dev):
# CORS_ALLOWED_ORIGINS=*
```

В `spa-app/.env` (куда spa ходит за API):

```bash
VITE_IDENTITY_SERVICE_URL=http://127.0.0.1:8100
```

**Проверка локально:**

```bash
# Терминал 1
cd doge-identity-service && make serve

# Терминал 2 — preflight как у браузера
curl -si -X OPTIONS http://127.0.0.1:8100/me \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: authorization" \
  | rg -i "access-control-allow"
# Ожидание: access-control-allow-origin: http://localhost:5173
```

Или из spa-app (identity должен быть жив):

```bash
SPA_ORIGIN=http://localhost:5173 \
GATEWAY_BASE_URL=http://127.0.0.1:8000 \
IDENTITY_SERVICE_URL=http://127.0.0.1:8100 \
  npm run verify:cors:preflight
```

---

## Railway (production / pilot)

В **Railway Variables** сервиса `doge-identity-service` (не в git):

```bash
CORS_ALLOWED_ORIGINS=https://dogestonia-spa-tallinn-demo.up.railway.app
```

Если нужен OAuth из Custom GPT в браузере — добавьте второй origin (через запятую):

```bash
CORS_ALLOWED_ORIGINS=https://dogestonia-spa-tallinn-demo.up.railway.app,https://chat.openai.com
```

**Важно:**

1. URL spa должен **совпадать** с тем, что видит пользователь в адресной строке (тот же хост, что в `SPA_BASE_URL` / Railway domain spa).
2. CORS **не поможет**, если identity не запущен (502/timeout) — сначала должен отвечать `GET /health` (см. [run-and-healthcheck.md](run-and-healthcheck.md)).
3. Gateway и identity — **разные** сервисы: у gateway свой CORS; spa ходит в **оба**.

**Проверка после деплоя:**

```bash
SPA_ORIGIN=https://dogestonia-spa-tallinn-demo.up.railway.app \
GATEWAY_BASE_URL=https://dogestonia-tallinn.up.railway.app \
IDENTITY_SERVICE_URL=https://doge-identity-service-tallinn-demo.up.railway.app \
  npm run verify:cors:preflight
```

---

## Симптомы и диагностика

| Симптом | Вероятная причина |
|---------|-------------------|
| `502` / timeout на `/health`, `/me`, `OPTIONS /me` | Процесс identity не запущен (crash loop, неверный `startCommand`) — **не CORS** |
| `401` на `GET /me` без Bearer | Норма — нужна Supabase-сессия |
| CORS error в браузере, curl с правильным `Origin` без `Access-Control-Allow-Origin` | Origin spa не в `CORS_ALLOWED_ORIGINS` |
| OAuth редирект ведёт не на тот spa | Первый origin в списке не тот; поправить порядок |
| `*` на pilot | Работает, но слабее с точки зрения политики; DEPLOY-01 просит явный origin spa |

---

## Связанные документы

- [08-ui-expectations.md](../runtime-docs/08-ui-expectations.md) — контракт spa ↔ identity
- [07-env-configuration-spec.md](../requirements/07-env-configuration-spec.md) — полная таблица env
- [spa-app railway-git-deploy-manual.md](../../../spa-app/docs/railway-git-deploy-manual.md) — URL spa на Railway
