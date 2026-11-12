## Task workspace — `task-ids-15-01-t02-profile-model-and-db-map`

- Story: [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-01-t01-migration-identity-verified/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000050`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) (Scope #1,#3, AC #1)  
---

## Task: implement — `ProfileRecord` + `db_supabase` map + repository defaults

### Цель
Маппинг model ↔ DB включает `identity_verified`: `ProfileRecord`, `_profile_to_row` / `_profile_from_row`, и constructors/defaults в `repositories.py` / supabase create paths.

### Почему это важно
Story Scope #3 / AC #1: поле должно round-trip; default false для новых без backfill.

### Факты из кода
1. [`models.py:22-45`](../../../../../../../src/core/domain/models.py) — `ProfileRecord` has `eid_verified` / `phone_verified`; no `identity_verified`.
2. [`db_supabase.py:98-141`](../../../../../../../src/core/infrastructure/db_supabase.py) — `_profile_to_row` / `_profile_from_row` map phone/eID only for verification flags.
3. [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — `ProfileRecord(...)` constructors default `phone_verified=False` / `eid_verified=False` (e.g. ~L124–139, ~L186–201).
4. Supabase create paths in `db_supabase.py` also construct `ProfileRecord` (~L456+, ~L541+).

### Gap / Проблема
Opaque field отсутствует в domain + row map + constructors.

### AC/DoD
- [x] (P0) `ProfileRecord.identity_verified: bool` present.
- [x] (P0) `_profile_to_row` / `_profile_from_row` include `identity_verified` (default false on missing row key).
- [x] (P0) In-memory + supabase profile constructors/defaults set `identity_verified=False` unless explicitly set.
- [x] (P1) No `/me` response field change (VB-02).

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/infrastructure/db_supabase.py`
- `doge-identity-service/src/core/infrastructure/repositories.py`

### Out of scope
- Migration (t01); backfill UPDATE (t03); tests (t04); gate (t05)

### Проверка
```bash
rg -n 'identity_verified' doge-identity-service/src/core/domain/models.py doge-identity-service/src/core/infrastructure/db_supabase.py doge-identity-service/src/core/infrastructure/repositories.py
```
