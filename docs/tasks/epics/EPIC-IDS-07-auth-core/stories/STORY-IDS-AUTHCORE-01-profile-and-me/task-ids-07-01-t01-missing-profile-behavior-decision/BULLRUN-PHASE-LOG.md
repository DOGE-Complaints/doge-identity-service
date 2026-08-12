# BULLRUN-PHASE-LOG

- **Wave:** pkg-000009
- **Process:** P3 Execute STORY-IDS-AUTHCORE-01 t01
- **Date:** 2026-06-04

| Phase | Status | Evidence |
|-------|--------|----------|
| Decision | Done | Вариант B: synthetic 200, no upsert |

## Решение

**Выбранный вариант:** вернуть **200** с синтетическим payload «не верифицирован» — **без** записи в `ProfileRepository`.

| Поле | Значение при отсутствии профиля |
|------|--------------------------------|
| `supabase_user_id` | из JWT `UserClaims` |
| `eid_verified` | `false` |
| `role` | из JWT |
| поля профиля (`display_name`, `avatar_url`, eID-метаданные) | `null` |

**Обоснование:**
1. **Детерминизм** — `get_by_supabase_user_id` → `None` даёт один фиксированный ответ; покрыто `test_me_missing_profile_returns_200_not_verified_no_db_write`.
2. **Без side-effect** — `GET /me` остаётся read-only; создание профиля — зона eID attach ([`attach_eid_verification`](../../../../../../../src/core/infrastructure/repositories.py)), вне scope AUTHCORE-01.
3. **Gateway** — [`09-gateway-expectations.md`](../../../../../../../runtime-docs/09-gateway-expectations.md): gateway читает `eid_verified=false` и не допускает civic-действия до eID-флоу.

**Отклонённый вариант:** upsert пустого профиля на GET — лишняя запись, гонки с eID-флоу, не требуется AC story.

**Передача в код:** docstring `handle_me` ([`handlers.py:63`](../../../../../../../src/core/api/handlers.py)); тесты t05.
