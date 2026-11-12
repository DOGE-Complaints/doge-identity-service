# 06. Technical Scaffold — Каркас проекта

> ⚠️ **Reference-only (2026-06-24):** этот документ скопирован из `doge-complaints-gateway` и описывает ДРУГОЙ сервис (intake/кластеризация историй), не identity. Фактический identity-код — в `src/`; актуальные факты — в `docs/analysis/identity-backend-full-audit-2026-06-24.md` и runtime-docs. Использовать только как шаблон-референс; подлежит переписыванию под identity.

> **Статус:** НЕ реализовано. Runbook для первого коммита.
> **Формат:** Исполнять последовательно. Каждый шаг — конкретная задача.
> **Референс:** `doge-complaints-gateway` — брать паттерны оттуда напрямую.

---

## Шаг 1: Структура директорий

Целевая структура файловой системы:

```
doge-identity-service/
├── src/
│   └── core/
│       ├── __init__.py
│       ├── bootstrap.py
│       ├── logging_setup.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── asgi_app.py           — FastAPI app, routes, lifespan
│       │   ├── dependencies.py       — ApiDependencies dataclass
│       │   ├── envelope.py           — build_error_envelope, ensure_trace_id
│       │   ├── handlers.py           — pure handler functions (no FastAPI deps)
│       │   └── security.py           — BearerTokenAuth (Supabase JWT validation)
│       ├── config/
│       │   ├── __init__.py
│       │   ├── env_file.py           — merge_dotenv_from_cwd (копия из complaints-gateway)
│       │   └── schema.py             — AppConfig, ENV_SCHEMA, load_config_from_env
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── supabase_validator.py — validate_supabase_jwt(token) → UserClaims
│       │   ├── eid_start.py          — build_eid_authorize_url, create_verification_session
│       │   ├── eid_callback.py       — handle_eid_callback(code, state) → EidResult
│       │   ├── authentigate_client.py — OIDCClient: discover, exchange_code, validate_id_token
│       │   ├── verification_session_store.py — create/consume/expire sessions (psycopg)
│       │   └── verified_person_hasher.py — generate_verified_person_hash(country, personal_code)
│       ├── profiles/
│       │   ├── __init__.py
│       │   ├── profile_repository.py — get_by_user_id, get_by_hash, attach_eid_verification
│       │   └── verification_service.py — orchestrates eid flow business logic
│       ├── oauth/
│       │   ├── __init__.py
│       │   ├── authorization_server.py — handle_authorize, handle_token
│       │   ├── client_store.py       — registered OAuth clients (static config or DB)
│       │   └── token_service.py      — issue_access_token, validate_access_token
│       ├── stories/
│       │   ├── __init__.py
│       │   ├── draft_repository.py   — create_draft, get_draft, submit_draft
│       │   └── story_authorization.py — require_eid_verified(user) → AuthzResult
│       ├── audit/
│       │   ├── __init__.py
│       │   └── audit_logger.py       — log_eid_event(event_type, user_id, success, ...)
│       └── infrastructure/
│           ├── __init__.py
│           └── db.py                 — get_connection(config) → psycopg Connection
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_health.py
├── supabase/
│   └── migrations/                   — SQL миграции (файл 08)
├── docs/
│   └── requirements/                 — этот файл и все остальные
├── example.env
├── pyproject.toml
├── pyrightconfig.json
├── Makefile
└── README.md
```

---

## Шаг 2: `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "doge-identity-service"
version = "0.1.0"
description = "DOGEstonia Identity and Authorization Service"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.115.0",
  "uvicorn>=0.30.0",
  "psycopg[binary]>=3.2.0",
  "httpx>=0.27.0",
  "joserfc>=1.0.0",       # JWT validation (RS256/HS256) — no PyJWT ambiguity
  "cryptography>=42.0.0", # AES encryption for code_verifier_encrypted
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
  "mock_oidc: tests requiring mock OIDC server running on localhost:8080",
]

[tool.pyright]
include = ["src", "tests"]
extraPaths = ["src", "tests"]
pythonVersion = "3.11"

[tool.basedpyright]
include = ["src", "tests"]
extraPaths = ["src", "tests"]
pythonVersion = "3.11"
```

**Обоснование выбора зависимостей:**
- `joserfc` — современная JWT библиотека с чёткой поддержкой RS256 (для Supabase JWKS) и HS256 (для секрета). Не путать с deprecated `python-jose`.
- `cryptography` — AES-256-GCM для шифрования `code_verifier_encrypted` в DB.
- Нет `python-dotenv` — используем свой `env_file.py` (паттерн из complaints-gateway).
- Нет `pydantic` — используем `dataclasses` для конфигурации (паттерн из complaints-gateway).

---

## Шаг 3: `pyrightconfig.json`

```json
{
  "include": ["src", "tests"],
  "extraPaths": ["src"],
  "pythonVersion": "3.11"
}
```

---

## Шаг 4: `Makefile`

```makefile
.PHONY: serve dev check-env test

serve:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8100}

dev:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src core.api.asgi_app:app \
	  --host 127.0.0.1 --port $${PORT:-8100} --reload --reload-dir src

check-env:
	@set -a && . ./.env && set +a && \
	echo "APP_PROFILE          = $${APP_PROFILE:-demo}" && \
	echo "SUPABASE_URL         = $${SUPABASE_URL:-<not set>}" && \
	echo "AUTHENTIGATE_ISSUER  = $${AUTHENTIGATE_ISSUER:-<not set>}" && \
	echo "PORT                 = $${PORT:-8100}"

test:
	.venv/bin/pytest tests/
```

Порт 8100 — не конфликтует с doge-complaints-gateway (8000).

---

## Шаг 5: `src/core/config/env_file.py`

**Копировать без изменений** из `doge-complaints-gateway/src/core/config/env_file.py`.

Функции: `merge_dotenv_from_path`, `merge_dotenv_from_cwd`.
Поведение: shell env переменные имеют приоритет над .env файлом.

---

## Шаг 6: `src/core/config/schema.py` — скелет

Паттерн: `dataclass(frozen=True)` для конфигурации. Enum для профилей. `ENV_SCHEMA` tuple для документации и валидации. Полная спецификация переменных — в файле 07.

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from os import environ
from typing import Mapping

from core.config.env_file import merge_dotenv_from_cwd


class ConfigError(ValueError):
    """Raised when environment configuration is invalid."""


class DeploymentProfile(str, Enum):
    DEMO = "demo"
    PILOT = "pilot"


@dataclass(frozen=True)
class AppConfig:
    profile: DeploymentProfile
    port: int
    api_base_url: str
    log_level: str
    log_format: str
    # Supabase
    supabase_url: str | None
    supabase_service_role: str | None
    supabase_jwt_secret: str | None
    database_url: str | None
    # Authentigate OIDC
    authentigate_issuer: str
    authentigate_client_id: str
    authentigate_client_secret: str
    authentigate_redirect_uri: str
    authentigate_scopes: str
    # Identity secrets
    eid_secret_pepper: str
    code_verifier_encryption_key: str
    # OAuth server
    oauth_access_token_secret: str
    oauth_access_token_ttl_s: int
    oauth_authorization_code_ttl_s: int
    gpt_oauth_client_id: str
    gpt_oauth_client_secret: str
    gpt_oauth_redirect_uri: str


def load_config_from_env(source: Mapping[str, str] | None = None) -> AppConfig:
    env: dict[str, str] = dict(environ)
    merge_dotenv_from_cwd(env, priority=environ)
    s = source or env
    # ... parse и validate здесь
    ...
```

Полная реализация `load_config_from_env` — в рамках задачи реализации файла 06.

---

## Шаг 7: `src/core/api/asgi_app.py` — минимальный скелет

Паттерн полностью из complaints-gateway:
- `@asynccontextmanager async def _lifespan(_: FastAPI)` — запуск/остановка
- `app = FastAPI(title="doge-identity-service", version="0.1.0", lifespan=_lifespan)`
- `CORSMiddleware` — CORS (настройка в файле 16)
- `@lru_cache(maxsize=1) def _cached_dependencies()` — singleton зависимостей
- `runtime_exception_diagnostics` middleware
- Минимальные routes: `/health`, `/ready`

---

## Шаг 8: `src/core/bootstrap.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from core.api import ApiDependencies, build_api_dependencies


@dataclass(frozen=True)
class AppBootstrap:
    api: ApiDependencies


def bootstrap_app() -> AppBootstrap:
    return AppBootstrap(api=build_api_dependencies())
```

---

## Шаг 9: Создать `.venv` и установить зависимости

```bash
python3.11 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

---

## Acceptance Criteria для Scaffold

- [ ] `make dev` запускает uvicorn на порту 8100
- [ ] `GET /health` возвращает `{"status": "ok"}`
- [ ] `GET /ready` возвращает `{"status": "ok"}` или `{"status": "degraded"}` (при отсутствии DB)
- [ ] `pytest tests/test_health.py` проходит без ошибок
- [ ] `make check-env` выводит значения из .env
- [ ] pyright не сообщает об ошибках в `src/`
