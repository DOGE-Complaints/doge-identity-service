# NFR: Supabase Persistence Layer

## Назначение

HTTP-клиент к Supabase PostgREST API без Supabase SDK. `SupabaseDatabase` выполняет CRUD через httpx. 5-уровневый healthcheck при старте. Bootstrap SQL schema. Инкрементные миграции.

## Источник паттерна

`docs/runtime-docs/bootstrap-infrastructure/04-supabase-persistence.md`

## Бизнес-контекст

Переключение сервиса с `DB_BACKEND=in_memory` на `DB_BACKEND=supabase` — всё сохраняется в реальной БД. Без этого эпика сервис работает только как in-memory demo.

## Предусловие

- Epic 01 выполнен: `AppConfig` с `supabase_url`, `supabase_service_role`
- Epic 04 выполнен: `provide_service_factory()` с заглушкой для supabase backend

## Целевые файлы

```
src/core/infrastructure/db_supabase.py
supabase/bootstrap/000_full_init.sql
supabase/migrations/YYYYMMDD_HHMM_description.sql
```

---

## Epic Goal

При `DB_BACKEND=supabase` сервер стартует и логи показывают `backend=supabase db_ready=True checks=connectivity:ok,schema:ok,...`. Story intake сохраняется в Supabase и читается обратно.

---

## Story 1: SupabaseDatabase — HTTP клиент

### Зачем

Прямые HTTP запросы к PostgREST вместо Supabase SDK: меньше зависимостей, полный контроль над запросами, легко тестировать. Каждый запрос несёт `apikey` и `Authorization: Bearer` с одним и тем же service_role key.

### Tasks

**Task 1.1:** Создать `src/core/infrastructure/db_supabase.py` — SupabaseDatabase класс.

```python
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SupabaseDatabase:
    base_url: str           # https://<ref>.supabase.co
    service_role_key: str   # service_role key (не anon key!)
    timeout_s: float = 15.0

    @classmethod
    def from_http(
        cls,
        supabase_url: str,
        service_role_key: str,
        timeout_s: float = 15.0,
    ) -> "SupabaseDatabase":
        if not supabase_url:
            raise ValueError("supabase_url is required")
        if not service_role_key:
            raise ValueError("service_role_key is required")
        return cls(
            base_url=supabase_url.rstrip("/"),
            service_role_key=service_role_key,
            timeout_s=timeout_s,
        )

    def _headers(self, *, prefer: str | None = None) -> dict[str, str]:
        headers = {
            "apikey": self.service_role_key,
            "Authorization": f"Bearer {self.service_role_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    def _request(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: dict | list | None = None,
        prefer: str | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=self._headers(prefer=prefer),
                    params=params,
                    json=json_body,
                )
            if not response.is_success:
                logger.error(
                    "supabase_request_error method=%s path=%s status=%d body=%.300s",
                    method, path, response.status_code, response.text,
                )
            response.raise_for_status()
            return response.json() if response.text.strip() else None
        except httpx.HTTPError as exc:
            logger.error("supabase_http_error method=%s path=%s exc=%r", method, path, exc)
            raise
```

**PostgREST фильтры** (использовать в params):

| Оператор | Пример params | Смысл |
|---------|--------------|-------|
| `eq.` | `{"story_id": "eq.abc"}` | WHERE story_id = 'abc' |
| `in.` | `{"status": "in.(a,b,c)"}` | WHERE status IN ('a','b','c') |
| `is.` | `{"field": "is.null"}` | WHERE field IS NULL |
| `gt.`, `lt.` | `{"score": "gt.50"}` | WHERE score > 50 |

### Acceptance Criteria

- `SupabaseDatabase.from_http("", "key")` бросает `ValueError`
- `SupabaseDatabase.from_http("https://test.co", "key")` создаёт объект с `base_url="https://test.co"`
- `_headers()` содержит `apikey` и `Authorization: Bearer` с одинаковым значением
- `_request()` при HTTP 4xx/5xx логирует ошибку и пробрасывает `httpx.HTTPError`

---

## Story 2: CRUD паттерны и репозитории

### Зачем

Каждый Supabase репозиторий — тонкая обёртка вокруг `_request()`. INSERT/UPSERT через POST с `prefer="resolution=merge-duplicates"`. SELECT через GET с PostgREST фильтрами. UPDATE через PATCH.

### Tasks

**Task 2.1:** Добавить `SupabaseStoryRepository` в `db_supabase.py`.

```python
class SupabaseStoryRepository:
    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def save_story(self, record: object) -> object:
        self._db._request(
            method="POST",
            path="/rest/v1/stories",
            json_body=_story_to_row(record),
            prefer="resolution=merge-duplicates",
        )
        return record

    def get_story(self, story_id: str) -> object | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/stories",
            params={"story_id": f"eq.{story_id}", "limit": "1"},
        )
        return _story_from_row(rows[0]) if rows else None

    def list_stories(self) -> list[object]:
        rows = self._db._request(method="GET", path="/rest/v1/stories") or []
        return [_story_from_row(r) for r in rows]

    def list_stories_ready_for_clustering(self) -> list[object]:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/stories",
            params={"lifecycle_status": "eq.ready_for_clustering"},
        ) or []
        return [_story_from_row(r) for r in rows]

    def update_lifecycle_status(self, story_id: str, status: object) -> None:
        self._db._request(
            method="PATCH",
            path="/rest/v1/stories",
            params={"story_id": f"eq.{story_id}"},
            json_body={"lifecycle_status": str(status.value if hasattr(status, 'value') else status)},
        )


def _story_to_row(record: object) -> dict:
    """Convert StoryRecord dataclass to Supabase row dict."""
    import dataclasses
    return {
        k: v for k, v in dataclasses.asdict(record).items()
        if v is not None
    }


def _story_from_row(row: dict) -> object:
    """Convert Supabase row dict back to StoryRecord."""
    # Import здесь — чтобы избежать circular import
    from core.domain.models import StoryRecord
    # JSONB поля могут прийти как dict или как str — всегда нормализуй
    for key in ("narrative_title_json", "narrative_description_json"):
        if key in row and isinstance(row[key], str):
            import json
            row[key] = json.loads(row[key])
    return StoryRecord(**{k: v for k, v in row.items() if k in StoryRecord.__dataclass_fields__})
```

**Task 2.2:** По аналогии добавить `SupabaseIdempotencyRepository`, `SupabaseStorySignalStore`, `SupabaseClusterMembershipStore`.

Паттерн одинаков для всех:

```python
class SupabaseIdempotencyRepository:
    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def get_by_key(self, key: str) -> object | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/idempotency_keys",
            params={"key": f"eq.{key}", "limit": "1"},
        )
        return _idempotency_from_row(rows[0]) if rows else None

    def save(self, record: object) -> object:
        self._db._request(
            method="POST",
            path="/rest/v1/idempotency_keys",
            json_body=_idempotency_to_row(record),
            prefer="resolution=merge-duplicates",
        )
        return record
```

**Task 2.3:** Обновить `provide_service_factory()` в `providers.py` — раскомментировать Supabase секцию после реализации репозиториев.

```python
if resolved_config.db_backend == "supabase" and resolved_config.supabase_url:
    from core.infrastructure.db_supabase import (
        SupabaseDatabase,
        SupabaseStoryRepository,
        SupabaseIdempotencyRepository,
        SupabaseStorySignalStore,
        SupabaseClusterMembershipStore,
        SupabaseIssueCandidateStore,
        SupabaseIssueProjectionStore,
        SupabaseReviewAuditLogRepository,
        SupabaseEvidencePackRepository,
    )
    supabase_db = SupabaseDatabase.from_http(
        supabase_url=resolved_config.supabase_url,
        service_role_key=resolved_config.supabase_service_role,
        timeout_s=float(resolved_config.request_timeout_s),
    )
    story_repository = SupabaseStoryRepository(supabase_db)
    idempotency_repository = SupabaseIdempotencyRepository(supabase_db)
    story_signal_store = SupabaseStorySignalStore(supabase_db)
    cluster_membership_store = SupabaseClusterMembershipStore(supabase_db)
    issue_candidate_store = SupabaseIssueCandidateStore(supabase_db)
    issue_projection_store = SupabaseIssueProjectionStore(supabase_db)
    review_audit_log_repository = SupabaseReviewAuditLogRepository(supabase_db)
    evidence_pack_repository = SupabaseEvidencePackRepository(supabase_db)
```

### Acceptance Criteria

- `SupabaseStoryRepository(db).save_story(record)` вызывает `POST /rest/v1/stories` с `Prefer: resolution=merge-duplicates`
- `SupabaseStoryRepository(db).get_story("id")` вызывает `GET /rest/v1/stories?story_id=eq.id&limit=1`
- POST всегда возвращает список — `get_story` проверяет `if rows else None`
- JSONB поля нормализуются: `isinstance(raw, str)` → `json.loads(raw)`

---

## Story 3: Healthcheck и Readiness Checks

### Зачем

5-уровневая проверка при старте. Сервер поднимается даже если Supabase недоступен — но `/ready` вернёт `degraded` и `db_ready=False`. Это intentional: нет crashloop, но оператор видит проблему.

### Tasks

**Task 3.1:** Добавить healthcheck методы в `SupabaseDatabase`.

```python
def healthcheck(self) -> bool:
    """Basic connectivity — GET /rest/v1/ with limit=1."""
    try:
        self._request(method="GET", path="/rest/v1/", params={"limit": "1"})
        return True
    except Exception:
        return False

def required_tables_ready(self) -> bool:
    """All required tables exist and are accessible."""
    tables = [
        "stories", "idempotency_keys", "story_embeddings",
        "doge_issues", "doge_issue_embeddings", "issue_candidates",
        "review_audit_log", "issue_story_links", "story_signals",
        "cluster_memberships",
    ]
    try:
        for table in tables:
            rows = self._request(
                method="GET",
                path=f"/rest/v1/{table}",
                params={"limit": "1"},
            )
            if rows is None:
                return False
        return True
    except Exception:
        return False

def required_columns_ready(self) -> bool:
    """Core columns exist in stories table."""
    try:
        self._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": "story_id,lifecycle_status,narrative_canonical_type,submitter_identity_issuer",
                "limit": "1",
            },
        )
        return True
    except Exception:
        return False

def required_stories_intake_v2_columns_ready(self) -> bool:
    """Intake v2 narrative columns exist."""
    try:
        self._request(
            method="GET",
            path="/rest/v1/stories",
            params={
                "select": "narrative_title_json,narrative_description_json,narrative_session_language",
                "limit": "1",
            },
        )
        return True
    except Exception:
        return False

def service_role_policy_probe(self) -> bool:
    """
    POST a dummy record to stories and DELETE it.
    Verifies RLS policy allows service_role INSERT.
    """
    import uuid
    dummy_id = f"probe-{uuid.uuid4()}"
    try:
        self._request(
            method="POST",
            path="/rest/v1/stories",
            json_body={"story_id": dummy_id, "_probe": True},
            prefer="resolution=merge-duplicates",
        )
        # cleanup
        self._request(
            method="DELETE",
            path="/rest/v1/stories",
            params={"story_id": f"eq.{dummy_id}"},
        )
        return True
    except Exception:
        return False
```

**Task 3.2:** Обновить `build_api_dependencies()` в `dependencies.py` — раскомментировать Supabase healthcheck секцию.

```python
if db_backend == "supabase":
    from core.infrastructure.db_supabase import SupabaseDatabase
    health_db = SupabaseDatabase.from_http(
        supabase_url=config.supabase_url,
        service_role_key=config.supabase_service_role,
    )
    db_checks = {
        "connectivity": health_db.healthcheck(),
        "schema": health_db.required_tables_ready(),
        "columns": health_db.required_columns_ready(),
        "columns_v2": health_db.required_stories_intake_v2_columns_ready(),
        "policy_probe": health_db.service_role_policy_probe(),
    }
    db_ready = all(db_checks.values())
```

### Acceptance Criteria

- Все 5 методов healthcheck возвращают `bool` (никогда не бросают исключений наружу)
- При сетевой ошибке — возвращают `False`, не `raise`
- `GET /ready` при `DB_BACKEND=supabase` с `db_ready=False` → HTTP 503 с `"status": "degraded"`
- Startup логи показывают `db_ready=True checks=connectivity:ok,schema:ok,...`

---

## Story 4: SQL Schema и Миграции

### Зачем

Bootstrap SQL создаёт все таблицы, индексы и RLS policies. Миграции накапливаются — применяются вручную через Supabase SQL Editor в хронологическом порядке.

### Tasks

**Task 4.1:** Создать `supabase/bootstrap/000_full_init.sql`.

```sql
-- Full initialization for a new Supabase project.
-- Run in Supabase Dashboard → SQL Editor.

-- ─── stories ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stories (
    story_id TEXT PRIMARY KEY,
    lifecycle_status TEXT NOT NULL DEFAULT 'intake_received',
    submitter_identity_issuer TEXT NOT NULL DEFAULT 'anonymous',
    narrative_canonical_type TEXT,
    narrative_title_json JSONB,
    narrative_description_json JSONB,
    narrative_session_language TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE stories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON stories FOR ALL TO service_role USING (true);

-- ─── idempotency_keys ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS idempotency_keys (
    key TEXT PRIMARY KEY,
    story_id TEXT REFERENCES stories(story_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE idempotency_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON idempotency_keys FOR ALL TO service_role USING (true);

-- ─── story_signals ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS story_signals (
    id BIGSERIAL PRIMARY KEY,
    story_id TEXT NOT NULL REFERENCES stories(story_id),
    policy TEXT NOT NULL,
    signals JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(story_id, policy)
);
ALTER TABLE story_signals ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON story_signals FOR ALL TO service_role USING (true);

-- ─── cluster_memberships ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cluster_memberships (
    id BIGSERIAL PRIMARY KEY,
    story_id TEXT NOT NULL REFERENCES stories(story_id),
    lens TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(story_id, lens)
);
ALTER TABLE cluster_memberships ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON cluster_memberships FOR ALL TO service_role USING (true);
CREATE INDEX IF NOT EXISTS cluster_memberships_cluster_lens_idx ON cluster_memberships(cluster_id, lens);

-- ─── issue_candidates ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS issue_candidates (
    cluster_id TEXT PRIMARY KEY,
    lens TEXT NOT NULL,
    readiness_score INTEGER NOT NULL DEFAULT 0,
    story_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE issue_candidates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON issue_candidates FOR ALL TO service_role USING (true);

-- ─── doge_issues ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doge_issues (
    issue_id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'DRAFT',
    cluster_id TEXT,
    title TEXT,
    description TEXT,
    geo_scope TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE doge_issues ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON doge_issues FOR ALL TO service_role USING (true);

-- ─── doge_issue_embeddings ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doge_issue_embeddings (
    issue_id TEXT PRIMARY KEY REFERENCES doge_issues(issue_id),
    embedding JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE doge_issue_embeddings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON doge_issue_embeddings FOR ALL TO service_role USING (true);

-- ─── issue_story_links ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS issue_story_links (
    id BIGSERIAL PRIMARY KEY,
    issue_id TEXT NOT NULL REFERENCES doge_issues(issue_id),
    story_id TEXT NOT NULL REFERENCES stories(story_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(issue_id, story_id)
);
ALTER TABLE issue_story_links ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON issue_story_links FOR ALL TO service_role USING (true);
CREATE INDEX IF NOT EXISTS issue_story_links_story_idx ON issue_story_links(story_id);

-- ─── review_audit_log ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS review_audit_log (
    id BIGSERIAL PRIMARY KEY,
    cluster_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE review_audit_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON review_audit_log FOR ALL TO service_role USING (true);

-- ─── story_embeddings ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS story_embeddings (
    story_id TEXT PRIMARY KEY REFERENCES stories(story_id),
    embedding JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
ALTER TABLE story_embeddings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON story_embeddings FOR ALL TO service_role USING (true);
```

**Task 4.2:** Конвенция имён миграций — `supabase/migrations/YYYYMMDD_HHMM_description.sql`.

Каждая миграция:
- Идемпотентна (`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`)
- Содержит RLS policy если добавляет новую таблицу
- Применяется вручную через Supabase SQL Editor

### Acceptance Criteria

- Bootstrap SQL выполняется в новом Supabase проекте без ошибок
- После bootstrap: `required_tables_ready()` → `True`
- После bootstrap: `required_columns_ready()` → `True`
- Все таблицы имеют RLS включённый и policy для service_role

---

## Story 5: Настройка Supabase проекта

### Tasks

**Task 5.1:** Получить credentials.

1. supabase.com → Create new project
2. Settings → API → `Project URL` = `SUPABASE_URL`
3. Settings → API → `service_role` key = `SUPABASE_SERVICE_ROLE`

**Task 5.2:** Применить bootstrap schema.

```
Supabase Dashboard → SQL Editor → вставить содержимое supabase/bootstrap/000_full_init.sql → Run
```

**Task 5.3:** Создать `.env` и проверить.

```bash
cp .env.example .env
# Заполнить SUPABASE_URL и SUPABASE_SERVICE_ROLE
make check-env
make serve
# Логи должны показать: db_backend=supabase db_ready=True
```

**Task 5.4:** Для live integration тестов создать отдельный тестовый Supabase проект (не production).

GitHub Secrets для CI:
- `SUPABASE_TEST_URL` — URL тестового проекта
- `SUPABASE_TEST_SERVICE_ROLE_KEY` — service_role key тестового проекта

### Acceptance Criteria

- `make serve` с правильным `.env` — логи: `backend=supabase db_ready=True`
- `python3.11 -m pytest tests/integration/supabase/test_supabase_dotenv_connectivity.py -v` — PASSED
- `service_role_policy_probe()` → `True`

---

## Critical Pitfalls

- **Service role vs anon key**: service_role bypasses RLS — никогда не отдавать клиентам. Только для серверной стороны
- **PostgREST всегда возвращает список**: `GET` с `limit=1` возвращает `[{...}]` или `[]`, не `{}` или `None`. Всегда `if rows else None`
- **JSONB поля**: PostgREST может вернуть JSONB как `dict` или как строку в зависимости от версии. Всегда `isinstance(raw, dict)` перед `json.loads()`
- **Upsert**: `prefer="resolution=merge-duplicates"` + POST + PK constraint. Без `Prefer` header будет дублирование строк
- **RLS**: если `service_role_policy_probe()` возвращает `False` — добавь: `CREATE POLICY "service_role_full" ON table FOR ALL TO service_role USING (true)`
- **`db_ready=False`**: сервер поднимается, но `/ready` → HTTP 503. Intentional — no crashloop

## Верификация эпика

```bash
# 1. Connectivity (требует реальный .env с Supabase creds)
python3.11 -m pytest tests/integration/supabase/test_supabase_dotenv_connectivity.py -v

# 2. Live smoke
python3.11 -m pytest tests/integration/supabase/test_supabase_live_smoke.py -v

# 3. Story roundtrip
python3.11 -m pytest tests/integration/supabase/test_supabase_live_story_roundtrip.py -v

# 4. Startup логи
make serve &
sleep 3
curl -s http://localhost:8000/ready | python3 -m json.tool
# Ожидаемо: {"data": {"status": "ready", "db_ready": true, "checks": {...}}}
kill %1
```
