# STORY-IDS-VB-03 — Set `identity_verified` on phone/eID success; keep existing audit

## Meta
- **Key:** `STORY-IDS-VB-03-set-opaque-on-verification-success`
- **Parent Epic:** [`../../EPIC-IDS-15-threads-verification-boolean.md`](../../EPIC-IDS-15-threads-verification-boolean.md)
- **Status:** 🟢 Done
- **source:** `backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`
- **Package:** [`threads-verification-boolean/INDEX.md`](../../../../backlog-stories/threads-verification-boolean/INDEX.md)
- **Parent REQ:** [`doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md`](../../../../../requirements/21-verification-boolean-and-audit.md)
- **Architecture:** [`docs/architecture/TECH-ARCH-threads-verification-boolean.md`](../../../../../architecture/TECH-ARCH-threads-verification-boolean.md) (§2.3, §2.6, §2.7)
- **Interview:** [`docs/analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../../../../../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md)
- **Decision Ref:** [`../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md); REQ21; TECH-ARCH §2.3/§2.6/§2.7; interview 2026-09-21
- **Siblings:** [VB-01](../STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) · [VB-02](../STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md); gateway `52` (pack — not this story)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Depends:** [STORY-IDS-VB-01-persist-identity-verified](../STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) 🟢 Done
- **Wave:** `pkg-000052`
- **P1 materialize:** 2026-09-21T20:47:00Z
- **P3 Done:** 2026-09-21T20:51:27Z

## Зачем простыми словами
Успех существующего phone или eID flow должен закреплять opaque-флаг. Failure не ставит true и не clear’ит уже true. Audit attempt остаётся прежним (AC-05).

## Scope
- На успешном phone verification persist path — также `identity_verified=true` (method flags as-is).
- На успешном eID verification persist path — также `identity_verified=true`.
- Failure: не set true; не clear already-true (arch).
- Сохранить вызовы `_log_phone_audit` / `_log_eid_audit` без новой event schema (AC-05).
- Offline tests: success → opaque true; failure → opaque unchanged; audit helpers still used (no new schema).

## Вне scope
- Как pack выбирает phone vs eID (gateway 52 / Open).
- Live EE smoke (arch verify = offline).
- OAuth introspection `phone_verified` rewrite — not this wave.
- Creating pipeline task folders until P1.3 (**name ≠ create**).

## Verified current state
| Fact | Path |
|------|------|
| Phone audit | `src/core/api/handlers.py:114-142` `_log_phone_audit` |
| eID audit | `src/core/api/handlers.py:145-176` `_log_eid_audit` |
| Phone success persist | `db_supabase.attach_phone_verification` (~494+); `repositories.attach_phone_verification` (~166+) |
| eID success persist | `db_supabase.attach_eid_verification` (~415+); `repositories.attach_eid_verification` (~105+) |

## Target / AC
- [x] AC-ID-THR-02: service executes existing verification integrations; does not define pack / API params for pack.
- [x] AC-ID-THR-03: after success, opaque persisted; audit log of attempt remains; boolean does not disclose method.
- [x] AC-ID-THR-05: logging precedent = existing phone/eID audit functions (no new schema).
- [x] Offline tests cover success/failure opaque behavior.

## Техническое решение (projected)

- **Approach (arch §2.3, §2.6–2.7):** in `attach_phone_verification` / `attach_eid_verification` (db + repository mirrors), set `identity_verified=true` alongside existing method flags on success. Do **not** clear opaque on failure. Leave `_log_phone_audit` / `_log_eid_audit` signatures/call sites — no new «opaque flipped» event type. Offline tests on attach success/failure; grep/assert no new audit event schema.
- **Depends:** VB-01 Done (column/model exist). Can run parallel with VB-02 after VB-01.
- **Skill:** python-pro
- **Arch:** [TECH-ARCH-threads-verification-boolean.md](../../../../../architecture/TECH-ARCH-threads-verification-boolean.md) §2.3, §2.6, §2.7

## Nested tasks (materialized pkg-000052)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-ids-15-03-t01-attach-phone-sets-opaque`](task-ids-15-03-t01-attach-phone-sets-opaque/README.md) | 🟢 Done | `attach_phone_verification` (db + repo): success → `identity_verified=true` |
| **T02** | [`task-ids-15-03-t02-attach-eid-sets-opaque`](task-ids-15-03-t02-attach-eid-sets-opaque/README.md) | 🟢 Done | `attach_eid_verification` (db + repo): success → `identity_verified=true` |
| **T03** | [`task-ids-15-03-t03-failure-no-clear-opaque`](task-ids-15-03-t03-failure-no-clear-opaque/README.md) | 🟢 Done | Failure paths: do not set true; do not clear already-true |
| **T04** | [`task-ids-15-03-t04-audit-precedent-unchanged`](task-ids-15-03-t04-audit-precedent-unchanged/README.md) | 🟢 Done | Keep `_log_phone_audit` / `_log_eid_audit`; no new event schema (AC-05) |
| **T05** | [`task-ids-15-03-t05-offline-success-failure-tests`](task-ids-15-03-t05-offline-success-failure-tests/README.md) | 🟢 Done | Offline: success → opaque true; failure → opaque unchanged |
| **T06** | [`task-ids-15-03-t06-story-acceptance-verification`](task-ids-15-03-t06-story-acceptance-verification/README.md) | 🟢 Done | AC-02/03/05 + offline suite for touched |

## Точки в коде
- `src/core/infrastructure/db_supabase.py` — `attach_phone_verification`, `attach_eid_verification`
- `src/core/infrastructure/repositories.py` — same methods
- `src/core/api/handlers.py` — audit helpers (read-only for schema; call sites stay)
- Tests around phone/eID attach (extend existing or add focused offline tests)

## Dependencies
- **Requires Todo→Done:** VB-01 (Done pkg-000050). May run parallel with VB-02 after VB-01.
