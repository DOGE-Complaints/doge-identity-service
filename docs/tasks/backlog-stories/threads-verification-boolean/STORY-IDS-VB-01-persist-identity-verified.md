# STORY-IDS-VB-01 — Persist method-opaque `identity_verified` on profile (+ backfill)

## Meta
- **Key:** `STORY-IDS-VB-01-persist-identity-verified`
- **Status:** 🟢 Done · pipeline [`STORY-IDS-VB-01-persist-identity-verified`](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) · pkg-000050
- **Package:** [`threads-verification-boolean/INDEX.md`](INDEX.md)
- **Parent REQ:** [`doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md`](../../../requirements/21-verification-boolean-and-audit.md)
- **Architecture:** [`docs/architecture/TECH-ARCH-threads-verification-boolean.md`](../../../architecture/TECH-ARCH-threads-verification-boolean.md) (§2.2–2.4)
- **Interview:** [`docs/analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../../../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md)
- **Siblings:** [VB-02](STORY-IDS-VB-02-me-expose-identity-verified.md) · [VB-03](STORY-IDS-VB-03-set-opaque-on-verification-success.md); gateway `52` (pack — not this story)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Depends:** —

## Зачем простыми словами
Нужен first-class флаг «пользователь прошёл гейт верификации» без слова phone/eID. Сейчас в профиле только method-флаги.

## Scope
- Добавить persisted field профиля со смыслом wire `identity_verified` (default physical name = `identity_verified`, arch §2.2).
- One-shot backfill: существующие `phone_verified OR eid_verified` → `identity_verified=true`.
- Маппинг model ↔ DB (`ProfileRecord`, `db_supabase` row map) включает новое поле.
- Offline tests на persist + backfill semantics.

## Вне scope
- Изменение `GET /me` payload (→ VB-02).
- Write hooks на success phone/eID (→ VB-03).
- Pack intake / new HTTP path / REQ8 / новая audit schema.
- Creating pipeline task folders until P1.3 (**name ≠ create**).

## Verified current state
| Fact | Path |
|------|------|
| Нет opaque-поля в `ProfileRecord` | `src/core/domain/models.py:28-38` (`eid_verified`, `phone_verified` only) |
| DB map phone/eID | `src/core/infrastructure/db_supabase.py:104-141` |
| Phone column migration etalon | `supabase/migrations/20260611000001_profiles_phone_verification.sql`; bootstrap `000_full_init.sql` ~230+ |
| Profiles create | `supabase/migrations/20260525000001_create_profiles.sql` (`eid_verified` there) |
| `/me` не отдаёт opaque | `src/core/api/me_response.py:17-51` |

## Target / AC
- [x] Profile может хранить `identity_verified` bool (default false для новых без backfill).
- [x] Backfill one-shot: rows with `phone_verified OR eid_verified` → opaque true (arch §2.4).
- [x] Failure paths не требуют clear-on-failure (arch §2.3).
- [x] Offline tests покрывают map + backfill; suite `-m "not live_integration"` зелёная для затронутых тестов.

## Техническое решение (projected)

- **Approach (arch §2.2–2.4):** first-class column/attribute `identity_verified` (align wire name); **not** read-time OR. Mirror phone-column migration pattern. Backfill SQL/one-shot: `UPDATE … SET identity_verified = true WHERE phone_verified OR eid_verified`. Domain `ProfileRecord` + `db_supabase` to/from row + any `repositories.py` constructors that default profile fields.
- **Depends:** none.
- **Skill:** python-pro
- **Arch:** [TECH-ARCH-threads-verification-boolean.md](../../../architecture/TECH-ARCH-threads-verification-boolean.md) §2.2–2.4

## Nested tasks (materialized pkg-000050)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-ids-15-01-t01-migration-identity-verified`](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/task-ids-15-01-t01-migration-identity-verified/README.md) | 🟢 Done | Migration + bootstrap sync: `profiles.identity_verified BOOLEAN NOT NULL DEFAULT FALSE` (etalon phone migration) |
| **T02** | [`task-ids-15-01-t02-profile-model-and-db-map`](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/task-ids-15-01-t02-profile-model-and-db-map/README.md) | 🟢 Done | `ProfileRecord` + `db_supabase` serialize/parse + `repositories` defaults include field |
| **T03** | [`task-ids-15-01-t03-backfill-existing-verified`](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/task-ids-15-01-t03-backfill-existing-verified/README.md) | 🟢 Done | One-shot backfill: `phone_verified OR eid_verified` → `identity_verified=true` |
| **T04** | [`task-ids-15-01-t04-offline-persist-tests`](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/task-ids-15-01-t04-offline-persist-tests/README.md) | 🟢 Done | Offline tests: default false; map round-trip; backfill semantics |
| **T05** | [`task-ids-15-01-t05-story-acceptance-verification`](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/task-ids-15-01-t05-story-acceptance-verification/README.md) | 🟢 Done | All VB-01 AC; suite `-m "not live_integration"` green for touched |

## Точки в коде
- `src/core/domain/models.py` — `ProfileRecord`
- `src/core/infrastructure/db_supabase.py` — row map
- `src/core/infrastructure/repositories.py` — profile construction defaults
- `supabase/migrations/` + `supabase/bootstrap/000_full_init.sql` — column + bootstrap parity
- `tests/` — new or extend profile/persist tests

## Dependencies
- None (first in package). Unlocks VB-02, VB-03.
