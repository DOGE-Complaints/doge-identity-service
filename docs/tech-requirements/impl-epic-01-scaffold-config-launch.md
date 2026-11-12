# NFR: Scaffold, Config и Launch

> ⚠️ **Reference-only (2026-06-24):** этот документ скопирован из `doge-complaints-gateway` и описывает ДРУГОЙ сервис (intake/кластеризация историй), не identity. Фактический identity-код — в `src/`; актуальные факты — в `docs/analysis/identity-backend-full-audit-2026-06-24.md` и runtime-docs. Использовать только как шаблон-референс; подлежит переписыванию под identity.

## Назначение

Фундамент проекта: структура пакета, конфигурация зависимостей, immutable AppConfig, кастомный dotenv без сторонних библиотек, Makefile для запуска и Railway деплой-конфиг.

## Источник паттерна

`docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md`

## Бизнес-контекст

`docs/requirements/` — все функциональные требования опираются на этот фундамент. Без рабочего scaffold и config ни один следующий эпик не может быть реализован.

## Предусловие

Нет. Это первый эпик — выполняется с нуля.

## Целевые файлы

```
src/core/__init__.py
src/core/config/__init__.py
src/core/config/schema.py
src/core/config/env_file.py
src/core/config/providers.py
pyproject.toml
Makefile
railpack.json
.env.example
```

---

## Epic Goal

Запущенный uvicorn сервер с правильно загруженным `AppConfig` из `.env`. `make serve` поднимает сервер, логи показывают `db_backend=in_memory` (или `supabase`). `make check-env` распечатывает переменные.

---

## Story 1: Инициализация пакета и зависимостей

### Зачем

`pyproject.toml` определяет как Python находит `core.*` модули и какие зависимости устанавливать. Без корректного `[tool.setuptools.packages.find]` и `pythonpath` в pytest — `ModuleNotFoundError` на каждом шаге.

### Tasks

**Task 1.1:** Создать директории пакета.

```
mkdir -p src/core/api
mkdir -p src/core/config
mkdir -p src/core/domain
mkdir -p src/core/application
mkdir -p src/core/infrastructure
mkdir -p tests/integration/supabase
mkdir -p tests/smoke
mkdir -p supabase/bootstrap
mkdir -p supabase/migrations
touch src/core/__init__.py
touch src/core/config/__init__.py
touch src/core/api/__init__.py
touch src/core/domain/__init__.py
touch src/core/application/__init__.py
touch src/core/infrastructure/__init__.py
```

**Task 1.2:** Создать `pyproject.toml`.

Точные версии зависимостей (проверены в реальном проекте):

```toml
[build-system]
requires = ["setuptools>=70.0.0"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "doge-complaints-gateway"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "psycopg[binary]>=3.2.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src", "tests"]
testpaths = ["tests"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
markers = [
    "live_integration: tests requiring SUPABASE_TEST_URL and live Supabase project",
]
```

`pythonpath = ["src", "tests"]` — критично: позволяет `import core.*` в тестах без editable install.

**Task 1.3:** Установить зависимости.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
```

В zsh `.[dev]` нужно оборачивать в кавычки.

### Acceptance Criteria

- `python -c "import core"` выполняется без ошибок
- `python -m pytest --collect-only` не выдаёт `ModuleNotFoundError`
- `python -m pytest --co -q` показывает `no tests ran` (тесты ещё не написаны) без импортных ошибок

---

## Story 2: AppConfig — immutable конфигурация

### Зачем

`AppConfig` — единственный источник истины о конфигурации сервиса. `frozen=True` гарантирует что никакой код не может изменить config после старта. Fail-fast при невалидных переменных — сервер не стартует с неверной конфигурацией.

### Tasks

**Task 2.1:** Создать `src/core/config/schema.py`.

```python
from __future__ import annotations

from dataclasses import dataclass
from os import environ
from typing import Mapping


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class FeatureFlags:
    wallet_adapter: bool = False
    blockchain_adapter: bool = False
    tokenization_pipeline: bool = False


@dataclass(frozen=True)
class DeploymentProfile:
    name: str  # "demo" | "pilot"

    @property
    def is_pilot(self) -> bool:
        return self.name == "pilot"


@dataclass(frozen=True)
class AppConfig:
    profile: DeploymentProfile
    api_base_url: str
    request_timeout_s: int
    flags: FeatureFlags
    log_level: str
    log_debug_dir: str | None
    log_format: str
    db_backend: str                     # "in_memory" | "sqlite" | "supabase"
    db_enabled: bool                    # True если db_backend != "in_memory"
    database_url: str | None            # sqlite:///path/to/db
    supabase_url: str | None
    supabase_service_role: str | None
    cluster_min_size: int
    cluster_readiness_threshold: int
    cluster_active_lenses: tuple[str, ...]
    cluster_primary_lens: str
    cluster_signal_source: str
    cluster_id_algorithm: str
    cluster_geo_filter: str
    cluster_geo_scope: str | None
    cluster_tie_breaker: str
    cluster_type_resolution: str
    cluster_cron_interval_s: int
    cluster_cron_enabled: bool
    service_api_token: str | None


def _get_value(source: Mapping[str, str], key: str, default: str | None = None) -> str:
    val = source.get(key, default or "")
    return val


def _require(source: Mapping[str, str], key: str) -> str:
    val = source.get(key, "")
    if not val:
        raise ConfigError(f"Required env var {key!r} is missing or empty")
    return val


def _parse_profile(raw: str) -> DeploymentProfile:
    name = raw.strip().lower() or "demo"
    if name not in ("demo", "pilot"):
        raise ConfigError(f"APP_PROFILE must be 'demo' or 'pilot', got {raw!r}")
    return DeploymentProfile(name=name)


def _parse_bool(raw: str) -> bool:
    return raw.strip().lower() in ("true", "1", "yes")


def _parse_lenses(raw: str) -> tuple[str, ...]:
    return tuple(x.strip() for x in raw.split(",") if x.strip())


def load_config_from_env(env: Mapping[str, str] | None = None) -> AppConfig:
    source = env or environ
    profile = _parse_profile(_get_value(source, "APP_PROFILE", "demo"))
    db_backend = _get_value(source, "DB_BACKEND", "in_memory")

    if db_backend not in ("in_memory", "sqlite", "supabase"):
        raise ConfigError(f"DB_BACKEND must be in_memory|sqlite|supabase, got {db_backend!r}")

    database_url = source.get("DATABASE_URL") or None
    supabase_url = source.get("SUPABASE_URL") or None
    supabase_service_role = source.get("SUPABASE_SERVICE_ROLE") or None

    # backend compatibility rules — fail-fast
    if db_backend == "sqlite" and not database_url:
        raise ConfigError("DB_BACKEND=sqlite requires DATABASE_URL=sqlite:///path/to/db.sqlite")
    if db_backend == "supabase" and (not supabase_url or not supabase_service_role):
        raise ConfigError("DB_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE")

    active_lenses_raw = _get_value(
        source,
        "CLUSTER_ACTIVE_LENSES",
        "civic_domain_micro,failure_pattern_micro,institution_micro,urgency_micro,geo_cluster_micro,keyword_micro",
    )
    active_lenses = _parse_lenses(active_lenses_raw)
    primary_lens = _get_value(source, "CLUSTER_PRIMARY_LENS", "civic_domain_micro")
    if primary_lens not in active_lenses:
        raise ConfigError(f"CLUSTER_PRIMARY_LENS={primary_lens!r} must be in CLUSTER_ACTIVE_LENSES")

    return AppConfig(
        profile=profile,
        api_base_url=_require(source, "API_BASE_URL"),
        request_timeout_s=int(_get_value(source, "REQUEST_TIMEOUT_S", "15")),
        flags=FeatureFlags(
            wallet_adapter=_parse_bool(source.get("FF_WALLET_ADAPTER", "")),
            blockchain_adapter=_parse_bool(source.get("FF_BLOCKCHAIN_ADAPTER", "")),
            tokenization_pipeline=_parse_bool(source.get("FF_TOKENIZATION_PIPELINE", "")),
        ),
        log_level=_get_value(source, "LOG_LEVEL", "INFO").upper(),
        log_debug_dir=source.get("LOG_DEBUG_DIR") or None,
        log_format=_get_value(source, "LOG_FORMAT", "text"),
        db_backend=db_backend,
        db_enabled=(db_backend != "in_memory"),
        database_url=database_url,
        supabase_url=supabase_url,
        supabase_service_role=supabase_service_role,
        cluster_min_size=int(_get_value(source, "CLUSTER_MIN_SIZE", "5")),
        cluster_readiness_threshold=int(_get_value(source, "CLUSTER_READINESS_THRESHOLD", "60")),
        cluster_active_lenses=active_lenses,
        cluster_primary_lens=primary_lens,
        cluster_signal_source=_get_value(source, "CLUSTER_SIGNAL_SOURCE", "canonical"),
        cluster_id_algorithm=_get_value(source, "CLUSTER_ID_ALGORITHM", "sha256"),
        cluster_geo_filter=_get_value(source, "CLUSTER_GEO_FILTER", "country"),
        cluster_geo_scope=source.get("CLUSTER_GEO_SCOPE") or None,
        cluster_tie_breaker=_get_value(source, "CLUSTER_TIE_BREAKER", "alpha"),
        cluster_type_resolution=_get_value(source, "CLUSTER_TYPE_RESOLUTION", "canonical_priority"),
        cluster_cron_interval_s=int(_get_value(source, "CLUSTER_CRON_INTERVAL_S", "60")),
        cluster_cron_enabled=_parse_bool(_get_value(source, "CLUSTER_CRON_ENABLED", "true")),
        service_api_token=source.get("SERVICE_API_TOKEN") or None,
    )
```

**Task 2.2:** Добавить экспорты в `src/core/config/__init__.py`.

```python
from core.config.schema import AppConfig, ConfigError, DeploymentProfile, FeatureFlags, load_config_from_env
from core.config.providers import provide_app_config

__all__ = [
    "AppConfig", "ConfigError", "DeploymentProfile", "FeatureFlags",
    "load_config_from_env", "provide_app_config",
]
```

### Acceptance Criteria

- `load_config_from_env({"APP_PROFILE": "demo", "API_BASE_URL": "http://test", "DB_BACKEND": "in_memory"})` возвращает `AppConfig` без ошибок
- `load_config_from_env({"DB_BACKEND": "supabase"})` бросает `ConfigError` (нет SUPABASE_URL)
- `load_config_from_env({"DB_BACKEND": "in_memory", "CLUSTER_PRIMARY_LENS": "unknown_lens", ...})` бросает `ConfigError`
- `AppConfig` является `frozen` — попытка `config.db_backend = "x"` бросает `FrozenInstanceError`

---

## Story 3: Кастомный dotenv без сторонних библиотек

### Зачем

Нет `python-dotenv`, нет `pydantic-settings`. Кастомный парсер `.env` в 40 строк. Ключевое правило: shell env vars имеют приоритет над `.env` — если переменная уже есть в `os.environ`, `.env` её не перезапишет.

### Tasks

**Task 3.1:** Создать `src/core/config/env_file.py`.

```python
from __future__ import annotations

from os import environ
from pathlib import Path
from typing import MutableMapping, Mapping


def merge_dotenv_from_cwd(
    target: MutableMapping[str, str],
    *,
    priority: Mapping[str, str],
) -> None:
    """Load .env from current working directory, skipping keys already in priority."""
    merge_dotenv_from_path(Path.cwd() / ".env", target, priority=priority)


def merge_dotenv_from_path(
    path: Path,
    target: MutableMapping[str, str],
    *,
    priority: Mapping[str, str],
) -> None:
    if not path.is_file():
        return
    fixed = frozenset(priority.keys())  # shell env vars frozen — cannot be overwritten by .env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key not in fixed:
            target[key] = value


def _parse_dotenv_file(path: Path) -> dict[str, str]:
    """Parse .env file to dict without merging into environ. Used in tests."""
    result: dict[str, str] = {}
    if not path.is_file():
        return result
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result
```

**Task 3.2:** Создать `src/core/config/providers.py`.

```python
from __future__ import annotations

from os import environ
from typing import Mapping

from core.config.schema import AppConfig, load_config_from_env
from core.config.env_file import merge_dotenv_from_cwd


def provide_app_config(env: Mapping[str, str] | None = None) -> AppConfig:
    """
    Build AppConfig.
    - env=None (production): reads os.environ + .env from CWD
    - env=dict(...) (tests): uses only the provided mapping, never touches os.environ
    """
    if env is None:
        priority = dict(environ)        # snapshot of current shell env
        source = dict(priority)
        merge_dotenv_from_cwd(source, priority=priority)  # fills from .env, respects priority
    else:
        source = dict(env)

    source.setdefault("APP_PROFILE", "demo")
    source.setdefault("API_BASE_URL", "https://demo.local")
    source.setdefault("REQUEST_TIMEOUT_S", "15")
    return load_config_from_env(source)
```

### Acceptance Criteria

- `merge_dotenv_from_path(path, target, priority={"KEY": "shell_value"})` — `KEY` не перезаписывается значением из `.env`
- `merge_dotenv_from_path(path, target, priority={})` — все ключи из `.env` попадают в `target`
- Строки с комментарием (`#`) и пустые строки игнорируются
- `provide_app_config({"APP_PROFILE": "demo", "API_BASE_URL": "http://test", "DB_BACKEND": "in_memory"})` — работает без `.env` файла

---

## Story 4: Makefile и Railway конфиг

### Зачем

`make serve` и `make dev` — единственный правильный способ запустить сервер локально: они загружают `.env` в shell перед запуском uvicorn. Без этого uvicorn не видит `.env` переменные и `db_backend=in_memory` будет в логах вместо `supabase`.

### Tasks

**Task 4.1:** Создать `Makefile` в корне проекта.

```makefile
.PHONY: serve dev simulate check-env test test-live

serve:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host $${HOST:-127.0.0.1} --port $${PORT:-8000}

dev:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host $${HOST:-127.0.0.1} --port $${PORT:-8000} --reload --reload-dir src

simulate:
	.venv/bin/python tests/simulation_runner.py

check-env:
	@set -a && . ./.env && set +a && \
	echo "APP_PROFILE    = $${APP_PROFILE:-<not set>}" && \
	echo "DB_BACKEND     = $${DB_BACKEND:-<not set>}" && \
	echo "SUPABASE_URL   = $${SUPABASE_URL:-<not set>}" && \
	echo "API_BASE_URL   = $${API_BASE_URL:-<not set>}"

test:
	.venv/bin/python -m pytest tests/ -q --tb=short -m "not live_integration"

test-live:
	.venv/bin/python -m pytest tests/ -q -m live_integration -v
```

**Task 4.2:** Создать `railpack.json` в корне проекта.

```json
{
  "packages": { "python": "3.11" },
  "deploy": {
    "startCommand": "python -m uvicorn --app-dir src core.api.asgi_app:app --host 0.0.0.0 --port ${PORT:-8000}"
  }
}
```

На Railway `PORT` задаётся платформой автоматически — не хардкодить.
`--host 0.0.0.0` обязателен для доступности снаружи контейнера.

**Task 4.3:** Создать `.env.example` в корне проекта.

```bash
# ─── Core ────────────────────────────────────
APP_PROFILE=demo
API_BASE_URL=https://your-service.up.railway.app
REQUEST_TIMEOUT_S=15

# ─── Auth ────────────────────────────────────
SERVICE_API_TOKEN=your-secret-token

# ─── Persistence ─────────────────────────────
DB_BACKEND=supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE=<service_role_key>

# ─── Logging ─────────────────────────────────
LOG_LEVEL=INFO
LOG_FORMAT=text

# ─── Clustering ──────────────────────────────
CLUSTER_MIN_SIZE=5
CLUSTER_READINESS_THRESHOLD=60
CLUSTER_CRON_ENABLED=true
CLUSTER_CRON_INTERVAL_S=60
CLUSTER_ACTIVE_LENSES=civic_domain_micro,failure_pattern_micro,institution_micro,urgency_micro,geo_cluster_micro,keyword_micro
CLUSTER_PRIMARY_LENS=civic_domain_micro
CLUSTER_SIGNAL_SOURCE=canonical
CLUSTER_TIE_BREAKER=alpha
```

### Acceptance Criteria

- `make check-env` выводит значения переменных из `.env` без ошибок
- `make serve` запускает uvicorn на порту 8000 с загруженным `.env`
- Логи startup показывают `db_backend=supabase` (если `.env` содержит `DB_BACKEND=supabase`)
- `railpack.json` содержит корректный `startCommand` с `--app-dir src`

---

## Critical Pitfalls

- `DB_BACKEND=in_memory` + любые `SUPABASE_*` переменные → `ConfigError` при старте (fail-fast, intentional)
- `python -m uvicorn` без `--app-dir src` → `ModuleNotFoundError: No module named 'core'`
- `python3 -m pip install -e '.[dev]'` — в zsh нужны кавычки вокруг `.[dev]`
- Railway: `PORT` задаётся платформой — используй `${PORT:-8000}`, не хардкоди
- `CLUSTER_PRIMARY_LENS` должен быть в `CLUSTER_ACTIVE_LENSES` — иначе `ConfigError`
- Shell env vars имеют приоритет: если в shell уже есть `DB_BACKEND=supabase`, `.env` с `DB_BACKEND=in_memory` его не перезапишет

## Верификация эпика

```bash
# 1. Импорт работает
python3.11 -c "from core.config import AppConfig, provide_app_config; print('OK')"

# 2. Config создаётся
python3.11 -c "
from core.config import load_config_from_env
cfg = load_config_from_env({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://test', 'DB_BACKEND': 'in_memory'})
assert cfg.db_backend == 'in_memory'
assert cfg.db_enabled is False
print('AppConfig OK')
"

# 3. Fail-fast работает
python3.11 -c "
from core.config import load_config_from_env, ConfigError
try:
    load_config_from_env({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://test', 'DB_BACKEND': 'supabase'})
    assert False, 'should have raised'
except ConfigError:
    print('ConfigError raised OK')
"

# 4. make check-env
make check-env

# 5. Pytest infrastructure
python3.11 -m pytest --collect-only -q 2>&1 | head -5
```
