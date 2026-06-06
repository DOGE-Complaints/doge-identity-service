# 02. База данных: как поднять с нуля и как проверяется готовность

## О чём этот документ

Простыми словами: где живут данные сервиса, как развернуть базу на чистом проекте «в один присест», и как сервис сам понимает, что база готова к работе. Если тебе нужно поднять identity на новом Supabase-проекте — тебе сюда.

> **Зрелость темы:** ✅ переключение хранилищ, миграции и проверка готовности реализованы; ⚪ единый bootstrap-скрипт собран в этой итерации.

Источник: [`supabase/migrations/`](../../supabase/migrations/), [`supabase/bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql), [`infrastructure/db_supabase.py`](../../src/core/infrastructure/db_supabase.py), [`runbook/supabase-project-setup.md`](../runbook/supabase-project-setup.md).

## Два режима хранения

Сервис умеет работать с данными двумя способами, переключается одной настройкой `DB_BACKEND` ([`schema.py:92-94`](../../src/core/config/schema.py)):

- **`in_memory`** (по умолчанию) — данные в оперативной памяти процесса. Ничего не нужно поднимать, идеально для локальной разработки и тестов. После перезапуска всё стирается.
- **`supabase`** — реальная база Postgres через PostgREST (HTTP-доступ к таблицам). Требует `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE`; иначе сервис намеренно не стартует ([`schema.py:107-108`](../../src/core/config/schema.py)).

## Поднять базу с нуля

Готовый единый скрипт: [`supabase/bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql) — выполняешь его целиком в SQL-редакторе Supabase, и схема identity готова. Он создаёт **три таблицы**: `profiles`, `eid_verification_sessions`, `eid_audit_events`. Скрипт собран строго из миграций (ничего лишнего не придумано).

Альтернатива — применить миграции по очереди (см. таблицу ниже). Пошаговая инструкция с креденшелами — в [runbook](../runbook/supabase-project-setup.md).

## Миграции (в порядке применения)

| # | Файл | Что делает |
|---|------|-----------|
| 1 | `20260525000001_create_profiles.sql` | Профиль пользователя + авто-обновление `updated_at` + RLS |
| 2 | `20260525000002_create_eid_verification_sessions.sql` | Сессии eID-проверки + RLS |
| 3 | `20260525000003_create_eid_audit_events.sql` | Журнал аудита eID + индексы + RLS |
| 4 | `20260526000001_eid_sessions_provider_abstraction.sql` | Добавляет поля провайдера, делает PKCE-поля необязательными |

## Проверка готовности (`/ready`) — 5 уровней

Когда `DB_BACKEND=supabase`, сервис при обращении к `/ready` прогоняет пять проверок ([`db_supabase.py:308-379`](../../src/core/infrastructure/db_supabase.py), собираются в [`dependencies.py:69-85`](../../src/core/api/dependencies.py)):

| Проверка | Что значит |
|----------|-----------|
| `connectivity` | PostgREST вообще отвечает |
| `schema` | нужные таблицы существуют |
| `columns` | в `profiles` есть eID-колонки |
| `provider_state` | в сессиях есть колонки провайдера |
| `policy_probe` | сервисная роль может писать/удалять в журнале аудита |

Если все пять — `true`, `/ready` отдаёт 200 «готов». Если хоть одна `false` — 503 «деградация» (сервис не падает, а честно сообщает, что не готов).

Список «нужных таблиц» в коде ([`db_supabase.py:287-291`](../../src/core/infrastructure/db_supabase.py)): `profiles`, `eid_verification_sessions`, `eid_audit_events` — совпадает с bootstrap-скриптом и operational migrations.

## Что видно в логах при старте

Строка `startup.persistence_backend backend=... db_ready=... db_checks=...` ([`asgi_app.py:87-100`](../../src/core/api/asgi_app.py)) — сразу показывает, какой backend выбран и прошли ли проверки.
