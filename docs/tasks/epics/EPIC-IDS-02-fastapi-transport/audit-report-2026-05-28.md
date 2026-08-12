# Аудит EPIC-IDS-02 — FastAPI Transport Layer

> **Дата:** 2026-05-28
> **Методология:** [`analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — только верифицированные факты с путями и строками
> **Предмет:** Acceptance Criteria каждой Story и Task vs фактический код
> **Статус эпика по итогам:** ✅ Implemented — все 5 stories, 14 tasks верифицированы

---

## Сводная таблица

| ID | Story | Severity | Суть | Статус |
|----|-------|----------|------|--------|
| A-1 | S4 | MEDIUM | Нет теста на CORS-заголовки в HTTP-ответе | 🟢 Closed |
| A-2 | S4/S5 | LOW | `/ready` → 503 для supabase не покрыт тестом | 🟢 Closed |

**Блокирующих findings нет.** Обе позиции — gap в тестовом покрытии.

---

## Story 1 — Response Envelope, Error, Trace-ID (IDS-02-01)

**Файлы:** [`src/core/api/envelope.py`](../../../../src/core/api/envelope.py) · [`src/core/api/idempotency.py`](../../../../src/core/api/idempotency.py) · [`tests/test_api_envelope.py`](../../../../tests/test_api_envelope.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `build_success_envelope(data)` → `{"data": data}` | `envelope.py:7` | ✅ |
| `build_error_envelope(code, msg, trace_id)` → `{"error": {...}}` | `envelope.py:10–20` | ✅ |
| `trace_id` включается в envelope только если не `None`/пустой | `envelope.py:18–19` | ✅ |
| `status_code` игнорируется (`del status_code`) — reserved | `envelope.py:16` | ✅ |
| `ensure_trace_id(None)` генерирует UUID4 | `envelope.py:23–26` | ✅ |
| `ensure_trace_id(" X ")` → `"X"` (strip) | `envelope.py:24` | ✅ |
| `resolve_idempotency_key` case-insensitive | `idempotency.py:7` | ✅ |
| Тесты: 8 кейсов | `test_api_envelope.py:13–55` | ✅ |

**Story 1: ✅ VERIFIED — 0 findings**

---

## Story 2 — Logging Setup (IDS-02-02)

**Файлы:** [`src/core/logging_setup.py`](../../../../src/core/logging_setup.py) · [`tests/test_logging_setup.py`](../../../../tests/test_logging_setup.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `configure_logging(log_level, log_format="text")` | `logging_setup.py:8` | ✅ |
| `log_format="json"` → JSON-строка формата | `logging_setup.py:16–20` | ✅ |
| `log_format="text"` → человекочитаемый формат | `logging_setup.py:21–22` | ✅ |
| `log_runtime_exception(exc, *, trace_id, path)` | `logging_setup.py:28` | ✅ |
| Logger name: `core.runtime`, level: `ERROR` | `logging_setup.py:29–35` | ✅ |
| Сообщение содержит `path`, `trace_id`, `repr(exc)` | `logging_setup.py:31–35` | ✅ |
| Импорт в `asgi_app.py` | `asgi_app.py:23` | ✅ |
| Тесты: 3 кейса (DEBUG level, json format, emit check) | `test_logging_setup.py:10–32` | ✅ |

**Story 2: ✅ VERIFIED — 0 findings**

---

## Story 3 — Auth Security Primitives + Bearer Stub (IDS-02-03)

**Файлы:** [`src/core/api/security.py`](../../../../src/core/api/security.py) · [`tests/test_security_primitives.py`](../../../../tests/test_security_primitives.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `UnauthorizedError.code = "AUTHENTICATION_REQUIRED"` | `security.py:14` | ✅ |
| `UserClaims(frozen=True)` с полями `supabase_user_id`, `email`, `role` | `security.py:21–24` | ✅ |
| `BearerTokenAuth(Protocol, @runtime_checkable)` | `security.py:28–30` | ✅ |
| `StubBearerTokenAuth.validate` без токена → `UnauthorizedError` | `security.py:37–38` | ✅ |
| `StubBearerTokenAuth.validate` с токеном → `UserClaims(STUB_UUID, None, "authenticated")` | `security.py:39–42` | ✅ |
| `isinstance(StubBearerTokenAuth(), BearerTokenAuth)` = True | `security.py:28` `@runtime_checkable` | ✅ |
| Lazy import в `_get_api_dependencies()` — нет circular import | `security.py:56–59` | ✅ |
| `get_current_user(request, deps=Depends(...))` — FastAPI dependency | `security.py:62–67` | ✅ |
| Тесты: 6 кейсов | `test_security_primitives.py:18–78` | ✅ |

**Story 3: ✅ VERIFIED — 0 findings**

---

## Story 4 — FastAPI App + create_app + lifespan + CORS + middleware (IDS-02-04)

**Файлы:** [`src/core/api/asgi_app.py`](../../../../src/core/api/asgi_app.py) · [`src/core/api/dependencies.py`](../../../../src/core/api/dependencies.py) · [`tests/conftest.py`](../../../../tests/conftest.py) · [`tests/test_asgi_transport.py`](../../../../tests/test_asgi_transport.py)

| Claim | Строка | ✅/❌ |
|-------|--------|-------|
| `create_app(config: AppConfig) → FastAPI` — фабрика (interview 4.1) | `asgi_app.py:62` | ✅ |
| CORS добавляется в `create_app`, не в `_lifespan` | `asgi_app.py:72–77` | ✅ |
| `allow_origins` читается из `config.cors_allowed_origins` | `asgi_app.py:74` | ✅ |
| Empty origins фильтруются: `if o.strip()` | `asgi_app.py:74` | ✅ |
| `_lifespan` только: `get_api_dependencies()` + `configure_logging()` | `asgi_app.py:84–91` | ✅ |
| `@lru_cache(maxsize=1)` синглтон `_cached_dependencies` | `asgi_app.py:48–51` | ✅ |
| `_clear_api_dependencies_cache()` для тестов | `asgi_app.py:58–59` | ✅ |
| `conftest.py` fixture: `_clear_cache → provide_app_config → create_app` | `conftest.py:21–25` | ✅ |
| Exception handler `UnauthorizedError` → 401 + envelope | `asgi_app.py:95–105` | ✅ |
| Exception handler `ConfigError` → 500 + envelope | `asgi_app.py:107–111` | ✅ |
| HTTP middleware `runtime_exception_diagnostics` → 500 `INTERNAL_ERROR` | `asgi_app.py:114–132` | ✅ |
| Module-level: `app = create_app(provide_app_config())` | `asgi_app.py:337–338` | ✅ |
| `ApiDependencies(frozen=True)` | `dependencies.py:12` | ✅ |
| `build_api_dependencies` использует `StubBearerTokenAuth` (stub для IDS-02) | `dependencies.py:22–32` | ✅ |

### A-1 [MEDIUM] — Нет теста на CORS-заголовки в HTTP-ответе

`conftest.py:16`: `CORS_ALLOWED_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"` — ограниченный список.

Ни один тест не проверяет, что `Access-Control-Allow-Origin` присутствует в ответах при запросе с разрешённым `Origin`. Тесты `test_options_me_returns_200` и `test_options_oauth_authorize_returns_200` проверяют только статус 200, но не CORS-заголовки.

**Как закрыть:** добавить тест в `tests/test_asgi_transport.py`:

```python
def test_cors_allowed_origin_header_present(test_client: TestClient) -> None:
    response = test_client.get(
        "/health", headers={"Origin": "http://localhost:3000"}
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_disallowed_origin_not_reflected(test_client: TestClient) -> None:
    response = test_client.get(
        "/health", headers={"Origin": "http://evil.com"}
    )
    assert response.headers.get("access-control-allow-origin") != "http://evil.com"
```

**Story 4: ✅ VERIFIED — 1 finding (A-1)**

---

## Story 5 — Routes Contract + Health/Ready + Identity Stubs + OPTIONS (IDS-02-05)

**Файлы:** [`src/core/api/asgi_app.py`](../../../../src/core/api/asgi_app.py) · [`src/core/api/handlers.py`](../../../../src/core/api/handlers.py) · [`tests/test_asgi_transport.py`](../../../../tests/test_asgi_transport.py)

### Таблица маршрутов

| Route | Метод | Тип | Файл:строка | Тест | ✅/❌ |
|-------|-------|-----|-------------|------|-------|
| `/health` | GET | public | `asgi_app.py:136` | `test_health_returns_ok_envelope` | ✅ |
| `/ready` | GET | public | `asgi_app.py:143` | `test_ready_in_memory_backend` | ✅ |
| `/me` | GET | bearer | `asgi_app.py:150` | `test_me_without_auth_returns_401`, `test_me_with_bearer_returns_501_stub` | ✅ |
| `/auth/eid/start` | POST | bearer stub | `asgi_app.py:162` | route table test | ✅ |
| `/auth/eideasy/callback` | GET | public stub | `asgi_app.py:174` | route table test | ✅ |
| `/auth/authentigate/callback` | GET | public stub | `asgi_app.py:186` | route table test | ✅ |
| `/auth/mock/callback` | GET | public stub | `asgi_app.py:198` | route table test | ✅ |
| `/oauth/authorize` | GET | bearer stub | `asgi_app.py:210` | route table test | ✅ |
| `/oauth/authorize/complete` | POST | bearer stub | `asgi_app.py:223` | route table test | ✅ |
| `/oauth/token` | POST | bearer stub | `asgi_app.py:236` | route table test | ✅ |
| `/story-drafts` | POST | bearer stub | `asgi_app.py:249` | route table test | ✅ |
| `/story-drafts/{draft_id}/submit` | POST | bearer stub | `asgi_app.py:262` | route table test | ✅ |
| `/stories` | POST | bearer stub | `asgi_app.py:277` | route table test | ✅ |
| `/gpt/actions/submit-story` | POST | bearer stub | `asgi_app.py:290` | route table test | ✅ |
| OPTIONS × 9 protected paths | OPTIONS | — | `asgi_app.py:303–309` | `test_options_me_returns_200` | ✅ |

**Callback routes НЕ в `PROTECTED_OPTIONS_PATHS`** — решение M-6 (interview 2026-05-27) применено корректно. `asgi_app.py:27–37`.

**`handle_health`** → `{"data": {"status": "ok", "trace_id": ...}}`, 200 — `handlers.py:12–14` ✅

**`handle_readiness`** → `{"data": {"status": "ready"/"degraded", "db_backend", "db_ready", "checks", "trace_id"}}`, 200/503 — `handlers.py:17–26` ✅

**`_not_implemented` добавляет `next_epic` в error envelope** — `handlers.py:33–37`; тест `test_me_with_bearer_returns_501_stub` проверяет `"next_epic" in error` ✅

**`test_route_table_contains_identity_contract_paths`** проверяет все 14 обязательных путей — `test_asgi_transport.py:56–74` ✅

### A-2 [LOW] — `/ready` → 503 для supabase-backend не покрыт тестом

`dependencies.py:25`: `db_ready = db_backend == "in_memory"` — при `db_backend="supabase"` всегда `False` до EPIC-IDS-05. `test_ready_in_memory_backend` тестирует только `in_memory`. Кейс supabase → 503 не покрыт.

**Как закрыть:** добавить тест:

```python
def test_ready_supabase_backend_reports_degraded() -> None:
    _clear_api_dependencies_cache()
    config = provide_app_config({
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "supabase",
        "EID_PROVIDER": "mock",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SERVICE_ROLE": "sr",
    })
    app = create_app(config)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["data"]["db_ready"] is False
```

**Story 5: ✅ VERIFIED — 1 finding (A-2)**

---

## Верификация Epic Goal

| Критерий | Факт | Статус |
|----------|------|--------|
| `curl http://localhost:8100/health` → `{"data": {"status": "ok", ...}}` | `asgi_app.py:136`, `handlers.py:12` | ✅ |
| `curl /me` без токена → 401 `AUTHENTICATION_REQUIRED` | `security.py:14`, `asgi_app.py:95–105` | ✅ |
| `curl /me` с Bearer → 501 `NOT_IMPLEMENTED` + `next_epic` | `handlers.py:40–51` | ✅ |
| CORS из `CORS_ALLOWED_ORIGINS` env var | `asgi_app.py:74` | ✅ |
| `create_app(config)` factory (interview 4.1) | `asgi_app.py:62` | ✅ |
| Все 14 identity-route stubs зарегистрированы | `asgi_app.py:135–309`, тест строки 56–74 | ✅ |
| OPTIONS только для protected paths, не для callbacks (M-6) | `asgi_app.py:27–37` | ✅ |
| Logging: при старте `configure_logging` из `config.log_level` | `asgi_app.py:87–90` | ✅ |
| Runtime exceptions → 500 envelope + `log_runtime_exception` | `asgi_app.py:116–132` | ✅ |

---

## Приоритет доработок

| Приоритет | ID | Задача | Файл | Статус |
|-----------|-----|--------|------|--------|
| 1 | A-1 | Добавить тест `test_cors_allowed_origin_header_present` + `test_cors_disallowed_origin_not_reflected` | `tests/test_asgi_transport.py` | 🟢 Closed 2026-05-29 |
| 2 | A-2 | Добавить тест `test_ready_supabase_backend_reports_degraded` | `tests/test_asgi_transport.py` | 🟢 Closed 2026-05-29 |

Оба gap — test coverage. Функциональный код корректен.
