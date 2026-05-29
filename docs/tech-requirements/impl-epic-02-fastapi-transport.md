# NFR: FastAPI Transport Layer

## Назначение

HTTP transport слой: FastAPI приложение с lifespan, CORS middleware, HTTP exception handlers, trace_id propagation, response envelope и полный список роутов. Никакой бизнес-логики — только routing, парсинг запросов, вызов handlers.

## Источник паттерна

`docs/runtime-docs/bootstrap-infrastructure/01-fastapi-transport.md`

## Бизнес-контекст

`docs/requirements/` — endpoint-ы `/intake/stories`, `/tallinn/issues`, `/health`, `/ready`, `/protected/status`.

## Предусловие

Epic 01 выполнен: `core.config.AppConfig`, `provide_app_config()`, `pyproject.toml` с fastapi/uvicorn.

## Целевые файлы

```
src/core/api/__init__.py
src/core/api/asgi_app.py
src/core/api/envelope.py
src/core/api/security.py
src/core/api/idempotency.py
src/core/api/handlers.py
src/core/logging_setup.py
```

---

## Epic Goal

`GET /health` возвращает `{"data": {"status": "ok"}}` с HTTP 200. `POST /intake/stories` с невалидным телом возвращает `{"error": {"code": "...", "trace_id": "..."}}` с HTTP 4xx. Trace ID propagation работает через заголовок `x-trace-id`.

---

## Story 1: Response Envelope и Error Types

### Зачем

Единый формат всех ответов API — `{"data": {...}}` для успешных, `{"error": {"code": "...", "trace_id": "..."}}` для ошибок. Клиенты (Custom GPT, spa-app) могут всегда ожидать один и тот же верхнеуровневый формат.

### Tasks

**Task 1.1:** Создать `src/core/api/envelope.py`.

```python
from __future__ import annotations
import uuid


def build_success_envelope(data: dict) -> dict:
    return {"data": data}


def build_error_envelope(
    code: str,
    message: str,
    trace_id: str | None = None,
    status_code: int = 400,
) -> dict:
    err: dict = {"code": code, "message": message}
    if trace_id:
        err["trace_id"] = trace_id
    return {"error": err}


def ensure_trace_id(incoming: str | None) -> str:
    if incoming and incoming.strip():
        return incoming.strip()
    return str(uuid.uuid4())
```

**Task 1.2:** Создать `src/core/api/security.py`.

```python
from __future__ import annotations
from typing import Mapping


class UnauthorizedError(Exception):
    def __init__(self, message: str = "Authentication required"):
        self.message = message
        super().__init__(message)


class ServiceTokenAuth:
    def __init__(self, token: str | None):
        self._token = token

    @classmethod
    def disabled(cls) -> "ServiceTokenAuth":
        return cls(token=None)

    def require(self, headers: Mapping[str, str]) -> None:
        if self._token is None:
            return  # auth disabled — demo mode
        auth_header = headers.get("authorization", "") or headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedError("Bearer token required")
        provided = auth_header.removeprefix("Bearer ").strip()
        if provided != self._token:
            raise UnauthorizedError("Invalid token")


def build_service_auth_from_env(token: str | None = None) -> ServiceTokenAuth:
    return ServiceTokenAuth(token=token)
```

**Task 1.3:** Создать `src/core/api/idempotency.py`.

```python
from __future__ import annotations
from typing import Mapping


def resolve_idempotency_key(headers: Mapping[str, str]) -> str | None:
    return (
        headers.get("idempotency-key")
        or headers.get("Idempotency-Key")
        or None
    )
```

### Acceptance Criteria

- `build_error_envelope("NOT_FOUND", "not found", trace_id="abc")` == `{"error": {"code": "NOT_FOUND", "message": "not found", "trace_id": "abc"}}`
- `build_success_envelope({"status": "ok"})` == `{"data": {"status": "ok"}}`
- `ServiceTokenAuth(token="secret").require({"authorization": "Bearer wrong"})` бросает `UnauthorizedError`
- `ServiceTokenAuth.disabled().require({})` не бросает исключений

---

## Story 2: Logging Setup

### Зачем

Тесты запускаются без ASGI lifespan — логирование не инициализируется автоматически. `configure_logging()` должен быть вызываемым напрямую (в lifespan и в `_pytest_session_logging` fixture).

### Tasks

**Task 2.1:** Создать `src/core/logging_setup.py`.

```python
from __future__ import annotations
import logging
import sys
from pathlib import Path


def configure_logging(
    log_level: str,
    log_format: str = "text",
    log_debug_dir: str | None = None,
) -> None:
    level = getattr(logging, log_level.upper(), logging.INFO)
    if log_format == "json":
        fmt = '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "msg": %(message)s}'
    else:
        fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(
        level=level,
        format=fmt,
        stream=sys.stdout,
        force=True,
    )
    if log_debug_dir:
        Path(log_debug_dir).mkdir(parents=True, exist_ok=True)


def log_runtime_exception(
    exc: Exception,
    *,
    trace_id: str | None,
    path: str,
) -> None:
    logger = logging.getLogger("core.runtime")
    logger.error(
        "unhandled_exception path=%s trace_id=%s exc=%r",
        path,
        trace_id,
        exc,
    )
```

### Acceptance Criteria

- `configure_logging("DEBUG")` устанавливает уровень DEBUG для root logger
- `configure_logging("INFO", log_format="json")` не бросает исключений
- `log_runtime_exception(ValueError("test"), trace_id="abc", path="/test")` — логирует ошибку без исключений

---

## Story 3: FastAPI App, Lifespan, CORS, Middleware

### Зачем

`asgi_app.py` — единственная точка входа ASGI. Lifespan инициализирует DI singleton при старте (не при первом запросе). CORS middleware — для доступа из браузера (spa-app). HTTP middleware логирует необработанные исключения с trace_id.

### Tasks

**Task 3.1:** Создать `src/core/api/handlers.py` с заглушками (реальные обработчики добавляются в других эпиках, здесь — контракт).

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.api.dependencies import ApiDependencies


def handle_health(deps: "ApiDependencies", *, trace_id: str) -> tuple[dict, int]:
    return {"data": {"status": "ok", "trace_id": trace_id}}, 200


def handle_readiness(deps: "ApiDependencies", *, trace_id: str) -> tuple[dict, int]:
    ready = deps.db_ready
    checks = deps.db_checks
    return {
        "data": {
            "status": "ready" if ready else "degraded",
            "db_backend": deps.db_backend,
            "db_ready": ready,
            "checks": checks,
            "trace_id": trace_id,
        }
    }, 200 if ready else 503


def handle_protected_status(deps: "ApiDependencies", *, trace_id: str) -> tuple[dict, int]:
    return {"data": {"status": "ok", "profile": deps.config.profile.name}}, 200


def handle_metrics(deps: "ApiDependencies", *, trace_id: str) -> tuple[dict, int]:
    return {"data": {"metrics": {}}}, 200


def handle_story_intake(
    deps: "ApiDependencies",
    *,
    payload: dict,
    idempotency_key: str | None,
    trace_id: str,
) -> tuple[dict, int]:
    # Stub — реализуется при подключении StoryIntakeService
    return {"data": {"story_id": "stub", "trace_id": trace_id}}, 202


def handle_tallinn_issues_list(
    deps: "ApiDependencies",
    *,
    status: str | None,
    trace_id: str,
) -> tuple[dict, int]:
    return {"data": [], "trace_id": trace_id}, 200


def handle_tallinn_issue_get(
    deps: "ApiDependencies",
    *,
    issue_id: str,
    trace_id: str,
) -> tuple[dict, int]:
    return {"error": {"code": "NOT_FOUND", "trace_id": trace_id}}, 404


def handle_tallinn_issue_create(
    deps: "ApiDependencies",
    *,
    payload: dict,
    trace_id: str,
) -> tuple[dict, int]:
    return {"data": {"issue_id": "stub", "trace_id": trace_id}}, 201
```

**Task 3.2:** Создать `src/core/api/asgi_app.py`.

```python
from __future__ import annotations

import json
import os
import signal
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any

import uvicorn
from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from core.api.dependencies import ApiDependencies, build_api_dependencies
from core.api.envelope import build_error_envelope, ensure_trace_id
from core.api.idempotency import resolve_idempotency_key
from core.api.handlers import (
    handle_health,
    handle_metrics,
    handle_protected_status,
    handle_readiness,
    handle_story_intake,
    handle_tallinn_issue_create,
    handle_tallinn_issue_get,
    handle_tallinn_issues_list,
)
from core.api.security import UnauthorizedError
from core.config import ConfigError
from core.logging_setup import log_runtime_exception, configure_logging

PUBLIC_ROUTES: tuple[str, ...] = (
    "/health",
    "/ready",
    "/demo/auth-page",
    "/intake/stories",
    "/tallinn/issues",
)
PROTECTED_ROUTES: tuple[str, ...] = ("/protected/status", "/metrics")


# ─── Singleton ───────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    return build_api_dependencies()


def _clear_api_dependencies_cache() -> None:
    """Used in tests to force re-creation of the DI singleton."""
    _cached_dependencies.cache_clear()


def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()


# ─── Lifespan ────────────────────────────────────────────────────────────────

@asynccontextmanager
async def _lifespan(_: FastAPI):
    deps = get_api_dependencies()
    configure_logging(
        deps.config.log_level,
        log_format=deps.config.log_format,
        log_debug_dir=deps.config.log_debug_dir,
    )
    # ClusterCronJob starts here (added in Epic 04)
    try:
        yield
    finally:
        pass  # ClusterCronJob.stop() goes here


# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="doge-complaints-gateway", version="0.1.0", lifespan=_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-trace-id", "authorization"],
)


@app.middleware("http")
async def runtime_exception_diagnostics(request: Request, call_next: Any) -> Any:
    trace_id = _read_trace_id(request)
    try:
        return await call_next(request)
    except Exception as exc:
        log_runtime_exception(exc, trace_id=trace_id, path=request.url.path)
        raise


@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    trace_id = _read_trace_id(request)
    return JSONResponse(
        content=build_error_envelope("UNAUTHORIZED", exc.message, trace_id=trace_id),
        status_code=401,
    )


@app.exception_handler(ConfigError)
async def config_error_handler(request: Request, exc: ConfigError) -> JSONResponse:
    trace_id = _read_trace_id(request)
    return JSONResponse(
        content=build_error_envelope("CONFIG_ERROR", str(exc), trace_id=trace_id),
        status_code=500,
    )


# ─── Auth dependency ─────────────────────────────────────────────────────────

def require_service_auth(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> None:
    deps.service_auth.require(dict(request.headers.items()))


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/health")
async def health(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_health(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/ready")
async def ready(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_readiness(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/protected/status", dependencies=[Depends(require_service_auth)])
async def protected_status(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_protected_status(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/metrics", dependencies=[Depends(require_service_auth)])
async def metrics(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_metrics(deps, trace_id=_read_trace_id(request))
    return JSONResponse(content=payload, status_code=status_code)


@app.options("/tallinn/issues")
async def tallinn_issues_options() -> Response:
    return Response(status_code=200)


@app.options("/tallinn/issues/{issue_id}")
async def tallinn_issue_options(issue_id: str) -> Response:
    return Response(status_code=200)


@app.get("/tallinn/issues")
async def tallinn_issues_list(
    request: Request,
    status: str | None = Query(default=None),
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_tallinn_issues_list(
        deps, status=status, trace_id=_read_trace_id(request)
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.get("/tallinn/issues/{issue_id}")
async def tallinn_issue_get(
    issue_id: str,
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    payload, status_code = handle_tallinn_issue_get(
        deps, issue_id=issue_id, trace_id=_read_trace_id(request)
    )
    return JSONResponse(content=payload, status_code=status_code)


@app.post("/tallinn/issues", dependencies=[Depends(require_service_auth)])
async def tallinn_issue_create(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    raw_body = await request.body()
    payload = json.loads(raw_body) if raw_body else {}
    envelope, status_code = handle_tallinn_issue_create(
        deps, payload=payload, trace_id=_read_trace_id(request)
    )
    return JSONResponse(content=envelope, status_code=status_code)


@app.post("/intake/stories")
async def intake_stories(
    request: Request,
    deps: ApiDependencies = Depends(get_api_dependencies),
) -> JSONResponse:
    raw_body = await request.body()
    payload = json.loads(raw_body) if raw_body else {}
    idempotency_key = resolve_idempotency_key(dict(request.headers))
    envelope, status_code = handle_story_intake(
        deps,
        payload=payload,
        idempotency_key=idempotency_key,
        trace_id=_read_trace_id(request),
    )
    return JSONResponse(content=envelope, status_code=status_code)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _read_trace_id(request: Request) -> str:
    return ensure_trace_id(request.headers.get("x-trace-id"))


# ─── Entry point ─────────────────────────────────────────────────────────────

def run_asgi_server(*, host: str | None = None, port: int | None = None) -> None:
    resolved_host = host or os.getenv("HOST", "127.0.0.1")
    resolved_port = port if port is not None else int(os.getenv("PORT", "8000"))
    uvicorn.run("core.api.asgi_app:app", host=resolved_host, port=resolved_port)


if __name__ == "__main__":
    run_asgi_server()
```

### Acceptance Criteria

- `GET /health` → `{"data": {"status": "ok"}}` HTTP 200
- `GET /ready` → `{"data": {"status": "ready"|"degraded", "db_backend": "...", ...}}` HTTP 200/503
- `GET /protected/status` без Authorization → HTTP 401 с `{"error": {"code": "UNAUTHORIZED"}}`
- `GET /protected/status` с `Authorization: Bearer valid-token` → HTTP 200
- `OPTIONS /tallinn/issues` → HTTP 200 (CORS preflight)
- Заголовок `x-trace-id: my-trace` проброшен в ответ как `trace_id` в envelope

---

## Story 4: Полный список роутов (финальный контракт)

### Зачем

Документирует все 13 роутов и их характеристики — чтобы агент, добавляющий бизнес-логику, не создавал новые маршруты с другими путями.

### Routes Contract

| Method | Path | Auth | Handler | Status |
|--------|------|------|---------|--------|
| GET | `/health` | public | `handle_health` | 200 |
| GET | `/ready` | public | `handle_readiness` | 200/503 |
| GET | `/protected/status` | Bearer | `handle_protected_status` | 200 |
| GET | `/metrics` | Bearer | `handle_metrics` | 200 |
| OPTIONS | `/tallinn/issues` | public | Response(200) | 200 |
| OPTIONS | `/tallinn/issues/{issue_id}` | public | Response(200) | 200 |
| GET | `/tallinn/issues` | public | `handle_tallinn_issues_list` | 200 |
| GET | `/tallinn/issues/{issue_id}` | public | `handle_tallinn_issue_get` | 200/404 |
| POST | `/tallinn/issues` | Bearer | `handle_tallinn_issue_create` | 201 |
| POST | `/intake/stories` | public | `handle_story_intake` | 202/400/409 |

**Инвариант:** `asgi_app.py` не содержит бизнес-логику. Любая логика — в `handlers.py`.

### Acceptance Criteria

- Все указанные роуты доступны (проверяется через TestClient)
- `POST /intake/stories` без тела → HTTP 400 (невалидный JSON) или HTTP 422
- Все защищённые роуты возвращают 401 без корректного Bearer token

---

## Critical Pitfalls

- `host=127.0.0.1` недоступен снаружи контейнера — для Railway/Docker `0.0.0.0`
- Lifespan инициализирует DI singleton — без него первый запрос медленнее + startup логи не появятся
- `_clear_api_dependencies_cache()` нужен в тестах — без него singleton использует env из предыдущего теста
- `OPTIONS` роуты нужно добавлять явно — FastAPI не создаёт их автоматически
- Не добавлять бизнес-логику в `asgi_app.py` — только routing, middleware, exception handlers

## Верификация эпика

```bash
# 1. Сервер стартует
python -m uvicorn --app-dir src core.api.asgi_app:app --host 127.0.0.1 --port 8000 &
sleep 2

# 2. Health check
curl -s http://localhost:8000/health | python3 -m json.tool
# Ожидаемо: {"data": {"status": "ok"}}

# 3. Ready check
curl -s http://localhost:8000/ready | python3 -m json.tool

# 4. Unauthorized
curl -s http://localhost:8000/protected/status | python3 -m json.tool
# Ожидаемо: {"error": {"code": "UNAUTHORIZED"}}

# 5. Pytest HTTP тесты
python3.11 -m pytest tests/test_http_transport_smoke.py -v

kill %1
```
