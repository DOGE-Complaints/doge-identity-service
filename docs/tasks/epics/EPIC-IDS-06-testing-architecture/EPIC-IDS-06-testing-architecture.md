# EPIC-IDS-06 — Testing Architecture

> **ID:** `EPIC-IDS-06`
> **Layer:** NFR / Testing
> **Статус:** Не реализовано
> **Зависит от:** EPIC-IDS-01 (pyproject markers), EPIC-IDS-02 (HTTP slой), EPIC-IDS-03 (DI singleton + `_clear_api_dependencies_cache`), EPIC-IDS-04 (InMemory-репозитории, MockEIDProvider), EPIC-IDS-05 (Supabase-репозитории, healthcheck)
> **Блокирует:** —

---

## 1. Назначение

6-слойная тест-сюита с чёткой изоляцией. Главный инвариант: **unit и integration тесты НИКОГДА не трогают реальный Supabase**. Гарантируется `autouse`-фикстурой `_block_dotenv_leakage`, которая перезаписывает все идентити-чувствительные env vars на безопасные mock-значения. CI разделён на offline (каждый push) и live integration (только `main` или `workflow_dispatch`).

## 2. Epic Goal

```bash
# Offline (< 30 сек, без сети)
python3.11 -m pytest tests/ -q -m "not live_integration"
# Ожидаемо: X passed in <30s

# Live Supabase — пропускается без creds
python3.11 -m pytest tests/ -q -m live_integration
# Без .env с creds → X skipped (no Supabase creds)
# С creds → X passed
```

После EPIC-IDS-06:
- `tests/conftest.py` содержит 3 autouse-фикстуры с identity-env defaults.
- HTTP smoke тесты покрывают `/health`, `/ready`, `/me` (401 + 501 stub), все identity-роуты как stub-501.
- Live Supabase тесты проверяют connectivity и identity-таблицы.
- CI workflows offline + live разделены.
- Smoke-тесты против live-сервера используют `IDENTITY_URL=http://localhost:8100`.

## 3. Бизнес-контекст

Identity-сервис обрабатывает PII (через `verified_person_hash`) и issued OAuth tokens. Любое попадание тестов в production Supabase → утечка данных, ложные verified-пользователи. Поэтому изоляция тестов — не "nice to have", а security-инвариант.

Дополнительно:
- `EID_PROVIDER=mock` (req-17 §"Mock провайдер") нужен для офлайн-тестов eID flow.
- HTTP offline smoke — `fastapi.testclient.TestClient` + autouse `_clear_api_dependencies_cache()` (не `pytest-asyncio`; async-тестов в сюите нет).
- Marker `mock_oidc` (req-06 шаг 2) — для тестов, требующих локальный mock-OIDC сервер (`docker run navikt/mock-oauth2-server`).

## 4. Предусловия

- EPIC-IDS-01: `pyproject.toml` с `pythonpath = ["src", "tests"]`, markers `live_integration` + `mock_oidc` + `smoke`.
- EPIC-IDS-02..05: все слои реализованы (хотя бы InMemory). HTTP-роуты с stubs.

## 5. Целевые файлы

```
tests/__init__.py
tests/conftest.py
tests/test_bootstrap_smoke.py
tests/test_http_transport_smoke.py
tests/test_di_singleton.py
tests/test_di_service_factory.py
tests/test_eid_provider_registry.py
tests/test_supabase_jwt_validator.py
tests/integration/__init__.py
tests/integration/supabase/__init__.py
tests/integration/supabase/test_supabase_dotenv_connectivity.py
tests/integration/supabase/test_supabase_identity_roundtrip.py
tests/smoke/__init__.py
tests/smoke/conftest.py
tests/smoke/test_local_server_smoke.py
.github/workflows/test-offline.yml
.github/workflows/integration-live.yml
```

## 6. Stories (заготовка)

### Story 1: `conftest.py` — три обязательные autouse-фикстуры

- **Why:** `_block_dotenv_leakage` — главный механизм изоляции. Без него тест, запущенный в директории с `.env` содержащим `DB_BACKEND=supabase` + реальные creds, попадает в реальный Supabase. `autouse=True` гарантирует применение к каждому тесту. Identity-env vars (Authentigate, EID, OAuth) перетираются на безопасные mock-значения.
- **Inputs:**
  - Паттерн: [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 1".
  - Identity env vars: req-07 + req-17 + req-18.
- **Outputs:**
  - `tests/conftest.py`:
    ```python
    # Top-level imports (audit H-1): base64 + os + pytest + configure_logging
    # требуются autouse-фикстурами ниже. Без них pytest падает с NameError
    # ещё на этапе сбора.
    import base64
    import os
    import pytest
    from core.logging_setup import configure_logging


    @pytest.fixture(autouse=True)
    def _block_dotenv_leakage(monkeypatch):
        # Deployment
        monkeypatch.setenv("APP_PROFILE", "demo")
        monkeypatch.setenv("PORT", "8100")
        monkeypatch.setenv("API_BASE_URL", "http://localhost:8100")
        monkeypatch.setenv("LOG_LEVEL", "INFO")
        monkeypatch.setenv("LOG_FORMAT", "text")
        # DB — never real Supabase in unit tests
        monkeypatch.setenv("DB_BACKEND", "in_memory")
        monkeypatch.setenv("SUPABASE_URL", "")
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
        monkeypatch.setenv("SUPABASE_JWT_SECRET", "")
        monkeypatch.setenv("DATABASE_URL", "")
        # Authentigate OIDC — stub
        monkeypatch.setenv("AUTHENTIGATE_ISSUER", "https://stub.local")
        monkeypatch.setenv("AUTHENTIGATE_CLIENT_ID", "stub-client")
        monkeypatch.setenv("AUTHENTIGATE_CLIENT_SECRET", "stub-secret")
        monkeypatch.setenv("AUTHENTIGATE_REDIRECT_URI", "http://localhost:8100/auth/authentigate/callback")
        monkeypatch.setenv("AUTHENTIGATE_SCOPES", "openid personal_code personal_code_country")
        # eID provider — mock everywhere
        monkeypatch.setenv("EID_PROVIDER", "mock")
        monkeypatch.setenv("DOGESTONIA_EID_SECRET", "test-eid-hash-secret-not-real")
        monkeypatch.setenv("NODE_ID", "test-node")
        # AES key (req-07) — 32 bytes base64
        monkeypatch.setenv("CODE_VERIFIER_ENCRYPTION_KEY", base64.b64encode(b"\x00" * 32).decode())
        # OAuth server
        monkeypatch.setenv("OAUTH_ACCESS_TOKEN_SECRET", "test-oauth-secret-not-real")
        monkeypatch.setenv("OAUTH_ACCESS_TOKEN_TTL_S", "3600")
        monkeypatch.setenv("OAUTH_AUTHORIZATION_CODE_TTL_S", "300")
        monkeypatch.setenv("GPT_OAUTH_CLIENT_ID", "test-gpt-client")
        monkeypatch.setenv("GPT_OAUTH_CLIENT_SECRET", "test-gpt-client-secret")
        monkeypatch.setenv("GPT_OAUTH_REDIRECT_URI", "https://oauth.pstmn.io/v1/callback")
        # eID Easy — empty (provider=mock использует только базовые)
        monkeypatch.setenv("EIDEASY_ENV", "test")
        monkeypatch.setenv("EIDEASY_BASE_URL", "https://test.eideasy.com")
        monkeypatch.setenv("EIDEASY_CLIENT_ID", "")
        monkeypatch.setenv("EIDEASY_CLIENT_SECRET", "")
        monkeypatch.setenv("EIDEASY_REDIRECT_URI", "http://localhost:8100/auth/eideasy/callback")
        # CORS
        monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "*")

    @pytest.fixture(scope="session", autouse=True)
    def _pytest_session_logging():
        configure_logging(os.environ.get("LOG_LEVEL", "INFO"), log_format="text", log_debug_dir=None)

    def pytest_collection_modifyitems(items):
        marker = pytest.mark.live_integration
        for item in items:
            path = str(item.path).replace("\\", "/")
            if "/tests/integration/supabase/" in path:
                item.add_marker(marker)
    ```
- **Acceptance Criteria:**
  - `pytest tests/ -q` без `.env` файла — все unit-тесты `DB_BACKEND=in_memory`, `EID_PROVIDER=mock`.
  - `pytest tests/ -q` с `.env` содержащим `DB_BACKEND=supabase` + реальные creds — тесты используют in_memory (env перезаписан).
  - `tests/integration/supabase/*.py` автоматически помечены `live_integration` без явного декоратора.
  - `pytest -m "not live_integration" -q` — пропускает все Supabase тесты.
  - В тесте, переопределяющем env через свой `monkeypatch.setenv()` ПОСЛЕ autouse — переопределение работает (autouse применяется первым).
- **Pattern source:** [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 1" — структура трёх фикстур. Identity env vars заменяют gateway `CLUSTER_*`.

### Story 2: HTTP Transport smoke + Bootstrap smoke + DI smoke

- **Why:** HTTP-слой тестируется через `fastapi.testclient.TestClient` (in-process, без реального сервера). `_clear_api_dependencies_cache()` перед каждым тестом — иначе singleton помнит env предыдущего теста.
- **Inputs:** Паттерн [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 2".
- **Outputs:**
  - `tests/test_bootstrap_smoke.py`:
    - `test_core_imports` — проверка импортов `core.config`, `core.api.asgi_app`, `core.api.dependencies`, `core.domain.contracts`, `core.providers.base`, `core.security.hashing`.
    - `test_app_config_from_env(monkeypatch)` — `DB_BACKEND=in_memory`, `EID_PROVIDER=mock` → `AppConfig.db_backend == "in_memory"`.
    - `test_config_fail_fast_on_invalid_backend` — `DB_BACKEND=postgres` → `ConfigError`.
    - `test_config_fail_fast_on_pilot_without_secrets` — `APP_PROFILE=pilot` без `OAUTH_ACCESS_TOKEN_SECRET` → `ConfigError`.
    - `test_config_fail_fast_on_pilot_empty_eid_secret` — `APP_PROFILE=pilot`, `DOGESTONIA_EID_SECRET=""` → `ConfigError` (interview 4.4).
    - `test_config_fail_fast_on_unknown_eid_provider` — `EID_PROVIDER=xyz` → `ConfigError`.
  - `tests/test_http_transport_smoke.py`:
    - autouse `_reset_deps` — `_clear_api_dependencies_cache()` до и после теста.
    - `test_health_returns_200` — `data.status == "ok"`.
    - `test_ready_returns_status` — `db_backend == "in_memory"`, `db_ready is True`.
    - `test_me_without_auth_returns_401` — `code == "AUTHENTICATION_REQUIRED"`.
    - `test_me_with_stub_bearer_returns_501` — пока handler stub: `code == "NOT_IMPLEMENTED"`.
    - `test_options_me_cors_preflight` — `status_code == 200`.
    - `test_trace_id_propagation` — заголовок `x-trace-id: custom` → есть в envelope.
    - `test_all_identity_routes_registered` — проверка что 14 paths из EPIC-IDS-02 Story 5 присутствуют в `app.routes`.
  - `tests/test_di_singleton.py`:
    - `test_singleton_is_same_object`.
    - `test_clear_cache_allows_recreation(monkeypatch)`.
    - `test_health_uses_singleton` — `r1` и `r2` идут через один и тот же DI.
  - `tests/test_di_service_factory.py`:
    - `test_factory_for_in_memory` — `provide_service_factory()` собирает InMemory-репозитории.
    - `test_factory_supabase_fallback_to_in_memory_without_epic5` — при `DB_BACKEND=supabase` без EPIC-IDS-05 фолбэк на InMemory + warning. **После EPIC-IDS-05** — заменяется на тест "raises ValueError without supabase creds".
    - `test_factory_returns_same_instance_for_same_repository_call` — singleton consistency.
  - `tests/test_eid_provider_registry.py`:
    - `test_mock_provider_registered_by_default`.
    - `test_get_active_returns_mock_when_eid_provider_mock`.
    - `test_get_unknown_provider_raises`.
    - `test_mock_provider_start_flow_creates_session` — через `InMemoryVerificationSessionStore`.
  - `tests/test_supabase_jwt_validator.py` (no network — синтетический JWT через `joserfc`):
    - `test_valid_token_returns_user_claims` — HMAC sign + decode.
    - `test_expired_token_raises_jwt_validation_error`.
    - `test_wrong_signature_raises`.
    - `test_alg_none_attack_rejected`.
    - `test_iss_mismatch_raises`.
- **Acceptance Criteria:**
  - Все 5 файлов smoke + DI + provider + validator проходят PASSED.
  - Тесты не делают сетевых вызовов (`TestClient` + in-memory только).
  - Общее время offline-сюиты < 30 секунд.
- **Pattern source:** [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 2" — `TestClient` + autouse reset (см. `tests/conftest.py` fixture `test_client`). Identity-тесты добавлены.

### Story 3: Live Supabase Integration тесты

- **Why:** Verifies реальный Supabase: connectivity, identity-таблицы, RLS policies, roundtrip. Без creds — `pytest.skip()` (не FAIL).
- **Inputs:**
  - Паттерн: [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 3".
  - Identity-таблицы: req-08 + req-17 + req-15.
- **Outputs:**
  - `tests/integration/supabase/__init__.py` (пустой).
  - `_require_supabase_creds_from_dotenv()` helper — парсит `.env` напрямую (минуя `_block_dotenv_leakage`).
  - `tests/integration/supabase/test_supabase_dotenv_connectivity.py`:
    - `test_supabase_connectivity` — `db.healthcheck() is True`.
    - `test_supabase_identity_tables_ready` — `db.required_tables_ready() is True` (для `profiles`, `eid_verification_sessions`, `eid_audit_events`, `story_drafts`).
    - `test_supabase_identity_columns_ready` — `db.required_columns_ready() is True`.
    - `test_supabase_provider_state_ready` — `db.provider_state_ready() is True` (req-17 миграция применена).
    - `test_supabase_service_role_policy` — `db.service_role_policy_probe() is True`.
  - `tests/integration/supabase/test_supabase_identity_roundtrip.py`:
    - `test_profile_upsert_and_read` — `SupabaseProfileRepository(db).upsert(ProfileRecord(...))` + `get_by_supabase_user_id(...)` — данные совпадают. UUID профиля генерится в тесте и удаляется в teardown.
    - `test_verification_session_create_and_consume` — create → mark_consumed → get_by_state возвращает session с `status="consumed"`.
    - `test_eid_audit_event_append` — log_event + list_events содержит новый event. Cleanup через DELETE по `request_id=test-...`.
    - `test_partial_unique_verified_person_hash` — первый `attach_eid_verification` успешен, второй с тем же `verified_person_hash` — `ProfileConflictError` (или 409). Cleanup.
  - Все тесты используют UUID4-генерированные ключи + teardown (DELETE) для cleanup.
- **Acceptance Criteria:**
  - Без `.env` с Supabase creds — все `live_integration` тесты SKIPPED (не FAILED).
  - С правильными creds (тестового, **не** production проекта) — все тесты PASSED.
  - После тестов в Supabase **не остаётся** новых profiles/sessions/events с `test-*` префиксами (cleanup работает).
  - Тесты используют **тестовый** Supabase проект (`SUPABASE_TEST_URL`, не production URL).
- **Pattern source:** [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 3" — паттерн `_require_supabase_creds_from_dotenv` + `pytest.skip()`. Identity-roundtrip — новый.

### Story 4: CI workflows — offline + live

- **Why:** Offline тесты на каждый push (~30 секунд), без сети. Live integration — только на `main` или `workflow_dispatch`, с GitHub Secrets.
- **Inputs:** [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 4".
- **Outputs:**
  - `.github/workflows/test-offline.yml`:
    - Triggers: `push`, `pull_request`.
    - Python 3.11, `pip install -e ".[dev]"`.
    - `python -m pytest -q -m "not live_integration" --tb=short`.
    - Upload pytest results as artifact.
  - `.github/workflows/integration-live.yml`:
    - Triggers: `push: branches: [main]`, `workflow_dispatch`.
    - Env: `SUPABASE_URL = ${{ secrets.SUPABASE_TEST_URL }}`, `SUPABASE_SERVICE_ROLE = ${{ secrets.SUPABASE_TEST_SERVICE_ROLE_KEY }}`, `SUPABASE_JWT_SECRET = ${{ secrets.SUPABASE_TEST_JWT_SECRET }}`, `DB_BACKEND = supabase`, `APP_PROFILE = demo`, `API_BASE_URL = https://test.local`, `EID_PROVIDER = mock`, `DOGESTONIA_EID_SECRET = ci-test-hash-secret`.
    - `python -m pytest -q -m live_integration -v`.
  - GitHub Secrets (документация в README/runbook):
    - `SUPABASE_TEST_URL`
    - `SUPABASE_TEST_SERVICE_ROLE_KEY`
    - `SUPABASE_TEST_JWT_SECRET`
- **Acceptance Criteria:**
  - `test-offline.yml` запускается на каждый push и PR.
  - `integration-live.yml` — только merge в `main` или ручной запуск.
  - В offline workflow нет `SUPABASE_*` secrets → live-тесты SKIPPED.
  - Offline workflow < 5 минут (setup + install + tests).
- **Pattern source:** [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 4" — YAML-структура. Identity env vars в `integration-live.yml`.

### Story 5: Smoke-тесты против живого сервера

- **Why:** Быстрая проверка после `make serve` или deploy. Не входят в стандартный pytest-run (отдельная директория `tests/smoke/`).
- **Inputs:**
  - [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 5".
  - Замена `GATEWAY_URL` → `IDENTITY_URL`, port 8000 → 8100.
- **Outputs:**
  - `tests/smoke/conftest.py`:
    - Marker `smoke`.
    - `@pytest.fixture(scope="session") def identity_url(): return os.environ.get("IDENTITY_URL", "http://localhost:8100").rstrip("/")`.
  - `tests/smoke/test_local_server_smoke.py`:
    - `test_health(identity_url)` — `httpx.get(f"{identity_url}/health")` → 200, `data.status == "ok"`.
    - `test_ready(identity_url)` — 200 или 503, response содержит `db_backend` и `db_ready`.
    - `test_me_without_auth(identity_url)` — 401, `error.code == "AUTHENTICATION_REQUIRED"`.
    - `test_options_me(identity_url)` — 200 (CORS preflight).
    - `test_options_oauth_authorize(identity_url)` — 200.
- **Acceptance Criteria:**
  - `IDENTITY_URL=http://localhost:8100 pytest tests/smoke/ -v` — PASSED при запущенном сервере (`make serve`).
  - Smoke тесты НЕ входят в `pytest tests/ -q` (`collect_ignore = ["smoke"]` в `tests/conftest.py`; `testpaths` остаётся `["tests"]`).
  - `IDENTITY_URL=https://identity.dogestonia.ee pytest tests/smoke/` работает против Railway deploy.
- **Pattern source:** [`docs/tech-requirements/impl-epic-06`](../../tech-requirements/impl-epic-06-testing-architecture.md) §"Story 5" — паттерн smoke conftest + env var. Замена URL и port.

## 7. Critical Pitfalls (identity-flavored)

- Без `_block_dotenv_leakage` тесты могут попасть в реальный Supabase — нарушение privacy invariants + flaky тесты.
- `core.api.asgi_app:app` — lazy (PEP 562 `__getattr__`); import модуля не вызывает `provide_app_config()` до первого доступа к `app` (audit F1).
- `_clear_api_dependencies_cache()` ДО теста (autouse fixture) — singleton создаётся при первом обращении.
- Live integration **MUST** использовать **отдельный тестовый** Supabase проект — не production. Защита: secrets named `*_TEST_*`.
- `pytest.skip()` при отсутствии creds — корректный паттерн. НИКОГДА не падать с FAILED при отсутствующих creds в live-тестах.
- `pythonpath = ["src", "tests"]` в `pyproject.toml` — критично для `import core.*` в тестах (EPIC-IDS-01).
- `CODE_VERIFIER_ENCRYPTION_KEY` в conftest — должен быть валидный base64 длиной 32 байта; иначе `cryptography` упадёт при первом обращении.
- Identity smoke тесты используют **IDENTITY_URL** и port 8100; не `GATEWAY_URL` / 8000.
- `_block_dotenv_leakage` задаёт `DOGESTONIA_EID_SECRET` — единственный HMAC-секрет (`ADR-IDS-008` пересмотр 2026-05-27); без dual env и fallback.
- В CI workflow `integration-live.yml` устанавливается `EID_PROVIDER=mock` — live-тесты Supabase не должны зависеть от eID-провайдер creds.

## 8. Верификация эпика

```bash
# 1. Все offline тесты проходят
python3.11 -m pytest tests/ -q -m "not live_integration"
# Ожидаемо: X passed in <30s

# 2. Live тесты пропускаются без creds
unset SUPABASE_URL SUPABASE_SERVICE_ROLE
python3.11 -m pytest tests/ -q -m live_integration
# Ожидаемо: X skipped

# 3. _block_dotenv_leakage эффективен (import-time config не крэшит collection)
DB_BACKEND=supabase SUPABASE_URL=https://prod.local python3.11 -m pytest tests/test_bootstrap_smoke.py --collect-only -q
DB_BACKEND=supabase SUPABASE_URL=https://prod.local python3.11 -m pytest tests/test_bootstrap_smoke.py -v
# Тесты всё равно используют DB_BACKEND=in_memory

# 4. CI offline workflow — после push коммита проверить через gh
gh run list --workflow=test-offline.yml --limit 1

# 5. Smoke against running server
make serve &
sleep 3
IDENTITY_URL=http://localhost:8100 python3.11 -m pytest tests/smoke/ -v
kill %1
```

## 9. Open Questions

- **mock OIDC сервер для тестов** — req-06 §"Шаг 2" markers содержит `mock_oidc` для тестов, требующих `docker run navikt/mock-oauth2-server`. В EPIC-IDS-06 — определены 5 tier-1 файлов тестов; mock_oidc тесты — задача функционального эпика (Authentigate provider implementation). Маркер существует в pyproject (EPIC-IDS-01), но тестов под ним пока нет.
- **Production-параметры smoke-тестов:** `IDENTITY_URL=https://identity.dogestonia.ee` — production URL ещё не задеплоен; smoke-тесты против production не запускаются автоматически. Story 5 — только local + CI.
- **`test_factory_supabase_fallback_to_in_memory_without_epic5`** vs **`test_factory_raises_without_supabase_creds`** — поведение `provide_service_factory` при `DB_BACKEND=supabase` без creds меняется между EPIC-IDS-04 (fallback + warning) и EPIC-IDS-05 (raise ValueError). Тест должен быть переключён при реализации EPIC-IDS-05. Зафиксировано в Story 2 как комментарий.
