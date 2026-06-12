# Runbook — запуск сервиса (localhost / Railway) + healthcheck и HTTP-smoke

> **Назначение:** как поднять `doge-identity-service` локально и на Railway, как за секунды проверить живость через healthcheck-эндпоинты и сетевой smoke.
> **Методология:** только фактические команды/пути из кода (см. [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc)).
> **Якоря в коде:** ASGI-объект [`core.api.asgi_app:app`](../../src/core/api/asgi_app.py) (`app = create_app(provide_app_config())`), запуск [`Makefile`](../../Makefile) / [`railpack.json`](../../railpack.json) / [`railway.json`](../../railway.json), эндпоинты [`handlers.py`](../../src/core/api/handlers.py), smoke [`tests/smoke/`](../../tests/smoke/).

---

## TL;DR

```bash
# Локально (профиль demo, in-memory, mock-провайдеры — без Supabase/секретов)
make serve                      # http://127.0.0.1:8100

# Быстрая проверка живости (в другом терминале)
curl -s http://localhost:8100/health | jq        # {"data":{"status":"ok",...}}
make smoke                                        # HTTP-smoke по /health,/ready,/me,OPTIONS

# Railway: старт берётся из railpack.json, healthcheck — из railway.json (/health)
```

---

## 1. Предусловия

```bash
python3.11 -m venv .venv
.venv/bin/pip install -e .          # ставит fastapi, uvicorn, httpx, joserfc, cryptography, psycopg
```

Зависимости и версия Python зафиксированы в [`pyproject.toml`](../../pyproject.toml) (`requires-python = ">=3.11"`, `uvicorn>=0.30.0`).

**Профиль по умолчанию.** Без переменных окружения [`provide_app_config`](../../src/core/config/providers.py) поднимает безопасные дефолты: `APP_PROFILE=demo`, `PORT=8100`, `API_BASE_URL=http://localhost:8100`, `DB_BACKEND=in_memory`, `EID_PROVIDER=mock`, `SMS_PROVIDER=mock`. То есть сервис стартует «из коробки» — без Supabase, БД и секретов.

`provide_app_config` мёржит переменные из cwd `.env` поверх process-env (см. `resolve_config_env`), так что локальный `.env` (по образцу [`.env.example`](../../.env.example)) подхватывается автоматически.

---

## 2. Localhost

| Команда | Что делает |
|---------|-----------|
| `make serve` | uvicorn на `127.0.0.1:${PORT:-8100}`, подхватывает `./.env` |
| `make dev` | то же + `--reload --reload-dir src` (горячая перезагрузка) |
| `make check-env` | печатает ключевые env (APP_PROFILE/PORT/SUPABASE_*/EID_PROVIDER) |

Под капотом обе цели запускают (из [`Makefile`](../../Makefile)):

```bash
.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app --host 127.0.0.1 --port ${PORT:-8100}
```

Сменить порт: `make serve PORT=9000` (или `PORT=9000` в `.env`).

---

## 3. Railway build

Старт и healthcheck заданы **в двух файлах** (так задумано — поля healthcheck нет в схеме Railpack, проверено по `https://schema.railpack.com`):

**[`railpack.json`](../../railpack.json)** — команда старта (builder Railpack):
```json
{
  "deploy": {
    "startCommand": ".venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8100}"
  }
}
```
Отличие от локала: `--host 0.0.0.0` (слушать снаружи) и `PORT` Railway подставляет сам.

**[`railway.json`](../../railway.json)** — deploy-настройки Railway (схема `railway.com`):
```json
{
  "deploy": {
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30
  }
}
```
Railway после деплоя сам опрашивает `/health` и не переключает трафик, пока не получит 200 (gate деплоя). `railway.json` переопределяет только healthcheck-поля; `startCommand` остаётся единственным источником истины в `railpack.json`.

**Переменные окружения в Railway.** Для `demo` достаточно дефолтов. Для боевого `APP_PROFILE=pilot` обязательны (fail-fast `ConfigError` на старте, см. [`schema.py`](../../src/core/config/schema.py) `pilot_required`):
`API_BASE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE`, `SUPABASE_JWT_SECRET`, `DATABASE_URL`, `DOGESTONIA_EID_SECRET`, `EID_SESSION_ENC_KEY`, `OAUTH_ACCESS_TOKEN_SECRET`, `GPT_OAUTH_CLIENT_SECRET`. `PORT` Railway задаёт сам — не переопределять.

---

## 4. Healthcheck-эндпоинты

Оба определены в [`handlers.py`](../../src/core/api/handlers.py) и смонтированы в [`asgi_app.py`](../../src/core/api/asgi_app.py) (`@app.get("/health")`, `@app.get("/ready")`).

### `GET /health` — liveness (всегда 200, без зависимостей)
```bash
curl -s http://localhost:8100/health | jq
# {"data":{"status":"ok","trace_id":"<uuid>"}}
```
Процесс жив и обслуживает HTTP. БД не трогает — годится как Railway healthcheckPath.

### `GET /ready` — readiness (200 / 503, проверяет БД)
```bash
curl -si http://localhost:8100/ready | head -1     # HTTP/1.1 200 OK  ИЛИ  503
curl -s  http://localhost:8100/ready | jq
# {"data":{"status":"ready","db_backend":"in_memory","db_ready":true,"db_checks":{...},"trace_id":"..."}}
```
- `db_ready=true` → **200** `status:"ready"`.
- `db_ready=false` → **503** `status:"degraded"` (например `DB_BACKEND=supabase` без доступной БД).

| Эндпоинт | Назначение | Зависит от БД | Коды |
|----------|-----------|:---:|------|
| `/health` | liveness, Railway healthcheck | нет | 200 |
| `/ready` | readiness (готов принимать трафик) | да | 200 / 503 |

---

## 5. HTTP-smoke (быстрая проверка работающего сервера)

Сетевой smoke бьёт по **запущенному** серверу (а не in-process). Файлы — [`tests/smoke/`](../../tests/smoke/), маркер `smoke`, исключены из дефолтного `pytest tests/` через `collect_ignore=["smoke"]` ([`conftest.py`](../../tests/conftest.py)); запускаются только явным путём.

```bash
# против локального сервера (дефолт IDENTITY_URL=http://localhost:8100)
make smoke
# или напрямую:
IDENTITY_URL=http://localhost:8100 .venv/bin/python -m pytest tests/smoke/ -q

# против деплоя Railway
make smoke IDENTITY_URL=https://<app>.up.railway.app
```

Если сервер недоступен — тесты **скипаются** (не падают): [`tests/smoke/conftest.py`](../../tests/smoke/conftest.py) пингует `/health` и при ошибке делает `pytest.skip`.

Что проверяет [`test_local_server_smoke.py`](../../tests/smoke/test_local_server_smoke.py):

| Тест | Ожидание |
|------|----------|
| `test_health` | `/health` → 200, `data.status == "ok"` |
| `test_ready` | `/ready` → 200 или 503, в теле `db_backend` + `db_ready` |
| `test_me_without_auth` | `/me` без токена → 401, `error.code == "AUTHENTICATION_REQUIRED"` |
| `test_options_me` | `OPTIONS /me` → 200 (CORS preflight) |
| `test_options_oauth_authorize` | `OPTIONS /oauth/authorize` → 200 |

**Однострочник для CI/деплой-гейта** (без pytest):
```bash
curl -fsS http://localhost:8100/health | jq -e '.data.status == "ok"' && echo "alive"
```

---

## 6. Troubleshooting

| Симптом | Причина / действие |
|---------|--------------------|
| `Address already in use` на старте | порт занят → `make serve PORT=9000` |
| `/me` отдаёт **401** | это норма без `Authorization: Bearer <supabase-jwt>` — smoke это и проверяет |
| `/ready` отдаёт **503** | `db_ready=false` — при `DB_BACKEND=supabase` проверь `SUPABASE_URL`/`DATABASE_URL`; для локала используй дефолтный `DB_BACKEND=in_memory` |
| `ConfigError: <VAR> is required for APP_PROFILE=pilot` | в pilot не задан обязательный секрет — см. список в §3 |
| `make smoke` всё скипает | сервер не поднят на `IDENTITY_URL` — сначала `make serve` |
| Railway: деплой висит на healthcheck | `/health` не отвечает 200 — смотри логи старта (вероятно `ConfigError` pilot-секретов) |

---

## Связанные документы
- [`supabase-project-setup.md`](./supabase-project-setup.md) — настройка Supabase (для `DB_BACKEND=supabase`/pilot).
- [`phone-sms-verification.md`](./phone-sms-verification.md) — телефонная верификация (Telnyx/`SMS_PROVIDER`).
- [`.env.example`](../../.env.example) — полный перечень переменных окружения.
