# 05. Модель данных

## О чём этот документ

Что и где хранит identity: какие таблицы, какие поля, какие правила-инварианты. Человеческим языком: identity хранит **только то, что касается личности и её проверки** — профиль, идущие eID-проверки и журнал событий. Контента историй/жалоб здесь нет (это домен gateway).

Источник: [`supabase/migrations/`](../../supabase/migrations/) (схема) + [`domain/models.py`](../../src/core/domain/models.py) (модели в коде) + [`infrastructure/db_supabase.py`](../../src/core/infrastructure/db_supabase.py) (маппинг строка↔модель).

## Таблицы identity

| Таблица | Зачем | Миграция | Статус |
|---------|-------|----------|--------|
| `public.profiles` | Профиль: статус eID, заготовка под кошелёк, отображаемое имя | `20260525000001` | ✅ |
| `public.eid_verification_sessions` | Идущие сейчас eID-проверки (state-машина) | `20260525000002` + `20260526000001` | ✅ |
| `public.eid_audit_events` | Неизменяемый журнал событий eID (без персональных данных) | `20260525000003` | ✅ |
| `auth.users` | Базовые пользователи — **управляется Supabase Auth**, мы только ссылаемся | внешняя | ✅ |

## profiles — центральная таблица

Связь схемы ([миграция](../../supabase/migrations/20260525000001_create_profiles.sql)) и модели ([`ProfileRecord` models.py:22-40](../../src/core/domain/models.py)):

- **Кто это:** `id`, `supabase_user_id` (уникальная ссылка на `auth.users`, при удалении пользователя профиль удаляется каскадом), `display_name`, `avatar_url`.
- **Статус eID:** `eid_verified` (да/нет), `verified_person_hash` (необратимый «отпечаток» личности), `eid_provider`, `eid_method`, `eid_country`, `eid_verified_at`.
- **Кошелёк (заготовка на будущее, см. [07-web3](07-web3-foundation.md)):** `wallet_address`, `wallet_linked_at`, `wallet_signature_verified_at`, `wallet_signature_scheme`, `wallet_chain_id`.
- **Служебное:** `created_at`, `updated_at` (обновляется триггером автоматически).

Два важных правила прямо в БД:
- `CHECK eid_consistency` — нельзя пометить `eid_verified=true`, не заполнив `verified_person_hash` и `eid_verified_at` (нельзя «верифицировать наполовину»).
- Частичный уникальный индекс `unique_verified_person_hash` — один и тот же реальный человек не может завести два верифицированных аккаунта (основа защиты от дублей, [req-13](../requirements/13-verified-person-hash-and-conflict.md)).

## eid_verification_sessions — «проверка в процессе»

Хранит каждую запущенную eID-проверку, чтобы безопасно довести её до конца ([base](../../supabase/migrations/20260525000002_create_eid_verification_sessions.sql) + [provider-abstraction](../../supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql), модель [`VerificationSession` models.py:43-59](../../src/core/domain/models.py)):

- `id`, `supabase_user_id`, `state` (уникальный, привязывает callback к сессии), `nonce`, `code_verifier_*` (после миграции №4 — необязательные);
- `return_context` (откуда пришли: дашборд / отправка истории / GPT) и `requested_action` — это и есть тот «флаг, зачем нужна верификация» из [04-security](04-security.md);
- `status` (started → consumed / failed / expired);
- `provider` + `provider_session_data` (поддержка разных eID-провайдеров);
- `created_at`, `expires_at`.

Важный принцип: привязка eID к пользователю берётся **из этой записи** (создана на старте), а не из текущей браузерной сессии — сессия могла смениться, пока человек проходил проверку.

## eid_audit_events — журнал без персональных данных

`event_type`, `provider`, `method`, `success`, `failure_reason`, плюс **хэши** `ip_hash`/`user_agent_hash` (не сырые значения) и `request_id`. Модель [`EIDAuditEvent` models.py:62-74](../../src/core/domain/models.py). Сделан как неизменяемый лог для разборов инцидентов без хранения PII.

## Прочие модели в коде

[`models.py`](../../src/core/domain/models.py): `UserClaims` (то, что достаём из JWT), `OAuthClient`, `OAuthTokenClaims` (для OAuth-сервера), исключения `JwtValidationError`, `ProfileConflictError`.

## Доступ к данным

- `in_memory` → [`repositories.py`](../../src/core/infrastructure/repositories.py) (dict в памяти).
- `supabase` → [`db_supabase.py`](../../src/core/infrastructure/db_supabase.py) (PostgREST через httpx; нормализация JSONB; маппинг строк в модели).

## Исторически удалённое из identity

Таблица `story_drafts` и story-маршруты **удалены** из кода identity (EPIC-IDS-08 CLEANUP-01). Контент историй — домен gateway; deprecated SQL [`20260527000001_create_story_drafts.sql`](../../supabase/migrations/20260527000001_create_story_drafts.sql) не входит в operational bootstrap. См. [09-gateway-expectations](09-gateway-expectations.md), [req-15](../requirements/15-story-authorization.md) (DEPRECATED).
