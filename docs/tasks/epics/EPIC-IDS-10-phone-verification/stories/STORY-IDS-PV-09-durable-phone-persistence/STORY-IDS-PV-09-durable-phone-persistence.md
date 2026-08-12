# STORY-IDS-PV-09 — Durable Supabase phone-персистентность (sessions + audit + bootstrap parity)

## Meta
- **Key:** `STORY-IDS-PV-09-durable-phone-persistence`
- **Parent Epic:** [`../../../../EPIC-IDS-10-phone-verification.md`](../../../../EPIC-IDS-10-phone-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-PHONE` · [`EPIC-IDS-PHONE`](../../../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md)
- **Decision Ref:** [`../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md); [`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 G-3/G-2a; [STORY-IDS-OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) (design precedent)
- **Источник:** [`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 — гэпы **G-3** (MEDIUM, durable phone-сессии) и **G-2a** (HIGH, durable phone-аудит); bootstrap-parity-замечание (§3 G-2 / §1 HD-1: bootstrap отстал от миграций).
- **Зависит от:** [STORY-IDS-PV-03](../STORY-IDS-PV-03-otp-engine-session/STORY-IDS-PV-03-otp-engine-session.md) 🟢; [STORY-IDS-PV-04](../STORY-IDS-PV-04-profile-flag-migration/STORY-IDS-PV-04-profile-flag-migration.md) 🟢. **Прецедент дизайна:** [STORY-IDS-OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) (🟢 Done).

## Зачем простыми словами
Сейчас весь стейт phone-гейта живёт **только в памяти процесса**. Любой редеплой/рестарт обнуляет два разных набора данных:
1. **Pending OTP-сессии** — пользователь запросил код, но не успел подтвердить: после рестарта сессия исчезает, `confirm` не находит активную сессию, флоу рвётся (G-3).
2. **Аудит-события телефона** — журнал кто/когда/какой шаг проходил: после рестарта **весь аудит пропадает** (G-2a). Для security-журнала это потеря доказательной базы.

OAuth уже прошёл этот путь: его короткоживущее состояние выдачи перенесено в Supabase Postgres при `DB_BACKEND=supabase`, а demo/offline остаётся in-memory ([OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md), 🟢). Phone-гейт должен получить **ту же durability** по тому же паттерну.

Дополнительно: **bootstrap-скрипт чистой установки отстал от миграций** — свежеподнятая БД из `000_full_init.sql` **не содержит** ни phone-колонок профиля, ни OAuth-таблиц, хотя они давно есть в инкрементальных миграциях. Это значит, что fresh bootstrap ≠ накат миграций, и phone-гейт на чистой БД физически негде персистить. Эту рассинхронизацию закрываем здесь же.

## Решение владельца (зафиксировать)
Supabase используется **только как слой персистентности (Postgres)** — как в [OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md). Контракт сторов/репо **не меняется**: durable-реализации обязаны быть drop-in заменой in-memory (тот же протокол), переключение — по `DB_BACKEND`. **Access-token statelessness — без изменений** (тема OAuth, здесь не трогаем). **Содержимое аудита (IP/UA-хэширование) — вне scope** (см. ниже, отдано SEC-02).

## Scope (только требования; без implementation proposals)
- **Durable phone-session store (Supabase, гейт `DB_BACKEND=supabase`):** реализация, удовлетворяющая существующему протоколу [`PhoneVerificationSessionStore`](../../../../../../src/core/domain/contracts.py) (тот же набор операций: `create` / `get_by_id` / `get_active_by_user` / `get_latest_for_confirm` / `get_by_provider_message_id` / `replace` / `mark_consumed` / `mark_failed` / `mark_expired` / `expire_pending`). TTL/expiry-семантика (`expires_at`, переход `started→expired`) enforce'ится в сторе. Парити с in-memory — как `SupabaseOAuthTokenService` парити `InMemoryOAuthTokenService` в [OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md).
- **Durable phone-audit repo (Supabase, гейт `DB_BACKEND=supabase`):** реализация протокола [`PhoneAuditLogRepository`](../../../../../../src/core/domain/contracts.py) (`log_event` / `list_events`) поверх Postgres. Аудит **переживает рестарт**.
- **Миграция(и) Supabase:** новая таблица `phone_audit_events` (зеркало назначения `eid_audit_events`); и/или `phone_verification_sessions` — если сессии персистятся (требуется для G-3). По образцу [`supabase/migrations/`](../../../../../../supabase/migrations/) (RLS + индексы по `expires_at` для очистки, как в OAuth-миграции).
- **DI-переключатель по backend:** при `DB_BACKEND=supabase` — Supabase-стор/репо; при `in_memory` (demo/tests) — прежние `InMemoryPhoneVerificationSessionStore` / `InMemoryPhoneAuditLogRepository`. По образцу OAuth-ветвления в [`providers.py`](../../../../../../src/core/infrastructure/providers.py).
- **Bootstrap parity:** перегенерировать/расширить [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) так, чтобы fresh bootstrap == полный накат миграций. Должны появиться: **phone-колонки профиля** (из [`20260611000001_profiles_phone_verification.sql`](../../../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql)), **OAuth-таблицы** (из [`20260624000001_oauth_authorization_tables.sql`](../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql) + [`20260624000002_oauth_authorization_request_context.sql`](../../../../../../supabase/migrations/20260624000002_oauth_authorization_request_context.sql)) и новые phone-persistence-таблицы этой стори.

## Вне scope
- **IP/UA-хэширование содержимого аудита** — это [STORY-IDS-SEC-02](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) (G-2b) в пакете security-hardening. Здесь — **durable хранилище**; проброс+хэш request-контекста — там. Разделение зафиксировано в [`EPIC-IDS-SEC`](../../../../backlog-stories/security-hardening/EPIC-IDS-SEC.md) (§Состав, §Порядок: «durable-хранилище — там, проброс+хэш IP/UA — здесь»).
- **Access-token statelessness** — не меняется (тема OAuth; stateless HS256-JWT и так переживает редеплой).
- **Rate-limiting** — [STORY-IDS-SEC-01](../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) (G-1).
- Выбор конкретной схемы колонок/индексов/middleware — этап реализации.

## Точки в коде (текущее состояние)
- **G-3 — phone-сессии in-memory only:** [`InMemoryPhoneVerificationSessionStore`](../../../../../../src/core/infrastructure/repositories.py) — [`repositories.py:284`](../../../../../../src/core/infrastructure/repositories.py); подключён **безусловно** (не по backend) — [`providers.py:121`](../../../../../../src/core/infrastructure/providers.py). Контракт: [`PhoneVerificationSessionStore`](../../../../../../src/core/domain/contracts.py) — [`contracts.py:74`](../../../../../../src/core/domain/contracts.py). В [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) **нет** phone-session стора (phone там фигурирует только как колонки профиля в read/write).
- **G-2a — phone-аудит in-memory only:** [`InMemoryPhoneAuditLogRepository`](../../../../../../src/core/infrastructure/repositories.py) — [`repositories.py:362`](../../../../../../src/core/infrastructure/repositories.py); подключён **безусловно** — [`providers.py:122`](../../../../../../src/core/infrastructure/providers.py). Контракт: [`PhoneAuditLogRepository`](../../../../../../src/core/domain/contracts.py) — [`contracts.py:97`](../../../../../../src/core/domain/contracts.py). Модель: [`PhoneAuditEvent`](../../../../../../src/core/domain/models.py) — [`models.py:93`](../../../../../../src/core/domain/models.py). Миграции `phone_audit_events` **нет** ([`supabase/migrations/`](../../../../../../supabase/migrations/) содержит только `eid_audit_events` из [`20260525000003`](../../../../../../supabase/migrations/20260525000003_create_eid_audit_events.sql)).
- **Контраст (прецедент):** OAuth уже ветвится по backend — `db_backend=="supabase"` → `SupabaseOAuthTokenService` + `SupabaseAuthorizationRequestStore`, иначе `InMemory*` — [`providers.py:91-103`](../../../../../../src/core/infrastructure/providers.py); durable-сторы — [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py); миграция — [`20260624000001_oauth_authorization_tables.sql`](../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql).
- **Bootstrap parity gap:** [`supabase/bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) создаёт только 3 core-таблицы — `profiles` (000_full_init.sql:33), `eid_verification_sessions` (000_full_init.sql:116), `eid_audit_events` (000_full_init.sql:166) — и **не содержит** phone-колонок профиля (добавлены [`20260611000001`](../../../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql)) **и** OAuth-таблиц (добавлены [`20260624000001`](../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql) / [`20260624000002`](../../../../../../supabase/migrations/20260624000002_oauth_authorization_request_context.sql)). Fresh bootstrap ≠ накат миграций.

## Acceptance Criteria
- [x] При `DB_BACKEND=supabase` pending OTP-сессия, созданная до пересоздания стора (эмуляция редеплоя/рестарта), **остаётся доступной** для `confirm` (G-3 закрыт); просроченная/использованная сессия даёт корректный статус (`expired`/`consumed`).
- [x] При `DB_BACKEND=supabase` событие phone-аудита, записанное до пересоздания репо, **читается после** (строка персистирована в Postgres; G-2a закрыт).
- [x] Durable phone-session store удовлетворяет тому же протоколу `PhoneVerificationSessionStore`, durable phone-audit repo — протоколу `PhoneAuditLogRepository`, без изменения контракта.
- [x] DI-переключатель: `DB_BACKEND=supabase` → Supabase-реализации; `DB_BACKEND=in_memory` → прежние `InMemory*`; **in-memory путь не изменён, существующие офлайн-тесты зелёные**.
- [x] Новая миграция создаёт `phone_audit_events` (+ `phone_verification_sessions`, если сессии персистятся) с RLS и индексом по `expires_at`/времени; миграция покрыта в `test_supabase_migrations_sql`.
- [x] Bootstrap-parity: свежий накат [`000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) создаёт phone-колонки профиля, OAuth-таблицы и новые phone-persistence-таблицы — т.е. fresh bootstrap эквивалентен полному накату миграций (проверяемо diff'ом схемы bootstrap vs миграции).
- [x] Аудит-содержимое (IP/UA) **не вводится** этой стори (остаётся как есть до SEC-02) — scope-граница не нарушена.

## Парадигма-якорь
[`identity-backend-full-audit-2026-06-24.md`](../../../../../analysis/identity-backend-full-audit-2026-06-24.md) §3 (G-2a/G-3 + bootstrap), [STORY-IDS-OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) (прецедент durable Supabase-персистентности), [`runtime-docs/04-security.md`](../../../../../runtime-docs/04-security.md) (durable аудит, session-binding), [`08-supabase-migrations`](../../../../../requirements/08-supabase-migrations.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-10-09-t01-phone-persistence-migration-sql`](./task-ids-10-09-t01-phone-persistence-migration-sql/README.md) | pkg-000039 |
| 2 | [`task-ids-10-09-t02-supabase-phone-verification-session-store`](./task-ids-10-09-t02-supabase-phone-verification-session-store/README.md) | pkg-000039 |
| 3 | [`task-ids-10-09-t03-supabase-phone-audit-log-repository`](./task-ids-10-09-t03-supabase-phone-audit-log-repository/README.md) | pkg-000039 |
| 4 | [`task-ids-10-09-t04-di-phone-store-backend-selection`](./task-ids-10-09-t04-di-phone-store-backend-selection/README.md) | pkg-000039 |
| 5 | [`task-ids-10-09-t05-bootstrap-full-init-parity`](./task-ids-10-09-t05-bootstrap-full-init-parity/README.md) | pkg-000039 |
| 6 | [`task-ids-10-09-t06-offline-phone-durability-regression-tests`](./task-ids-10-09-t06-offline-phone-durability-regression-tests/README.md) | pkg-000039 |
| 7 | [`task-ids-10-09-t07-story-acceptance-verification`](./task-ids-10-09-t07-story-acceptance-verification/README.md) | pkg-000039 |
