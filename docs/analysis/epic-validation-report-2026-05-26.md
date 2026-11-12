# Validation Report: EPIC-IDS-01..06

> **Дата:** 2026-05-26
> **Методология:** analysis.mdc — verify every claim, no assumptions. Каждый факт перекрёстно проверен против requirements/06, 07, 08, 09, 17 и реальных источников кода (bootstrap-infrastructure patterns).
> **Контекст:** `src/` не существует — проект не реализован. Валидация документ-к-документу: эпики vs requirements vs bootstrap-паттерны.

---

## TL;DR

Эпики структурно выверены, правильно ссылаются на requirements, dependency graph чистый (01→02→03→04→05→06), security-инварианты соблюдены. Найдено **3 критических проблемы** (блокируют реализацию), **4 проблемы высокого уровня** (нужно исправить до передачи агенту), **6 средних несоответствий** (нужно договориться).

---

## Граф зависимостей эпиков

```
EPIC-IDS-01 (Scaffold / Config)
    ├── EPIC-IDS-02 (Transport)        ← AppConfig.cors_allowed_origins, port
    ├── EPIC-IDS-03 (DI)               ← AppConfig, provide_app_config
    ├── EPIC-IDS-04 (SOA Factory)      ← AppConfig fields (supabase_jwt_secret, eid_provider, ...)
    ├── EPIC-IDS-05 (Supabase)         ← AppConfig.supabase_url + supabase_service_role
    └── EPIC-IDS-06 (Testing)          ← pyproject.toml markers, conftest env vars

EPIC-IDS-02 (Transport)
    ├── EPIC-IDS-03 (DI) ← asgi_app.py stub singleton, StubBearerTokenAuth
    └── EPIC-IDS-06 (Testing) ← HTTP smoke pattern

EPIC-IDS-03 (DI)
    ├── EPIC-IDS-04 (SOA) ← ApiDependencies hook slots
    ├── EPIC-IDS-05 (Supabase) ← db_checks provider_state key
    └── EPIC-IDS-06 (Testing) ← _clear_api_dependencies_cache

EPIC-IDS-04 (SOA Factory)
    ├── EPIC-IDS-05 (Supabase) ← Protocols → Supabase implementations
    └── EPIC-IDS-06 (Testing) ← factory unit tests, MockEIDProvider

EPIC-IDS-05 (Supabase)
    └── EPIC-IDS-06 (Testing) ← live integration tests
```

**Вывод:** граф ацикличен ✅. Все зависимости явно объявлены в заголовках эпиков ✅.

---

## КРИТИЧЕСКИЕ ПРОБЛЕМЫ (блокируют реализацию)

### C-1: `request_timeout_s` — поле используется, но не определено в AppConfig

**Где обнаружено:** EPIC-IDS-05 Story 6, `provide_service_factory()`:
```python
supabase_db = SupabaseDatabase.from_http(
    ...
    timeout_s=float(resolved_config.request_timeout_s or 15),
)
```

**Проблема:** `request_timeout_s` отсутствует в списке полей `AppConfig` в EPIC-IDS-01 Story 2. При реализации Story 2 агент не включит это поле — Story 6 упадёт с `AttributeError`.

**Проверка req-07:** поле `REQUEST_TIMEOUT_S` отсутствует в таблице env vars req-07. Поле есть в gateway AppConfig (bootstrap-infrastructure/05), но для identity-сервиса намеренно опущено — и тогда EPIC-IDS-05 не может его использовать.

**Исправление:** В EPIC-IDS-01 Story 2 добавить в AppConfig:
```python
request_timeout_s: int = 15  # default: выровнять с gateway
```
В req-07 добавить строку: `REQUEST_TIMEOUT_S | No | 15 | Таймаут исходящих HTTP запросов к Supabase PostgREST`.

---

### C-2: `SupabaseHealthRepository` — класс используется, нигде не определён

**Где обнаружено:** EPIC-IDS-05 Story 6, ветка `db_backend == "supabase"`:
```python
health_repository = SupabaseHealthRepository(supabase_db)
```

**Проблема:** Нигде в эпиках (включая EPIC-IDS-04 Story 2 InMemory + Story Story 1 Protocols + EPIC-IDS-05 Story 2 Supabase репозитории) `SupabaseHealthRepository` не определён. При реализации — `NameError`.

Схема: `HealthRepository(Protocol)` → `InMemoryHealthRepository` → ??? (Supabase)

**Исправление:** Добавить в EPIC-IDS-05 Story 2 Outputs:
```python
class SupabaseHealthRepository:
    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db
    def ping(self) -> bool:
        return self._db.healthcheck()  # повторно использует уже реализованный метод
```

---

### C-3: `validate_supabase_jwt()` — несоответствие между Acceptance Criteria и Implementation

**Где обнаружено:** EPIC-IDS-04 Story 5 Acceptance Criteria:
```
• validate_supabase_jwt(valid_token, jwt_secret, supabase_url) → UserClaims
• validate_supabase_jwt(expired_token) → JwtValidationError
• validate_supabase_jwt(alg_none_token) → JwtValidationError
```

**Проблема:** Это signature standalone-функции `validate_supabase_jwt(token, jwt_secret, supabase_url)`. Но Outputs описывают класс `SupabaseJwtValidatorImpl` с методом `validate(self, token: str)`. AC проверяет функцию, реализация — класс. Тест, написанный по AC, не будет проверять реальную реализацию.

**Проверка req-09:** req-09 §"Спецификация модуля" описывает именно `class SupabaseJwtValidatorImpl`. Никакой standalone-функции в req-09 нет.

**Исправление:** Переписать AC в EPIC-IDS-04 Story 5 под класс:
```
• SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(valid_token) → UserClaims
• SupabaseJwtValidatorImpl(...).validate(expired_token) → raises JwtValidationError
• SupabaseJwtValidatorImpl(...).validate(alg_none_token) → raises JwtValidationError
```
И добавить в Story 6 тест `tests/test_supabase_jwt_validator.py` соответствующие вызовы.

---

## ПРОБЛЕМЫ ВЫСОКОГО УРОВНЯ (исправить до передачи агенту)

### H-1: `import base64` отсутствует в conftest.py fixture

**Где обнаружено:** EPIC-IDS-06 Story 1, тело `_block_dotenv_leakage`:
```python
monkeypatch.setenv("CODE_VERIFIER_ENCRYPTION_KEY", base64.b64encode(b"\x00" * 32).decode())
```

**Проблема:** `base64` не импортирован в fixture body и нет `import base64` в показанном фрагменте conftest. При запуске pytest — `NameError: name 'base64' is not defined`.

**Исправление:** Добавить в начало `tests/conftest.py`:
```python
import base64
import os
import pytest
from core.logging_setup import configure_logging
```

---

### H-2: `InMemoryOAuthClientStore.from_config()` — factory method не определён в Story 2

**Где обнаружено:** EPIC-IDS-04 Story 6, `provide_service_factory()`:
```python
oauth_client_store = InMemoryOAuthClientStore.from_config(resolved_config)
```

**Проблема:** EPIC-IDS-04 Story 2 Outputs описывает `InMemoryOAuthClientStore` как:
> "static dict (заполняется из `AppConfig` при construction: `{config.gpt_oauth_client_id: OAuthClient(...)}`)"

Но не определяет `from_config()` classmethod. Реализующий агент Story 2 не создаст этот метод, а Story 6 упадёт.

**Исправление:** Добавить в EPIC-IDS-04 Story 2 Outputs явный контракт:
```python
class InMemoryOAuthClientStore:
    def __init__(self, clients: dict[str, OAuthClient]) -> None:
        self._clients = clients

    @classmethod
    def from_config(cls, config: AppConfig) -> "InMemoryOAuthClientStore":
        """Build with GPT client from AppConfig."""
        client = OAuthClient(
            client_id=config.gpt_oauth_client_id or "test-gpt-client",
            client_secret_hash=...,
            redirect_uri=config.gpt_oauth_redirect_uri or "",
            scopes=["profile:read", "stories:draft", "stories:create"],
        )
        return cls(clients={client.client_id: client})
```

---

### H-3: `sqlite` backend — AppConfig допускает, ServiceFactory отказывает

**Где обнаружено:**
- EPIC-IDS-01 Story 2: `db_backend: str  # "in_memory" | "sqlite" | "supabase"`
- EPIC-IDS-04 Story 6:
  ```python
  elif resolved_config.db_backend == "supabase":
      ...
  else:
      raise ValueError(f"Unsupported db_backend: {resolved_config.db_backend}")
  ```

**Проблема:** `DB_BACKEND=sqlite` проходит AppConfig валидацию (не ConfigError), но при первом вызове `provide_service_factory()` бросает `ValueError`. Это нарушает fail-fast принцип — сервер поднимается из AppConfig, но падает позже в DI.

**Решение (выбрать одно):**

Вариант A: Убрать `sqlite` из допустимых значений `AppConfig` для identity-сервиса:
```python
if db_backend not in ("in_memory", "supabase"):
    raise ConfigError(f"DB_BACKEND must be in_memory|supabase, got {db_backend!r}")
```

Вариант B: Оставить `sqlite` в AppConfig с явной пометкой "not implemented" + добавить заглушку в `provide_service_factory` (не `raise`, а фолбэк на InMemory + warning).

Вариант A предпочтителен для identity-сервиса — SQLite не является плановым backend (req-07 не упоминает `sqlite`).

---

### H-4: `UnauthorizedError` — потенциальное двойное определение

**Где обнаружено:**
- EPIC-IDS-02 Story 3 Outputs: `class UnauthorizedError(Exception)` в `src/core/api/security.py`
- EPIC-IDS-04 Story 1 Outputs (domain/models.py): `class JwtValidationError(Exception), class UnauthorizedError(Exception) (или импорт из core.api.security)`

**Проблема:** Текст EPIC-IDS-04 Story 1 допускает два варианта размещения `UnauthorizedError` — в `core.domain.models` или импорт из `core.api.security`. Если реализующий агент выберет определение в `core.domain.models`, возникнет два класса с одинаковым именем в разных модулях. Exception handlers в `asgi_app.py` (EPIC-IDS-02) ловят `UnauthorizedError` из `core.api.security` — не из `core.domain.models`.

**Исправление:** Убрать опцию из EPIC-IDS-04 Story 1, оставить только:
> `UnauthorizedError` — всегда импортировать из `core.api.security`. В `core.domain.models` не определять.

---

## СРЕДНИЕ НЕСООТВЕТСТВИЯ (договориться до реализации)

### M-1: `EID_HASH_SECRET` vs `DOGESTONIA_EID_SECRET_PEPPER` — не разрешён в AppConfig

**Где обнаружено:**
- req-07: `DOGESTONIA_EID_SECRET_PEPPER` — одна переменная
- req-17: `EID_HASH_SECRET` — другое имя той же семантики
- EPIC-IDS-01 Story 2: AppConfig содержит **оба поля** (`eid_secret_pepper` и `eid_hash_secret`)
- EPIC-IDS-06 conftest: перезаписывает **оба** (`DOGESTONIA_EID_SECRET_PEPPER` и `EID_HASH_SECRET`)
- README-index §"Открытые вопросы": унификация отложена

**Проблема:** Если AppConfig читает оба env var, и реализующий агент (функциональный эпик) использует одно из них — код будет брать неправильный секрет при стандартном `.env` (который задаёт только `DOGESTONIA_EID_SECRET_PEPPER`).

**Рекомендация:** До старта EPIC-IDS-04 (который использует `subject_hash`) — принять решение. В AppConfig оставить ONE поле с именем `eid_hash_secret`, читать его из `EID_HASH_SECRET` env, добавить fallback: если `EID_HASH_SECRET` пустой, читать из `DOGESTONIA_EID_SECRET_PEPPER`. Зафиксировать в ADR-IDS-005 или новом ADR.

---

### M-2: `check-env` Makefile — расширение без обоснования

**Где обнаружено:**
- req-06 Makefile §"Шаг 4": `check-env` печатает `APP_PROFILE`, `SUPABASE_URL`, `AUTHENTIGATE_ISSUER`, `PORT`
- EPIC-IDS-01 Story 4 Outputs: расширяет до `APP_PROFILE`, `PORT`, `SUPABASE_URL`, `SUPABASE_JWT_SECRET`, `AUTHENTIGATE_ISSUER`, `EID_PROVIDER`

**Проблема:** Расширение правильное (добавлены `SUPABASE_JWT_SECRET` и `EID_PROVIDER`, которые критичны для identity-сервиса), но не отмечено явно как "расширение vs req-06". Реализующий агент мог бы взять req-06 буквально и пропустить `EID_PROVIDER`.

**Рекомендация:** В EPIC-IDS-01 Story 4 добавить фразу: "Расширение паттерна req-06 — добавлены `SUPABASE_JWT_SECRET` (нужен для JWT-валидации) и `EID_PROVIDER` (нужен для debug)".

---

### M-3: `supabase_anon_key` — поле без потребителя

**Где обнаружено:**
- req-07: `SUPABASE_ANON_KEY | No | — | Anon key. Для dev/testing сценариев.`
- EPIC-IDS-01 Story 2: поле `supabase_anon_key: str | None` в AppConfig

**Проблема:** Ни один из 6 эпиков не использует `supabase_anon_key`. PostgREST использует `service_role_key`. Supabase JWT validation использует `supabase_jwt_secret`. Поле определено, но ни один `_request()` или validator его не читает.

**Риск:** Агент реализует поле, оставит его навсегда без потребителя — технический долг + confusion.

**Рекомендация:** Либо исключить из AppConfig (req-07 помечает как "dev/testing"), либо добавить TODO-комментарий в EPIC-IDS-01: "Поле зарезервировано для будущего клиентского SDK тестирования, не используется server-side".

---

### M-4: `eideasy_allowed_methods` и `eideasy_allowed_countries` — нет defaults в EPIC-IDS-01

**Где обнаружено:**
- EPIC-IDS-01 Story 2 перечисляет поля: `eideasy_allowed_methods`, `eideasy_allowed_countries` (из req-18)
- req-18 §"Env vars": `EIDEASY_ALLOWED_METHODS | No | "smartid,mid-login,ee-id-login" | ...`, `EIDEASY_ALLOWED_COUNTRIES | No | "EE" | ...`
- EPIC-IDS-01 не указывает defaults для этих полей

**Проблема:** AppConfig без defaults для optional полей = они типизированы как `str | None`. Но в EPIC-IDS-04 `EIDEasyProvider` (когда появится) будет сравнивать `login_method in config.eideasy_allowed_methods` — если `None`, упадёт.

**Исправление:** В EPIC-IDS-01 Story 2, секция eID Easy:
```python
eideasy_allowed_methods: str = "smartid,mid-login,ee-id-login"
eideasy_default_country: str = "EE"
eideasy_allowed_countries: str = "EE"
eideasy_base_url: str = "https://test.eideasy.com"
```

---

### M-5: CORS setup в EPIC-IDS-02 — условие demo/pilot не реализовано

**Где обнаружено:**
- EPIC-IDS-02 Story 4 Outputs: `allow_origins=config.cors_allowed_origins.split(",")`
- EPIC-IDS-02 Critical Pitfalls: "CORS `allow_origins=["*"]` приемлем только в `APP_PROFILE=demo` — в pilot брать из `config.cors_allowed_origins`"
- req-07: `CORS_ALLOWED_ORIGINS | No | * (demo)` — `*` является default в demo

**Наблюдение:** Противоречия нет — если `config.cors_allowed_origins = "*"` в demo, `"*".split(",") == ["*"]` — CORS правильно даёт `allow_origins=["*"]`. В pilot `CORS_ALLOWED_ORIGINS=https://dogestonia.ee,...` — разбивается в список. Механизм корректен.

**Но:** в EPIC-IDS-02 Story 4 Outputs показана `CORSMiddleware` с `allow_origins=config.cors_allowed_origins.split(",")`, но CORS middleware добавляется в `app = FastAPI(...)` body — до `get_api_dependencies()`. Конкретно middleware инициализируется при определении app, а не в lifespan. `config` должна быть доступна в момент definition.

**Риск:** Паттерн gateway использовал `allow_origins=["*"]` хардкод. Identity-сервис хочет динамический список. Lifespan-инициализация решает это, только если CORS middleware добавляется после `deps = get_api_dependencies()`. EPIC-IDS-02 Story 4 не показывает как именно вызвать `deps.config` для CORS — нужно уточнить порядок.

**Рекомендация:** В EPIC-IDS-02 Story 4 добавить явный паттерн:
```python
# CORS настраивается ОДИН РАЗ при старте через lifespan
@asynccontextmanager
async def _lifespan(app: FastAPI):
    deps = get_api_dependencies()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=deps.config.cors_allowed_origins.split(","),
        ...
    )
    yield
```

---

### M-6: OPTIONS routes для public callback paths избыточны

**Где обнаружено:** EPIC-IDS-02 Story 5 таблица:
```
OPTIONS | (all above non-public) | public | Response(200) | 200
```

Но `eideasy/callback`, `authentigate/callback`, `mock/callback` — уже **public** GET endpoints. Им OPTIONS не нужны (браузер не делает CORS preflight к GET-запросам без custom headers).

**Проблема:** Нет, но лишний шум. Добавление OPTIONS к public GET callback URL'ам не нужно — это eID провайдер редиректит браузер через `302 → GET`. Браузер не добавляет `Authorization` заголовки к redirect.

**Рекомендация:** Уточнить в Story 5: OPTIONS нужны только для `/auth/eid/start` (POST Bearer), `/me`, `/oauth/*`, `/story-drafts*`. Callback routes не нужны.

---

## НАБЛЮДЕНИЯ (не проблемы, информация)

### N-1: `eid_audit_events.supabase_user_id` допускает NULL ✅

EPIC-IDS-05 Story 3 `service_role_policy_probe` использует `supabase_user_id=null` в eid_audit_events. Проверено: req-08 Migration 3 определяет `supabase_user_id UUID` без `NOT NULL`. ✅ Probe не нарушит constraint.

---

### N-2: req-08 `eid_verification_sessions.nonce|code_verifier_*` — NOT NULL изначально ✅

EPIC-IDS-05 Story 4 Migration `20260526000001` делает `DROP NOT NULL` для этих полей (req-17). Порядок миграций корректен: сначала создать таблицу с NOT NULL (req-08 basis), потом сделать nullable (req-17 extension). ✅

---

### N-3: `MockEIDProvider` получает `verification_session_store` через DI ✅

EPIC-IDS-04 Critical Pitfalls фиксирует: "MockEIDProvider использует `verification_session_store` через DI — не хранит state в себе". Правильная изоляция для тестов. ✅

---

### N-4: Gateway-поля не просочились ✅

Проверено по всем эпикам: `cluster_*`, `story_intake_service`, `issue_*`, `cluster_orchestrator` нигде не упоминаются как поля или сервисы. Изоляция identity-сервиса от gateway соблюдена. ✅

---

### N-5: Зависимость EPIC-IDS-03 от EPIC-IDS-02 корректна ✅

EPIC-IDS-03 Story 2 правильно документирует что `StubBearerTokenAuth` (из EPIC-IDS-02) используется до реализации EPIC-IDS-04. Комментарии `# replaced in EPIC-IDS-04` и `# TODO EPIC-IDS-05` корректно маркируют временные решения. ✅

---

### N-6: Конвенция имён миграций — расхождение

- req-08 файлы: `20260525000001_create_profiles.sql` (формат `YYYYMMDDHHMMSS`)
- EPIC-IDS-05 Story 4 в тексте: "конвенция `YYYYMMDD_HHMM_description.sql`"

req-08 использует 6-значный time part (без разделителей `_`). EPIC-IDS-05 называет формат неверно. Не критично — конкретные filename-ы в Story 4 Outputs используют правильный формат из req-08.

---

## СВОДНАЯ ТАБЛИЦА

| ID | Уровень | Эпик | Описание | Статус |
|----|---------|------|----------|--------|
| C-1 | 🔴 CRITICAL | IDS-01, IDS-05 | `request_timeout_s` не в AppConfig, но используется в EPIC-IDS-05 | Требует исправления |
| C-2 | 🔴 CRITICAL | IDS-04, IDS-05 | `SupabaseHealthRepository` нигде не определён | Требует исправления |
| C-3 | 🔴 CRITICAL | IDS-04, IDS-06 | AC Story 5 проверяет standalone-функцию, реализация — класс | Требует исправления |
| H-1 | 🟠 HIGH | IDS-06 | `import base64` отсутствует в conftest | Требует исправления |
| H-2 | 🟠 HIGH | IDS-04 | `InMemoryOAuthClientStore.from_config()` не определён в Story 2 | Требует исправления |
| H-3 | 🟠 HIGH | IDS-01, IDS-04 | `sqlite` допустим в AppConfig, но ServiceFactory бросает ValueError | Решить до реализации |
| H-4 | 🟠 HIGH | IDS-02, IDS-04 | `UnauthorizedError` — риск двойного определения | Исправить формулировку |
| M-1 | 🟡 MEDIUM | IDS-01, IDS-06 | `EID_HASH_SECRET` vs `DOGESTONIA_EID_SECRET_PEPPER` — открытый вопрос в AppConfig | Принять решение |
| M-2 | 🟡 MEDIUM | IDS-01 | `check-env` расширен vs req-06 без явного обоснования | Документировать |
| M-3 | 🟡 MEDIUM | IDS-01 | `supabase_anon_key` без потребителя ни в одном эпике | Прояснить назначение |
| M-4 | 🟡 MEDIUM | IDS-01 | eID Easy fields без defaults | Добавить defaults |
| M-5 | 🟡 MEDIUM | IDS-02 | CORS middleware + lifespan порядок неявен | Уточнить паттерн |
| M-6 | 🟡 MEDIUM | IDS-02 | OPTIONS для public callback routes избыточны | Уточнить |
| N-1 | ℹ️ INFO | IDS-05 | `supabase_user_id=null` в probe — допустимо по req-08 | ✅ OK |
| N-2 | ℹ️ INFO | IDS-05 | Порядок миграций req-08 → req-17 корректен | ✅ OK |
| N-3 | ℹ️ INFO | IDS-04 | MockEIDProvider DI-изоляция правильная | ✅ OK |
| N-4 | ℹ️ INFO | ALL | Gateway-поля не просочились в identity epics | ✅ OK |
| N-5 | ℹ️ INFO | IDS-03 | Stub → реальный переход правильно задокументирован | ✅ OK |
| N-6 | ℹ️ INFO | IDS-05 | Конвенция имён миграций в тексте неточна, в file names — OK | Уточнить текст |

---

## Покрытие requirements

| Requirement | Ссылается в эпике | Статус |
|-------------|------------------|--------|
| req-06 (scaffold) | EPIC-IDS-01 Stories 1-4 | ✅ Полное покрытие |
| req-07 (env vars) | EPIC-IDS-01 Story 2 | ✅ Полное покрытие (см. M-3, M-4) |
| req-08 (migrations) | EPIC-IDS-04 Story 1 (models), EPIC-IDS-05 Stories 2-4 | ✅ Полное покрытие |
| req-09 (JWT validation) | EPIC-IDS-02 Story 3, EPIC-IDS-04 Story 5 | ✅ Полное покрытие (см. C-3) |
| req-10 (/me endpoint) | EPIC-IDS-02 Story 5 (stub) | ✅ Stub зарегистрирован |
| req-11 (eID flow) | EPIC-IDS-02 Story 5 (stub) | ✅ Stub зарегистрирован |
| req-14 (OAuth server) | EPIC-IDS-04 Stories 1-3, EPIC-IDS-02 Story 5 (stub) | ✅ Protocols + stubs |
| req-15 (story auth) | EPIC-IDS-04 Story 1 (models), EPIC-IDS-05 Story 4 | ✅ StoryDraft покрыт |
| req-16 (security/CORS) | EPIC-IDS-02 Story 4 (CORS), req via Story 5 (/health, /ready) | ✅ Частично (см. M-5) |
| req-17 (provider abstraction) | EPIC-IDS-04 Story 4, EPIC-IDS-05 Story 3-4 | ✅ Полное покрытие |
| req-18 (eideasy) | EPIC-IDS-01 Story 2 (env), EPIC-IDS-04 Story 4 (registry slot) | ⚠️ Env vars OK, реализация — в будущем |

---

## Рекомендации по порядку исправлений

**Немедленно (до передачи эпиков агенту):**

1. **C-1** — Добавить `request_timeout_s: int = 15` в EPIC-IDS-01 Story 2 AppConfig + обновить req-07.
2. **C-2** — Добавить `SupabaseHealthRepository` в EPIC-IDS-05 Story 2 Outputs.
3. **C-3** — Переписать Acceptance Criteria EPIC-IDS-04 Story 5 под класс.
4. **H-1** — Добавить `import base64` в EPIC-IDS-06 conftest snippet.
5. **H-2** — Добавить `from_config()` classmethod в EPIC-IDS-04 Story 2 `InMemoryOAuthClientStore`.
6. **H-4** — Уточнить в EPIC-IDS-04 Story 1: `UnauthorizedError` только из `core.api.security`.

**До EPIC-IDS-01 реализации:**

7. **H-3** — Принять решение: убрать `sqlite` из AppConfig identity-сервиса или добавить fallback в ServiceFactory.
8. **M-1** — ADR: EID_HASH_SECRET vs DOGESTONIA_EID_SECRET_PEPPER — одно поле, fallback.
9. **M-4** — Добавить defaults для eideasy полей в EPIC-IDS-01 Story 2.

**До EPIC-IDS-02 реализации:**

10. **M-5** — Уточнить паттерн CORS + lifespan в EPIC-IDS-02 Story 4.
11. **M-6** — Убрать OPTIONS для public callback GET routes из Story 5 таблицы.

---

*Отчёт сгенерирован по методологии analysis.mdc: каждый факт верифицирован против req-06, 07, 08, 09, 17, bootstrap-infrastructure docs. Код (`src/`) отсутствует — проверено только документ-к-документу.*
