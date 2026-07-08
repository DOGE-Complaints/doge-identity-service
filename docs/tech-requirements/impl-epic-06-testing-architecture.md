# NFR: Testing Architecture

> ⚠️ **Reference-only (2026-06-24):** этот документ скопирован из `doge-complaints-gateway` и описывает ДРУГОЙ сервис (intake/кластеризация историй), не identity. Фактический identity-код — в `src/`; актуальные факты — в `docs/analysis/identity-backend-full-audit-2026-06-24.md` и runtime-docs. Использовать только как шаблон-референс; подлежит переписыванию под identity.

## Назначение

6-слойная тест-сюита с чёткой изоляцией. Главный инвариант: **unit и integration тесты никогда не трогают реальный Supabase**. Гарантируется `autouse` фикстурой `_block_dotenv_leakage`. CI разделён на offline (каждый push) и live integration (только `main`).

## Источник паттерна

`docs/runtime-docs/bootstrap-infrastructure/06-testing-architecture.md`

## Бизнес-контекст

Весь функциональный слой (intake, clustering, issues) должен тестироваться без внешних зависимостей. Live Supabase тесты — только на отдельном тестовом проекте, никогда на production.

## Предусловие

- Epic 01: `pyproject.toml` с `asyncio_mode = "auto"`, `pythonpath = ["src", "tests"]`, marker `live_integration`
- Epic 02–05: все сервисы реализованы (хотя бы InMemory)

## Целевые файлы

```
tests/conftest.py
tests/test_bootstrap_smoke.py
tests/test_http_transport_smoke.py
tests/test_di_singleton.py
tests/integration/supabase/__init__.py
tests/integration/supabase/test_supabase_dotenv_connectivity.py
tests/smoke/conftest.py
tests/smoke/test_local_server_smoke.py
.github/workflows/test-offline.yml
.github/workflows/integration-live.yml
```

---

## Epic Goal

`python3.11 -m pytest tests/ -q -m "not live_integration"` — все тесты проходят за < 30 секунд без сетевых вызовов. `python3.11 -m pytest -m live_integration` — пропускается локально без `.env` creds, проходит в CI с GitHub Secrets.

---

## Story 1: conftest.py — три обязательные фикстуры

### Зачем

`_block_dotenv_leakage` — центральный механизм изоляции. Без него тест, запущенный в рабочей директории с `.env` содержащим `DB_BACKEND=supabase`, попадает в реальную БД. `autouse=True` гарантирует применение к каждому тесту автоматически.

### Tasks

**Task 1.1:** Создать `tests/conftest.py`.

```python
from __future__ import annotations

import os
import pytest

from core.logging_setup import configure_logging


# ─── 1. Env isolation ────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def _block_dotenv_leakage(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent .env vars from leaking into tests (DB_BACKEND=supabase would hit real DB)."""
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.local")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "60")
    monkeypatch.setenv(
        "CLUSTER_ACTIVE_LENSES",
        "civic_domain_micro,failure_pattern_micro,institution_micro,urgency_micro,geo_cluster_micro,keyword_micro",
    )
    monkeypatch.setenv("CLUSTER_PRIMARY_LENS", "civic_domain_micro")
    monkeypatch.setenv("CLUSTER_SIGNAL_SOURCE", "canonical")
    monkeypatch.setenv("CLUSTER_TIE_BREAKER", "alpha")


# ─── 2. Session logging ───────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def _pytest_session_logging() -> None:
    """Without ASGI lifespan, tests still get predictable log levels."""
    configure_logging(
        os.environ.get("LOG_LEVEL", "INFO"),
        log_format="text",
        log_debug_dir=None,
    )


# ─── 3. Auto-tag live_integration tests ──────────────────────────────────────

def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Auto-tag tests/integration/supabase/ as live_integration."""
    marker = pytest.mark.live_integration
    for item in items:
        path = str(item.path).replace("\\", "/")
        if "/tests/integration/supabase/" in path:
            item.add_marker(marker)
```

**Важно:** Переменные в `_block_dotenv_leakage` должны совпадать с реальным проектом:
- `CLUSTER_ACTIVE_LENSES` — все 6 активных lens из `AppConfig` defaults
- `CLUSTER_PRIMARY_LENS` = `civic_domain_micro` (должен быть в ACTIVE_LENSES)
- Тесты, которым нужен не-in_memory backend, переопределяют через `monkeypatch.setenv()` в своих фикстурах (применяются после `autouse`)

### Acceptance Criteria

- `python3.11 -m pytest tests/ -q` без `.env` файла — все тесты используют `in_memory` backend
- `python3.11 -m pytest tests/ -q` с `.env` содержащим `DB_BACKEND=supabase` — тесты всё равно используют `in_memory`
- `tests/integration/supabase/*.py` автоматически получают маркер `live_integration` без декоратора
- `python3.11 -m pytest -m "not live_integration" -q` — пропускает все Supabase тесты

---

## Story 2: HTTP Transport тесты (ASGI TestClient паттерн)

### Зачем

Тестирование HTTP слоя без реального сервера: `httpx.AsyncClient` с `ASGITransport`. `_clear_api_dependencies_cache()` перед каждым тестом — иначе singleton использует env из предыдущего теста.

### Tasks

**Task 2.1:** Создать `tests/test_http_transport_smoke.py`.

```python
from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport

from core.api.asgi_app import app, _clear_api_dependencies_cache


@pytest.fixture(autouse=True)
def _reset_deps():
    """Reset DI singleton before and after each test."""
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()


async def test_health_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "ok"


async def test_ready_returns_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/ready")
    assert resp.status_code in (200, 503)
    data = resp.json()["data"]
    assert data["db_backend"] == "in_memory"
    assert data["db_ready"] is True


async def test_protected_status_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/protected/status")
    # demo mode: SERVICE_API_TOKEN not set → auth disabled
    assert resp.status_code == 200


async def test_protected_status_requires_auth_in_pilot(monkeypatch):
    monkeypatch.setenv("APP_PROFILE", "pilot")
    monkeypatch.setenv("SERVICE_API_TOKEN", "secret-token")
    _clear_api_dependencies_cache()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp_no_auth = await client.get("/protected/status")
        resp_with_auth = await client.get(
            "/protected/status",
            headers={"Authorization": "Bearer secret-token"},
        )
    assert resp_no_auth.status_code == 401
    assert resp_with_auth.status_code == 200


async def test_options_tallinn_issues_cors_preflight():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.options("/tallinn/issues")
    assert resp.status_code == 200


async def test_trace_id_propagation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health", headers={"x-trace-id": "my-custom-trace"})
    assert resp.status_code == 200
    # trace_id must appear in response body
    body = resp.json()
    assert "my-custom-trace" in str(body)


async def test_intake_stories_accepts_post():
    payload = {
        "story_id": "test-1",
        "description": "Test story",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/intake/stories", json=payload)
    assert resp.status_code in (202, 400, 422)  # accepted or validation error
```

**Task 2.2:** Создать `tests/test_bootstrap_smoke.py`.

```python
from __future__ import annotations

import pytest


def test_core_imports():
    from core.config import AppConfig, provide_app_config
    from core.api.asgi_app import app, get_api_dependencies
    from core.api.dependencies import ApiDependencies, build_api_dependencies
    assert AppConfig is not None
    assert app is not None


def test_app_config_from_env(monkeypatch):
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "http://test")
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    from core.config import provide_app_config
    config = provide_app_config()
    assert config.db_backend == "in_memory"
    assert config.db_enabled is False
    assert config.profile.name == "demo"


def test_config_fail_fast_on_invalid_backend(monkeypatch):
    from core.config import load_config_from_env, ConfigError
    monkeypatch.setenv("DB_BACKEND", "postgres")
    with pytest.raises(ConfigError):
        load_config_from_env({
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://test",
            "DB_BACKEND": "postgres",
        })
```

### Acceptance Criteria

- `python3.11 -m pytest tests/test_http_transport_smoke.py -v` — все тесты PASSED
- `python3.11 -m pytest tests/test_bootstrap_smoke.py -v` — все тесты PASSED
- Тесты не делают реальных HTTP запросов (ASGITransport работает in-process)
- `test_protected_status_requires_auth_in_pilot` проверяет что 401 возвращается корректно

---

## Story 3: Live Supabase Integration тесты

### Зачем

Verifies реальный Supabase проект: connectivity, schema, roundtrip. Запускаются только при наличии credentials — пропускаются без ошибки если creds отсутствуют.

### Tasks

**Task 3.1:** Создать `tests/integration/supabase/__init__.py` (пустой).

**Task 3.2:** Создать `tests/integration/supabase/test_supabase_dotenv_connectivity.py`.

```python
from __future__ import annotations

from pathlib import Path

import pytest


def _require_supabase_creds_from_dotenv() -> tuple[str, str]:
    """Parse .env file directly (bypasses _block_dotenv_leakage fixture)."""
    from core.config.env_file import _parse_dotenv_file
    dotenv = _parse_dotenv_file(Path(__file__).parents[3] / ".env")
    url = dotenv.get("SUPABASE_URL", "")
    key = dotenv.get("SUPABASE_SERVICE_ROLE", "")
    if not url or not key:
        pytest.skip("No Supabase creds in .env — skipping live integration test")
    return url, key


def test_supabase_connectivity():
    url, key = _require_supabase_creds_from_dotenv()
    from core.infrastructure.db_supabase import SupabaseDatabase
    db = SupabaseDatabase.from_http(url, key)
    assert db.healthcheck() is True, "Supabase connectivity check failed"


def test_supabase_tables_ready():
    url, key = _require_supabase_creds_from_dotenv()
    from core.infrastructure.db_supabase import SupabaseDatabase
    db = SupabaseDatabase.from_http(url, key)
    assert db.required_tables_ready() is True, "Required tables not found — run bootstrap SQL"


def test_supabase_columns_ready():
    url, key = _require_supabase_creds_from_dotenv()
    from core.infrastructure.db_supabase import SupabaseDatabase
    db = SupabaseDatabase.from_http(url, key)
    assert db.required_columns_ready() is True


def test_supabase_service_role_policy():
    url, key = _require_supabase_creds_from_dotenv()
    from core.infrastructure.db_supabase import SupabaseDatabase
    db = SupabaseDatabase.from_http(url, key)
    assert db.service_role_policy_probe() is True, (
        "service_role RLS policy missing — run: "
        "CREATE POLICY 'service_role_full' ON stories FOR ALL TO service_role USING (true)"
    )
```

**Task 3.3:** Создать `tests/integration/supabase/test_supabase_live_story_roundtrip.py`.

```python
from __future__ import annotations

from pathlib import Path
import pytest


def _require_supabase_creds_from_dotenv() -> tuple[str, str]:
    from core.config.env_file import _parse_dotenv_file
    dotenv = _parse_dotenv_file(Path(__file__).parents[3] / ".env")
    url = dotenv.get("SUPABASE_URL", "")
    key = dotenv.get("SUPABASE_SERVICE_ROLE", "")
    if not url or not key:
        pytest.skip("No Supabase creds in .env")
    return url, key


def test_story_write_read_roundtrip():
    """Write a story to Supabase and read it back — verifies basic CRUD."""
    url, key = _require_supabase_creds_from_dotenv()
    from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseStoryRepository
    import uuid

    db = SupabaseDatabase.from_http(url, key)
    repo = SupabaseStoryRepository(db)

    test_id = f"test-roundtrip-{uuid.uuid4()}"
    # Минимальный StoryRecord — добавить реальный тип после реализации domain/models
    # record = StoryRecord(story_id=test_id, ...)
    # repo.save_story(record)
    # retrieved = repo.get_story(test_id)
    # assert retrieved is not None
    # assert retrieved.story_id == test_id
    pytest.skip("Implement after StoryRecord is defined in domain/models.py")
```

### Acceptance Criteria

- Без `.env` с Supabase creds: все `live_integration` тесты — `SKIPPED` (не `FAILED`)
- С правильными creds: `test_supabase_connectivity` — PASSED
- `pytest.skip()` в `_require_supabase_creds_from_dotenv()` — корректный механизм пропуска
- Live тесты используют **отдельный тестовый** Supabase проект, не production

---

## Story 4: CI — два workflow

### Зачем

Offline тесты на каждый push — быстро (< 30s), без внешних зависимостей. Live integration — только на `main` или вручную, с Supabase credentials из GitHub Secrets.

### Tasks

**Task 4.1:** Создать `.github/workflows/test-offline.yml`.

```yaml
name: Tests (offline)

on:
  push:
  pull_request:

jobs:
  pytest-offline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run offline tests
        run: python -m pytest -q -m "not live_integration" --tb=short

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pytest-results
          path: "*.xml"
          if-no-files-found: ignore
```

**Task 4.2:** Создать `.github/workflows/integration-live.yml`.

```yaml
name: Tests (live Supabase integration)

on:
  push:
    branches: [main]
  workflow_dispatch:    # ← ручной запуск через GitHub UI

jobs:
  pytest-live-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run live integration tests
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_TEST_URL }}
          SUPABASE_SERVICE_ROLE: ${{ secrets.SUPABASE_TEST_SERVICE_ROLE_KEY }}
          DB_BACKEND: supabase
          APP_PROFILE: demo
          API_BASE_URL: https://test.local
        run: python -m pytest -q -m live_integration -v
```

**GitHub Secrets необходимые для live integration:**
- `SUPABASE_TEST_URL` — URL тестового Supabase проекта (отдельный от production!)
- `SUPABASE_TEST_SERVICE_ROLE_KEY` — service_role key тестового проекта

### Acceptance Criteria

- `test-offline.yml` запускается на каждый push и PR
- `integration-live.yml` запускается только при merge в `main` или через `workflow_dispatch`
- В offline workflow: нет `SUPABASE_*` secrets — все live тесты автоматически SKIP
- Offline тесты занимают < 30 секунд

---

## Story 5: Smoke тесты (живой сервер)

### Зачем

После деплоя или локально — быстрая проверка что сервер отвечает на `/health` и `/ready`. Не входят в стандартный pytest run.

### Tasks

**Task 5.1:** Создать `tests/smoke/conftest.py`.

```python
from __future__ import annotations

import os
import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "smoke: smoke tests against a live server")


@pytest.fixture(scope="session")
def gateway_url() -> str:
    url = os.environ.get("GATEWAY_URL", "http://localhost:8000")
    return url.rstrip("/")
```

**Task 5.2:** Создать `tests/smoke/test_local_server_smoke.py`.

```python
from __future__ import annotations

import httpx
import pytest


def test_health(gateway_url: str):
    resp = httpx.get(f"{gateway_url}/health", timeout=5)
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "ok"


def test_ready(gateway_url: str):
    resp = httpx.get(f"{gateway_url}/ready", timeout=5)
    assert resp.status_code in (200, 503)
    data = resp.json()["data"]
    assert "db_backend" in data
    assert "db_ready" in data


def test_tallinn_issues_list(gateway_url: str):
    resp = httpx.get(f"{gateway_url}/tallinn/issues", timeout=5)
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body
```

### Acceptance Criteria

- `GATEWAY_URL=http://localhost:8000 python3.11 -m pytest tests/smoke/ -v` — PASSED при запущенном сервере
- Smoke тесты не входят в `python3.11 -m pytest tests/ -q` (testpaths = ["tests"] без smoke, или через marker)
- `GATEWAY_URL` можно заменить Railway URL для проверки prod деплоя

---

## Команды для локальной разработки

```bash
# Стандартный run (offline, ~15-30 секунд)
python3.11 -m pytest tests/ -q --tb=short

# Только offline (явно исключить live)
python3.11 -m pytest -m "not live_integration" -q

# Только live Supabase (нужен .env с creds)
python3.11 -m pytest -m live_integration -v

# Конкретный файл
python3.11 -m pytest tests/test_http_transport_smoke.py -v

# С debug логами
LOG_LEVEL=DEBUG python3.11 -m pytest tests/test_bootstrap_smoke.py -v -s

# Быстрый smoke после изменений
python3.11 -m pytest tests/test_bootstrap_smoke.py tests/test_http_transport_smoke.py -q

# Smoke против живого сервера
GATEWAY_URL=http://localhost:8000 python3.11 -m pytest tests/smoke/ -v
```

---

## Critical Pitfalls

- Без `_block_dotenv_leakage` тесты могут попасть в реальный Supabase — данные не те, скорость упадёт, тесты падают из-за сетевых ошибок
- `asyncio_mode = "auto"` обязателен — иначе каждый `async` тест нужно декорировать `@pytest.mark.asyncio`
- `_clear_api_dependencies_cache()` нужно вызывать ДО теста — singleton создаётся при первом вызове, нужен чистый env к этому моменту
- Live integration тесты MUST использовать **отдельный тестовый** Supabase проект, не production
- `pytest.skip()` в `_require_supabase_creds_from_dotenv()` — корректный паттерн: тест SKIP (не FAIL) без creds
- `pythonpath = ["src", "tests"]` в `pyproject.toml` — критично для `import core.*` в тестах

## Верификация эпика

```bash
# 1. Все offline тесты проходят
python3.11 -m pytest tests/ -q -m "not live_integration"
# Ожидаемо: X passed in <30s

# 2. Live тесты пропускаются без creds
python3.11 -m pytest tests/ -q -m live_integration
# Ожидаемо: X skipped (no Supabase creds)

# 3. _block_dotenv_leakage работает
python3.11 -c "
import pytest, sys
# Если этот тест запустить с DB_BACKEND=supabase в env — он должен увидеть in_memory
print('Check manually: run pytest with DB_BACKEND=supabase in .env')
"

# 4. CI offline
# Push any commit → .github/workflows/test-offline.yml должен запуститься и пройти
```
