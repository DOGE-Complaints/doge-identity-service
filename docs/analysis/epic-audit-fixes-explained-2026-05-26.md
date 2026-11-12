# Объяснение правок по аудиту EPIC-IDS-01..06 — простым языком

> **⚠️ Актуальность:** §4.1–4.6 («слабые места») **пересмотрены** в [`interview-cpo-cto-epics-2026-05-27.md`](./interview-cpo-cto-epics-2026-05-27.md). Для CORS, `DOGESTONIA_EID_SECRET`, `hashing.py`, pilot AC, порядка валидации и таймаутов — ориентируйтесь на интервью и обновлённые эпики/requirements, а не на §4 ниже.

> **Дата:** 2026-05-26
> **Связанные документы:**
> - Исходный аудит: [`epic-validation-report-2026-05-26.md`](./epic-validation-report-2026-05-26.md)
> - Принятый план: `.cursor/plans/epic-audit-fixes-2026-05-26_8688276b.plan.md`
> **Цель документа:** Зафиксировать в одном месте, ЧТО было исправлено, ПОЧЕМУ так, какие env-переменные затронуты и что они означают. Документ адресован человеку, который будет проверять логическую нить и искать пропущенные косяки.

---

## 0. Резюме (TL;DR)

Аудит нашёл 14 проблем в 6 эпиках. Я исправил их строго по плану, без вольной интерпретации. Главные смысловые сдвиги:

1. **Унифицирован HMAC-секрет** для генерации `verified_person_hash`. Раньше документация описывала две переменные с одним смыслом (`DOGESTONIA_EID_SECRET_PEPPER` и `EID_HASH_SECRET`); это приводило к тому, что код мог взять одну, а `.env` задавать другую. Теперь одна каноническая (`EID_HASH_SECRET`) + одна fallback (`DOGESTONIA_EID_SECRET_PEPPER`).
2. **Убраны "мёртвые" концепции** — `sqlite` как backend (не используется) и `SUPABASE_ANON_KEY` (не нужен на server-side).
3. **Добавлены отсутствующие куски** — поле `request_timeout_s` в `AppConfig`, класс `SupabaseHealthRepository`, метод `InMemoryOAuthClientStore.from_config()`, импорт `import base64` в conftest.
4. **Сняты неоднозначности** — `UnauthorizedError` определяется только в одном месте, Acceptance Criteria JWT-валидатора переписаны под класс (а не несуществующую функцию), для CORS зафиксирован порядок инициализации через lifespan, OPTIONS-роуты перечислены явно.

---

## 1. Что изменилось по проблемам аудита

### Критические (блокировали реализацию)

#### C-1 — `request_timeout_s` отсутствовал в `AppConfig`, хотя использовался

**Что было сломано.** В EPIC-IDS-05 Story 6 (сборка фабрики для Supabase) есть строка `timeout_s=float(resolved_config.request_timeout_s or 15)`. Но в EPIC-IDS-01 Story 2 — где описан весь набор полей `AppConfig` — `request_timeout_s` отсутствовал. При реализации Story 2 агент бы не создал поле, и Story 6 упала бы с `AttributeError`.

**Как исправлено.**
- В [`docs/requirements/07-env-configuration-spec.md`](../requirements/07-env-configuration-spec.md) §Deployment добавлена строка `REQUEST_TIMEOUT_S | No | 15 | Таймаут исходящих HTTP-запросов к Supabase PostgREST`. То же в `example.env`.
- В [`EPIC-IDS-01`](../tasks/epics/EPIC-IDS-01-scaffold-config-launch.md) Story 2 список Deployment-полей дополнен `request_timeout_s: int = 15`.
- В Acceptance Criteria добавлен явный кейс: `... → AppConfig с request_timeout_s == 15`.

**Почему такое значение.** `15` секунд — выровнено с complaints-gateway (см. `docs/bootstrap-infrastructure/05-env-config-and-launch.md`), это компромисс между "не вешать пользователя" и "не убивать долгий запрос Supabase при холодном старте".

---

#### C-2 — `SupabaseHealthRepository` нигде не был определён

**Что было сломано.** В EPIC-IDS-05 Story 6 (Supabase backend) есть строка `health_repository = SupabaseHealthRepository(supabase_db)`, но ни в одном эпике класс не описан. При реализации был бы `NameError`.

**Как исправлено.** В EPIC-IDS-05 Story 2 добавлено явное определение:

```python
class SupabaseHealthRepository:
    """Backend-specific HealthRepository for /ready endpoint."""

    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def ping(self) -> bool:
        return self._db.healthcheck()
```

Это тонкая обёртка над уже описанным методом `SupabaseDatabase.healthcheck()` (Story 1). Удовлетворяет Protocol `HealthRepository` из EPIC-IDS-04 Story 1 (метод `ping() -> bool`).

**Почему именно делегирование, а не отдельная логика.** `/ready` endpoint всё равно зовёт `SupabaseDatabase.healthcheck()` напрямую через `db_checks["connectivity"]` (Story 3). `HealthRepository` нужен как Protocol-совместимая сущность для DI-контейнера, реальная работа уже сделана в `SupabaseDatabase`.

---

#### C-3 — Acceptance Criteria для JWT-валидатора были написаны под функцию, а реализация — класс

**Что было сломано.** EPIC-IDS-04 Story 5 описывает класс `SupabaseJwtValidatorImpl` с методом `validate(self, token)`. Но Acceptance Criteria были написаны так, будто существует standalone-функция `validate_supabase_jwt(token, jwt_secret, supabase_url)`. Тест по такой AC не проверял бы реальную реализацию.

**Как исправлено.** Acceptance Criteria переписаны на класс-форму:

```
SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(valid_token) → UserClaims
SupabaseJwtValidatorImpl(...).validate(expired_token) raises JwtValidationError
SupabaseJwtValidatorImpl(...).validate(alg_none_token) raises JwtValidationError
SupabaseJwtValidatorImpl(...).validate(token_with_iss_mismatch) raises JwtValidationError
```

Плюс добавлен один кейс на адаптер уровнем выше: `SupabaseJwtBearerTokenAuth(validator=...)` корректно превращает `JwtValidationError` в `UnauthorizedError(code="AUTHENTICATION_REQUIRED")`. Это важно, потому что HTTP-слой ловит именно `UnauthorizedError`, а не `JwtValidationError`.

---

### High (нужно исправить до передачи агенту)

#### H-1 — В conftest использовался `base64`, но не было `import base64`

**Что было сломано.** EPIC-IDS-06 Story 1 показывала фрагмент `tests/conftest.py`, где есть строка `monkeypatch.setenv("CODE_VERIFIER_ENCRYPTION_KEY", base64.b64encode(b"\x00" * 32).decode())`. При запуске pytest агент-исполнитель просто скопировал бы тело фикстуры и получил `NameError`.

**Как исправлено.** В начало conftest-сниппета добавлен явный блок импортов:

```python
import base64
import os
import pytest
from core.logging_setup import configure_logging
```

`os` нужен для `os.environ.get(...)` в `_pytest_session_logging`, `pytest` — для декораторов, `configure_logging` — для второй фикстуры.

---

#### H-2 — `InMemoryOAuthClientStore.from_config()` использовался, но контракта метода не было

**Что было сломано.** EPIC-IDS-04 Story 6 (сборка фабрики) делает `oauth_client_store = InMemoryOAuthClientStore.from_config(resolved_config)`. Но Story 2 (где описаны InMemory-репозитории) просто говорил "static dict (заполняется из AppConfig при construction)" — без явного `classmethod from_config(...)`. Агент-исполнитель Story 2 не создал бы этот метод.

**Как исправлено.** В Story 2 теперь полное тело класса, включая classmethod:

```python
class InMemoryOAuthClientStore:
    def __init__(self, clients: dict[str, OAuthClient]) -> None:
        self._clients = clients

    @classmethod
    def from_config(cls, config: AppConfig) -> "InMemoryOAuthClientStore":
        client = OAuthClient(
            client_id=config.gpt_oauth_client_id or "test-gpt-client",
            client_secret_hash=hash_secret(config.gpt_oauth_client_secret or "demo"),
            redirect_uri=config.gpt_oauth_redirect_uri or "",
            scopes=["profile:read", "stories:draft", "stories:create"],
        )
        return cls(clients={client.client_id: client})

    def get_client(self, client_id: str) -> OAuthClient | None: ...
    def list_clients(self) -> list[OAuthClient]: ...
```

`hash_secret(...)` — локальный helper (HMAC-SHA256 или bcrypt, конкретная реализация — в функциональном эпике OAuth-сервера по req-14).

---

#### H-3 — `sqlite` допускался в `AppConfig`, но `ServiceFactory` его не поддерживал

**Что было сломано.** EPIC-IDS-01 Story 2 говорил, что `db_backend: str  # "in_memory" | "sqlite" | "supabase"`, а EPIC-IDS-04 Story 6 в `provide_service_factory()` имел `else: raise ValueError("Unsupported db_backend: ...")`. То есть `DB_BACKEND=sqlite` проходил валидацию конфига, но падал позже в DI — это нарушает fail-fast принцип.

**Решение, которое ты одобрил.** Вариант A: убрать `sqlite` из допустимых значений (`sqlite` нигде в req-07 не упоминается, это не плановый backend для identity-сервиса).

**Как исправлено.**
- EPIC-IDS-01 Story 2: комментарий backend selector → `"in_memory" | "supabase"`, в `load_config_from_env` добавлено правило `db_backend ∉ {"in_memory", "supabase"} → ConfigError`. AC дополнены кейсом `DB_BACKEND=sqlite → ConfigError`.
- EPIC-IDS-03 Epic Goal: `assert d1.db_backend in ("in_memory", "supabase")` (без `"sqlite"`).
- EPIC-IDS-04 Story 6: в ветке `else` raise остаётся, но `sqlite` туда никогда не дойдёт — он отрезается раньше валидацией `AppConfig`.

---

#### H-4 — `UnauthorizedError` мог быть определён дважды

**Что было сломано.** EPIC-IDS-02 Story 3 явно определяет `class UnauthorizedError(Exception)` в `src/core/api/security.py`. А EPIC-IDS-04 Story 1 в outputs `core/domain/models.py` писал: "`class UnauthorizedError(Exception) (или импорт из core.api.security)`" — двусмысленно. Если бы агент выбрал "определить в `core.domain.models`", то это был бы **другой класс с тем же именем**. Exception handler в `asgi_app.py` ловит конкретный класс из `core.api.security`, и второй из `core.domain.models` пролетал бы мимо, превращаясь в 500 вместо 401.

**Как исправлено.** В EPIC-IDS-04 Story 1 убрана альтернатива; теперь явно написано: "`UnauthorizedError` НЕ определяется в `core.domain.models`. Единственный источник — `core.api.security` (EPIC-IDS-02 Story 3). `core.auth.*`, тесты и валидаторы всегда импортируют `from core.api.security import UnauthorizedError`."

Это паттерн single source of truth: один класс — одна точка определения.

---

### Medium (договорённости и косметика)

#### M-1 — Унификация `EID_HASH_SECRET` и `DOGESTONIA_EID_SECRET_PEPPER`

**Контекст.** Это та же сущность под двумя именами:
- `DOGESTONIA_EID_SECRET_PEPPER` — историческое имя из req-07.
- `EID_HASH_SECRET` — провайдер-агностичное имя из req-17, req-18.

Если оба поля остаются в `AppConfig`, реализующий агент может взять одно, а `.env` задавать другое — `verified_person_hash` начнёт генериться от пустой строки или от неправильного секрета.

**Как исправлено (фиксируется в `ADR-IDS-008`).**
1. В `AppConfig` теперь **одно** поле — `eid_hash_secret: str`.
2. Loader читает значение в таком порядке: `EID_HASH_SECRET` (primary) → `DOGESTONIA_EID_SECRET_PEPPER` (deprecated fallback) → пустая строка.
3. В `pilot` профиле проверяется итоговое значение `eid_hash_secret` (не отдельные env vars), чтобы fallback срабатывал без false-positive `ConfigError`.
4. В `req-07` `DOGESTONIA_EID_SECRET_PEPPER` помечен как deprecated.
5. В `README-index` пункт про этот конфликт закрыт ссылкой на ADR.
6. В EPIC-IDS-06 conftest сетит **обе** переменные — чтобы покрыть и приоритет, и fallback в loader'е.

**Почему не просто переименовать.** Старые `.env` в production-средах уже содержат `DOGESTONIA_EID_SECRET_PEPPER`. Если "просто переименовать", все эти `.env` придётся править одновременно с релизом. Fallback даёт окно мягкой миграции: задеплоить новый код → потом постепенно переименовать env в `.env` файлах → потом удалить fallback.

---

#### M-2 — `make check-env` расширен относительно req-06 без обоснования

**Что было сломано.** req-06 говорит, что `check-env` печатает `APP_PROFILE`, `SUPABASE_URL`, `AUTHENTIGATE_ISSUER`, `PORT`. EPIC-IDS-01 Story 4 расширил список до 6 переменных (добавлены `SUPABASE_JWT_SECRET` и `EID_PROVIDER`). Расширение правильное, но не было документировано — реализующий агент мог скопировать req-06 буквально и пропустить новые.

**Как исправлено.** В Story 4 добавлена явная фраза:

> Расширение паттерна req-06 (audit M-2): к базовому набору из req-06 §"Шаг 4" (`APP_PROFILE`, `SUPABASE_URL`, `AUTHENTIGATE_ISSUER`, `PORT`) явно добавлены `SUPABASE_JWT_SECRET` (нужен для JWT-валидации в EPIC-IDS-04) и `EID_PROVIDER` (нужен для debug eID flow).

Это сигнал агенту: "не сокращай список обратно к четырём — это сознательное расширение".

---

#### M-3 — Удалено `SUPABASE_ANON_KEY` (не используется server-side)

**Контекст.** В req-07 строка `SUPABASE_ANON_KEY | No | — | Anon key. Для dev/testing сценариев.` Поле было прописано в `AppConfig`, но **ни один из 6 эпиков его не читает**. Все запросы к Supabase идут через `SUPABASE_SERVICE_ROLE` (он bypass'ит RLS — это server-side ключ). JWT-валидация идёт через `SUPABASE_JWT_SECRET`. То есть `SUPABASE_ANON_KEY` — мёртвое поле.

**Как исправлено.**
- В req-07 строка удалена из таблицы Supabase. Добавлено примечание: "anon key опущен намеренно — identity-сервис server-side всегда работает через `SUPABASE_SERVICE_ROLE`. Anon key используется только во фронтенд-приложениях, которые конфигурируются отдельно."
- В EPIC-IDS-01 Story 2 список Supabase-полей `AppConfig` обновлён, поле удалено, добавлено такое же объяснение.

---

#### M-4 — В `AppConfig` не было defaults для eID Easy полей

**Что было сломано.** EPIC-IDS-01 Story 2 перечислял `eideasy_allowed_methods`, `eideasy_allowed_countries` без defaults. Без defaults они типизировались бы как `str | None`. Будущий `EIDEasyProvider` (req-18) делает `if login_method in config.eideasy_allowed_methods.split(",")` — на `None` это упадёт.

**Как исправлено.** В Story 2 явно прописаны defaults из req-18:

```
eideasy_env: str = "test"
eideasy_base_url: str = "https://test.eideasy.com"
eideasy_client_id: str = ""
eideasy_client_secret: str = ""
eideasy_redirect_uri: str = ""
eideasy_allowed_methods: str = "smartid,mid-login,ee-id-login"
eideasy_default_country: str = "EE"
eideasy_allowed_countries: str = "EE"
```

При `EID_PROVIDER=mock` они не используются вовсе, но AppConfig всё равно их корректно сконструирует.

---

#### M-5 — CORS требует `config`, но `config` доступен только после `get_api_dependencies()`

**Что было сломано.** EPIC-IDS-02 Story 4 говорил: `CORSMiddleware с allow_origins из deps.config.cors_allowed_origins`. Но не показывал, КАК именно это сделать. Если `app.add_middleware(CORSMiddleware, ...)` вызвать в module-level (при создании `app = FastAPI(...)`), `deps.config` ещё не существует — DI не инициализирован.

**Как исправлено.** В Story 4 добавлен явный паттерн внутри `_lifespan`:

```python
@asynccontextmanager
async def _lifespan(app: FastAPI):
    deps = get_api_dependencies()
    configure_logging(deps.config.log_level, log_format=deps.config.log_format)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=deps.config.cors_allowed_origins.split(","),
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["authorization", "content-type", "x-trace-id"],
    )
    yield
```

И зафиксировано правило: CORS добавляется ВНУТРИ lifespan, ПОСЛЕ `get_api_dependencies()`.

> **Замечание для логической проверки (см. раздел 4):** FastAPI на самом деле не любит вызов `app.add_middleware` после старта приложения — middleware регистрируется на этапе сборки. Это может потребовать альтернативного решения (см. раздел 4 ниже).

---

#### M-6 — OPTIONS для public callback paths избыточны

**Что было сломано.** В таблице роутов EPIC-IDS-02 Story 5 была размытая строка `OPTIONS | (all above non-public) | public | Response(200) | 200`. Это создавало двусмысленность: считаются ли callback-роуты (`/auth/eideasy/callback`, `/auth/authentigate/callback`, `/auth/mock/callback`) "non-public"? Они public GET, но трактовка зависела от агента.

**Как исправлено.** Строка заменена на явный список из 9 OPTIONS-роутов (только для защищённых endpoints):

- `/me`, `/auth/eid/start`, `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token`, `/story-drafts`, `/story-drafts/{draft_id}/submit`, `/stories`, `/gpt/actions/submit-story`.

Под таблицей примечание: callback-роуты не требуют OPTIONS, потому что eID-провайдер редиректит браузер через `302 → GET` без preflight; `/health` и `/ready` тоже не требуют (public GET без custom headers).

---

### Info

#### N-6 — Текстовая опечатка про конвенцию имён миграций

EPIC-IDS-05 Story 4 говорил "конвенция `YYYYMMDD_HHMM_description.sql`", но реальные filename'ы используют 14-значный timestamp без разделителей (например `20260525000001_create_profiles.sql`). Исправлено на `YYYYMMDDHHMMSS_description.sql`.

---

## 2. Глоссарий переменных окружения

Здесь — детальное объяснение каждой переменной, которая упоминается в правках или в `AppConfig`. Для каждой указано:
- **Где брать значение** — конкретный путь в Supabase Dashboard / провайдер / правило генерации.
- **Что это значит и зачем нужно**.
- **Кто этим пользуется** в коде.
- **Что будет, если не задать**.

---

### Deployment

#### `APP_PROFILE`
- **Что это:** строковый идентификатор окружения, всего два значения — `demo` или `pilot`.
- **Откуда брать:** задаётся вручную в `.env`. На локалке — всегда `demo`. На Railway в production — `pilot`.
- **Зачем нужен:** переключает строгость валидации. В `demo` многие секреты могут быть пустыми (сервис стартует, чтобы можно было руками разрабатывать scaffold). В `pilot` все боевые секреты обязательны — сервер не стартует, если хотя бы один отсутствует. Это fail-fast принцип: лучше падение на старте с понятной ошибкой, чем работающий сервис с пустым секретом.
- **Кто читает:** `load_config_from_env()` сравнивает все Yes (pilot)-поля из req-07 § "Валидация конфигурации при старте".

#### `PORT`
- **Что это:** TCP-порт, на котором слушает uvicorn.
- **Откуда брать:** для локального dev — `8100` (default). На Railway платформа сама задаёт `PORT` в env (динамически), Makefile использует `${PORT:-8100}` чтобы это работало и локально, и в облаке.
- **Зачем нужно `8100`:** complaints-gateway уже занимает `8000` (см. соседний сервис). Идентити нельзя на тот же порт.
- **Кто читает:** uvicorn CLI через Makefile.

#### `API_BASE_URL`
- **Что это:** полный URL сервиса, который клиенты используют для callback-ов и cross-service запросов.
- **Откуда брать:** локально — `http://localhost:8100`. Production — `https://identity.dogestonia.ee` (когда задеплоится).
- **Зачем нужен:** OAuth 2.0 server должен знать свой собственный URL, чтобы выдавать корректные `redirect_uri` подсказки и формировать `iss` claim в issued access-токенах.
- **Required даже в demo:** иначе сервис не знает, как себя называть.

#### `LOG_LEVEL`
- **Что это:** уровень логирования Python `logging`.
- **Откуда брать:** в dev — `INFO` (умеренное). В CI — `DEBUG` для расследования флейков. В production — `INFO` или `WARNING`.
- **Default:** `INFO`.

#### `LOG_FORMAT`
- **Что это:** формат лог-строки.
- **Откуда брать:** dev — `text` (читаемо в терминале). Production — `json` (структурированно, можно искать в Datadog/Loki).
- **Default:** `text`.

#### `REQUEST_TIMEOUT_S` (добавлено по C-1)
- **Что это:** таймаут исходящих HTTP-запросов от identity-сервиса в Supabase PostgREST.
- **Откуда брать:** обычно не задают, оставляют default. Если Supabase медленный — увеличить до 30.
- **Зачем нужно:** без таймаута запрос может висеть бесконечно, что приведёт к зависанию HTTP-handler'ов. С таймаутом — `httpx.TimeoutException` за разумное время, оператор видит её в логах.
- **Default:** `15` секунд (выровнено с complaints-gateway).
- **Кто читает:** `SupabaseDatabase.from_http(..., timeout_s=float(config.request_timeout_s))` в EPIC-IDS-05 Story 6.

---

### Supabase

#### `SUPABASE_URL`
- **Что это:** базовый URL Supabase проекта, вида `https://abcdefgh.supabase.co`.
- **Откуда брать:** Supabase Dashboard → выбрать проект → **Settings** → **API** → **Project URL**.
- **Зачем нужен:** к нему identity-сервис добавляет `/rest/v1/...` для PostgREST-запросов и `/auth/v1/...` если бы использовал Supabase Auth.
- **Required в pilot:** без него ничего не работает с реальным Supabase. В demo (`DB_BACKEND=in_memory`) — опционален.

#### `SUPABASE_SERVICE_ROLE`
- **Что это:** "service_role" JWT-ключ Supabase, который **bypass'ит Row Level Security**. То есть может читать/писать любые таблицы независимо от RLS-policies.
- **Откуда брать:** Supabase Dashboard → **Settings** → **API** → **Project API keys** → **`service_role`** (отдельный ключ от `anon`).
- **Зачем нужен:** identity-сервис работает на server-side от имени системы, а не пользователя. Нужно писать в `eid_audit_events`, обновлять `profiles.eid_verified` — это всё привилегированные операции. Без service_role RLS бы блокировал.
- **Опасность:** service_role-ключ даёт полный доступ к БД. Его НИКОГДА не отдают клиенту (фронтенду/мобильному). Только в server-side env.
- **Required в pilot.**

#### `SUPABASE_JWT_SECRET`
- **Что это:** HMAC-SHA256 секрет, которым Supabase подписывает access-токены пользователей (когда пользователь логинится через Supabase Auth — Magic Link, Google OAuth и т.п.).
- **Откуда брать:** Supabase Dashboard → **Settings** → **API** → **JWT Settings** → **JWT Secret**.
- **Зачем нужен:** наш identity-сервис принимает `Authorization: Bearer <supabase_access_token>` от SPA. Чтобы проверить подпись токена, нужен тот же секрет. Без него любой может подделать токен.
- **Required если HS256:** Supabase Cloud может работать на HS256 (один shared secret) или RS256 (через JWKS endpoint). Для self-hosted Supabase — HS256 типично. Для Supabase Cloud с RS256 этот var не нужен, вместо него — JWKS endpoint.
- **Кто читает:** `SupabaseJwtValidatorImpl(jwt_secret=..., supabase_url=...)`.

#### `DATABASE_URL`
- **Что это:** строка прямого Postgres-подключения, формата `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`.
- **Откуда брать:** Supabase Dashboard → **Settings** → **Database** → **Connection string** → **URI**. Пароль = тот, который задавали при создании проекта.
- **Зачем нужен:** если используется `psycopg` для прямых SQL-запросов (например, для транзакционных eID conflict checks). Если идём через PostgREST (текущий выбор по EPIC-IDS-05) — не используется, но оставлен на случай ADR-IDS-005 разворота.
- **Required в pilot ЕСЛИ psycopg выбран.**

#### `SUPABASE_ANON_KEY` (удалено по M-3)
- **Что это:** publishable "anon" JWT-ключ Supabase. С ним любой может ходить в Supabase, но RLS-policies ограничивают что именно.
- **Откуда брать:** Supabase Dashboard → **Settings** → **API** → **Project API keys** → **`anon` `public`**.
- **Почему НЕ нужен у нас:** identity-сервис **всегда** работает server-side через service_role. Anon-ключ нужен фронтенду (SPA, мобильное), но фронтенд получает его из своего собственного `.env`, не из идентити-конфига.

---

### Authentigate OIDC (SK ID Solutions)

#### `AUTHENTIGATE_ISSUER`
- **Что это:** issuer URL OIDC-провайдера. Используется для discovery (`{issuer}/.well-known/openid-configuration`).
- **Откуда брать:**
  - Demo (mock-OAuth2-сервер локально): `http://localhost:8080`. Запускается командой `docker run -p 8080:8080 ghcr.io/navikt/mock-oauth2-server:latest`.
  - Demo (SK ID): `https://oidc.demo.sk.ee` (требует креды от SK ID Solutions).
  - Production: `https://id.authentigate.eu`.
- **Зачем нужен:** код проверяет `iss` claim в ID token, делает discovery для получения JWKS endpoint.

#### `AUTHENTIGATE_CLIENT_ID`, `AUTHENTIGATE_CLIENT_SECRET`
- **Что это:** OAuth2 client credentials, выданные SK ID Solutions.
- **Откуда брать:** контакт `sales@skidsolutions.eu`. На момент написания — не получены (см. ADR-IDS-004).
- **Required в pilot.**

#### `AUTHENTIGATE_REDIRECT_URI`
- **Что это:** callback URL, зарегистрированный у Authentigate. После успешного логина провайдер редиректит браузер сюда с `?code=...&state=...`.
- **Локально:** `http://localhost:8100/auth/eid/callback` (или `/auth/authentigate/callback` по req-17).
- **Production:** `https://identity.dogestonia.ee/auth/eid/callback`.
- **Важно:** должен быть **точно зарегистрирован** в Authentigate Dashboard. Любое отличие — `redirect_uri_mismatch` ошибка.

#### `AUTHENTIGATE_SCOPES`
- **Что это:** OIDC scopes, которые мы запрашиваем у Authentigate.
- **Default:** `openid personal_code personal_code_country`. Это минимум, который нужен для генерации `verified_person_hash` (personal_code + country).
- **Никогда НЕ добавлять:** `given_name`, `family_name`, `birthdate` — privacy-инвариант (req-16). Идентити-сервис принципиально не хранит ФИО и дату рождения.

---

### Identity Secrets

#### `EID_HASH_SECRET` (новое каноническое имя, по ADR-IDS-008)
- **Что это:** HMAC-SHA256 ключ для генерации `verified_person_hash`. Формула из req-13:

  ```python
  verified_person_hash = hmac.new(
      EID_HASH_SECRET.encode("utf-8"),
      f"{country_uppercase}:{personal_code}".encode("utf-8"),
      hashlib.sha256
  ).hexdigest()
  ```

- **Откуда брать:** сгенерировать командой:

  ```bash
  python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
  ```

  Это даст 32 случайных байта, кодированных в base64. Минимум 32 байта — чтобы HMAC-SHA256 был криптостойким.

- **Зачем нужен:** превращает `personal_code` (раскрывающий идентификатор) в детерминированный псевдоним:
  - Тот же человек всегда даёт тот же hash → можно проверить "уже верифицирован" без хранения personal_code.
  - Без секрета hash превратить обратно в personal_code нельзя (one-way).
  - Без секрета любой не может вычислить hash → defence-in-depth даже если БД утечёт.
- **Required в pilot.**
- **Privacy-критично:** никогда не логировать, не отдавать в response, ротировать только по incident response plan.
- **Provider-agnostic:** один секрет для всех eID-провайдеров (mock, eideasy, authentigate). Провайдер сам формирует message (`"eideasy:EE:{idcode}"` для eID Easy), но ключ один.

#### `DOGESTONIA_EID_SECRET_PEPPER` (deprecated fallback, по ADR-IDS-008)
- **Что это:** то же самое, что `EID_HASH_SECRET`, только под старым именем.
- **Откуда брать:** в новых деплоях — НЕ задавать (использовать `EID_HASH_SECRET`). В старых `.env` оставить как было; loader подхватит как fallback.
- **Зачем оставлен:** мягкая миграция. После того как все деплои переименуют переменную, в отдельном PR fallback удалим.
- **Не required.**

#### `CODE_VERIFIER_ENCRYPTION_KEY`
- **Что это:** AES-256-GCM ключ для симметричного шифрования OAuth2 PKCE `code_verifier` перед сохранением в БД (`eid_verification_sessions.code_verifier_encrypted`).
- **Откуда брать:**

  ```bash
  python3 -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"
  ```

  Ровно 32 байта (AES-256), base64-encoded.

- **Зачем нужен:** Authentigate-провайдер использует PKCE S256. `code_verifier` — секретный nonce, который генерится перед `/authorize` и используется при `/token`. Если БД утечёт с `code_verifier` в открытом виде, атакующий может завершить чужую verification-сессию. AES-GCM добавляет authenticated encryption.
- **Required в pilot.**
- **eID Easy и mock провайдеры:** не используют PKCE, этот ключ им не нужен — но AppConfig его всё равно читает (чтобы переключение `EID_PROVIDER` не требовало менять схему).

---

### OAuth 2.0 Server (для Custom GPT)

Здесь identity-сервис **выдаёт** OAuth-токены для ChatGPT — это его роль как Authorization Server, а не как клиента.

#### `OAUTH_ACCESS_TOKEN_SECRET`
- **Что это:** HMAC-SHA256 ключ, которым identity-сервис подписывает access-токены, выданные ChatGPT'у. Это **другой** секрет, не Supabase JWT secret.
- **Откуда брать:** генерим как другие секреты (`secrets.token_bytes(32)` + base64).
- **Зачем нужен:** complaints-gateway (другой сервис) валидирует эти токены — он должен знать тот же секрет. То есть это shared secret между identity-сервисом и gateway.
- **Required в pilot.**

#### `OAUTH_ACCESS_TOKEN_TTL_S`
- **Что это:** время жизни access-токена в секундах.
- **Default:** `3600` (1 час).
- **Логика:** ChatGPT действует от имени пользователя; токен короткоживущий, чтобы revocation работала быстро.

#### `OAUTH_AUTHORIZATION_CODE_TTL_S`
- **Что это:** TTL authorization code между `/oauth/authorize` и `/oauth/token`.
- **Default:** `300` (5 минут).
- **Логика:** стандарт OAuth 2.0 (RFC 6749 §10.5): authorization codes должны быть короткоживущими, single-use.

#### `GPT_OAUTH_CLIENT_ID`
- **Что это:** идентификатор OAuth-клиента ChatGPT.
- **Default:** `openai-custom-gpt`.
- **Откуда:** сами выбираем. Это просто строка-идентификатор, ChatGPT передаёт её в `/oauth/authorize?client_id=...`.

#### `GPT_OAUTH_CLIENT_SECRET`
- **Что это:** client_secret OAuth-клиента ChatGPT. ChatGPT передаёт его в `/oauth/token` как HTTP Basic auth.
- **Откуда брать:** генерим `secrets.token_urlsafe(32)`. Один раз вводится в OpenAI ChatGPT Builder при настройке кастомного GPT.
- **Required в pilot.**

#### `GPT_OAUTH_REDIRECT_URI`
- **Что это:** куда ChatGPT хочет редирект после `/oauth/authorize`.
- **Production:** `https://oauth.pstmn.io/v1/callback` (это стандартный callback URL OpenAI, см. их Custom GPT documentation).
- **Required.**

---

### Security & CORS

#### `CORS_ALLOWED_ORIGINS`
- **Что это:** список origins (схема + хост + порт), которым разрешены cross-origin запросы.
- **Откуда брать:**
  - Demo: `*` (любой origin — для удобства разработки). Дефолт.
  - Production: `https://dogestonia.ee,https://chat.openai.com`.
- **Формат:** comma-separated (loader делает `.split(",")`).
- **Кто читает:** `CORSMiddleware` в `_lifespan` (см. M-5 фикс).

#### `ALLOWED_RETURN_URLS`
- **Что это:** allowlist `return_url` параметра для `/auth/eid/start`. После верификации пользователь редиректится назад в SPA — но только если URL в этом allowlist (защита от open redirect).
- **Demo:** хардкодится в код.
- **Pilot:** комплектируется из env.

---

### eID Provider Selection

#### `EID_PROVIDER`
- **Что это:** какой eID-провайдер активен.
- **Допустимые значения:** `mock` | `eideasy` | `authentigate`.
- **Default:** `mock` (для локального dev без credentials).
- **Откуда брать:**
  - Локально — `mock`.
  - test/staging — `eideasy` (если есть `test.eideasy.com` credentials).
  - Production — `eideasy` (ADR-IDS-006) или `authentigate` после получения SK ID creds.
- **Кто читает:** `EIDProviderRegistry.get_active(config)` для выбора провайдера на каждый запрос (не cached — req-17 правило).

#### `NODE_ID`
- **Что это:** идентификатор инстанса/пода для audit-логов (req-17).
- **Откуда брать:** на Railway — `${RAILWAY_REPLICA_ID}` или подобное. Локально — `test-node` или hostname.

#### `EIDEASY_*` (8 переменных)
- Используются только когда `EID_PROVIDER=eideasy`. См. req-18 для деталей. Defaults — заданы в EPIC-IDS-01 Story 2 (`test.eideasy.com`, `smartid,mid-login,ee-id-login`, `EE`).

---

### Backend selection

#### `DB_BACKEND`
- **Что это:** какой backend использует identity-сервис для персистентности.
- **Допустимые значения:** `in_memory` | `supabase`. (`sqlite` убран по H-3 — см. выше.)
- **Default:** `in_memory`.
- **Кто читает:** `provide_service_factory(config)` выбирает реализации репозиториев.
- **Локально:** обычно `in_memory` (быстро, без сети). При работе с Supabase — `supabase`.

---

## 3. Сводка по `ADR-IDS-008` (для контекста)

Это новый ADR, который я добавил. Содержит:

- **Контекст:** два имени для одного HMAC-секрета приводят к расхождению между AppConfig, кодом и `.env` файлами.
- **Решение:** одно поле `eid_hash_secret` в AppConfig; loader читает `EID_HASH_SECRET` с fallback на `DOGESTONIA_EID_SECRET_PEPPER`; в req-07 `PEPPER` помечен deprecated.
- **Обоснование:** один потребитель в коде, provider-agnostic имя, мягкая миграция без breaking change.
- **Последствия:** перечислены конкретные файлы, которые синхронизированы (EPIC-IDS-01, EPIC-IDS-06, req-07, README-index).

---

## 4. Где может быть слабое место (для твоей проверки)

Эти моменты я хочу подсветить — здесь логика может оказаться сломанной, и стоит дополнительно посмотреть.

### 4.1. CORS-middleware и FastAPI lifespan — потенциальный конфликт

В M-5 я добавил паттерн с `app.add_middleware(CORSMiddleware, ...)` ВНУТРИ `_lifespan`. Это решает доступ к `deps.config`, но **FastAPI/Starlette официально не поддерживает регистрацию middleware после старта приложения** — `middleware_stack` собирается при первом запросе.

В реальной реализации скорее всего понадобится один из вариантов:
1. **Module-level + чтение env напрямую** в момент `app = FastAPI(...)`: `cors_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "*").split(",")` — без DI singleton. Минус: нарушение SOA (CORS читает env минуя AppConfig).
2. **Module-level с fabric-функцией**: создать функцию `create_app(config: AppConfig) -> FastAPI`, вызывать `provide_app_config()` в `asgi_app.py` до `FastAPI(...)`. Lifespan тогда только инициализирует DI и configure_logging.
3. **Кастомный middleware** вместо стандартного CORSMiddleware, который читает origins из `app.state.deps` на каждом запросе.

**Решение:** возможно, M-5 фикс надо переформулировать как "вариант 2" — не `add_middleware` в lifespan, а module-level через factory function. Я оставил то, что сказано в аудите дословно, но это место требует подтверждения.

### 4.2. `DOGESTONIA_EID_SECRET_PEPPER` в pilot-валидации

В req-07 я написал:
> `EID_HASH_SECRET | optional | required (или DOGESTONIA_EID_SECRET_PEPPER как fallback)`

Это формально корректно, но **код в `load_config_from_env` должен валидировать ИТОГОВОЕ значение `config.eid_hash_secret`**, а не отдельные env vars. Я это в EPIC-IDS-01 Story 2 указал ("в pilot-валидации проверяется итоговое значение"), но строка в таблице req-07 двусмысленна — её можно прочесть как "обязательна `EID_HASH_SECRET`, иначе `PEPPER`". Логически это одно и то же при правильной реализации, но текст может ввести агента в заблуждение.

**Возможное улучшение:** переписать в более явную форму, например: "`eid_hash_secret` (вычисленное поле AppConfig) — обязательно в pilot. Loader формирует его из `EID_HASH_SECRET` или, если пусто, из `DOGESTONIA_EID_SECRET_PEPPER`."

### 4.3. `hash_secret(...)` в `InMemoryOAuthClientStore.from_config`

Я написал `client_secret_hash=hash_secret(config.gpt_oauth_client_secret or "demo")`, но `hash_secret` — не определён нигде в эпиках. Я пометил это словесно как "локальный helper", но если агент Story 2 не догадается, что это нужно создать (или импортировать из req-14) — будет `NameError`.

**Возможное улучшение:** добавить в Story 2 явное замечание "перед использованием реализовать `hash_secret(plaintext: str) -> str` как HMAC-SHA256 c `OAUTH_ACCESS_TOKEN_SECRET` в качестве ключа", или импортировать из req-14.

### 4.4. `pilot` валидация: `EID_HASH_SECRET` vs `pepper` — что именно required

Я перечислил в pilot-таблице `EID_HASH_SECRET | required (или PEPPER fallback)`. Но что если в production случайно зададут оба пустыми, ожидая что fallback "что-нибудь подберёт"? Loader должен явно проверить: после применения fallback, если строка всё ещё пустая → `ConfigError`. Я это в EPIC-IDS-01 Story 2 описал, но не как отдельный AC.

**Возможное улучшение:** добавить AC `load_config_from_env({"APP_PROFILE": "pilot", ..., "EID_HASH_SECRET": "", "DOGESTONIA_EID_SECRET_PEPPER": ""}) → ConfigError`.

### 4.5. `DB_BACKEND=sqlite` — где именно raise?

Я добавил в EPIC-IDS-01 Story 2 правило валидации, но не уточнил **последовательность проверок**. Что если loader сначала проверит supabase-секреты (которые при `sqlite` пустые), а потом backend-валидацию — пользователь получит ConfigError про `SUPABASE_URL`, а не про `sqlite`. Это сбивает с толку при отладке.

**Возможное улучшение:** в Story 2 описать порядок проверок: сначала backend ∈ {in_memory, supabase}, потом всё остальное.

### 4.6. `request_timeout_s` — но ведь это не только Supabase

Я описал `REQUEST_TIMEOUT_S` как "Таймаут исходящих HTTP-запросов к Supabase PostgREST". Но identity-сервис делает исходящие запросы и к Authentigate (OIDC discovery, token endpoint), к eID Easy (OAuth2 token endpoint). Если все они используют тот же таймаут — описание слишком узкое. Если только Supabase — другие исходящие запросы остаются без таймаута.

**Возможное улучшение:** уточнить описание: либо общий таймаут для всех исходящих, либо разделить на `SUPABASE_REQUEST_TIMEOUT_S` и `OIDC_REQUEST_TIMEOUT_S` (req-12 уже упоминает `OIDC_REQUEST_TIMEOUT_S = 10.0` хардкодом).

---

## 5. Что НЕ сделано и почему

- **Не редактирована `src/`** — её ещё нет, реализация — следующий слой работы.
- **Не редактированы `docs/tech-requirements/impl-epic-*.md`** — это паттерны-source из complaints-gateway, оставлены как референс. Все идентити-адаптации живут в `docs/tasks/epics/EPIC-IDS-*`.
- **Не реализованы стори/таски** — план явно говорил, что это слой документации, декомпозиция в Tasks — следующий слой.
- **Не тронуты req-08, 09, 15, 17, 18** — там всё корректно по аудиту, только в части перекрёстных ссылок.
- **Не удалён `DOGESTONIA_EID_SECRET_PEPPER` полностью** — это сделано намеренно как мягкая миграция (см. ADR-IDS-008). Удаление — отдельная задача после полной миграции деплоев.

---

## 6. Итоговая таблица "что → где → почему"

| ID | Файл | Изменение | Зачем |
|---|---|---|---|
| C-1 | req-07, EPIC-IDS-01 | +`REQUEST_TIMEOUT_S` / `request_timeout_s: int = 15` | EPIC-IDS-05 уже использовал поле, без него — `AttributeError` |
| C-2 | EPIC-IDS-05 | +`class SupabaseHealthRepository` | EPIC-IDS-05 Story 6 уже использовал класс, без него — `NameError` |
| C-3 | EPIC-IDS-04 | AC переписаны под класс `SupabaseJwtValidatorImpl.validate(...)` | Реализация — класс, не функция; тест по старой AC проверял бы пустоту |
| H-1 | EPIC-IDS-06 | +`import base64`, `import os`, `import pytest`, `from core.logging_setup import configure_logging` | Без них pytest падает на сборе |
| H-2 | EPIC-IDS-04 | +`@classmethod from_config(cls, config)` | Story 6 уже вызывает этот метод |
| H-3 | EPIC-IDS-01/03/04 + req-07 | `sqlite` убран из allowed `DB_BACKEND` | Fail-fast: либо валидно, либо `ConfigError` при загрузке, а не позже в DI |
| H-4 | EPIC-IDS-04 | `UnauthorizedError` — only `core.api.security` | Single source of truth: один класс — одна точка |
| M-1 | req-05, req-07, EPIC-IDS-01, EPIC-IDS-06, README-index | `ADR-IDS-008` + единое поле `eid_hash_secret` + fallback loader | Расхождение между `req-07` и `req-17`/`req-18` именами — мёртвый угол для багов |
| M-2 | EPIC-IDS-01 | +фраза "Расширение паттерна req-06" в `check-env` | Чтобы агент не схлопнул список к четырём переменным |
| M-3 | req-07, EPIC-IDS-01 | `SUPABASE_ANON_KEY` удалён | Поле без потребителя — технический долг |
| M-4 | EPIC-IDS-01 | +defaults для `eideasy_*` | Без defaults — None → `TypeError` в провайдере |
| M-5 | EPIC-IDS-02 | +явный паттерн `_lifespan` с `add_middleware(CORSMiddleware, ...)` | Зафиксировать порядок инициализации (см. 4.1 — требует подтверждения) |
| M-6 | EPIC-IDS-02 | Явный список OPTIONS-роутов + примечание | Размытая формулировка "all above non-public" двусмысленна |
| N-6 | EPIC-IDS-05 | `YYYYMMDD_HHMM` → `YYYYMMDDHHMMSS` | Текст не совпадал с filename'ами из req-08 |

---

## 7. Метаданные

- **Methodology:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc) — каждый факт верифицирован против реальных документов (req-07, req-13, req-17, req-18, ADR log).
- **Quality gates пройдены:** 10 `rg`-проверок и markdown linter — без ошибок.
- **Файлы, изменённые в этой итерации:** 9 (`05-adr-log.md`, `07-env-configuration-spec.md`, `README-index.md`, все 6 эпиков).
