# EPIC-IDS-02 — FastAPI Transport Layer

> **ID:** `EPIC-IDS-02`
> **Layer:** NFR / HTTP Transport
> **Статус:** Реализовано (transport P3 pkg-000003; операторский curl smoke — §8)
> **Зависит от:** EPIC-IDS-01 (`AppConfig`, `provide_app_config`, pyproject deps)
> **Блокирует:** EPIC-IDS-03 (singleton hook), EPIC-IDS-06 (HTTP smoke тесты)

---

## 1. Назначение

HTTP transport-слой: FastAPI-приложение с lifespan, CORS, exception handlers, trace-id propagation, response envelope. Никакой бизнес-логики — только routing, парсинг запросов, вызов handlers. Реальные роуты в этом эпике: `/health`, `/ready`. Identity-роуты (`/me`, `/auth/eid/*`, `/oauth/*`, `/story-drafts*`, `/stories`, `/gpt/actions/submit-story`) фиксируются в контрактной таблице и существуют как **stub-handlers** — фактическая логика приходит в функциональных эпиках следующего слоя.

## 2. Epic Goal

```bash
make serve
curl -i http://localhost:8100/health         # 200 {"data": {"status": "ok", "trace_id": "..."}}
curl -i http://localhost:8100/ready          # 200/503 {"data": {"db_backend": "in_memory", "db_ready": true, ...}}
curl -i http://localhost:8100/me             # 401 {"error": {"code": "AUTHENTICATION_REQUIRED", "trace_id": "..."}}
curl -i -X OPTIONS http://localhost:8100/me  # 200 (CORS preflight)
```

- `x-trace-id: my-trace` пробрасывается в response envelope как `trace_id`.
- ASGI lifespan вызывает `get_api_dependencies()` при старте — singleton инициализируется до первого запроса.
- Никакой бизнес-логики в `asgi_app.py`.

## 3. Бизнес-контекст

Identity-сервису требуется:
- `/health` + `/ready` — operability ([`docs/requirements/16`](../../requirements/16-security-privacy-observability.md) §"Health и Readiness Endpoints").
- `/me` — основной authenticated endpoint ([`docs/requirements/10`](../../requirements/10-me-endpoint.md)).
- `/auth/eid/start` + provider-specific callbacks (`/auth/eideasy/callback`, `/auth/authentigate/callback`, `/auth/mock/callback`) — eID flow ([`docs/requirements/11`](../../requirements/11-eid-verification-flow.md), [`17`](../../requirements/17-eid-provider-abstraction.md) §"Публичные HTTP endpoints").
- `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` — OAuth 2.0 server для Custom GPT ([`docs/requirements/14`](../../requirements/14-oauth-server-custom-gpt.md)).
- `/story-drafts`, `/story-drafts/{id}/submit`, `/stories`, `/gpt/actions/submit-story` — story authorization ([`docs/requirements/15`](../../requirements/15-story-authorization.md)).

В этом эпике все identity-роуты создаются как stub-handlers (`return 501 NOT_IMPLEMENTED`), чтобы зафиксировать **routes contract** — функциональные эпики будут заменять stubs реальной логикой, не двигая URL.

Gateway-роуты (`/intake/stories`, `/tallinn/issues`) исключены — это другой сервис.

## 4. Предусловия

- EPIC-IDS-01 выполнен: `core.config.AppConfig`, `provide_app_config()`, pyproject содержит `fastapi`, `uvicorn`, `httpx`.

## 5. Целевые файлы

```
src/core/api/__init__.py
src/core/api/asgi_app.py
src/core/api/envelope.py
src/core/api/security.py
src/core/api/idempotency.py
src/core/api/handlers.py
src/core/logging_setup.py
```

## 6. Stories (заготовка)

### Story 1: Response envelope, error types и trace-id

- **Why:** Единый формат всех ответов — `{"data": {...}}` для успешных, `{"error": {"code": "...", "message": "...", "trace_id": "..."}}` для ошибок. SPA, Custom GPT и тесты могут полагаться на этот контракт. Trace ID propagation — observability minimum ([`docs/requirements/16`](../../requirements/16-security-privacy-observability.md) §"Trace ID паттерн").
- **Inputs:** Паттерн envelope из [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 1".
- **Outputs:**
  - `src/core/api/envelope.py`:
    - `build_success_envelope(data: dict) -> dict`.
    - `build_error_envelope(code: str, message: str, trace_id: str | None, status_code: int) -> dict`.
    - `ensure_trace_id(incoming: str | None) -> str` — возвращает входящий заголовок `x-trace-id` или генерирует UUID4.
  - `src/core/api/idempotency.py`:
    - `resolve_idempotency_key(headers) -> str | None` — кейс-инсенситив поиск `Idempotency-Key`.
- **Acceptance Criteria:**
  - `build_success_envelope({"status": "ok"}) == {"data": {"status": "ok"}}`.
  - `build_error_envelope("NOT_FOUND", "missing", trace_id="abc", status_code=404)["error"]["trace_id"] == "abc"`.
  - `ensure_trace_id(None)` возвращает строку с UUID4 (validate via `uuid.UUID(...)`).
  - `resolve_idempotency_key({"idempotency-key": "K"})` == `"K"`; case-insensitive.
- **Pattern source:** [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 1" — копия Task 1.1 + 1.3. Task 1.2 (ServiceTokenAuth) **не используется** — заменяется в Story 3 на `BearerTokenAuth` stub (см. ниже).

### Story 2: Logging setup

- **Why:** Тесты запускаются без ASGI lifespan — логирование должно инициализироваться явно (в lifespan + в `_pytest_session_logging` fixture EPIC-IDS-06). Поддержка `json` формата для production.
- **Inputs:** [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 2", Task 2.1.
- **Outputs:**
  - `src/core/logging_setup.py`:
    - `configure_logging(log_level: str, log_format: str = "text", log_debug_dir: str | None = None) -> None`.
    - `log_runtime_exception(exc, *, trace_id, path)`.
- **Acceptance Criteria:**
  - `configure_logging("DEBUG")` — root logger level = DEBUG.
  - `configure_logging("INFO", log_format="json")` без исключений.
  - `log_runtime_exception(ValueError("test"), trace_id="abc", path="/me")` — логирует через `core.runtime` без исключений.
- **Pattern source:** [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 2" — копия Task 2.1, без identity-адаптации.

### Story 3: Auth security primitives — BearerTokenAuth stub

- **Why:** В identity-сервисе authorization устроена через Supabase JWT (Bearer) — `ServiceTokenAuth` из gateway здесь не подходит. На этом эпике делаем stub-валидатор (всегда `401 AUTHENTICATION_REQUIRED` если нет валидного `Authorization: Bearer ...`). Реальная JWT-валидация подключается в EPIC-IDS-04 через DI (`supabase_jwt_validator`) и FastAPI dependency `get_current_user`, описанный в [`docs/requirements/09`](../../requirements/09-supabase-jwt-validation.md).
- **Inputs:**
  - Контракт authentication errors: [`docs/requirements/09`](../../requirements/09-supabase-jwt-validation.md) §"FastAPI Dependency Pattern" + [`docs/requirements/16`](../../requirements/16-security-privacy-observability.md) §"Security Requirements".
  - Pattern для exception-handler: [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 3", Task 3.2 §"Exception handlers".
- **Outputs:**
  - `src/core/api/security.py`:
    - `class UnauthorizedError(Exception)` с `code: str = "AUTHENTICATION_REQUIRED"`, `message: str`.
    - `class BearerTokenAuth(Protocol)`:
      - `def validate(self, headers: Mapping[str, str]) -> "UserClaims | None"`.
    - `class StubBearerTokenAuth` — реализация для EPIC-IDS-02..03:
      - Любой запрос без `Authorization: Bearer ...` → `UnauthorizedError`.
      - Любой запрос с `Bearer ...` (любым) → возвращает `UserClaims(supabase_user_id="00000000-0000-0000-0000-000000000000", email=None, role="authenticated")` (placeholder; реальная валидация в EPIC-IDS-04).
    - `def get_current_user(...)` — FastAPI dependency, использует `deps.bearer_token_auth.validate(headers)`; бросает `UnauthorizedError` или возвращает `UserClaims`.
- **Acceptance Criteria:**
  - `StubBearerTokenAuth().validate({})` бросает `UnauthorizedError`.
  - `StubBearerTokenAuth().validate({"authorization": "Bearer xyz"})` возвращает `UserClaims` с заглушечным UUID.
  - `BearerTokenAuth` — Protocol (без наследования); `StubBearerTokenAuth` соответствует.
  - `UnauthorizedError.code == "AUTHENTICATION_REQUIRED"` (req-09 acceptance).
- **Pattern source:** [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 1", Task 1.2 — структура `ServiceTokenAuth` (классы + auth header parsing), но **переименован/перепрофилирован** под Bearer-JWT model. Конкретный JWT decode придёт в EPIC-IDS-04 как `SupabaseJwtBearerTokenAuth`.

### Story 4: FastAPI app, lifespan, CORS, middleware, exception handlers

- **Why:** `asgi_app.py` — единственная точка входа ASGI. Lifespan форсирует создание DI singleton при старте. CORS — для SPA и Custom GPT клиентов. Глобальные exception handlers переводят `UnauthorizedError`, `ConfigError`, неизвестные exceptions в envelope-формат.
- **Inputs:**
  - Lifespan + CORS pattern: [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 3", Task 3.2.
  - CORS spec: [`docs/requirements/16`](../../requirements/16-security-privacy-observability.md) §"CORS Configuration" — `allow_origins=config.cors_allowed_origins.split(",")`, `allow_methods=["GET", "POST", "OPTIONS"]`, `allow_headers=["authorization", "content-type", "x-trace-id"]`.
- **Outputs:**
  - `src/core/api/asgi_app.py`:
    - **`create_app(config: AppConfig) -> FastAPI`** — сборка приложения на module-level; CORS регистрируется **при создании app**, не в lifespan (interview 4.1).
    - `_lifespan` — только `get_api_dependencies()` + `configure_logging(...)`; **без** `add_middleware(CORSMiddleware)`.

      ```python
      from contextlib import asynccontextmanager
      from fastapi.middleware.cors import CORSMiddleware

      def create_app(config: AppConfig) -> FastAPI:
          app = FastAPI(title="doge-identity-service", version="0.1.0", lifespan=_lifespan)
          app.add_middleware(
              CORSMiddleware,
              allow_origins=config.cors_allowed_origins.split(","),
              allow_methods=["GET", "POST", "OPTIONS"],
              allow_headers=["authorization", "content-type", "x-trace-id"],
          )
          _register_routes(app)
          return app

      @asynccontextmanager
      async def _lifespan(app: FastAPI):
          deps = get_api_dependencies()
          configure_logging(deps.config.log_level, log_format=deps.config.log_format)
          yield

      _config = provide_app_config()
      app = create_app(_config)
      ```

    - `@app.middleware("http")` `runtime_exception_diagnostics` — пробрасывает `x-trace-id`, ловит unhandled exceptions, `log_runtime_exception`.
    - `@app.exception_handler(UnauthorizedError)` → 401 envelope с `code="AUTHENTICATION_REQUIRED"`.
    - `@app.exception_handler(ConfigError)` → 500 envelope с `code="CONFIG_ERROR"`.
    - `@lru_cache(maxsize=1)` `_cached_dependencies()` + `_clear_api_dependencies_cache()` + `get_api_dependencies()` (минимальная версия — реальная в EPIC-IDS-03).
  - `src/core/api/__init__.py` экспортирует `app`, `get_api_dependencies`, `ApiDependencies` (последний из EPIC-IDS-03).
- **Acceptance Criteria:**
  - `GET /health` → 200 envelope.
  - `OPTIONS /me` → 200 (CORS preflight).
  - Заголовок `x-trace-id: my-trace` → в envelope `data.trace_id == "my-trace"`.
  - `GET /me` без `Authorization` → 401 envelope с `code="AUTHENTICATION_REQUIRED"`.
  - `app.title == "doge-identity-service"`.
  - `CORSMiddleware` зарегистрирован до первого HTTP-запроса (в `create_app`, не в runtime lifespan).
  - `allow_origins` берётся из `config.cors_allowed_origins`, не из прямого `os.environ`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 3" — копия Task 3.2 с адаптациями: title, `create_app(config)` + CORS при сборке, exception handler `AUTHENTICATION_REQUIRED` per req-09. См. [`interview-cpo-cto-epics-2026-05-27.md`](../../analysis/interview-cpo-cto-epics-2026-05-27.md) §4.1.

### Story 5: Routes contract — `/health`, `/ready` (реальные) + identity-routes (stubs)

- **Why:** Зафиксировать полный список URL'ов один раз — функциональные эпики не должны менять paths. Stubs возвращают `501 NOT_IMPLEMENTED` envelope с `next_epic` подсказкой — это даёт смоук-тесту EPIC-IDS-06 что-то проверять, и человеку — карту незавершённой работы.
- **Inputs:**
  - `/health` + `/ready` шаблон: [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 3", Task 3.1 — `handle_health`, `handle_readiness`.
  - `/me` контракт: [`docs/requirements/10`](../../requirements/10-me-endpoint.md) §"Endpoint" + §"Auth".
  - eID routes: [`docs/requirements/11`](../../requirements/11-eid-verification-flow.md) (POST `/auth/eid/start`) + [`docs/requirements/17`](../../requirements/17-eid-provider-abstraction.md) §"Provider callbacks" (`/auth/eideasy/callback`, `/auth/authentigate/callback`, `/auth/mock/callback`).
  - OAuth routes: [`docs/requirements/14`](../../requirements/14-oauth-server-custom-gpt.md) §"GET /oauth/authorize", §"POST /oauth/authorize/complete", §"POST /oauth/token".
  - Story routes: [`docs/requirements/15`](../../requirements/15-story-authorization.md) §"Canonical Story Lifecycle".
- **Outputs:**
  - `src/core/api/handlers.py`:
    - `handle_health(deps, *, trace_id) -> (envelope, status_code)`.
    - `handle_readiness(deps, *, trace_id)` → читает `deps.db_backend`, `deps.db_ready`, `deps.db_checks` (последние заполнятся в EPIC-IDS-03/05). Возвращает 200 если `db_ready`, иначе 503.
    - `handle_me_stub(deps, *, current_user, trace_id) -> envelope` → 501 `{"error": {"code": "NOT_IMPLEMENTED", "message": "GET /me implemented in EPIC-IDS-AUTH-CORE", ...}}`.
    - Аналогичные stub-handlers для всех identity-роутов.
  - Регистрация роутов в `asgi_app.py`:

| Method | Path | Auth | Handler | Status | Источник |
|--------|------|------|---------|--------|----------|
| GET | `/health` | public | `handle_health` | 200 | tech-req-02 |
| GET | `/ready` | public | `handle_readiness` | 200/503 | tech-req-02 + req-16 |
| GET | `/me` | Bearer | `handle_me_stub` | 501 | req-10 |
| POST | `/auth/eid/start` | Bearer | stub | 501 | req-11, req-17 |
| GET | `/auth/eideasy/callback` | public | stub | 501 | req-17, req-18 |
| GET | `/auth/authentigate/callback` | public | stub | 501 | req-17 |
| GET | `/auth/mock/callback` | public | stub | 501 | req-17 mock provider |
| GET | `/oauth/authorize` | Bearer | stub | 501 | req-14 |
| POST | `/oauth/authorize/complete` | Bearer | stub | 501 | req-14 |
| POST | `/oauth/token` | Basic (client) | stub | 501 | req-14 |
| POST | `/story-drafts` | Bearer | stub | 501 | req-15 |
| POST | `/story-drafts/{draft_id}/submit` | Bearer | stub | 501 | req-15 |
| POST | `/stories` | Bearer | stub | 501 | req-15 |
| POST | `/gpt/actions/submit-story` | Bearer (OAuth) | stub | 501 | req-15 |
| OPTIONS | `/me` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/auth/eid/start` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/oauth/authorize` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/oauth/authorize/complete` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/oauth/token` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/story-drafts` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/story-drafts/{draft_id}/submit` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/stories` | public | `Response(status_code=200)` | 200 | CORS preflight |
| OPTIONS | `/gpt/actions/submit-story` | public | `Response(status_code=200)` | 200 | CORS preflight |

> **Примечание (audit M-6):** OPTIONS регистрируется ТОЛЬКО для защищённых (Bearer) endpoints, где браузер делает CORS preflight перед запросом с `Authorization`/custom headers. Public GET-callback paths (`/auth/eideasy/callback`, `/auth/authentigate/callback`, `/auth/mock/callback`) НЕ требуют OPTIONS — eID-провайдер редиректит браузер через `302 → GET`, без preflight. Аналогично `/health`, `/ready` — public GET без custom headers.

  - Все stubs возвращают envelope с `code="NOT_IMPLEMENTED"`, `message` указывает целевой следующий эпик; `next_epic` — поле для агента-исполнителя.

- **Acceptance Criteria:**
  - `GET /health` → 200, `data.status == "ok"`.
  - `GET /ready` (in_memory backend) → 200, `data.db_backend == "in_memory"`, `data.db_ready is True`.
  - `GET /me` без token → 401 `AUTHENTICATION_REQUIRED`.
  - `GET /me` с `Bearer xyz` → 501 `NOT_IMPLEMENTED` (stub).
  - `OPTIONS /me` → 200.
  - `app.routes` — содержит все 14 paths из таблицы выше; smoke-тест EPIC-IDS-06 пройдёт.
  - `asgi_app.py` не содержит бизнес-логики — только routing + lifespan + middleware + exception handlers.
- **Pattern source:** [`docs/tech-requirements/impl-epic-02`](../../tech-requirements/impl-epic-02-fastapi-transport.md) §"Story 3" + §"Story 4" — структура handlers + routes contract. Полностью адаптировано под identity URL'ы.

## 7. Critical Pitfalls (identity-flavored)

- `host=127.0.0.1` недоступен снаружи контейнера — для Railway/Docker `0.0.0.0` (Story 4 lifespan/uvicorn).
- Lifespan **обязан** вызывать `get_api_dependencies()` — без этого singleton инициализируется при первом запросе, startup-логи не появятся, латентность первого запроса выше.
- `_clear_api_dependencies_cache()` нужен в тестах — без него singleton использует env предыдущего теста.
- `OPTIONS` роуты НЕ создаются FastAPI автоматически — добавлять явно для каждого защищённого пути.
- Не добавлять бизнес-логику в `asgi_app.py` — только routing, middleware, exception handlers (паттерн остаётся прежним).
- Identity-сервис **не имеет** gateway-роутов `/tallinn/*`, `/intake/stories` — не копировать из tech-requirements.
- Stub-handler `/me` возвращает **501**, а **401** возвращает только `UnauthorizedError` exception handler — не путать (см. acceptance Story 4 vs Story 5).
- CORS настраивается в `create_app(config)` из `config.cors_allowed_origins` — не в `_lifespan` и не из `os.environ` напрямую (req-16, interview 4.1).

## 8. Верификация эпика

```bash
# 1. Сервер стартует
make serve &
sleep 2

# 2. Health
curl -s http://localhost:8100/health | python3 -m json.tool
# Ожидаемо: {"data": {"status": "ok", "trace_id": "..."}}

# 3. Ready
curl -s http://localhost:8100/ready | python3 -m json.tool
# Ожидаемо: {"data": {"status": "ready", "db_backend": "in_memory", "db_ready": true, ...}}

# 4. /me без auth — 401
curl -si http://localhost:8100/me | head -5
# Ожидаемо: HTTP/1.1 401, {"error":{"code":"AUTHENTICATION_REQUIRED",...}}

# 5. /me со stub bearer — 501
curl -si -H 'Authorization: Bearer stub' http://localhost:8100/me | head -5
# Ожидаемо: HTTP/1.1 501, {"error":{"code":"NOT_IMPLEMENTED",...}}

# 6. CORS preflight
curl -si -X OPTIONS http://localhost:8100/me | head -5
# Ожидаемо: HTTP/1.1 200

# 7. trace_id propagation
curl -s -H 'x-trace-id: my-tr' http://localhost:8100/health | python3 -m json.tool | grep my-tr

# 8. Pytest HTTP smoke (после EPIC-IDS-06)
python3.11 -m pytest tests/test_http_transport_smoke.py -v

kill %1
```

## 9. Open Questions

- В `handle_readiness` — список `db_checks` для identity-таблиц определяется в EPIC-IDS-05 (`profiles`, `eid_verification_sessions`, `eid_audit_events`, +`eid_provider_state` после req-17 миграции). В EPIC-IDS-02 — поле существует, но пустое при `db_backend=in_memory`.
- В Story 5 `/gpt/actions/submit-story` помечен `Bearer (OAuth)` — реально это другой validator: OAuth access token, выданный нашим `/oauth/token` (req-14 §"Access Token Format"), а не Supabase JWT. В EPIC-IDS-02 stub не различает; разделение — в функциональном эпике (auth core + oauth server).
