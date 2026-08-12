## Task workspace — `task-ids-10-04-t01-profiles-phone-migration-sql`

- Story: [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md)
- Prerequisite: STORY-IDS-PV-01 Done; PV-03 Done (parallel dependency only)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000025`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) Scope bullet 1; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §4, §10.1  
---

## Task: implement — Supabase migration for profile phone columns

### Цель
Добавить phone-колонки в `public.profiles` и partial unique index на `verified_phone_hash` — Story Scope bullet 1 (колонки профиля).

### Почему это важно
Story AC #1: миграция — SSOT для Supabase persistence; зеркало eID `unique_verified_person_hash` в [`20260525000001_create_profiles.sql`](../../../../../../../supabase/migrations/20260525000001_create_profiles.sql).

### Факты из кода
1. Базовая таблица profiles: [`20260525000001_create_profiles.sql`](../../../../../../../supabase/migrations/20260525000001_create_profiles.sql) — eID columns + `unique_verified_person_hash`.
2. Последняя миграция: `20260527000001_create_story_drafts.sql` — phone columns **отсутствуют**.
3. Migration SQL test pattern: [`tests/test_supabase_migrations_sql.py`](../../../../../../../tests/test_supabase_migrations_sql.py) (`test_profiles_critical_columns_for_healthcheck`).
4. Architecture §4: `phone_verified` / `verified_phone_hash` / `phone_verified_at` (+ provider, dial_prefix).

### Gap / Проблема
Нет SQL-миграции для phone-полей профиля; дедуп на уровне БД невозможен без index.

### AC/DoD
- [ ] (P0) Новая миграция `supabase/migrations/20260611000001_profiles_phone_verification.sql` добавляет: `phone_verified`, `verified_phone_hash`, `phone_provider`, `phone_dial_prefix`, `phone_verified_at`.
- [ ] (P0) Partial unique index на `verified_phone_hash` WHERE NOT NULL (зеркало eID index).
- [ ] (P0) Optional `phone_consistency` CHECK (mirror `eid_consistency`) — если добавляется, задокументировать в migration comment.
- [ ] (P1) Story AC #1: offline migration SQL test в `test_supabase_migrations_sql.py`.

### Где менять код
- `doge-identity-service/supabase/migrations/20260611000001_profiles_phone_verification.sql` (new)
- `doge-identity-service/tests/test_supabase_migrations_sql.py`

### Out of scope
- `ProfileRecord` / repository — t02–t04
- `/me` — t05
- HTTP flow attach — PV-05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_supabase_migrations_sql.py -q
```
