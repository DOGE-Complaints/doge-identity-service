# EPIC-IDS-04 — SOA Service Factory

> **ID:** `EPIC-IDS-04`
> **Layer:** NFR / SOA Architecture
> **Статус:** Не реализовано
> **Зависит от:** EPIC-IDS-01 (AppConfig), EPIC-IDS-03 (ApiDependencies hooks)
> **Блокирует:** EPIC-IDS-05 (Supabase реализации Protocols), EPIC-IDS-06 (factory unit-тесты)

---

## 1. Назначение

Protocol-based SOA. Каждый репозиторий и провайдер — `Protocol` в `core/domain/contracts.py`. `DefaultServiceFactory(frozen=True)` принимает реализации (InMemory или Supabase) и собирает их в `ApiDependencies`. `provide_service_factory(config)` выбирает backend по `DB_BACKEND`. Смена backend = смена одной env var. Без этого эпика identity-сервис останется без auth-core, eID и OAuth сервисов.

## 2. Epic Goal

```python
from core.infrastructure.providers import provide_service_factory
from core.api.dependencies import build_api_dependencies

factory = provide_service_factory(config)
assert factory.config.db_backend == "in_memory"
assert factory.get_profile_repository() is not None
assert factory.get_eid_provider_registry().get("mock").provider_name == "mock"

deps = build_api_dependencies()
assert deps.profile_repository is not None
assert deps.verification_session_store is not None
assert deps.eid_provider_registry is not None
assert deps.bearer_token_auth is not None  # SupabaseJwtBearerTokenAuth теперь
```

После EPIC-IDS-04:
- Все Protocols определены, InMemory-реализации работают и проходят `isinstance(repo, ProtocolName)`.
- `EIDProviderRegistry` содержит `mock`-провайдер; `eideasy` и `authentigate` — заглушки до функциональных эпиков.
- `provide_service_factory` для `db_backend=supabase` — заглушка с TODO для EPIC-IDS-05.

## 3. Бизнес-контекст

Identity-сервис нуждается в нескольких Protocol-абстракциях:

| Protocol | Зачем | Источник |
|----------|-------|----------|
| `ProfileRepository` | CRUD профилей DOGEstonia пользователей с eID-статусом | req-08 §"profiles" |
| `VerificationSessionStore` | OAuth-state / OIDC-сессии (single-use, expiring) | req-08 §"eid_verification_sessions" + req-17 §"provider_session_data" |
| `EIDAuditLogRepository` | Immutable журнал eID-событий (17 типов) | req-08 §"eid_audit_events" + req-16 §"Audit Events" |
| `OAuthClientStore` | Зарегистрированные OAuth-клиенты (MVP — статический ChatGPT) | req-14 §"Registered OAuth Client" |
| `OAuthTokenService` | Issue/validate access tokens identity-сервиса | req-14 §"token_service.py" |
| `StoryDraftRepository` | Черновики story перед submit | req-15 §"story_drafts table" |
| `HealthRepository` | DB ping для `/ready` | req-16 §"Health и Readiness" |
| `EIDProviderPort` | Plug-in eID-провайдеры (mock, eideasy, authentigate) | req-17 §"base.py" |
| `BearerTokenAuth` | Supabase JWT validation header → UserClaims | req-09 §"FastAPI Dependency Pattern" |
| `SupabaseJwtValidator` | Низкоуровневый JWT decode (joserfc HS256) | req-09 §"supabase_validator.py" |

Все они должны быть взаимозаменяемы (InMemory ↔ Supabase) — это требование SOA архитектуры и условие тестируемости (см. EPIC-IDS-06 `_block_dotenv_leakage`).

## 4. Предусловия

- EPIC-IDS-01: `AppConfig`, `provide_app_config`.
- EPIC-IDS-03: `ApiDependencies` с зарезервированными `None`-полями, `_clear_api_dependencies_cache()`.

## 5. Целевые файлы

```
src/core/domain/contracts.py
src/core/infrastructure/repositories.py
src/core/application/factory.py
src/core/infrastructure/service_factory.py
src/core/infrastructure/providers.py
src/core/providers/__init__.py
src/core/providers/base.py
src/core/providers/registry.py
src/core/providers/mock/__init__.py
src/core/providers/mock/mock_provider.py
src/core/api/security.py            (update — добавить SupabaseJwtBearerTokenAuth)
src/core/auth/__init__.py
src/core/auth/supabase_validator.py
src/core/security/__init__.py
src/core/security/hashing.py
src/core/api/dependencies.py        (update — типизировать поля Protocol-ами, заменить build_api_dependencies)
```

## 6. Stories (заготовка)

### Story 1: Domain Protocols в `core/domain/contracts.py`

- **Why:** Единственный источник истины об интерфейсах репозиториев. Domain не импортирует httpx/sqlite/fastapi. Сервисы знают только Protocol — им всё равно какой backend (тестируемость + замена backend без касания application).
- **Inputs:**
  - Гatewey-паттерн Protocols + `@runtime_checkable`: [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 1".
  - Identity-домены: req-08 §миграции (поля таблиц = поля Protocol-методов), req-14 §"client_store" / "token_service", req-15 §"story_drafts table", req-17 §"EIDProviderPort", req-09 §"validate_supabase_jwt".
- **Outputs:**
  - `src/core/domain/contracts.py`:
    - `@runtime_checkable class HealthRepository(Protocol): def ping(self) -> bool: ...`
    - `@runtime_checkable class ProfileRepository(Protocol)`:
      - `def get_by_supabase_user_id(self, user_id: str) -> ProfileRecord | None`
      - `def get_by_verified_person_hash(self, hash_: str) -> ProfileRecord | None`
      - `def upsert(self, profile: ProfileRecord) -> ProfileRecord`
      - `def attach_eid_verification(self, user_id: str, *, provider: str, country: str, method: str, verified_person_hash: str, verified_at: datetime) -> ProfileRecord`
    - `@runtime_checkable class VerificationSessionStore(Protocol)`:
      - `def create(self, session: VerificationSession) -> VerificationSession`
      - `def get_by_state(self, state: str) -> VerificationSession | None`
      - `def mark_consumed(self, session_id: str) -> None`
      - `def mark_failed(self, session_id: str, reason: str) -> None`
      - `def expire_pending(self, now: datetime) -> int`
    - `@runtime_checkable class EIDAuditLogRepository(Protocol)`:
      - `def log_event(self, event: EIDAuditEvent) -> None`
      - `def list_events(self, *, supabase_user_id: str | None = None, event_type: str | None = None, limit: int = 100) -> list[EIDAuditEvent]`
    - `@runtime_checkable class OAuthClientStore(Protocol)`:
      - `def get_client(self, client_id: str) -> OAuthClient | None`
      - `def list_clients(self) -> list[OAuthClient]`
    - `@runtime_checkable class OAuthTokenService(Protocol)`:
      - `def issue_authorization_code(self, ...) -> str` (signature детализируется в req-14)
      - `def issue_access_token(self, ...) -> str`
      - `def validate_access_token(self, token: str) -> OAuthTokenClaims`
    - `@runtime_checkable class StoryDraftRepository(Protocol)`:
      - `def create(self, draft: StoryDraft) -> StoryDraft`
      - `def get(self, draft_id: str) -> StoryDraft | None`
      - `def update_status(self, draft_id: str, status: str) -> None`
    - `@runtime_checkable class SupabaseJwtValidator(Protocol)`:
      - `def validate(self, token: str) -> UserClaims` (raises `JwtValidationError`)
    - `@runtime_checkable class BearerTokenAuth(Protocol)`:
      - `def validate(self, headers: Mapping[str, str]) -> UserClaims` (raises `UnauthorizedError`)
  - `src/core/domain/models.py` (новый):
    - `@dataclass(frozen=True) class ProfileRecord`: поля из req-08 миграции 1.
    - `@dataclass(frozen=True) class VerificationSession`: поля из req-08 миграции 2 + `provider`, `provider_session_data` из req-17.
    - `@dataclass(frozen=True) class EIDAuditEvent`: req-08 миграция 3 + `event_type` enum из req-08 §"event_type значения".
    - `@dataclass(frozen=True) class OAuthClient`: client_id, client_secret_hash, redirect_uri, scopes (req-14).
    - `@dataclass(frozen=True) class OAuthTokenClaims`: sub, scopes, exp, client_id (req-14).
    - `@dataclass(frozen=True) class StoryDraft`: draft_id, supabase_user_id, payload, status, created_at, submitted_at (req-15).
    - `@dataclass(frozen=True) class UserClaims`: supabase_user_id, email, role (копия из req-09).
    - `class JwtValidationError(Exception)` — определяется здесь.
    - **`UnauthorizedError` (audit H-4):** НЕ определяется в `core.domain.models`. Единственный источник — `core.api.security` (EPIC-IDS-02 Story 3). `core.auth.*`, тесты и валидаторы всегда импортируют `from core.api.security import UnauthorizedError`. Exception handler в `asgi_app.py` ловит именно этот класс — двойное определение приведёт к "ловится не тот класс" и 500 вместо 401.
  - `EIDProviderPort`, `EIDVerificationResult`, `EIDStartResult` — определены в `src/core/providers/base.py` (Story 4), но `ApiDependencies.eid_provider_registry` хранит `EIDProviderRegistry`, не сам Protocol.
- **Acceptance Criteria:**
  - `from core.domain.contracts import ProfileRepository, VerificationSessionStore, ...` — без ошибок.
  - Все Protocols имеют `@runtime_checkable`.
  - `from core.domain.models import ProfileRecord, VerificationSession, EIDAuditEvent` — без ошибок.
  - Domain-слой (`core/domain/*`) не импортирует ничего из `core.infrastructure.*`, `httpx`, `fastapi`, `joserfc`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 1" — паттерн `@runtime_checkable Protocol + forward refs`. Identity-набор Protocols новый.

### Зависимость: `core/security/hashing.py` (interview 4.3)

Перед InMemory OAuth store — единый модуль HMAC:

```python
def hash_secret(plaintext: str, *, key: str) -> str:
    """HMAC-SHA256 hex digest; key передаётся явно (без global state)."""
```

Используется в `InMemoryOAuthClientStore.from_config` и позже в eID-провайдерах (req-13/14).

### Story 2: InMemory реализации

- **Why:** Все unit/service/HTTP-тесты идут через InMemory. Без них тесты бы трогали Supabase (нарушение инварианта EPIC-IDS-06). InMemory не имеет внешних зависимостей.
- **Inputs:**
  - Паттерн InMemory из [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 2".
  - Поведенческие требования: req-08 (state machine `started → consumed/failed/expired`), req-13 (1 eID = 1 account через unique `verified_person_hash`).
- **Outputs:**
  - `src/core/infrastructure/repositories.py`:
    - `InMemoryHealthRepository` — `ping() -> True`.
    - `InMemoryProfileRepository` — dict по `supabase_user_id`, secondary index по `verified_person_hash`; `attach_eid_verification` enforces unique hash (RuntimeError при коллизии).
    - `InMemoryVerificationSessionStore` — dict по `id`, index по `state`; `mark_consumed` идемпотентен; `expire_pending` сравнивает с now().
    - `InMemoryEIDAuditLogRepository` — append-only list.
    - `InMemoryOAuthClientStore` — static dict OAuth-клиентов. **Явный контракт (audit H-2):**

      ```python
      class InMemoryOAuthClientStore:
          def __init__(self, clients: dict[str, OAuthClient]) -> None:
              self._clients = clients

          @classmethod
          def from_config(cls, config: AppConfig) -> "InMemoryOAuthClientStore":
              """Build store with single GPT OAuth client from AppConfig.

              Используется в provide_service_factory(); единственная точка, где OAuthClient
              собирается из env. Все три gpt_oauth_* поля fallback'ятся на demo-значения,
              чтобы InMemory работал и в тестах без явных creds.
              """
              from core.security.hashing import hash_secret

              client = OAuthClient(
                  client_id=config.gpt_oauth_client_id or "test-gpt-client",
                  client_secret_hash=hash_secret(
                      config.gpt_oauth_client_secret or "demo",
                      key=config.oauth_access_token_secret or "demo-key",
                  ),
                  redirect_uri=config.gpt_oauth_redirect_uri or "",
                  scopes=["profile:read", "stories:draft", "stories:create"],
              )
              return cls(clients={client.client_id: client})

          def get_client(self, client_id: str) -> OAuthClient | None:
              return self._clients.get(client_id)

          def list_clients(self) -> list[OAuthClient]:
              return list(self._clients.values())
      ```

    - `InMemoryOAuthTokenService` — HMAC-SHA256 подпись через `config.oauth_access_token_secret`, in-memory issued codes для anti-replay.
    - `InMemoryStoryDraftRepository` — dict по `draft_id`.
- **Acceptance Criteria:**
  - `isinstance(InMemoryProfileRepository(), ProfileRepository)` — True (runtime Protocol check).
  - `InMemoryProfileRepository().attach_eid_verification(user_id="u1", ..., verified_person_hash="h")` + повторный вызов с тем же `hash` для другого `user_id` → RuntimeError (имитация unique index).
  - `InMemoryVerificationSessionStore().get_by_state("unknown")` → `None`.
  - `from core.security.hashing import hash_secret` — импортируется без ошибок; unit-тест на детерминизм (опционально, одна строка).
  - Все InMemory классы зависят только от stdlib + `core.security.hashing` (нет httpx, joserfc, fastapi импортов).
- **Pattern source:** [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 2" — паттерн dict + secondary index. Адаптация поведения под req-13 conflict detection.

### Story 3: `ServiceFactory(Protocol)` + `DefaultServiceFactory(frozen=True)`

- **Why:** Factory — единственный объект, который знает связи между сервисами. `frozen=True` гарантирует иммутабельность. Заглушки `return object()` уходят — реальные конструкторы.
- **Inputs:** Паттерн [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 3".
- **Outputs:**
  - `src/core/application/factory.py`:
    ```python
    class ServiceFactory(Protocol):
        @property
        def config(self) -> AppConfig: ...
        def get_health_repository(self) -> HealthRepository: ...
        def get_supabase_jwt_validator(self) -> SupabaseJwtValidator: ...
        def get_bearer_token_auth(self) -> BearerTokenAuth: ...
        def get_profile_repository(self) -> ProfileRepository: ...
        def get_verification_session_store(self) -> VerificationSessionStore: ...
        def get_eid_audit_log_repository(self) -> EIDAuditLogRepository: ...
        def get_eid_provider_registry(self) -> EIDProviderRegistry: ...
        def get_oauth_client_store(self) -> OAuthClientStore: ...
        def get_oauth_token_service(self) -> OAuthTokenService: ...
        def get_story_draft_repository(self) -> StoryDraftRepository: ...
    ```
  - `src/core/infrastructure/service_factory.py`:
    - `@dataclass(frozen=True) class DefaultServiceFactory`:
      - Fields: `config: AppConfig`, `health_repository: HealthRepository`, `profile_repository: ProfileRepository`, `verification_session_store: VerificationSessionStore`, `eid_audit_log_repository: EIDAuditLogRepository`, `oauth_client_store: OAuthClientStore`, `oauth_token_service: OAuthTokenService`, `story_draft_repository: StoryDraftRepository`, `supabase_jwt_validator: SupabaseJwtValidator`, `bearer_token_auth: BearerTokenAuth`, `eid_provider_registry: EIDProviderRegistry`.
      - Методы `get_*()` — возвращают соответствующее поле.
- **Acceptance Criteria:**
  - `DefaultServiceFactory(...).config` — возвращает переданный `AppConfig`.
  - `factory.get_profile_repository() is factory.get_profile_repository()` — True (same instance, factory не плодит копии).
  - `factory.something = "x"` → `FrozenInstanceError`.
  - `ServiceFactory` — `Protocol`, не базовый класс; `DefaultServiceFactory` его удовлетворяет.
- **Pattern source:** [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 3" — структура `dataclass(frozen=True)` + методы `get_*()`.

### Story 4: eID Provider Port + Registry + Mock Provider

- **Why:** Identity-сервис должен поддерживать минимум 3 eID-провайдера (req-17 §"Plugin архитектура"). `EIDProviderPort` Protocol изолирует HTTP-слой от провайдер-специфичных деталей (PKCE/OAuth2). `EIDProviderRegistry` выбирает активный провайдер по `config.eid_provider`. Mock-провайдер позволяет работать локально без credentials (req-17 §"Mock провайдер").
- **Inputs:**
  - Спека Port + Registry + Mock: [`docs/requirements/17-eid-provider-abstraction.md`](../../requirements/17-eid-provider-abstraction.md) §"base.py", §"registry.py", §"Mock провайдер".
  - Mock callback path: req-17 §"Provider callbacks" — `/auth/mock/callback`.
- **Outputs:**
  - `src/core/providers/base.py`:
    - `@dataclass(frozen=True) class EIDVerificationResult`: provider, country, subject_hash, login_method, verified_at.
    - `@dataclass class EIDStartResult`: redirect_url, session_id, expires_at.
    - `@runtime_checkable class EIDProviderPort(Protocol)` — `provider_name`, `callback_path` properties + `start_flow(...)`, `handle_callback(...)`.
    - `class EIDProviderError(Exception)` с `code: str`.
  - `src/core/providers/registry.py`:
    - `class EIDProviderRegistry`:
      - Конструктор принимает `dict[str, EIDProviderPort]` (mock всегда; eideasy/authentigate — опционально, регистрируются если cred-vars в `AppConfig`).
      - `def get(self, name: str) -> EIDProviderPort` — KeyError если нет.
      - `def get_active(self, config: AppConfig) -> EIDProviderPort` — читает `config.eid_provider`.
    - **Не `@lru_cache`**: per-request lookup через `deps.eid_provider_registry`.
  - `src/core/providers/mock/mock_provider.py`:
    - `class MockEIDProvider`:
      - `provider_name == "mock"`, `callback_path == "/auth/mock/callback"`.
      - `start_flow` — создаёт session в `verification_session_store`, возвращает `EIDStartResult` с `redirect_url=/auth/mock/callback?session_id=...`.
      - `handle_callback` — возвращает фиктивный `EIDVerificationResult(provider="mock", country="EE", subject_hash="mock-..." + secrets.token_hex(8), ...)`.
- **Acceptance Criteria:**
  - `isinstance(MockEIDProvider(...), EIDProviderPort)` — True.
  - `EIDProviderRegistry({"mock": MockEIDProvider(...)}).get("mock").provider_name == "mock"`.
  - `EIDProviderRegistry({}).get_active(config_with_eid_provider_eideasy)` → `KeyError` (или `EIDProviderError` — выбрать; решение фиксируется здесь).
  - При `config.eid_provider == "mock"` flow проходит без EIDEASY_*/AUTHENTIGATE_* (req-17 acceptance).
- **Forward (interview 4.6):** при HTTP к Authentigate/eID Easy — `httpx` timeout=`config.oidc_request_timeout_s` (EPIC-IDS-01). `MockEIDProvider` — без внешних HTTP.
- **Pattern source:** [`docs/requirements/17-eid-provider-abstraction.md`](../../requirements/17-eid-provider-abstraction.md) §"base.py" / §"registry.py" / §"Mock провайдер". Полная адаптация к Plugin-архитектуре — нет аналога в gateway tech-requirements.

### Story 5: Supabase JWT validator + `SupabaseJwtBearerTokenAuth`

- **Why:** EPIC-IDS-02 ввёл `StubBearerTokenAuth`. Здесь приходит реальный валидатор Supabase JWT через `joserfc`. Это закрывает auth-цепочку: `Authorization: Bearer <supabase_jwt> → validate → UserClaims → FastAPI Depends(get_current_user)`.
- **Inputs:**
  - Спека: [`docs/requirements/09-supabase-jwt-validation.md`](../../requirements/09-supabase-jwt-validation.md) §"Спецификация модуля" + §"Реализация (псевдокод с joserfc)".
  - Безопасность: req-09 §"Атака на `alg: none`" — `algorithms=["HS256"]` явно.
- **Outputs:**
  - `src/core/auth/supabase_validator.py`:
    - `@dataclass(frozen=True) class UserClaims` — переэкспорт из `core.domain.models`.
    - `class JwtValidationError(Exception)`.
    - `class SupabaseJwtValidatorImpl`:
      - `__init__(self, *, jwt_secret: str, supabase_url: str)`.
      - `def validate(self, token: str) -> UserClaims` — joserfc, HS256, проверка `iss`, `sub`, `exp`, `role=="authenticated"`.
  - `src/core/api/security.py` (обновление из EPIC-IDS-02):
    - `class SupabaseJwtBearerTokenAuth`:
      - `__init__(self, *, validator: SupabaseJwtValidator)`.
      - `def validate(self, headers: Mapping[str, str]) -> UserClaims` — парсит `Authorization`, делегирует валидатору, переводит `JwtValidationError` в `UnauthorizedError("AUTHENTICATION_REQUIRED")`.
    - `def get_current_user(request, deps) -> UserClaims` — обновление: использует `deps.bearer_token_auth` (полиморфно). Поведение совместимо с `StubBearerTokenAuth` для тестов до закрытия валидатора.
- **Acceptance Criteria (audit C-3 — переписаны под класс-реализацию, не под несуществующую standalone-функцию):**
  - `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(valid_token)` → `UserClaims` с корректным `supabase_user_id` (req-09 acceptance).
  - `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(expired_token)` raises `JwtValidationError` (req-09 acceptance).
  - `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(alg_none_token)` raises `JwtValidationError` (req-09 §"Атака на alg: none").
  - `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(token_with_iss_mismatch)` raises `JwtValidationError`.
  - `SupabaseJwtBearerTokenAuth(validator=...)` корректно конвертирует `JwtValidationError` → `UnauthorizedError(code="AUTHENTICATION_REQUIRED")`.
  - `GET /me` с валидным токеном — `bearer_token_auth.validate(headers)` возвращает `UserClaims`; `/me` остаётся stub до функционального эпика, но 401 больше не возвращается.
- **Pattern source:** [`docs/requirements/09-supabase-jwt-validation.md`](../../requirements/09-supabase-jwt-validation.md) §"Спецификация модуля" + §"Реализация (псевдокод с joserfc)". Полностью identity-specific. Тесты EPIC-IDS-06 Story 2 (`tests/test_supabase_jwt_validator.py`) реализуют именно класс-форму.

### Story 6: `provide_service_factory()` — backend selection + интеграция в `build_api_dependencies`

- **Why:** Единственная точка, где `DB_BACKEND` решает какие реализации брать. Все остальные модули не знают про backend.
- **Inputs:** Паттерн [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 4".
- **Outputs:**
  - `src/core/infrastructure/providers.py`:
    ```python
    def provide_service_factory(config: AppConfig | None = None) -> ServiceFactory:
        resolved_config = config or provide_app_config()
        # 1. Build repositories по DB_BACKEND
        if resolved_config.db_backend == "in_memory":
            profile_repository = InMemoryProfileRepository()
            verification_session_store = InMemoryVerificationSessionStore()
            eid_audit_log_repository = InMemoryEIDAuditLogRepository()
            health_repository = InMemoryHealthRepository()
            oauth_client_store = InMemoryOAuthClientStore.from_config(resolved_config)
            story_draft_repository = InMemoryStoryDraftRepository()
        elif resolved_config.db_backend == "supabase":
            # TODO EPIC-IDS-05: SupabaseProfileRepository, ... через SupabaseDatabase.from_http(...)
            # Пока — фолбэк на InMemory + лог-предупреждение (db_ready=False вычисляется отдельно)
            ...
        else:
            raise ValueError(f"Unsupported db_backend: {resolved_config.db_backend}")

        # 2. Build OAuth token service (всегда HMAC, не зависит от backend)
        oauth_token_service = InMemoryOAuthTokenService(config=resolved_config)

        # 3. Build auth
        supabase_jwt_validator = SupabaseJwtValidatorImpl(
            jwt_secret=resolved_config.supabase_jwt_secret or "test-secret-for-demo",
            supabase_url=resolved_config.supabase_url or "https://demo.local",
        )
        bearer_token_auth = SupabaseJwtBearerTokenAuth(validator=supabase_jwt_validator)

        # 4. Build eID provider registry
        registry = EIDProviderRegistry({"mock": MockEIDProvider(verification_session_store)})
        # TODO functional epic: register eideasy/authentigate when AppConfig has creds

        return DefaultServiceFactory(
            config=resolved_config,
            health_repository=health_repository,
            profile_repository=profile_repository,
            verification_session_store=verification_session_store,
            eid_audit_log_repository=eid_audit_log_repository,
            oauth_client_store=oauth_client_store,
            oauth_token_service=oauth_token_service,
            story_draft_repository=story_draft_repository,
            supabase_jwt_validator=supabase_jwt_validator,
            bearer_token_auth=bearer_token_auth,
            eid_provider_registry=registry,
        )
    ```
  - `src/core/api/dependencies.py` (обновление):
    - `build_api_dependencies()` использует `provide_service_factory()` и заполняет все identity-поля `ApiDependencies` (вместо `None`).
    - Типы полей `ApiDependencies` уточняются с `object | None` до конкретных Protocol-типов.
  - `src/core/api/asgi_app.py` — без изменений (singleton hook не меняется).
- **Acceptance Criteria:**
  - `provide_service_factory()` при `DB_BACKEND=in_memory` возвращает `DefaultServiceFactory` с InMemory-репозиториями.
  - `provide_service_factory(config_with_supabase)` — fallback на InMemory + warning (до EPIC-IDS-05), не падает.
  - `build_api_dependencies().profile_repository is not None` (после EPIC-IDS-04 уже не `None`).
  - `build_api_dependencies().eid_provider_registry.get("mock").provider_name == "mock"`.
  - `build_api_dependencies().bearer_token_auth.__class__.__name__ == "SupabaseJwtBearerTokenAuth"`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-04`](../../tech-requirements/impl-epic-04-soa-service-factory.md) §"Story 4" — паттерн `if/elif db_backend` + сборка `DefaultServiceFactory`. Identity-набор сервисов — новый.

## 7. Critical Pitfalls (identity-flavored)

- Protocol не базовый класс — `isinstance(obj, ProfileRepository)` требует `@runtime_checkable`. Type-checking — через pyright/mypy.
- `DefaultServiceFactory.get_*()` возвращает **тот же** объект — не пересоздавать (InMemory state must be shared).
- `EIDProviderRegistry` НЕ `@lru_cache` — provider выбирается per request через `deps.eid_provider_registry.get_active(config)` (req-17 правило).
- Domain (`core/domain/*`) не должен импортировать `infrastructure.*`, `httpx`, `fastapi`, `joserfc` — иначе circular import + смешение слоёв.
- При `DB_BACKEND=supabase` без EPIC-IDS-05 — fallback на InMemory + warning, **не raise**, чтобы EPIC-IDS-04 можно было верифицировать в изоляции.
- `MockEIDProvider` использует `verification_session_store` через DI — не хранит state в себе (иначе тесты теряют изоляцию).
- В `SupabaseJwtValidatorImpl` `algorithms=["HS256"]` хардкод, иначе `alg: none` attack (req-09 §"Атака на alg: none").
- `code_verifier_encryption_key` (AES) **не** используется в этом эпике — он нужен Authentigate-провайдеру (функциональный эпик), не Mock и не eID Easy.

## 8. Верификация эпика

```bash
# 1. Импорты
python3.11 -c "
from core.domain.contracts import ProfileRepository, VerificationSessionStore, EIDAuditLogRepository, OAuthClientStore, OAuthTokenService, StoryDraftRepository, BearerTokenAuth, SupabaseJwtValidator
from core.infrastructure.repositories import InMemoryProfileRepository
from core.infrastructure.service_factory import DefaultServiceFactory
from core.infrastructure.providers import provide_service_factory
from core.providers.base import EIDProviderPort, EIDVerificationResult, EIDStartResult
from core.providers.registry import EIDProviderRegistry
from core.providers.mock.mock_provider import MockEIDProvider
from core.auth.supabase_validator import SupabaseJwtValidatorImpl, JwtValidationError
from core.api.security import SupabaseJwtBearerTokenAuth
print('Imports OK')
"

# 2. runtime Protocol check
python3.11 -c "
from core.domain.contracts import ProfileRepository
from core.infrastructure.repositories import InMemoryProfileRepository
assert isinstance(InMemoryProfileRepository(), ProfileRepository)
print('Protocol isinstance OK')
"

# 3. Factory создаётся
python3.11 -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://localhost:8100', 'DB_BACKEND': 'in_memory', 'EID_PROVIDER': 'mock'})
from core.infrastructure.providers import provide_service_factory
f = provide_service_factory()
print('db_backend:', f.config.db_backend)
print('mock provider:', f.get_eid_provider_registry().get('mock').provider_name)
print('Factory OK')
"

# 4. build_api_dependencies интеграция
python3.11 -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://localhost:8100', 'DB_BACKEND': 'in_memory', 'EID_PROVIDER': 'mock'})
from core.api.dependencies import build_api_dependencies
d = build_api_dependencies()
assert d.profile_repository is not None
assert d.eid_provider_registry is not None
assert type(d.bearer_token_auth).__name__ == 'SupabaseJwtBearerTokenAuth'
print('DI integration OK')
"

# 5. Tests (после EPIC-IDS-06)
python3.11 -m pytest tests/test_di_service_factory.py -v
```

## 9. Open Questions

- **`code_verifier_encryption_key`** AES-helper — нужен для Authentigate-провайдера, который не реализуется в EPIC-IDS-04. Решение: добавить отдельный модуль `core/auth/code_verifier_cipher.py` в EPIC-IDS-04 (заглушка с TODO) или отложить до функционального эпика. Парковка: на P1 функционального плана. В EPIC-IDS-04 — не реализуется.
- **`InMemoryOAuthTokenService` vs `JwtBackedOAuthTokenService`** — req-14 §"Access Token Format" описывает JWT с HMAC-SHA256. `InMemory*` имя может ввести в заблуждение: реально это JWT-stateless, in-memory только anti-replay set для authorization codes. Решить именование на P1.
- **Authentigate провайдер** — README-index §"Открытые вопросы": "Authentigate остаётся как второй провайдер в архитектуре (файл 17). Реализовать `authentigate/provider.py` при получении credentials от SK ID Solutions." В EPIC-IDS-04 — не реализуется.
