# Supabase project setup — doge-identity-service

Runbook для поднятия identity-сервиса на **новом** Supabase-проекте (EPIC-IDS-05 Story 5).

**Предусловия:** аккаунт [supabase.com](https://supabase.com), локально склонирован `doge-identity-service`, Python venv (`.venv`).

---

## 1. Create Supabase project

1. Откройте [supabase.com/dashboard](https://supabase.com/dashboard).
2. **New project** → выберите организацию, имя, регион, пароль БД.
3. Дождитесь статуса **Active**.

Зафиксируйте **Project ref** (из URL dashboard: `https://supabase.com/dashboard/project/<project-ref>`).

---

## 2. API credentials → `.env`

В проекте: **Settings → API**.

| Dashboard field | Environment variable | Notes |
|-----------------|----------------------|--------|
| Project URL | `SUPABASE_URL` | `https://<project-ref>.supabase.co` |
| `service_role` key (secret) | `SUPABASE_SERVICE_ROLE` | **Server only** — never in browser or client apps |
| JWT Secret | `SUPABASE_JWT_SECRET` | Для HS256 validation (req-09); Settings → API → JWT Settings |

Скопируйте шаблон:

```bash
cd doge-identity-service
cp .env.example .env
```

В `.env` установите минимум для Supabase backend:

```env
DB_BACKEND=supabase
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE=<service_role_key>
SUPABASE_JWT_SECRET=<jwt_secret>
APP_PROFILE=demo
API_BASE_URL=http://localhost:8100
EID_PROVIDER=mock
```

Опционально: `DATABASE_URL` (direct Postgres) — для psycopg/CLI, не обязателен для PostgREST-клиента.

---

## 3. Apply SQL migrations (Story 4)

For **new identity deployments**, apply migrations **1–4** only. Canonical full schema (without `story_drafts`): [`supabase/bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql).

В **SQL Editor** выполните файлы **по порядку** (каждый файл целиком → Run):

| Order | File |
|------:|------|
| 1 | [`supabase/migrations/20260525000001_create_profiles.sql`](../../supabase/migrations/20260525000001_create_profiles.sql) |
| 2 | [`supabase/migrations/20260525000002_create_eid_verification_sessions.sql`](../../supabase/migrations/20260525000002_create_eid_verification_sessions.sql) |
| 3 | [`supabase/migrations/20260525000003_create_eid_audit_events.sql`](../../supabase/migrations/20260525000003_create_eid_audit_events.sql) |
| 4 | [`supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql`](../../supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql) |

> **Historical (do not apply on new deployments):** [`20260527000001_create_story_drafts.sql`](../../supabase/migrations/20260527000001_create_story_drafts.sql) — **DEPRECATED** 2026-06 (stories are gateway domain). File retained for audit trail only; not in bootstrap and not in `_REQUIRED_TABLES` healthcheck.

### Optional: Supabase CLI

Если установлен [Supabase CLI](https://supabase.com/docs/guides/cli):

```bash
cd doge-identity-service
supabase link --project-ref <project-ref>
supabase db push
```

Ручной SQL Editor остаётся каноническим способом для первого bootstrap.

---

## 4. Verify environment

```bash
cd doge-identity-service
make check-env
```

Убедитесь, что `SUPABASE_URL` и `SUPABASE_JWT_SECRET` не `<not set>`.

---

## 5. Start server and check startup logs

```bash
make serve
```

Ожидаемая строка в stdout (после применения миграций и рабочего PostgREST):

```text
startup.persistence_backend backend=supabase db_ready=True db_checks={'connectivity': True, 'schema': True, 'columns': True, 'provider_state': True, 'policy_probe': True}
```

Если `db_ready=False` — см. [EPIC-IDS-05 §8 troubleshooting](../tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md) (connectivity snippet).

---

## 6. Verify `/ready`

В другом терминале:

```bash
curl -s http://localhost:8100/ready | python3 -m json.tool
```

При `db_ready=True` ожидается HTTP **200** и `"status": "ready"` с заполненным `db_checks`.

При недоступном Supabase или неприменённых миграциях — HTTP **503**, `"status": "degraded"` (сервер **не** падает — intentional).

---

## Connectivity snippet (epic §8)

```bash
cd doge-identity-service
# .env loaded
set -a && . ./.env && set +a
.venv/bin/python -c "
from core.config import provide_app_config
from core.infrastructure.db_supabase import SupabaseDatabase
cfg = provide_app_config()
assert cfg.db_backend == 'supabase', 'set DB_BACKEND=supabase in .env'
db = SupabaseDatabase.from_http(cfg.supabase_url, cfg.supabase_service_role)
print('connectivity:', db.healthcheck())
print('tables:', db.required_tables_ready())
print('columns:', db.required_columns_ready())
print('provider_state:', db.provider_state_ready())
print('policy_probe:', db.service_role_policy_probe())
"
```

Все значения должны быть `True` после успешного bootstrap.

---

## CI: test project secrets (EPIC-IDS-06)

Live integration tests используют **отдельный** Supabase-проект. URL тестового проекта **должен отличаться** от production/staging `SUPABASE_URL`.

### GitHub Actions workflows

| Workflow | File | When |
|----------|------|------|
| Offline tests (every push/PR) | [`.github/workflows/test-offline.yml`](../../.github/workflows/test-offline.yml) | `push`, `pull_request` — `pytest -m "not live_integration"` |
| Live Supabase integration | [`.github/workflows/integration-live.yml`](../../.github/workflows/integration-live.yml) | `push` to `main`, `workflow_dispatch` — `pytest -m live_integration` |

`test-offline.yml` **не** использует Supabase secrets — live-тесты в CI offline job не запускаются (marker deselect / skip).

`integration-live.yml` перед pytest записывает `.env` с `SUPABASE_TEST_*` (live tests читают файл напрямую, минуя autouse env block) и выставляет runner env для `DB_BACKEND=supabase` и smoke будущих job.

### GitHub Actions secrets

| GitHub Secret | Purpose |
|---------------|---------|
| `SUPABASE_TEST_URL` | PostgREST base URL тестового проекта |
| `SUPABASE_TEST_SERVICE_ROLE_KEY` | `service_role` key тестового проекта |
| `SUPABASE_TEST_JWT_SECRET` | JWT secret тестового проекта (positive JWT tests) |

Workflow (EPIC-IDS-06) маппит в runner env, например:

- `SUPABASE_URL` ← `secrets.SUPABASE_TEST_URL`
- `SUPABASE_SERVICE_ROLE` ← `secrets.SUPABASE_TEST_SERVICE_ROLE_KEY`
- `SUPABASE_JWT_SECRET` ← `secrets.SUPABASE_TEST_JWT_SECRET`

### Operator checklist

1. Создайте **второй** Supabase project только для CI/local live tests.
2. Примените те же 5 миграций (раздел 3).
3. Добавьте secrets в GitHub → Settings → Secrets and variables → Actions.
4. После EPIC-IDS-06: `make test-live` с `.env`, указывающим на тестовый проект.

**Isolation rule:** `SUPABASE_TEST_URL` ≠ production `SUPABASE_URL` (разные project ref в hostname).

---

## Related

- Migrations SSOT: [`docs/requirements/08-supabase-migrations.md`](../requirements/08-supabase-migrations.md)
- Epic: [`docs/tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md`](../tasks/epics/EPIC-IDS-05-supabase-persistence/EPIC-IDS-05-supabase-persistence.md)
- Live tests (future): [`docs/tasks/epics/EPIC-IDS-06-testing-architecture.md`](../tasks/epics/EPIC-IDS-06-testing-architecture.md)
