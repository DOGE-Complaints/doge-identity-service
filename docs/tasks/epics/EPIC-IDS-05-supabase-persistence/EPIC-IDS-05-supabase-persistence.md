# EPIC-IDS-05 — Supabase Persistence Layer

> **ID:** `EPIC-IDS-05`
> **Layer:** NFR / Infrastructure
> **Статус:** Не реализовано
> **Зависит от:** EPIC-IDS-01 (`AppConfig.supabase_url`, `supabase_service_role`, `database_url`), EPIC-IDS-04 (Protocols `ProfileRepository`, `VerificationSessionStore`, `EIDAuditLogRepository`, `OAuthClientStore`, `StoryDraftRepository`, `HealthRepository`; `provide_service_factory` с заглушкой `supabase`)
> **Блокирует:** EPIC-IDS-06 (live integration tests)

---

## 1. Назначение

HTTP-клиент к Supabase PostgREST API без Supabase SDK — `SupabaseDatabase` через httpx. Supabase-реализации Protocols из EPIC-IDS-04. 5-уровневый healthcheck identity-таблиц при старте. Применение SQL-схемы из [`docs/requirements/08-supabase-migrations.md`](../../requirements/08-supabase-migrations.md) и дополнительной миграции для plug-in eID-провайдеров из [`docs/requirements/17`](../../requirements/17-eid-provider-abstraction.md) §"Изменения в DB схеме".

## 2. Epic Goal

При `DB_BACKEND=supabase` в `.env`:
- `make serve` стартует, логи: `backend=supabase db_ready=True db_checks={connectivity:ok, schema:ok, columns:ok, provider_state:ok, policy_probe:ok}`.
- `GET /ready` возвращает 200 с тем же `db_checks`.
- Insert профиля через `provide_service_factory().get_profile_repository().upsert(...)` сохраняется в Supabase; чтение возвращает тот же объект.
- Если Supabase недоступен на старте — `db_ready=False`, `/ready` возвращает 503 с `degraded`, сервер не падает.

## 3. Бизнес-контекст

`DB_BACKEND=supabase` — единственный режим, который сохраняет:
- профили пользователей (`profiles` — req-08 миграция 1),
- in-flight eID-сессии (`eid_verification_sessions` — req-08 миграция 2 + req-17 ALTER),
- immutable audit-журнал (`eid_audit_events` — req-08 миграция 3),
- OAuth-клиенты и issued tokens (если хранить state, иначе stateless JWT — req-14),
- story drafts (`story_drafts` — req-15 §"story_drafts table").

Без этого эпика identity-сервис работает только in-memory (демо-режим). Требования к надёжности:
- service_role bypass RLS — серверная сторона (req-08 §"RLS").
- Identity-сервис **не** использует gateway-таблицы (`stories`, `doge_issues`, `cluster_memberships`).
- ADR-IDS-005 (REQ-README open question) — psycopg vs supabase-py: в этом эпике используется **PostgREST + httpx** (паттерн gateway, без supabase-py SDK).

## 4. Предусловия

- EPIC-IDS-01: `AppConfig` содержит `supabase_url`, `supabase_service_role`, `supabase_jwt_secret`, `database_url`. Fail-fast `ConfigError` при `pilot` без секретов.
- EPIC-IDS-04: Protocols + `provide_service_factory` с веткой `db_backend == "supabase"` (фолбэк на InMemory + warning). InMemory-репозитории — справочная реализация поведения.

## 5. Целевые файлы

```
src/core/infrastructure/db_supabase.py
supabase/migrations/20260525000001_create_profiles.sql              (из req-08)
supabase/migrations/20260525000002_create_eid_verification_sessions.sql (из req-08)
supabase/migrations/20260525000003_create_eid_audit_events.sql      (из req-08)
supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql (из req-17)
supabase/migrations/YYYYMMDD_HHMM_create_story_drafts.sql           (из req-15)
supabase/migrations/YYYYMMDD_HHMM_create_oauth_state.sql            (req-14; опционально если stateless)
src/core/infrastructure/providers.py                                (update — раскомментировать Supabase ветку)
src/core/api/dependencies.py                                        (update — Supabase healthcheck)
```

## 6. Stories (заготовка)

### Story 1: `SupabaseDatabase` HTTP-клиент

- **Why:** PostgREST через httpx — меньше зависимостей, полный контроль над запросами, тестируемо. Один `service_role_key` передаётся и в `apikey`, и в `Authorization: Bearer` (требование Supabase PostgREST).
- **Inputs:** Паттерн [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 1".
- **Outputs:**
  - `src/core/infrastructure/db_supabase.py`:
    - `@dataclass(frozen=True) class SupabaseDatabase`: `base_url`, `service_role_key`, `timeout_s`.
    - `classmethod from_http(cls, supabase_url, service_role_key, timeout_s=15.0)` — раздаёт `ValueError` при пустых аргументах, нормализует `base_url`.
    - `_headers(prefer=None)` — `apikey` + `Authorization: Bearer` + `Content-Type: application/json` + опциональный `Prefer`.
    - `_request(method, path, params=None, json_body=None, prefer=None)` — `httpx.Client(timeout=...)`, `response.raise_for_status()`, JSON-парсинг или `None` (при пустом ответе).
    - PostgREST filter cheat sheet в docstring модуля: `eq.`, `in.()`, `is.null`, `gt.`, `lt.`.
- **Acceptance Criteria:**
  - `SupabaseDatabase.from_http("", "key")` → `ValueError`.
  - `SupabaseDatabase.from_http("https://x.co/", "key").base_url == "https://x.co"` (без trailing slash).
  - `_headers()["apikey"] == _headers()["Authorization"].split()[-1]` (одинаковое значение).
  - `_request` при HTTP 5xx логирует через `logger.error` и пробрасывает `httpx.HTTPError`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 1" — копия Task 1.1 без изменений.

### Story 2: Supabase-репозитории (identity-набор)

- **Why:** Тонкие обёртки над `_request`. Один паттерн на все репозитории: POST + `Prefer: resolution=merge-duplicates` для upsert, GET + `eq.` для lookup, PATCH для update. JSONB-поля (`provider_session_data`) нормализуются.
- **Inputs:**
  - Паттерн: [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 2".
  - Схемы таблиц: [`docs/requirements/08`](../../requirements/08-supabase-migrations.md) §миграции 1-3, [`docs/requirements/17`](../../requirements/17-eid-provider-abstraction.md) §"Изменения в DB схеме" (новые колонки `provider`, `provider_session_data`).
- **Outputs (в `db_supabase.py`):**
  - `SupabaseProfileRepository`:
    - `get_by_supabase_user_id(user_id)` → `GET /rest/v1/profiles?supabase_user_id=eq.{user_id}&limit=1`.
    - `get_by_verified_person_hash(hash_)` → `GET /rest/v1/profiles?verified_person_hash=eq.{hash}&limit=1`.
    - `upsert(profile)` → `POST /rest/v1/profiles` + `Prefer: resolution=merge-duplicates`.
    - `attach_eid_verification(...)` → `PATCH /rest/v1/profiles?supabase_user_id=eq.{user_id}` с `eid_verified=true`, hash, timestamp. При коллизии unique-индекса (req-08 partial unique on `verified_person_hash`) — `httpx.HTTPStatusError 409` → возвращается как доменная `ProfileConflictError`.
  - `SupabaseVerificationSessionStore`:
    - `create(session)` → POST `eid_verification_sessions` с `provider`, `provider_session_data` (JSONB).
    - `get_by_state(state)` → `GET /rest/v1/eid_verification_sessions?state=eq.{state}&status=eq.started&limit=1`.
    - `mark_consumed(session_id)` → `PATCH ?id=eq.{id}` `{status: "consumed"}`.
    - `mark_failed(session_id, reason)` → `PATCH ?id=eq.{id}` `{status: "failed", failure_reason: reason}` (если поле есть).
    - `expire_pending(now)` → `PATCH ?status=eq.started&expires_at=lt.{now_iso}` `{status: "expired"}`.
  - `SupabaseEIDAuditLogRepository`:
    - `log_event(event)` → POST. Идемпотентность не требуется (append-only).
    - `list_events(...)` → GET с фильтрами + `order=created_at.desc&limit=...`.
  - `SupabaseOAuthClientStore` — read-only, MVP из env (`gpt_oauth_client_id`), но опционально из таблицы `oauth_clients` (если решим хранить динамически — Open Question).
  - `SupabaseStoryDraftRepository` — CRUD по `story_drafts` (req-15 §"story_drafts table"). Поля: `draft_id`, `supabase_user_id`, `payload jsonb`, `status`, `created_at`, `submitted_at`.
  - **`SupabaseHealthRepository` (audit C-2):** тонкая обёртка над уже реализованным `SupabaseDatabase.healthcheck()` из Story 1. Удовлетворяет Protocol `HealthRepository` из EPIC-IDS-04 Story 1 — без неё ветка `db_backend == "supabase"` в Story 6 упадёт с `NameError` при сборке factory.

    ```python
    class SupabaseHealthRepository:
        """Backend-specific HealthRepository for /ready endpoint."""

        def __init__(self, db: SupabaseDatabase) -> None:
            self._db = db

        def ping(self) -> bool:
            return self._db.healthcheck()
    ```

  - `_jsonb_normalize(row, fields)` — helper: если PostgREST вернул JSONB как `str`, делает `json.loads`.
- **Acceptance Criteria:**
  - `SupabaseProfileRepository(db).get_by_supabase_user_id("u1")` — GET с `eq.u1&limit=1`; пустой результат → `None`.
  - `SupabaseProfileRepository(db).attach_eid_verification(...)` с уже занятым `verified_person_hash` → доменная ошибка conflict (не bare httpx exception).
  - `SupabaseVerificationSessionStore.create(session)` — body содержит `provider`, `provider_session_data` (даже пустой `{}`).
  - `SupabaseEIDAuditLogRepository.log_event(event)` идемпотентен на app-уровне: повторный вызов с тем же event объектом не падает (audit append-only).
  - `SupabaseHealthRepository(db).ping()` делегирует на `db.healthcheck()`; `isinstance(SupabaseHealthRepository(db), HealthRepository)` — True (runtime Protocol check из EPIC-IDS-04).
  - JSONB поля при чтении — всегда `dict` (или `list`), никогда `str`.
- **Pattern source:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 2" — паттерн `_request("POST", path, json_body=..., prefer="resolution=merge-duplicates")`. Таблицы заменены на identity-набор.

### Story 3: 5-уровневый healthcheck

- **Why:** Сервер поднимается даже если Supabase упал — `/ready` возвращает `degraded` и `db_ready=False`. Это intentional: нет crashloop, оператор видит проблему через readiness. Identity-таблицы — иные чем у gateway.
- **Inputs:**
  - Паттерн методов: [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 3", Task 3.1.
  - identity-таблицы: req-08 §"Readiness check" + req-17 §"Изменения в DB схеме".
- **Outputs (методы на `SupabaseDatabase`):**
  - `healthcheck() -> bool` — GET `/rest/v1/?limit=1`, любая ошибка → False.
  - `required_tables_ready() -> bool` — проверка существования identity-таблиц:
    ```python
    tables = ["profiles", "eid_verification_sessions", "eid_audit_events", "story_drafts"]
    ```
    Для каждой: `GET /rest/v1/{table}?limit=1`. Возвращает `True` только если все 4 запроса успешны.
  - `required_columns_ready() -> bool` — `GET /rest/v1/profiles?select=supabase_user_id,eid_verified,verified_person_hash,eid_verified_at&limit=1`. Проверяет наличие критичных колонок req-08 миграция 1.
  - `provider_state_ready() -> bool` — `GET /rest/v1/eid_verification_sessions?select=provider,provider_session_data&limit=1`. Проверяет что миграция req-17 применена (новые колонки).
  - `service_role_policy_probe() -> bool` — `POST /rest/v1/eid_audit_events` с dummy event (`event_type=health_probe`, `success=true`, `supabase_user_id=null`) + `DELETE /rest/v1/eid_audit_events?event_type=eq.health_probe`. Использует **low-traffic** таблицу `eid_audit_events`, не `profiles` (чтобы не засорять профили). При ошибке RLS → False.
- **`build_api_dependencies()` update (`src/core/api/dependencies.py`):**
  - При `db_backend == "supabase"`:
    ```python
    health_db = SupabaseDatabase.from_http(config.supabase_url, config.supabase_service_role)
    db_checks = {
        "connectivity": health_db.healthcheck(),
        "schema": health_db.required_tables_ready(),
        "columns": health_db.required_columns_ready(),
        "provider_state": health_db.provider_state_ready(),
        "policy_probe": health_db.service_role_policy_probe(),
    }
    db_ready = all(db_checks.values())
    ```
- **Acceptance Criteria:**
  - Все 5 healthcheck-методов возвращают `bool`, никогда не raise (внутри `try/except Exception: return False`).
  - При сетевой ошибке → `False`.
  - `GET /ready` при `db_backend=supabase` + `db_ready=False` → HTTP 503, envelope `{"data": {"status": "degraded", ..., "db_checks": {...}}}`.
  - Startup-лог содержит `db_checks={'connectivity': True/False, ...}` (после `configure_logging`).
- **Pattern source:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 3" — структура методов + интеграция в `build_api_dependencies`. Замена tables/columns на identity-набор; `service_role_policy_probe` использует `eid_audit_events` вместо `stories`.

### Story 4: SQL schema — ссылка на req-08 + новые миграции

- **Why:** Bootstrap-схема identity-сервиса полностью описана в [`docs/requirements/08`](../../requirements/08-supabase-migrations.md) (3 миграции). Эпик **ссылается, не дублирует**. Добавляются миграции из req-17 (`provider`/`provider_session_data`) и опционально req-15 (`story_drafts`).
- **Inputs:**
  - [`docs/requirements/08-supabase-migrations.md`](../../requirements/08-supabase-migrations.md) — миграции 1-3 целиком.
  - [`docs/requirements/17`](../../requirements/17-eid-provider-abstraction.md) §"Изменения в DB схеме" — ALTER миграция.
  - [`docs/requirements/15-story-authorization.md`](../../requirements/15-story-authorization.md) §"story_drafts table".
- **Outputs:**
  - `supabase/migrations/20260525000001_create_profiles.sql` — копия из req-08 миграция 1 (с RLS, partial unique index, trigger `update_profiles_updated_at`).
  - `supabase/migrations/20260525000002_create_eid_verification_sessions.sql` — из req-08 миграция 2.
  - `supabase/migrations/20260525000003_create_eid_audit_events.sql` — из req-08 миграция 3.
  - `supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql` — из req-17:
    - `ADD COLUMN provider TEXT NOT NULL DEFAULT 'eideasy'`.
    - `ADD COLUMN provider_session_data JSONB NOT NULL DEFAULT '{}'`.
    - `ALTER COLUMN nonce DROP NOT NULL`, `code_verifier_encrypted DROP NOT NULL`, `code_verifier_hash DROP NOT NULL`.
    - `CREATE INDEX IF NOT EXISTS idx_eid_sessions_provider`.
  - `supabase/migrations/20260527000001_create_story_drafts.sql` — из req-15 (поля `draft_id UUID PK`, `supabase_user_id UUID FK`, `payload JSONB`, `status TEXT CHECK (status IN ('draft', 'submitted'))`, timestamps + RLS + service_role policy).
  - Конвенция (audit N-6): `YYYYMMDDHHMMSS_description.sql` — 14 цифр timestamp без разделителей, без `_` между датой и временем. Соответствует filename'ам из req-08 (`20260525000001_create_profiles.sql`) и filename'ам этой Story (см. Outputs выше). Идемпотентность через `IF NOT EXISTS`, каждая новая таблица — с `ENABLE ROW LEVEL SECURITY` и явной service_role policy (req-08 шаблон).
- **Acceptance Criteria:**
  - Все миграции применяются на чистый Supabase-проект последовательно без ошибок.
  - После применения: `required_tables_ready() == True`, `required_columns_ready() == True`, `provider_state_ready() == True`.
  - `service_role_policy_probe()` → True (RLS не блокирует service_role).
  - Каждая таблица имеет `service_role` policy (либо bypass через service_role API key, явная policy для INSERT/SELECT/UPDATE).
- **Pattern source:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 4" — конвенция имён + идемпотентность + RLS policy. SQL содержимое — из identity-requirements.

### Story 5: Настройка Supabase проекта + live integration credentials

- **Why:** Любой агент должен уметь поднять идентити-сервис на новом Supabase-проекте за фиксированные шаги. Тестовые creds должны быть отдельными от production.
- **Inputs:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 5".
- **Outputs (runbook + secrets layout, не код):**
  - Runbook (в README-блоке эпика или в docs/runbook):
    1. supabase.com → Create new project.
    2. Settings → API → `Project URL` = `SUPABASE_URL`.
    3. Settings → API → `service_role` key = `SUPABASE_SERVICE_ROLE`.
    4. Settings → API → `JWT Secret` = `SUPABASE_JWT_SECRET` (для req-09 HS256).
    5. SQL Editor → выполнить все 5 миграций последовательно (Story 4).
    6. `.env` заполнить, `make check-env`, `make serve` → проверить startup-логи `db_ready=True`.
  - GitHub Secrets для CI (EPIC-IDS-06 будет использовать):
    - `SUPABASE_TEST_URL` — отдельный тестовый проект.
    - `SUPABASE_TEST_SERVICE_ROLE_KEY` — service_role key тестового проекта.
    - `SUPABASE_TEST_JWT_SECRET` — JWT secret тестового проекта (для positive JWT-тестов).
- **Acceptance Criteria:**
  - `make serve` с заполненным `.env` (`DB_BACKEND=supabase`) → логи `backend=supabase db_ready=True db_checks={connectivity:True, schema:True, columns:True, provider_state:True, policy_probe:True}`.
  - `make test-live` (после EPIC-IDS-06) с `.env` тестового проекта → connectivity test PASSED.
  - Производственный Supabase проект изолирован от тестового (разные URLs).
- **Pattern source:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 5" — структура runbook.

### Story 6: Backend switch — раскомментирование Supabase в `provide_service_factory`

- **Why:** После Story 1-3 у нас есть рабочие Supabase-реализации Protocols. Финальный шаг — заменить заглушку `# TODO EPIC-IDS-05` в `provide_service_factory` (EPIC-IDS-04) на реальную композицию.
- **Inputs:** `provide_service_factory` из EPIC-IDS-04 + Supabase-репозитории из Story 2.
- **Outputs:**
  - `src/core/infrastructure/providers.py` — ветка `db_backend == "supabase"`:
    ```python
    elif resolved_config.db_backend == "supabase":
        if not resolved_config.supabase_url or not resolved_config.supabase_service_role:
            raise ValueError("DB_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE")
        supabase_db = SupabaseDatabase.from_http(
            supabase_url=resolved_config.supabase_url,
            service_role_key=resolved_config.supabase_service_role,
            timeout_s=float(resolved_config.request_timeout_s or 15),  # только Supabase PostgREST; OIDC — config.oidc_request_timeout_s (EPIC-IDS-01)
        )
        profile_repository = SupabaseProfileRepository(supabase_db)
        verification_session_store = SupabaseVerificationSessionStore(supabase_db)
        eid_audit_log_repository = SupabaseEIDAuditLogRepository(supabase_db)
        health_repository = SupabaseHealthRepository(supabase_db)
        oauth_client_store = SupabaseOAuthClientStore(supabase_db, fallback_config=resolved_config)
        story_draft_repository = SupabaseStoryDraftRepository(supabase_db)
    ```
  - Все остальные сервисы (`oauth_token_service`, `bearer_token_auth`, `eid_provider_registry`) остаются как в EPIC-IDS-04 (backend-agnostic).
- **Acceptance Criteria:**
  - `provide_service_factory(config_with_db_backend_supabase)` возвращает factory с `SupabaseProfileRepository` и т.д.
  - `build_api_dependencies()` при `DB_BACKEND=supabase` — `db_checks` заполнен, `db_ready` отражает реальность.
  - Переключение `DB_BACKEND=in_memory ↔ supabase` через env — единственный механизм; код не модифицируется.
- **Pattern source:** [`docs/tech-requirements/impl-epic-05`](../../tech-requirements/impl-epic-05-supabase-persistence.md) §"Story 2", Task 2.3 — точная позиция в `providers.py`.

## 7. Critical Pitfalls (identity-flavored)

- **Service role vs anon key:** `SUPABASE_SERVICE_ROLE` bypass RLS — никогда не отдавать клиентам. Только server-side (req-08 §"RLS").
- **PostgREST всегда возвращает список:** `GET ...?limit=1` возвращает `[{...}]` или `[]`, не объект. Всегда `if rows else None`.
- **JSONB-поля:** PostgREST может вернуть `provider_session_data` как `dict` или `str` (зависит от accept-header / версии). Всегда нормализовать через `_jsonb_normalize`.
- **Upsert через POST + Prefer:** `prefer="resolution=merge-duplicates"` + PK constraint. Без `Prefer` — дублирование (или 409 если есть unique).
- **RLS policies:** если `service_role_policy_probe()` False — добавить `CREATE POLICY ... FOR ALL TO service_role USING (true)` к таблице. Identity-таблицы (req-08) уже имеют policies — но при добавлении новых (`story_drafts`, `oauth_*`) — обязательно создать policy.
- **db_ready=False при старте:** сервер поднимается (no crashloop), `/ready` возвращает 503. Это intentional — оператор видит проблему, нет каскадных рестартов.
- **Identity-таблицы, не gateway:** в `required_tables_ready` использовать `["profiles", "eid_verification_sessions", "eid_audit_events", "story_drafts"]`. НЕ `["stories", "doge_issues", "cluster_memberships"]`.
- **`service_role_policy_probe` использует `eid_audit_events`:** низкий трафик, append-only, безопасно для probe. НЕ использовать `profiles` (засорение реальных данных).
- **Partial unique index на `verified_person_hash`:** позволяет много NULL (unverified users), но enforce unique для verified — критичный инвариант 1 eID = 1 account (req-13). Conflict при `attach_eid_verification` должен превращаться в доменное исключение, не raw httpx.

## 8. Верификация эпика

```bash
# 1. Импорт
python3.11 -c "
from core.infrastructure.db_supabase import (
    SupabaseDatabase, SupabaseProfileRepository, SupabaseVerificationSessionStore,
    SupabaseEIDAuditLogRepository, SupabaseOAuthClientStore, SupabaseStoryDraftRepository,
    SupabaseHealthRepository,
)
print('Supabase imports OK')
"

# 2. Connectivity (требует реальный .env с DB_BACKEND=supabase)
python3.11 -c "
from core.config import provide_app_config
from core.infrastructure.db_supabase import SupabaseDatabase
cfg = provide_app_config()
if cfg.db_backend == 'supabase':
    db = SupabaseDatabase.from_http(cfg.supabase_url, cfg.supabase_service_role)
    print('connectivity:', db.healthcheck())
    print('tables:', db.required_tables_ready())
    print('columns:', db.required_columns_ready())
    print('provider_state:', db.provider_state_ready())
    print('policy_probe:', db.service_role_policy_probe())
else:
    print('DB_BACKEND != supabase, skipping live check')
"

# 3. /ready endpoint
make serve &
sleep 3
curl -s http://localhost:8100/ready | python3 -m json.tool
# Ожидаемо при db_backend=supabase: {"data": {"status": "ready", "db_backend": "supabase", "db_ready": true, "db_checks": {...}}}
kill %1

# 4. Live integration tests (после EPIC-IDS-06)
python3.11 -m pytest tests/integration/supabase/ -v
```

## 9. Open Questions

- **ADR-IDS-005 (README-index):** psycopg vs PostgREST. Этот эпик принимает PostgREST + httpx (gateway-паттерн). Решение зафиксировано в ADR — если ADR-IDS-005 пересмотрит выбор в пользу psycopg, EPIC-IDS-05 нужно пересмотреть полностью (другой `SupabaseDatabase` контракт, другие репозитории). Парковка: статус ADR-IDS-005 проверяется до старта Story 1.
- **OAuth state storage:** stateless JWT access tokens (req-14 §"Access Token Format") не требуют DB. Но authorization codes (5-минутный TTL) обычно хранят. Решение: использовать `InMemoryOAuthTokenService` с in-process anti-replay set, либо отдельная таблица `oauth_authorization_codes` (миграция в Story 4). На P1 — выбрать. По умолчанию: anti-replay in-memory (per-pod), это OK для MVP.
- **HMAC-секрет:** **закрыто** — `DOGESTONIA_EID_SECRET` / `config.eid_secret` (`ADR-IDS-008` пересмотр 2026-05-27). EPIC-IDS-05 не использует секрет напрямую (хэш в `EIDProviderPort.handle_callback`).
- **Supabase CLI vs SQL Editor:** README-блок Story 5 предлагает оба способа применения миграций. `supabase db push` требует supabase CLI и `supabase link`. Для MVP — SQL Editor достаточно; CLI добавляется в Story 5 как опциональный шаг.
