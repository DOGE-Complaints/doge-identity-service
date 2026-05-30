# NFR: Dependency Injection

## Назначение

Manual singleton DI без IoC контейнера: `ApiDependencies(frozen=True)` dataclass содержит все сервисы, `build_api_dependencies()` строит его один раз, `@lru_cache(maxsize=1)` делает singleton per process, FastAPI роуты получают его через `Depends(get_api_dependencies)`.

## Источник паттерна

`docs/runtime-docs/bootstrap-infrastructure/02-dependency-injection.md`

## Бизнес-контекст

DI контейнер — точка интеграции config, persistence backend, и сервисов. Здесь же — db healthcheck при старте для Supabase backend.

## Предусловие

- Epic 01 выполнен: `AppConfig`, `provide_app_config()`
- Epic 02 выполнен: `asgi_app.py` с `get_api_dependencies()`, `ServiceTokenAuth`

## Целевые файлы

```
src/core/api/dependencies.py
src/core/api/asgi_app.py    (обновление: импорт build_api_dependencies)
```

---

## Epic Goal

При первом HTTP-запросе (или при lifespan startup) `_cached_dependencies()` создаёт `ApiDependencies` singleton. Все последующие запросы получают тот же объект. В тестах `_clear_api_dependencies_cache()` позволяет пересоздать singleton с другим env.

---

## Story 1: ApiDependencies dataclass

### Зачем

`ApiDependencies` — единственный контейнер всех сервисов, доступных HTTP слою. `frozen=True` предотвращает случайную мутацию shared state в request handlers.

### Tasks

**Task 1.1:** Создать `src/core/api/dependencies.py`.

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core.api.security import ServiceTokenAuth, build_service_auth_from_env
from core.config import AppConfig, provide_app_config

if TYPE_CHECKING:
    # Избегаем circular import: dependencies -> service_factory -> config
    # Реальные типы добавляются после реализации Epic 04
    pass


@dataclass(frozen=True)
class ApiDependencies:
    # ── Config ────────────────────────────────────────────────────────
    config: AppConfig

    # ── Auth ──────────────────────────────────────────────────────────
    service_auth: ServiceTokenAuth

    # ── DB state ──────────────────────────────────────────────────────
    db_backend: str           # "in_memory" | "sqlite" | "supabase"
    db_ready: bool            # False если Supabase healthcheck упал при старте
    db_checks: dict[str, bool]  # {"connectivity": True, "schema": True, ...}

    # ── Services (добавляются по мере реализации Epic 04 и выше) ──────
    # health_service: HealthService           # добавить в Epic 04
    # story_intake_service: StoryIntakeService # добавить в Epic 04
    # story_cluster_orchestrator: StoryClusterOrchestrator  # добавить в Epic 04
    # issue_create_service: IssueCreateService  # добавить в Epic 04
    # issue_projection_read_store: IssueProjectionReadStore  # добавить в Epic 04


# Backward-compatibility alias (используется в тестах и handlers)
HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    """
    Build the DI container. Called once per process via lru_cache.

    Steps:
    1. provide_service_factory() — reads DB_BACKEND from env, selects backend
    2. Supabase healthchecks (if DB_BACKEND=supabase)
    3. Build ApiDependencies with all services

    NOTE: service_factory integration added in Epic 04.
    Until then, uses provide_app_config() directly.
    """
    config = provide_app_config()
    db_backend = config.db_backend
    db_checks: dict[str, bool] = {}
    db_ready = True

    if db_backend == "supabase":
        # Supabase healthchecks добавляются в Epic 05
        # from core.infrastructure.db_supabase import SupabaseDatabase
        # health_db = SupabaseDatabase.from_http(config.supabase_url, config.supabase_service_role)
        # db_checks = {
        #     "connectivity": health_db.healthcheck(),
        #     "schema": health_db.required_tables_ready(),
        #     "columns": health_db.required_columns_ready(),
        #     "columns_v2": health_db.required_stories_intake_v2_columns_ready(),
        #     "policy_probe": health_db.service_role_policy_probe(),
        # }
        # db_ready = all(db_checks.values())
        pass

    return ApiDependencies(
        config=config,
        service_auth=build_service_auth_from_env(token=config.service_api_token),
        db_backend=db_backend,
        db_ready=db_ready,
        db_checks=db_checks,
    )
```

### Acceptance Criteria

- `build_api_dependencies()` возвращает `ApiDependencies` без ошибок при `DB_BACKEND=in_memory`
- `deps.config.db_backend == "in_memory"` при `DB_BACKEND=in_memory` в env
- `deps.service_auth` — `ServiceTokenAuth` с корректным токеном из `SERVICE_API_TOKEN`
- `ApiDependencies` не мутабельна: `deps.db_backend = "x"` бросает `FrozenInstanceError`
- `HandlerDependencies is ApiDependencies` — True (это алиас)

---

## Story 2: lru_cache Singleton и интеграция в asgi_app.py

### Зачем

`@lru_cache(maxsize=1)` гарантирует: `build_api_dependencies()` вызывается ровно один раз за время жизни процесса. `_clear_api_dependencies_cache()` нужен только в тестах — позволяет пересоздать singleton с новым env после `monkeypatch.setenv()`.

### Tasks

**Task 2.1:** Обновить `src/core/api/asgi_app.py` — добавить импорт `build_api_dependencies` и убедиться что singleton паттерн реализован корректно.

Убедиться что в `asgi_app.py` присутствует:

```python
from functools import lru_cache
from core.api.dependencies import ApiDependencies, build_api_dependencies

@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    return build_api_dependencies()

def _clear_api_dependencies_cache() -> None:
    """Used in tests to force re-creation of the DI singleton with a fresh env."""
    _cached_dependencies.cache_clear()

def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()
```

**Task 2.2:** Убедиться что lifespan вызывает `get_api_dependencies()` при startup.

```python
@asynccontextmanager
async def _lifespan(_: FastAPI):
    deps = get_api_dependencies()   # ← форсирует создание singleton ДО первого запроса
    configure_logging(
        deps.config.log_level,
        log_format=deps.config.log_format,
        log_debug_dir=deps.config.log_debug_dir,
    )
    try:
        yield
    finally:
        pass
```

**Task 2.3:** Написать smoke-тест для DI singleton.

Создать `tests/test_di_singleton.py`:

```python
import os
import pytest
from httpx import AsyncClient, ASGITransport
from core.api.asgi_app import app, _clear_api_dependencies_cache, get_api_dependencies


@pytest.fixture(autouse=True)
def _reset_deps():
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()


async def test_singleton_is_same_object():
    deps1 = get_api_dependencies()
    deps2 = get_api_dependencies()
    assert deps1 is deps2, "DI singleton must return the same object"


async def test_health_uses_singleton():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r1 = await client.get("/health")
        r2 = await client.get("/health")
    assert r1.status_code == 200
    assert r2.status_code == 200


async def test_clear_cache_allows_recreation(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    _clear_api_dependencies_cache()
    deps = get_api_dependencies()
    assert deps.config.log_level == "DEBUG"
```

### Acceptance Criteria

- `get_api_dependencies() is get_api_dependencies()` — True (один объект)
- После `_clear_api_dependencies_cache()` следующий вызов `get_api_dependencies()` создаёт новый объект
- `_clear_api_dependencies_cache()` после изменения env через monkeypatch — новый `ApiDependencies` содержит изменённые значения
- Два параллельных HTTP запроса получают один и тот же `ApiDependencies` объект

---

## Story 3: Расширение ApiDependencies для сервисов (Epic 04 hook)

### Зачем

После реализации Epic 04 (SOA Service Factory), `ApiDependencies` должен содержать реальные сервисы. Этот story описывает точный контракт расширения.

### Tasks

**Task 3.1:** После реализации Epic 04, обновить `ApiDependencies` в `dependencies.py`.

Добавить поля (раскомментировать):

```python
from core.application.services import (
    HealthService,
    StoryIntakeService,
    StoryClusterOrchestrator,
    IssueCreateService,
)
from core.domain.projections import IssueProjectionReadStore

@dataclass(frozen=True)
class ApiDependencies:
    # ... существующие поля ...

    # Services (раскомментировать после Epic 04)
    health_service: HealthService
    story_intake_service: StoryIntakeService
    story_cluster_orchestrator: StoryClusterOrchestrator
    issue_create_service: IssueCreateService
    issue_projection_read_store: IssueProjectionReadStore
```

**Task 3.2:** Обновить `build_api_dependencies()` — использовать `provide_service_factory()`.

```python
def build_api_dependencies() -> ApiDependencies:
    from core.infrastructure.providers import provide_service_factory
    service_factory = provide_service_factory()
    config = service_factory.config
    db_backend = config.db_backend
    db_checks: dict[str, bool] = {}
    db_ready = True

    if db_backend == "supabase":
        from core.infrastructure.db_supabase import SupabaseDatabase
        health_db = SupabaseDatabase.from_http(
            supabase_url=config.supabase_url,
            service_role_key=config.supabase_service_role,
        )
        db_checks = {
            "connectivity": health_db.healthcheck(),
            "schema": health_db.required_tables_ready(),
            "columns": health_db.required_columns_ready(),
            "columns_v2": health_db.required_stories_intake_v2_columns_ready(),
            "policy_probe": health_db.service_role_policy_probe(),
        }
        db_ready = all(db_checks.values())

    return ApiDependencies(
        config=config,
        service_auth=build_service_auth_from_env(token=config.service_api_token),
        db_backend=db_backend,
        db_ready=db_ready,
        db_checks=db_checks,
        health_service=service_factory.get_health_service(),
        story_intake_service=service_factory.get_story_intake_service(),
        story_cluster_orchestrator=service_factory.get_story_cluster_orchestrator(),
        issue_create_service=service_factory.get_issue_create_service(),
        issue_projection_read_store=service_factory.get_issue_projection_read_store(),
    )
```

### Acceptance Criteria

- После Epic 04: `deps.story_intake_service` не None
- После Epic 05: при `DB_BACKEND=supabase`, `deps.db_checks` содержит 5 ключей
- `deps.db_ready` = True только если все 5 проверок прошли
- `GET /ready` с `DB_BACKEND=supabase` и упавшей connectivity → HTTP 503 с `"status": "degraded"`

---

## Critical Pitfalls

- `lru_cache` кешируется на всё время процесса — при тестах нужно вызывать `_clear_api_dependencies_cache()` ДО первого теста с другим env
- Если lifespan НЕ вызывает `get_api_dependencies()` при старте — DI инициализируется при первом запросе (медленнее, логи startup не появятся)
- `frozen=True` на dataclass предотвращает мутацию сервисов — не убирать
- Не добавлять mutable state в `ApiDependencies` — это shared singleton
- `HandlerDependencies = ApiDependencies` — backward-compatibility alias, не удалять

## Верификация эпика

```bash
# 1. DI создаётся без ошибок
python3.11 -c "
import os
os.environ['APP_PROFILE'] = 'demo'
os.environ['API_BASE_URL'] = 'http://test'
os.environ['DB_BACKEND'] = 'in_memory'
from core.api.dependencies import build_api_dependencies
deps = build_api_dependencies()
print('db_backend:', deps.db_backend)
print('db_ready:', deps.db_ready)
print('OK')
"

# 2. Singleton тест
python3.11 -m pytest tests/test_di_singleton.py -v

# 3. Health через HTTP
python3.11 -m pytest tests/test_http_transport_smoke.py -v -k health
```
