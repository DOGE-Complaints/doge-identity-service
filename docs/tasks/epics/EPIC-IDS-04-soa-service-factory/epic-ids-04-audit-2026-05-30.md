# Аудит EPIC-IDS-04 — SOA Service Factory

> **Дата:** 2026-05-30
> **Методология:** [`analysis.mdc`](../../.cursor/rules/analysis.mdc) — только верифицированные факты с путями и строками
> **Предмет:** AC каждой Story vs фактический код; регрессии vs EPIC-IDS-03; gaps с severity
> **Статус эпика по итогам:** 🔴 REGRESSION — 2 теста из `test_api_dependencies.py` FAIL

---

## Сводная таблица findings

| ID | Story | Severity | Тип | Суть | Статус |
|----|-------|----------|-----|------|--------|
| RG-1 | S6 / t03 | HIGH | Регрессия | `test_build_api_dependencies_has_epic_hook_comments` — ищет удалённый TODO-комментарий | ⚪ Open |
| RG-2 | S6 / t03 | HIGH | Регрессия | `test_build_api_dependencies_zero_arg` — expects `profile_repository is None`, теперь filled | ⚪ Open |
| S5-1 | S5 | MEDIUM | Дизайн | `BearerTokenAuth` Protocol определён дважды — в `security.py` И в `contracts.py` | ⚪ Open |
| S2-1 | S2 | MEDIUM | Покрытие | `InMemoryOAuthTokenService.issue_access_token` игнорирует `client_secret` без документации | ⚪ Open |
| S1-2 | S1 | LOW | Модель | Мутируемые `list` поля в `frozen=True` dataclasses (`scopes`) | ⚪ Open |
| S5-2 | S5 | LOW | Код | Двойная `iss`-валидация в `SupabaseJwtValidatorImpl` (redundant explicit check) | ⚪ Open |
| S6-1 | S6 | LOW | Тест | `test_get_me_with_valid_supabase_token_not_401` хрупкий — зависит от порядка вызовов | ⚪ Open |

---

## Новые файлы EPIC-IDS-04

| Файл | Статус |
|------|--------|
| `src/core/domain/contracts.py` | ✅ Создан |
| `src/core/domain/models.py` | ✅ Создан |
| `src/core/infrastructure/repositories.py` | ✅ Создан |
| `src/core/infrastructure/service_factory.py` | ✅ Создан |
| `src/core/infrastructure/providers.py` | ✅ Создан |
| `src/core/application/factory.py` | ✅ Создан |
| `src/core/providers/base.py` | ✅ Создан |
| `src/core/providers/registry.py` | ✅ Создан |
| `src/core/providers/mock/mock_provider.py` | ✅ Создан |
| `src/core/auth/supabase_validator.py` | ✅ Создан |
| `src/core/api/security.py` | ✅ Обновлён (`SupabaseJwtBearerTokenAuth` + `UserClaims` → domain) |
| `src/core/api/dependencies.py` | ✅ Обновлён (заменён stub на `provide_service_factory()`) |

---

## Story 1 — Domain Protocols в `core/domain/contracts.py`

| AC | Строка | Статус |
|----|--------|--------|
| Все 9 Protocols импортируются без ошибок | `contracts.py:18–118` | ✅ |
| Все Protocols `@runtime_checkable` | каждый класс | ✅ |
| `ProfileRecord`, `VerificationSession`, `EIDAuditEvent` импортируются | `models.py:19–69` | ✅ |
| Domain не импортирует `core.infrastructure`, `httpx`, `fastapi`, `joserfc` | `test_domain_contracts.py:74–96` (AST) | ✅ |
| `UnauthorizedError` НЕ в `core.domain.models` (audit H-4) | `test_domain_contracts.py:68–71` | ✅ |

**Полный список Protocols в contracts.py:**

| Protocol | Методов | Строки |
|----------|---------|--------|
| `HealthRepository` | 1 (`ping`) | 19–20 |
| `ProfileRepository` | 4 | 23–40 |
| `VerificationSessionStore` | 5 | 43–53 |
| `EIDAuditLogRepository` | 2 | 56–66 |
| `OAuthClientStore` | 2 | 69–73 |
| `OAuthTokenService` | 3 | 76–99 |
| `StoryDraftRepository` | 3 | 102–108 |
| `SupabaseJwtValidator` | 1 | 111–113 |
| `BearerTokenAuth` | 1 | 116–118 |

### S1-2 [LOW] — Мутируемые `list` в `frozen=True` dataclasses

`models.py:74`: `OAuthClient.scopes: list[str]`
`models.py:85`: `OAuthTokenClaims.scopes: list[str]`
`models.py:54`: `VerificationSession.provider_session_data: dict[str, object]`

`frozen=True` предотвращает замену поля (`client.scopes = [...]` → `FrozenInstanceError`), но НЕ предотвращает мутацию содержимого: `client.scopes.append("x")` выполнится без ошибки. Нет теста на это поведение.

**Как закрыть:** использовать `tuple[str, ...]` вместо `list[str]` для `scopes`, `tuple[tuple[str, object], ...]` или `types.MappingProxyType` для `provider_session_data`. Либо добавить тест, документирующий что shallow-мутация допустима (осознанное решение).

**Сложность:** LOW · **Важность:** LOW (InMemory-only в этом эпике; Supabase реализации в IDS-05 будут читать из БД)

**Story 1: ✅ VERIFIED — 1 finding (S1-2)**

---

## Story 2 — InMemory реализации

| AC | Строка | Статус |
|----|--------|--------|
| `isinstance(InMemoryProfileRepository(), ProfileRepository)` — True | `test_inmemory_repositories.py:83` | ✅ |
| `isinstance(InMemory*, Protocol)` для всех 7 классов | `test_inmemory_repositories.py:83–110` | ✅ |
| `attach_eid_verification` с дубликатом `hash` → RuntimeError | `test_inmemory_repositories.py:113–132` | ✅ |
| `get_by_state("unknown")` → `None` | `test_inmemory_repositories.py:135–136` | ✅ |
| `mark_consumed` идемпотентен | `test_inmemory_repositories.py:151–173` | ✅ |
| `hash_secret` детерминирован | `test_security_hashing.py:10–15` | ✅ |
| InMemory-файл не импортирует `httpx`, `fastapi`, `joserfc` | `test_inmemory_repositories.py:176–195` (AST) | ✅ |
| `from_config` использует demo-fallbacks | `test_inmemory_repositories.py:143–148` | ✅ |

**Проверка методов:**
- `InMemoryVerificationSessionStore.expire_pending`: `if session.expires_at >= now: continue` — корректная логика (сессия НЕ истекла если `expires_at >= now`) ✅
- `InMemoryOAuthTokenService._encode_jwt` / `_decode_jwt` — HMAC-SHA256, без joserfc ✅

### S2-1 [MEDIUM] — `issue_access_token` игнорирует `client_secret` без документации

`repositories.py:274`:
```python
def issue_access_token(self, *, code: str, client_id: str, client_secret: str, ...):
    del client_secret  # ← parameter received but immediately deleted
```

`client_secret` передаётся в метод (требуется Protocol), но InMemory-реализация его не проверяет против `OAuthClientStore.get_client(...).client_secret_hash`. Это значит InMemory-режим принимает ЛЮБОЙ `client_secret`, в т.ч. пустой.

Без документирующего комментария или теста неясно — это намеренное упрощение (InMemory ≠ security) или пропущенная логика.

**Как закрыть:** добавить комментарий:
```python
del client_secret  # InMemory intentionally skips client_secret validation;
                   # security is enforced by Supabase impl (EPIC-IDS-05).
```
Добавить тест: `issue_access_token(code=..., client_id=..., client_secret="wrong", ...)` → успешно (задокументировать InMemory поведение).

**Сложность:** LOW · **Важность:** MEDIUM (риск что кто-то при EPIC-IDS-05 не добавит real validation в Supabase impl)

**Story 2: ✅ VERIFIED — 1 finding (S2-1)**

---

## Story 3 — ServiceFactory(Protocol) + DefaultServiceFactory

| AC | Строка | Статус |
|----|--------|--------|
| `factory.config` возвращает `AppConfig` | `test_service_factory.py:92–95` | ✅ |
| `factory.get_profile_repository() is factory.get_profile_repository()` — True | `test_service_factory.py:98–100` | ✅ |
| `factory.something = "x"` → `FrozenInstanceError` | `test_service_factory.py:103–106` | ✅ |
| `isinstance(factory, ServiceFactory)` — True | `test_service_factory.py:109–111` | ✅ |
| Все `get_*()` возвращают тот же объект | `test_service_factory.py:114–124` | ✅ |

**`ServiceFactory` Protocol (`application/factory.py`):**

- `@runtime_checkable` ✅
- `@property def config` ✅
- Все 10 `get_*()` методов ✅
- TYPE_CHECKING imports — корректный паттерн (метод-сигнатуры не проверяются при `isinstance`) ✅

**Story 3: ✅ VERIFIED — 0 findings**

---

## Story 4 — eID Provider Port + Registry + Mock

| AC | Строка | Статус |
|----|--------|--------|
| `isinstance(MockEIDProvider(...), EIDProviderPort)` — True | `test_eid_providers.py:59–61` | ✅ |
| `registry.get("mock").provider_name == "mock"` | `test_eid_providers.py:64–67` | ✅ |
| `registry.get_active(config_eideasy)` → `KeyError` (решение зафиксировано) | `test_eid_providers.py:70–74` | ✅ |
| mock flow без external credentials | `test_eid_providers.py:88–114` | ✅ |
| `EIDProviderRegistry` НЕ `@lru_cache` | `test_eid_providers.py:77–78` (AST) | ✅ |
| `MockEIDProvider.provider_name == "mock"`, `callback_path == "/auth/mock/callback"` | `test_eid_providers.py:81–85` | ✅ |

**`EIDStartResult` не frozen** — `base.py:17`: `@dataclass class EIDStartResult` (без `frozen=True`). Epic spec явно не требует frozen для `EIDStartResult`. `EIDVerificationResult` — frozen ✅.

**`MockEIDProvider` DI через конструктор** — `mock_provider.py:13`: `def __init__(self, verification_session_store: VerificationSessionStore)` ✅

**Решение KeyError vs EIDProviderError** зафиксировано в коде: `KeyError` (`registry.py:13`), в тесте `pytest.raises(KeyError)` ✅.

**Story 4: ✅ VERIFIED — 0 findings**

---

## Story 5 — Supabase JWT validator + SupabaseJwtBearerTokenAuth

| AC | Строка | Статус |
|----|--------|--------|
| `validate(valid_token)` → `UserClaims` | `test_supabase_jwt_auth.py:75–82` | ✅ |
| `validate(expired_token)` → `JwtValidationError` | `test_supabase_jwt_auth.py:85–88` | ✅ |
| `validate(alg_none_token)` → `JwtValidationError` | `test_supabase_jwt_auth.py:91–94` | ✅ |
| `validate(iss_mismatch_token)` → `JwtValidationError` | `test_supabase_jwt_auth.py:97–100` | ✅ |
| `SupabaseJwtBearerTokenAuth` converts `JwtValidationError` → `UnauthorizedError("AUTHENTICATION_REQUIRED")` | `test_supabase_jwt_auth.py:103–109` | ✅ |
| `GET /me` с valid token → не 401 | `test_supabase_jwt_auth.py:127–153` | ✅ |
| `algorithms=["HS256"]` hardcoded (alg:none protection) | `supabase_validator.py:26` | ✅ |
| `role == "authenticated"` проверяется | `supabase_validator.py:36–37` | ✅ |
| `isinstance(validator, SupabaseJwtValidator)` — True | `test_supabase_jwt_auth.py:121–124` | ✅ |

### S5-1 [MEDIUM] — `BearerTokenAuth` Protocol определён ДВАЖДЫ

`core.api.security:23–24`:
```python
@runtime_checkable
class BearerTokenAuth(Protocol):
    def validate(self, headers: Mapping[str, str]) -> UserClaims: ...
```

`core.domain.contracts:116–118`:
```python
@runtime_checkable
class BearerTokenAuth(Protocol):
    def validate(self, headers: Mapping[str, str]) -> UserClaims: ...
```

Две отдельных Python-классы с одинаковой структурой:
- `dependencies.py:21`: `TYPE_CHECKING: from core.api.security import BearerTokenAuth` → `security`-версия для типизации `ApiDependencies.bearer_token_auth`
- `service_factory.py:7`: `from core.domain.contracts import BearerTokenAuth` → `contracts`-версия для типизации `DefaultServiceFactory.bearer_token_auth`

Нарушение Single Source of Truth. При runtime все `isinstance` проходят (одинаковый Protocol API), но статические type-checker'ы могут ругаться.

**Как закрыть:** `security.py` должен импортировать `BearerTokenAuth` из `core.domain.contracts`, не определять его повторно. Убрать определение из `security.py:23–24`, добавить `from core.domain.contracts import BearerTokenAuth`.

**Сложность:** MEDIUM · **Важность:** MEDIUM (нарушение Single Source of Truth в архитектурно центральном контракте)

### S5-2 [LOW] — Двойная `iss`-валидация в `SupabaseJwtValidatorImpl`

`supabase_validator.py:18–21`: joserfc `JWTClaimsRegistry` с `iss={"essential": True, "value": self._expected_iss}` уже проверяет `iss`. Если joserfc validation fails → `JoseError` → `JwtValidationError`.

`supabase_validator.py:34–35`: явная повторная проверка `claims.get("iss") != self._expected_iss`. Если joserfc уже проверил, эта ветка никогда не выполнится.

Не баг, но dead code / redundant check.

**Как закрыть:** убрать строки 34–35 (`if claims.get("iss") != self._expected_iss: raise ...`). Либо убрать `iss` из `_claims_registry` и оставить только явную проверку (явная понятнее).

**Сложность:** LOW · **Важность:** LOW

### S6-1 [LOW] — `test_get_me_with_valid_supabase_token_not_401` хрупкий

`test_supabase_jwt_auth.py:127–153`: тест вызывает `create_app(...)` дважды, `_clear_api_dependencies_cache()` один раз, monkeypatch'ит `get_api_dependencies` после первого `create_app`. Второй `create_app` внутри `TestClient(...)` снова вызывает `_clear_api_dependencies_cache()`, но monkeypatch уже установлен — поэтому когда lifespan вызывает `get_api_dependencies()`, он получает monkeypatched-версию.

Тест проходит, но опирается на нестандартный порядок: `create_app → get_deps → replace → monkeypatch → TestClient(create_app)`. Любое изменение в `_lifespan` или `create_app` может сломать сценарий.

**Как закрыть:** упростить тест, использовать `conftest.py`-паттерн через `monkeypatch.setenv` + `_clear_api_dependencies_cache`. Или добавить комментарий объясняющий порядок вызовов.

**Сложность:** LOW · **Важность:** LOW

**Story 5: ✅ VERIFIED — 3 findings (S5-1 MEDIUM, S5-2 LOW, S6-1 LOW)**

---

## Story 6 — `provide_service_factory()` + интеграция в `build_api_dependencies`

| AC | Строка | Статус |
|----|--------|--------|
| `provide_service_factory()` при `in_memory` → `DefaultServiceFactory` с InMemory | `test_epic_ids_04_integration.py:84–97` | ✅ |
| `provide_service_factory(supabase_config)` → fallback InMemory + warning EPIC-IDS-05 | `test_epic_ids_04_integration.py:100–110` | ✅ |
| `provide_service_factory(sqlite_config)` → `ValueError` | `test_epic_ids_04_integration.py:113–117` | ✅ |
| `build_api_dependencies().profile_repository is not None` | `test_epic_ids_04_integration.py:124` | ✅ |
| `build_api_dependencies().eid_provider_registry.get("mock").provider_name == "mock"` | `test_epic_ids_04_integration.py:126` | ✅ |
| `build_api_dependencies().bearer_token_auth.__class__.__name__ == "SupabaseJwtBearerTokenAuth"` | `test_epic_ids_04_integration.py:127–128` | ✅ |
| valid demo JWT через `build_api_dependencies().bearer_token_auth` | `test_epic_ids_04_integration.py:131–139` | ✅ |

---

### 🔴 RG-1 [HIGH] — `test_build_api_dependencies_has_epic_hook_comments` — регрессия

**Файл:** `tests/test_api_dependencies.py:151–159`

```python
def test_build_api_dependencies_has_epic_hook_comments() -> None:
    ...
    assert "# TODO EPIC-IDS-04: replace with provide_service_factory(...)" in text  # ← FAILS
    assert "# TODO EPIC-IDS-05: run 5-level Supabase healthchecks" in text           # ← passes
    assert "provide_service_factory" in text                                          # ← passes
    assert "get_story_draft_repository" in text                                       # ← passes
```

**Причина:** Тест из EPIC-IDS-03 Story 3 проверял, что `dependencies.py` содержит `# TODO EPIC-IDS-04: replace with provide_service_factory(...)`. В EPIC-IDS-04 этот TODO-комментарий был заменён реальной реализацией — `service_factory = provide_service_factory(config)`. Комментарий удалён из кода (правильно), но тест НЕ был обновлён.

**Как закрыть:** удалить первый `assert` из теста (он проверял промежуточное состояние EPIC-IDS-03). Переименовать тест в `test_build_api_dependencies_epic_05_hook_comments` и оставить только актуальные проверки:
```python
assert "# TODO EPIC-IDS-05: run 5-level Supabase healthchecks" in text
assert "provide_service_factory" in text
```

**Сложность:** TRIVIAL · **Важность:** HIGH (test suite fails)

---

### 🔴 RG-2 [HIGH] — `test_build_api_dependencies_zero_arg` — регрессия

**Файл:** `tests/test_api_dependencies.py:82–87`

```python
def test_build_api_dependencies_zero_arg(monkeypatch: pytest.MonkeyPatch) -> None:
    _apply_env(monkeypatch, _BASE_ENV)
    deps = build_api_dependencies()
    assert deps.db_backend == "in_memory"
    assert deps.db_ready is True
    assert deps.profile_repository is None  # ← FAILS after EPIC-IDS-04
```

**Причина:** В EPIC-IDS-03 `build_api_dependencies()` использовал `StubBearerTokenAuth()` и оставлял `profile_repository=None`. В EPIC-IDS-04 `build_api_dependencies()` вызывает `provide_service_factory(config)`, который создаёт `InMemoryProfileRepository()`. Теперь `deps.profile_repository is not None`.

**Как закрыть:** заменить assertion:
```python
# Было (EPIC-IDS-03 era):
assert deps.profile_repository is None

# Стало (EPIC-IDS-04):
from core.infrastructure.repositories import InMemoryProfileRepository
assert isinstance(deps.profile_repository, InMemoryProfileRepository)
```

**Сложность:** TRIVIAL · **Важность:** HIGH (test suite fails)

---

## Верификация Epic Goal (Section 8)

| Шаг | Ожидание | Факт | Статус |
|-----|----------|------|--------|
| Импорты всех компонентов | без ошибок | `test_epic_ids_04_integration.py:55–78` | ✅ |
| `isinstance(InMemoryProfileRepository(), ProfileRepository)` | True | `test_epic_ids_04_integration.py:80–81` | ✅ |
| `factory = provide_service_factory()` + `factory.config.db_backend == "in_memory"` | — | `test_epic_ids_04_integration.py:84–91` | ✅ |
| `factory.get_eid_provider_registry().get('mock').provider_name == "mock"` | — | `test_epic_ids_04_integration.py:126` | ✅ |
| `build_api_dependencies()` integration | все поля не None | `test_epic_ids_04_integration.py:120–139` | ✅ |

---

## Регрессионная проверка: EPIC-IDS-03 vs EPIC-IDS-04

| Компонент | EPIC-IDS-03 | EPIC-IDS-04 | Регрессия? |
|-----------|-------------|-------------|------------|
| `build_api_dependencies()` заполняет identity-поля | `None` (заглушки) | реальными InMemory объектами | ✅ ожидаемо |
| `bearer_token_auth` тип | `StubBearerTokenAuth` | `SupabaseJwtBearerTokenAuth` | ✅ ожидаемо |
| `# TODO EPIC-IDS-04` в `dependencies.py` | существовал | удалён | 🔴 тест RG-1 не обновлён |
| `deps.profile_repository is None` | True | False | 🔴 тест RG-2 не обновлён |
| `_clear_api_dependencies_cache()` | в `create_app` | в `create_app` | ✅ не изменилось |
| Domain isolation (no httpx/fastapi in `contracts.py`) | — | проверяется AST-тестом | ✅ |

---

## Приоритет исправлений

| Приоритет | ID | Файл | Строка | Действие |
|-----------|-----|------|--------|----------|
| 1 | RG-1 | `tests/test_api_dependencies.py` | 155 | Удалить `assert "# TODO EPIC-IDS-04..." in text` |
| 2 | RG-2 | `tests/test_api_dependencies.py` | 87 | Заменить `is None` на `isinstance(..., InMemoryProfileRepository)` |
| 3 | S5-1 | `src/core/api/security.py` | 23–24 | Убрать дублирующий `BearerTokenAuth` Protocol, импортировать из `core.domain.contracts` |
| 4 | S2-1 | `src/core/infrastructure/repositories.py` | 274 | Добавить комментарий или тест на намеренно пропущенную валидацию |
| 5 | S1-2 | `src/core/domain/models.py` | 74,85,54 | Решить: tuple/MappingProxyType или задокументировать |
| 6 | S5-2 | `src/core/auth/supabase_validator.py` | 34–35 | Убрать redundant iss-check |
| 7 | S6-1 | `tests/test_supabase_jwt_auth.py` | 127–153 | Упростить или задокументировать порядок вызовов |

RG-1 и RG-2 — тривиальные однострочные правки, блокируют test suite.
