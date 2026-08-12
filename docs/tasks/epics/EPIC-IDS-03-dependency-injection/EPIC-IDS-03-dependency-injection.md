# EPIC-IDS-03 — Dependency Injection

> **ID:** `EPIC-IDS-03`
> **Layer:** NFR / DI Container
> **Статус:** Не реализовано
> **Зависит от:** EPIC-IDS-01 (AppConfig), EPIC-IDS-02 (`asgi_app.py`, `StubBearerTokenAuth`, `get_api_dependencies()` stub)
> **Блокирует:** EPIC-IDS-04 (расширение полей), EPIC-IDS-05 (db_checks integration), EPIC-IDS-06 (singleton smoke test)

---

## 1. Назначение

Manual singleton DI без IoC-контейнера: `ApiDependencies(frozen=True)` dataclass содержит все сервисы и состояние, `build_api_dependencies()` строит его один раз, `@lru_cache(maxsize=1)` гарантирует singleton per process, FastAPI роуты получают его через `Depends(get_api_dependencies)`. В этом эпике вводятся **идентити-специфичные слоты** (заглушки), а реальные сервисы инжектятся в EPIC-IDS-04 (SOA factory) и EPIC-IDS-05 (Supabase healthchecks).

## 2. Epic Goal

```python
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache

d1 = get_api_dependencies()
d2 = get_api_dependencies()
assert d1 is d2                              # singleton
assert d1.config.port == 8100                # config из EPIC-IDS-01
assert d1.bearer_token_auth is not None      # из EPIC-IDS-02
assert d1.db_backend in ("in_memory", "supabase")  # sqlite removed per audit H-3 / ADR-IDS-008 context
assert isinstance(d1.db_checks, dict)
# d1.profile_repository, d1.verification_session_store, ... — None в этом эпике; заполнятся в EPIC-IDS-04
```

После EPIC-IDS-03:
- `_clear_api_dependencies_cache()` существует и работает в тестах.
- Lifespan вызывает `get_api_dependencies()` при startup — singleton инициализируется один раз.
- Все hooks для EPIC-IDS-04 определены (`# TODO EPIC-IDS-04` маркеры на закомментированных полях/инициализациях).

## 3. Бизнес-контекст

Identity-service не имеет `story_intake_service`, `cluster_*`, `issue_*` — это gateway-сущности. Целевой набор полей `ApiDependencies` (определяется в Story 3 этого эпика, реализуется в EPIC-IDS-04):

| Поле | Тип (контракт) | Источник требования |
|------|----------------|---------------------|
| `config: AppConfig` | EPIC-IDS-01 | required |
| `bearer_token_auth: BearerTokenAuth` | EPIC-IDS-02 Protocol | req-09 §"FastAPI Dependency Pattern" |
| `db_backend: str` | this epic | req-08 readiness |
| `db_ready: bool` | this epic | req-08 readiness |
| `db_checks: dict[str, bool]` | this epic, заполняется в EPIC-IDS-05 | req-08 §"Readiness check" |
| `supabase_jwt_validator: SupabaseJwtValidator \| None` | EPIC-IDS-04 | req-09 |
| `profile_repository: ProfileRepository \| None` | EPIC-IDS-04 | req-08 |
| `verification_session_store: VerificationSessionStore \| None` | EPIC-IDS-04 | req-08 + req-17 |
| `eid_audit_log_repository: EIDAuditLogRepository \| None` | EPIC-IDS-04 | req-08 + req-16 §"Audit Events" |
| `eid_provider_registry: EIDProviderRegistry \| None` | EPIC-IDS-04 | req-17 §"registry.py" |
| `oauth_client_store: OAuthClientStore \| None` | EPIC-IDS-04 | req-14 §"Registered OAuth Client" |
| `oauth_token_service: OAuthTokenService \| None` | EPIC-IDS-04 | req-14 §"token_service.py" |
| `story_draft_repository: StoryDraftRepository \| None` | EPIC-IDS-04 | req-15 §"story_drafts table" |

В EPIC-IDS-03 — поля **только зарезервированы как Optional/закомментированы**, реальные значения — после EPIC-IDS-04.

## 4. Предусловия

- EPIC-IDS-01: `AppConfig`, `provide_app_config`.
- EPIC-IDS-02: `asgi_app.py` со stub singleton, `StubBearerTokenAuth`, lifespan который форсирует singleton.

## 5. Целевые файлы

```
src/core/api/dependencies.py          (new)
src/core/api/asgi_app.py              (update — импорт build_api_dependencies из core.api.dependencies)
src/core/api/__init__.py              (update — экспорт ApiDependencies, build_api_dependencies)
tests/test_di_singleton.py            (new — будет создан в EPIC-IDS-06; в этом эпике — только указан как target)
```

## 6. Stories (заготовка)

### Story 1: `ApiDependencies` dataclass + `HandlerDependencies` alias

- **Why:** `ApiDependencies` — единственный контейнер, который видит HTTP-слой. `frozen=True` предотвращает случайную мутацию shared state. Алиас `HandlerDependencies = ApiDependencies` нужен для имени, используемого в handlers (паттерн gateway).
- **Inputs:** Паттерн dataclass из [`docs/tech-requirements/impl-epic-03`](../../tech-requirements/impl-epic-03-dependency-injection.md) §"Story 1", Task 1.1.
- **Outputs:**
  - `src/core/api/dependencies.py`:
    ```python
    @dataclass(frozen=True)
    class ApiDependencies:
        # ── Always present ──────────────────────────────────────────────
        config: AppConfig
        bearer_token_auth: BearerTokenAuth  # Protocol from core.api.security

        # ── DB state ───────────────────────────────────────────────────
        db_backend: str
        db_ready: bool
        db_checks: dict[str, bool] = field(default_factory=dict)

        # ── Identity services (None в EPIC-IDS-03, заполняются в EPIC-IDS-04) ──
        supabase_jwt_validator: object | None = None
        profile_repository: object | None = None
        verification_session_store: object | None = None
        eid_audit_log_repository: object | None = None
        eid_provider_registry: object | None = None
        oauth_client_store: object | None = None
        oauth_token_service: object | None = None
        story_draft_repository: object | None = None

    HandlerDependencies = ApiDependencies
    ```
  - Поля типизированы как `object | None` — реальные типы вводятся в EPIC-IDS-04 (когда определены Protocols).
- **Acceptance Criteria:**
  - `from core.api.dependencies import ApiDependencies, HandlerDependencies`.
  - `HandlerDependencies is ApiDependencies` — True.
  - `ApiDependencies(config=..., bearer_token_auth=..., db_backend="in_memory", db_ready=True)` — конструируется; все identity-сервисы дефолтятся в `None`.
  - Попытка `deps.config = new_config` → `FrozenInstanceError`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-03`](../../tech-requirements/impl-epic-03-dependency-injection.md) §"Story 1" — структура dataclass. Удалены поля `service_auth` (заменено на `bearer_token_auth`), `story_intake_service`, `story_cluster_orchestrator`, `issue_create_service`, `issue_projection_read_store` — gateway-сущности отсутствуют.

### Story 2: `build_api_dependencies()` + `@lru_cache` singleton + lifespan integration

- **Why:** Один процесс — один объект `ApiDependencies`. `@lru_cache(maxsize=1)` обеспечивает per-process кеширование. `_clear_api_dependencies_cache()` нужен в тестах для пересоздания singleton после `monkeypatch.setenv()`. Lifespan форсирует создание singleton на startup — иначе первый запрос медленнее + startup-логи (`db_ready`, `backend=...`) не появятся.
- **Inputs:** Singleton pattern из [`docs/tech-requirements/impl-epic-03`](../../tech-requirements/impl-epic-03-dependency-injection.md) §"Story 2".
- **Outputs:**
  - `src/core/api/dependencies.py`:
    ```python
    def build_api_dependencies() -> ApiDependencies:
        """
        Build the DI container. Called once per process via lru_cache (in asgi_app).
        Steps:
          1. provide_app_config() — reads env + .env.
          2. Build StubBearerTokenAuth (will be replaced by SupabaseJwtBearerTokenAuth in EPIC-IDS-04).
          3. Compute db_backend, db_ready, db_checks (Supabase healthchecks added in EPIC-IDS-05).
          4. Identity services left as None — populated in EPIC-IDS-04.
        """
        config = provide_app_config()
        bearer_token_auth = StubBearerTokenAuth()  # replaced in EPIC-IDS-04
        db_backend = config.db_backend
        db_checks: dict[str, bool] = {}
        db_ready = True
        # TODO EPIC-IDS-05: if db_backend == "supabase": run 5-level healthchecks
        return ApiDependencies(
            config=config,
            bearer_token_auth=bearer_token_auth,
            db_backend=db_backend,
            db_ready=db_ready,
            db_checks=db_checks,
        )
    ```
  - `src/core/api/asgi_app.py` (update из EPIC-IDS-02):
    - `from core.api.dependencies import ApiDependencies, build_api_dependencies` — заменить временную stub-функцию.
    - `@lru_cache(maxsize=1) def _cached_dependencies() -> ApiDependencies: return build_api_dependencies()`.
    - `def _clear_api_dependencies_cache() -> None: _cached_dependencies.cache_clear()`.
    - `def get_api_dependencies() -> ApiDependencies: return _cached_dependencies()`.
    - В `_lifespan`: только warmup DI + logging — `deps = get_api_dependencies(); configure_logging(...)`. **CORS** — в `create_app(config)` (EPIC-IDS-02 Story 4), не в lifespan.
    - Module-level `app = create_app(provide_app_config())` (EPIC-IDS-02).
- **Acceptance Criteria:**
  - `get_api_dependencies() is get_api_dependencies()` — True.
  - После `_clear_api_dependencies_cache()` следующий вызов создаёт новый объект (другое `id()`).
  - `monkeypatch.setenv("LOG_LEVEL", "DEBUG"); _clear_api_dependencies_cache(); get_api_dependencies().config.log_level == "DEBUG"`.
  - При startup сервера лог содержит запись `configure_logging` уровня deps.config.log_level (см. lifespan).
  - Два параллельных HTTP запроса получают один и тот же `ApiDependencies` (verifiable через `id()` логирование).
- **Pattern source:** [`docs/tech-requirements/impl-epic-03`](../../tech-requirements/impl-epic-03-dependency-injection.md) §"Story 2" — копия с заменой gateway-Supabase секции на TODO для EPIC-IDS-05.

### Story 3: Hook расширения для EPIC-IDS-04 — контракт

- **Why:** Зафиксировать заранее, **как** `build_api_dependencies()` будет интегрирован с `provide_service_factory()` из EPIC-IDS-04. Это снижает риск разрыва контракта между эпиками: EPIC-IDS-04 не будет придумывать новые поля, EPIC-IDS-03 знает что готовить.
- **Inputs:**
  - Целевой код после EPIC-IDS-04 описан в [`docs/tech-requirements/impl-epic-03`](../../tech-requirements/impl-epic-03-dependency-injection.md) §"Story 3" — паттерн взаимодействия `service_factory ↔ build_api_dependencies`.
  - Identity-сервисы — список из секции 3 этого эпика.
- **Outputs (документация-контракт, реальный код в EPIC-IDS-04):**
  - В `build_api_dependencies()` появится:
    ```python
    # EPIC-IDS-04 will replace this block:
    from core.infrastructure.providers import provide_service_factory
    service_factory = provide_service_factory(config)
    return ApiDependencies(
        config=config,
        bearer_token_auth=service_factory.get_bearer_token_auth(),  # SupabaseJwtBearerTokenAuth
        db_backend=config.db_backend,
        db_ready=db_ready,
        db_checks=db_checks,
        supabase_jwt_validator=service_factory.get_supabase_jwt_validator(),
        profile_repository=service_factory.get_profile_repository(),
        verification_session_store=service_factory.get_verification_session_store(),
        eid_audit_log_repository=service_factory.get_eid_audit_log_repository(),
        eid_provider_registry=service_factory.get_eid_provider_registry(),
        oauth_client_store=service_factory.get_oauth_client_store(),
        oauth_token_service=service_factory.get_oauth_token_service(),
        story_draft_repository=service_factory.get_story_draft_repository(),
    )
    ```
  - В `ApiDependencies` (EPIC-IDS-04 апгрейд) типы `object | None` заменяются на конкретные Protocol-типы из `core.domain.contracts`.
- **Acceptance Criteria (документация):**
  - В EPIC-IDS-03 — комментарии `# TODO EPIC-IDS-04: replace with provide_service_factory(...)` стоят над хардкодным `StubBearerTokenAuth()`.
  - В EPIC-IDS-03 — комментарии `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks` стоят над `db_checks: dict[str, bool] = {}`.
  - Список целевых полей в Story 1 совпадает с тем, что EPIC-IDS-04 реализует через `provide_service_factory`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-03`](../../tech-requirements/impl-epic-03-dependency-injection.md) §"Story 3" — секция "Расширение для сервисов (Epic 04 hook)" из gateway-template.

## 7. Critical Pitfalls (identity-flavored)

- `lru_cache` кешируется на всё время процесса — при тестах нужно вызывать `_clear_api_dependencies_cache()` ДО первого теста с другим env.
- Если lifespan НЕ вызывает `get_api_dependencies()` при старте — DI инициализируется при первом запросе (медленнее + startup-логи не появятся).
- `frozen=True` на dataclass предотвращает мутацию сервисов — не убирать.
- Не добавлять mutable state в `ApiDependencies` — это shared singleton; коллекции должны быть либо `frozenset/tuple`, либо иммутабельно копироваться при чтении.
- `HandlerDependencies = ApiDependencies` — backward-compatibility alias, не удалять.
- НЕ копировать gateway-поля (`story_intake_service`, `cluster_*`, `issue_*`) — идентити-сервис их не использует.
- В identity-сервисе **нет `service_api_token`** auth-паттерна (как в gateway). Auth — через Supabase JWT (req-09), значит `bearer_token_auth` (Protocol), не `service_auth` (token compare).

## 8. Верификация эпика

```bash
# 1. Импорт DI
python3.11 -c "
from core.api.dependencies import ApiDependencies, HandlerDependencies, build_api_dependencies
assert HandlerDependencies is ApiDependencies
print('DI imports OK')
"

# 2. Singleton создаётся
python3.11 -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://localhost:8100', 'DB_BACKEND': 'in_memory', 'EID_PROVIDER': 'mock'})
from core.api.dependencies import build_api_dependencies
d = build_api_dependencies()
print('db_backend:', d.db_backend)
print('db_ready:', d.db_ready)
print('config.port:', d.config.port)
print('bearer_token_auth:', type(d.bearer_token_auth).__name__)
print('profile_repository:', d.profile_repository)  # None в этом эпике
"

# 3. Singleton identity
python3.11 -c "
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
_clear_api_dependencies_cache()
d1 = get_api_dependencies()
d2 = get_api_dependencies()
assert d1 is d2, 'must be singleton'
print('singleton OK')
"

# 4. Frozen
python3.11 -c "
from dataclasses import FrozenInstanceError
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
_clear_api_dependencies_cache()
d = get_api_dependencies()
try:
    d.db_backend = 'x'
    assert False
except FrozenInstanceError:
    print('frozen OK')
"

# 5. Tests (после EPIC-IDS-06)
python3.11 -m pytest tests/test_di_singleton.py -v
```

## 9. Open Questions

- В этом эпике используется `StubBearerTokenAuth` из EPIC-IDS-02. EPIC-IDS-04 заменит на `SupabaseJwtBearerTokenAuth` — но если функциональный эпик (Auth Core) реализуется параллельно, нужно явно зафиксировать порядок: bearer auth — после `EIDProviderRegistry`, или вместе с ним. Парковка до P1 функционального плана.
- Если `db_backend=supabase`, но `db_ready=False` (Supabase недоступен на старте) — сервер всё равно поднимается (паттерн "no crashloop, degraded ready"). Это решение фиксируется здесь и используется в EPIC-IDS-05.
