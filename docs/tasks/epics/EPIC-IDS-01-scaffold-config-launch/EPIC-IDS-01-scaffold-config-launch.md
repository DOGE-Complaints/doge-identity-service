# EPIC-IDS-01 — Scaffold, Config и Launch

> **ID:** `EPIC-IDS-01`
> **Layer:** NFR / Infrastructure
> **Статус:** Implemented (Waiting Acceptance)
> **Зависит от:** —
> **Блокирует:** EPIC-IDS-02, EPIC-IDS-03, EPIC-IDS-04, EPIC-IDS-05, EPIC-IDS-06

---

## 1. Назначение

Фундамент `doge-identity-service`: структура пакета, конфигурация зависимостей с поддержкой JWT/AES, immutable `AppConfig`, кастомный dotenv-парсер без сторонних библиотек, Makefile и Railway-конфиг. Сервер должен подниматься на порту `8100` с правильно загруженным `AppConfig` без единого identity-эндпойнта (они приходят в EPIC-IDS-02 и далее).

## 2. Epic Goal

```bash
make serve
# Логи: uvicorn started on 127.0.0.1:8100, app_profile=demo, db_backend=in_memory (или supabase)
curl http://localhost:8100/health  # резолвится после EPIC-IDS-02
```

Эпик считается завершённым, когда:
- `python3.11 -c "from core.config import AppConfig, provide_app_config"` — ImportError = 0.
- `provide_app_config({...identity env...})` строит валидный `AppConfig` без `cluster_*` полей.
- `make check-env` печатает identity-vars (`AUTHENTIGATE_ISSUER`, `SUPABASE_URL`, `EID_PROVIDER`).
- Fail-fast: при `APP_PROFILE=pilot` без обязательных секретов — `ConfigError`.

## 3. Бизнес-контекст

Все 18 функциональных требований ([`docs/requirements/01-18`](../../requirements/)) опираются на этот фундамент. Без рабочего scaffold + AppConfig ни один следующий эпик (FastAPI transport, DI, SOA factory, Supabase persistence, тесты) не может стартовать.

Identity-домен отличается от gateway:
- Порт `8100` (не `8000`) — конкуренция с doge-complaints-gateway (`docs/requirements/06`, шаг 4).
- Зависимости `joserfc>=1.0.0` (JWT) и `cryptography>=42.0.0` (AES-256-GCM для `code_verifier_encrypted`) — `docs/requirements/06`, шаг 2.
- AppConfig содержит блоки `supabase_*`, `authentigate_*`, `eid_*`, `oauth_*`, `gpt_oauth_*` — `docs/requirements/06`, шаг 6 + `docs/requirements/07`.
- `cluster_*` поля (gateway) отсутствуют.

## 4. Предусловия

Нет. Это первый эпик, выполняется с нуля.

## 5. Целевые файлы

```
src/core/__init__.py
src/core/config/__init__.py
src/core/config/schema.py
src/core/config/env_file.py
src/core/config/providers.py
pyproject.toml
pyrightconfig.json
Makefile
railpack.json
.env.example
```

Модульная структура `src/core/{api,auth,profiles,oauth,stories,audit,infrastructure,providers}/__init__.py` — заранее создаются пустые `__init__.py` (заполняются в EPIC-IDS-02..05). Spec из [`docs/requirements/06-technical-scaffold.md`](../../requirements/06-technical-scaffold.md) §"Шаг 1".

## 6. Stories (заготовка — Tasks вынесены в следующий слой)

### Story 1: Инициализация пакета и зависимостей

- **Why:** `pyproject.toml` задаёт `name = "doge-identity-service"`, корректный `[tool.setuptools.packages.find]` и `pythonpath = ["src", "tests"]` — без этого `ModuleNotFoundError: core` на каждом шаге. Identity-specific deps (`joserfc`, `cryptography`) задаются здесь — все следующие эпики их предполагают.
- **Inputs:**
  - Reference list зависимостей из [`docs/requirements/06-technical-scaffold.md`](../../requirements/06-technical-scaffold.md) §"Шаг 2".
  - Pytest markers `live_integration` + `mock_oidc` (ibid., §"Шаг 2", блок `[tool.pytest.ini_options]`).
- **Outputs:**
  - `pyproject.toml` с `name = "doge-identity-service"`, `requires-python = ">=3.11"`, deps `fastapi>=0.115.0`, `uvicorn>=0.30.0`, `psycopg[binary]>=3.2.0`, `httpx>=0.27.0`, `joserfc>=1.0.0`, `cryptography>=42.0.0`. Dev: `pytest>=8.0.0`, `pytest-asyncio>=0.24.0`, `httpx>=0.27.0`.
  - `pyrightconfig.json` (см. требование 06 §"Шаг 3").
  - Создан скелет директорий: `src/core/{api,auth,profiles,oauth,stories,audit,infrastructure,config,security}/` + `tests/`, `tests/integration/supabase/`, `tests/smoke/`, `supabase/migrations/`, `supabase/bootstrap/`. Все `__init__.py` пусты.
  - `src/core/security/hashing.py` — реализован `hash_secret(plaintext: str, *, key: str) -> str` (HMAC-SHA256); EPIC-IDS-04 Story 2 только импортирует модуль.
  - Активный venv с `pip install -e ".[dev]"` без ошибок.
- **Acceptance Criteria:**
  - `python3.11 -c "import core"` — exit 0.
  - `python3.11 -m pytest --collect-only -q` — завершается без `ModuleNotFoundError` (количество тестов может быть > 0).
  - `pip show doge-identity-service` показывает version `0.1.0`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §"Story 1" — паттерн идентичен; замена `name`, добавление `joserfc`/`cryptography`, markers.

### Story 2: AppConfig — immutable identity-конфигурация

- **Why:** `AppConfig(frozen=True)` — единственный источник истины. Identity-сервису нужны блоки полей (Supabase, Authentigate/OIDC, eID secrets, OAuth server, GPT OAuth client), а **не** gateway-овский cluster lens-апппарат. Fail-fast в `pilot` профиле обязателен — сервер не должен стартовать без секретов в проде.
- **Inputs:**
  - Полный набор env vars: [`docs/requirements/07-env-configuration-spec.md`](../../requirements/07-env-configuration-spec.md) — секции Deployment / Supabase / Authentigate OIDC / Identity Secrets / OAuth 2.0 Server / Security & CORS.
  - Дополнительные provider-vars: [`docs/requirements/17-eid-provider-abstraction.md`](../../requirements/17-eid-provider-abstraction.md) §"Изменения в `src/core/config/schema.py`" — `EID_PROVIDER`, `DOGESTONIA_EID_SECRET`, `NODE_ID`.
  - eID Easy vars: [`docs/requirements/18-eideasy-provider.md`](../../requirements/18-eideasy-provider.md) §"Env vars" — `EIDEASY_*` (необязательны при `EID_PROVIDER=mock`).
  - Demo/pilot matrix: [`docs/requirements/07`](../../requirements/07-env-configuration-spec.md) §"Валидация конфигурации при старте".
- **Outputs:**
  - `src/core/config/schema.py`:
    - `class ConfigError(ValueError)`.
    - `class DeploymentProfile(str, Enum)` со значениями `DEMO`, `PILOT`.
    - `@dataclass(frozen=True) class AppConfig` с полями:
      - Deployment: `profile`, `port` (default `8100`), `api_base_url`, `log_level`, `log_format`, `request_timeout_s: int = 15` (только Supabase PostgREST; req-07), `oidc_request_timeout_s: int = 10` (Authentigate / eID Easy HTTP; req-07 `OIDC_REQUEST_TIMEOUT_S`).
      - Supabase: `supabase_url`, `supabase_service_role`, `supabase_jwt_secret`, `database_url`. (`supabase_anon_key` намеренно отсутствует: identity-сервер server-side всегда через `service_role`, anon key — только для клиентских SDK.)
      - Authentigate: `authentigate_issuer`, `authentigate_client_id`, `authentigate_client_secret`, `authentigate_redirect_uri`, `authentigate_scopes`.
      - Identity secrets: `eid_secret: str = ""` из `DOGESTONIA_EID_SECRET` (без fallback; `ADR-IDS-008` пересмотр 2026-05-27), `code_verifier_encryption_key`, `node_id` (req-17).
      - OAuth: `oauth_access_token_secret`, `oauth_access_token_ttl_s` (default 3600), `oauth_authorization_code_ttl_s` (default 300), `gpt_oauth_client_id`, `gpt_oauth_client_secret`, `gpt_oauth_redirect_uri`.
      - eID provider: `eid_provider` (default `mock`).
      - eID Easy (все с defaults, см. M-4 аудита): `eideasy_env: str = "test"`, `eideasy_base_url: str = "https://test.eideasy.com"`, `eideasy_client_id: str = ""`, `eideasy_client_secret: str = ""`, `eideasy_redirect_uri: str = ""`, `eideasy_allowed_methods: str = "smartid,mid-login,ee-id-login"`, `eideasy_default_country: str = "EE"`, `eideasy_allowed_countries: str = "EE"`.
      - Backend selector: `db_backend` (`"in_memory" | "supabase"`, см. `ADR-IDS-008` контекст и audit H-3: `sqlite` не плановый backend), `db_enabled` (derived: `True` при `supabase`).
      - Security/CORS: `cors_allowed_origins`, `allowed_return_urls`.
    - `def load_config_from_env(source: Mapping[str, str] | None = None) -> AppConfig`:
      - Парсит, нормализует, валидирует.
      - **Порядок валидации (interview 4.5):** первая проверка — `db_backend ∈ {"in_memory", "supabase"}`; при невалидном значении — `ConfigError` до разбора остальных полей.
      - `eid_secret` loader: `eid_secret = source.get("DOGESTONIA_EID_SECRET", "")` — одна строка, без `or`.
      - `db_backend=supabase` без `supabase_url` или `supabase_service_role` → `ConfigError`.
      - `profile=pilot` без секретов из таблицы pilot-required → `ConfigError` (см. req-07).
      - `eid_provider` ∉ `{mock, eideasy, authentigate}` → `ConfigError` (req-17 acceptance).
      - `eid_provider=eideasy` + пустые `eideasy_client_id|client_secret|redirect_uri` → `ConfigError` (req-18 §"Env vars" required marker).
      - `profile=pilot` + пустой `eid_secret` → `ConfigError` (interview 4.4).
- **Acceptance Criteria:**
  - `load_config_from_env({"APP_PROFILE": "demo", "API_BASE_URL": "http://localhost:8100"})` → `AppConfig` с `db_backend=in_memory`, `eid_provider=mock`, `request_timeout_s == 15`, `oidc_request_timeout_s == 10` (default).
  - `load_config_from_env({"DB_BACKEND": "supabase", ...})` без `SUPABASE_*` → `ConfigError`.
  - `load_config_from_env({"DB_BACKEND": "sqlite", "APP_PROFILE": "demo", "API_BASE_URL": "x"})` → `ConfigError` (`sqlite` не поддерживается; audit H-3).
  - `load_config_from_env({"APP_PROFILE": "pilot", ...})` без `OAUTH_ACCESS_TOKEN_SECRET` → `ConfigError`.
  - `load_config_from_env({"EID_PROVIDER": "unknown"})` → `ConfigError`.
  - `config.port == 8100` (default), `config.api_base_url` — required.
  - `config.eid_secret = "x"` → `FrozenInstanceError` (immutable).
  - **Pilot + пустой секрет (interview 4.4):** `load_config_from_env({"APP_PROFILE": "pilot", "API_BASE_URL": "https://identity.dogestonia.ee", "DOGESTONIA_EID_SECRET": "", ...})` → `ConfigError` с понятным сообщением.
- **Pattern source:** [`docs/tech-requirements/impl-epic-01`](../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §"Story 2" — паттерн `@dataclass(frozen=True)` + `_require/_get_value/_parse_*` хелперы. Замена field-set на identity (см. список выше).

### Story 3: Кастомный dotenv-парсер (паттерн-копия)

- **Why:** Нет `python-dotenv` (требование 06 §"Шаг 2" — "паттерн из complaints-gateway"). Кастомный парсер в ~40 строк, ключевое правило: shell env переменные имеют приоритет над `.env`.
- **Inputs:** Полный код [`docs/tech-requirements/impl-epic-01`](../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §"Story 3", Task 3.1 — без идентити-специфичной адаптации, копируем 1:1.
- **Outputs:**
  - `src/core/config/env_file.py` с функциями `merge_dotenv_from_cwd`, `merge_dotenv_from_path`, `_parse_dotenv_file`.
  - `src/core/config/providers.py` с `provide_app_config(env=None)` — production читает `os.environ` + .env, тесты передают явный `Mapping`. Defaults для `APP_PROFILE`, `API_BASE_URL` те же что в gateway, но `API_BASE_URL` default → `http://localhost:8100`.
- **Acceptance Criteria:**
  - `merge_dotenv_from_path(path, target, priority={"KEY": "shell"})` — `KEY` не перезаписывается.
  - Строки `#` и пустые игнорируются; значения с `"..."` или `'...'` распаковываются.
  - `provide_app_config({"APP_PROFILE": "demo", "API_BASE_URL": "http://localhost:8100"})` работает без `.env` файла.
- **Pattern source:** [`docs/tech-requirements/impl-epic-01`](../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §"Story 3" — копия без изменений.

### Story 4: Makefile, Railway-конфиг, `.env.example`

- **Why:** `make serve`/`make dev` — единственный корректный путь старта локально. Без `set -a && . ./.env && set +a` uvicorn не видит `.env` (нет `python-dotenv`). Railway требует `--host 0.0.0.0` и `${PORT:-...}` — но локальный default = `8100` (требование 06 §"Шаг 4").
- **Inputs:**
  - Шаблон Makefile gateway: [`docs/tech-requirements/impl-epic-01`](../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §"Story 4", Task 4.1.
  - Identity-вариант Makefile: [`docs/requirements/06-technical-scaffold.md`](../../requirements/06-technical-scaffold.md) §"Шаг 4" — порт 8100, `make check-env` печатает `AUTHENTIGATE_ISSUER`, `SUPABASE_URL`.
  - Env vars для `.env.example`: [`docs/requirements/07-env-configuration-spec.md`](../../requirements/07-env-configuration-spec.md) §"`example.env`" + [`docs/requirements/17`](../../requirements/17-eid-provider-abstraction.md) §"Конфигурация для `EID_PROVIDER=mock`" + [`docs/requirements/18`](../../requirements/18-eideasy-provider.md) §"`example.env` фрагмент".
- **Outputs:**
  - `Makefile` с целями `serve`, `dev`, `check-env`, `test`, `test-live`:
    - `serve`/`dev` — host `127.0.0.1`, port `${PORT:-8100}`.
    - `check-env` печатает: `APP_PROFILE`, `PORT`, `SUPABASE_URL`, `SUPABASE_JWT_SECRET`, `AUTHENTIGATE_ISSUER`, `EID_PROVIDER`.
      - **Расширение паттерна req-06** (audit M-2): к базовому набору из req-06 §"Шаг 4" (`APP_PROFILE`, `SUPABASE_URL`, `AUTHENTIGATE_ISSUER`, `PORT`) явно добавлены `SUPABASE_JWT_SECRET` (нужен для JWT-валидации в EPIC-IDS-04) и `EID_PROVIDER` (нужен для debug eID flow). Расширение оправдано identity-домена.
    - `test` — `pytest -m "not live_integration"`.
    - `test-live` — `pytest -m live_integration -v`.
  - `railpack.json` со startCommand на `--host 0.0.0.0 --port ${PORT:-8100} --app-dir src core.api.asgi_app:app`.
  - `.env.example` — полный набор identity-vars из req-07 (`DOGESTONIA_EID_SECRET`, `OIDC_REQUEST_TIMEOUT_S`) + req-17 + req-18 (`EID_PROVIDER=mock` по умолчанию).
- **Acceptance Criteria:**
  - `make check-env` выводит identity-vars без ошибок.
  - `make serve` поднимает uvicorn на `:8100` с loaded `.env` (когда EPIC-IDS-02 готов; в этом эпике — `make serve` запускает uvicorn, но получит `ImportError` на `core.api.asgi_app` пока EPIC-IDS-02 не реализован — это ожидаемо).
  - `railpack.json` JSON-валиден; `startCommand` использует `${PORT:-8100}` и `--app-dir src`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-01`](../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §"Story 4" — структура Makefile. Идентичный паттерн с подменой порта `8000 → 8100` и переменных в `check-env`.

## 7. Critical Pitfalls (identity-flavored)

- `python -m uvicorn` без `--app-dir src` → `ModuleNotFoundError: No module named 'core'`.
- В zsh `.[dev]` обязательно кавычить: `pip install -e ".[dev]"`.
- Railway: `PORT` задаётся платформой — используй `${PORT:-8100}`, не хардкодь.
- `DB_BACKEND=supabase` + пустой `SUPABASE_URL` → `ConfigError` при старте (fail-fast — это правильно).
- `APP_PROFILE=pilot` + любой отсутствующий секрет из таблицы pilot-required (`docs/requirements/07`) → `ConfigError`.
- `EID_PROVIDER=eideasy` без `EIDEASY_CLIENT_ID/SECRET/REDIRECT_URI` → `ConfigError` (req-18).
- Shell env vars имеют приоритет: если в shell `DB_BACKEND=supabase`, `.env` с `DB_BACKEND=in_memory` его не перезапишет.
- НЕ копировать поля `cluster_*` из gateway-шаблона — identity-сервису они не нужны и собьют валидацию.

## 8. Верификация эпика

```bash
# 1. Импорты работают
python3.11 -c "from core.config import AppConfig, provide_app_config, ConfigError; print('OK')"

# 2. demo Config создаётся
python3.11 -c "
from core.config import load_config_from_env
cfg = load_config_from_env({
    'APP_PROFILE': 'demo',
    'API_BASE_URL': 'http://localhost:8100',
    'DB_BACKEND': 'in_memory',
    'EID_PROVIDER': 'mock',
})
assert cfg.port == 8100
assert cfg.eid_provider == 'mock'
assert cfg.db_enabled is False
print('demo AppConfig OK')
"

# 3. fail-fast: pilot без секретов
python3.11 -c "
from core.config import load_config_from_env, ConfigError
try:
    load_config_from_env({
        'APP_PROFILE': 'pilot',
        'API_BASE_URL': 'https://identity.dogestonia.ee',
    })
    assert False, 'should have raised'
except ConfigError as e:
    print('pilot fail-fast OK:', e)
"

# 4. fail-fast: unknown EID_PROVIDER
python3.11 -c "
from core.config import load_config_from_env, ConfigError
try:
    load_config_from_env({'EID_PROVIDER': 'unknown', 'APP_PROFILE': 'demo', 'API_BASE_URL': 'x'})
    assert False
except ConfigError:
    print('eid_provider validation OK')
"

# 5. make check-env
make check-env

# 6. Pytest infrastructure
python3.11 -m pytest --collect-only -q 2>&1 | head -5
```

## 9. Open Questions

- **ADR-IDS-005** — `psycopg` vs `supabase-py` для DB-доступа. Решение влияет на `database_url` field семантику и набор Supabase healthchecks в EPIC-IDS-05. Парковка: `docs/requirements/README-index.md` §"Открытые вопросы". Зафиксировать перед стартом EPIC-IDS-05; на схеме `AppConfig` оба варианта работают (`database_url` опционален).
- **`EID_HASH_SECRET` vs `DOGESTONIA_EID_SECRET_PEPPER`** — **закрыто** пересмотром `ADR-IDS-008` (2026-05-27): единственное имя `DOGESTONIA_EID_SECRET` → `AppConfig.eid_secret`. См. Story 2.
- **`COMPLAINTS_GATEWAY_URL` + `SERVICE_API_TOKEN`** — для проксирования story-submit в gateway (req-15 §"Проброс запроса"). Добавляется в env spec и в `AppConfig` когда определится деплой complaints-gateway. На этом эпике — не включаются.
