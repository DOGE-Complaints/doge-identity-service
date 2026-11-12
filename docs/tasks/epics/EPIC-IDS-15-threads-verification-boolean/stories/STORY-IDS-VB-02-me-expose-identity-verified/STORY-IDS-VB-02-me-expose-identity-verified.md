# STORY-IDS-VB-02 — Expose `identity_verified` on `GET /me` (coexist with legacy)

## Meta
- **Key:** `STORY-IDS-VB-02-me-expose-identity-verified`
- **Parent Epic:** [`../../EPIC-IDS-15-threads-verification-boolean.md`](../../EPIC-IDS-15-threads-verification-boolean.md)
- **Status:** 🟢 Done
- **source:** `backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`
- **Package:** [`threads-verification-boolean/INDEX.md`](../../../../backlog-stories/threads-verification-boolean/INDEX.md)
- **Parent REQ:** [`doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md`](../../../../../requirements/21-verification-boolean-and-audit.md)
- **Architecture:** [`docs/architecture/TECH-ARCH-threads-verification-boolean.md`](../../../../../architecture/TECH-ARCH-threads-verification-boolean.md) (§2.1, §2.5)
- **Interview:** [`docs/analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../../../../../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md)
- **Decision Ref:** [`../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`](../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md); REQ21; TECH-ARCH §2.1/§2.5; interview 2026-09-21
- **Siblings:** [VB-01](../STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) · [VB-03](../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md); gateway `52` (pack — not this story)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Depends:** [STORY-IDS-VB-01-persist-identity-verified](../STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) 🟢 Done
- **Wave:** `pkg-000051`
- **P1 materialize:** 2026-09-21T20:36:40Z
- **P3 Done:** 2026-09-21T20:40:59Z

## Зачем простыми словами
Consumers (gateway / threads / spa) должны читать method-opaque boolean. Новый HTTP path запрещён — только extend `/me`.

## Scope
- `GET /me` `data` включает `identity_verified` (bool) из профиля; без профиля → `false` (зеркало default method flags).
- Legacy `phone_verified` / `eid_verified` остаются в том же payload (coexistence).
- `account_status` не используется как verified boolean (REQ §4.5).
- Синхронизировать runtime API docs (`openapi` / `API_REFERENCE` MeData) — по etalon AUTHCORE-02.
- Offline tests: present key; no-profile false; with profile reflects persisted value; method fields still present.

## Вне scope
- Pack intake; gateway/threads client changes; REQ8; new path; удаление `phone_verified`.
- Creating pipeline task folders until P1.3 (**name ≠ create**).
- Write hooks на success phone/eID (→ VB-03).

## Verified current state
| Fact | Path |
|------|------|
| Builder `/me` data | `src/core/api/me_response.py:17-51` |
| Route | `src/core/api/asgi_app.py` `GET /me` (~302) |
| Me tests | `tests/test_me_profile.py` |
| Etalon extend `/me` | AUTHCORE-02 / ONB-01 patterns |

## Target / AC
- [x] AC-ID-THR-01: no new HTTP path; surface = existing `/me`. Wire key = `identity_verified` (arch lock; product name «verified boolean»).
- [x] AC-ID-THR-03 (wire): consumer contract includes method-opaque `identity_verified`; does not disclose method; `phone_verified` may coexist but is not sole contract.
- [x] AC-ID-THR-04: wire flag is the same boolean regardless of method (no second method bit for consumers).
- [x] Docs + offline tests updated; suite green for touched tests.

## Техническое решение (projected)

- **Approach (arch §2.1, §2.5):** extend `build_me_data` only — default `identity_verified=False`; if profile → from `profile.identity_verified`. Keep emitting `phone_verified` / `eid_verified`. Sync `MeData` in openapi + API_REFERENCE. No new route in `asgi_app.py`.
- **Depends:** VB-01 Done (persisted field).
- **Skill:** python-pro
- **Arch:** [TECH-ARCH-threads-verification-boolean.md](../../../../../architecture/TECH-ARCH-threads-verification-boolean.md) §2.1, §2.5

## Nested tasks (materialized pkg-000051)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-ids-15-02-t01-me-response-identity-verified`](task-ids-15-02-t01-me-response-identity-verified/README.md) | 🟢 Done | `build_me_data`: add `identity_verified`; no-profile → false; keep method flags |
| **T02** | [`task-ids-15-02-t02-api-docs-medata`](task-ids-15-02-t02-api-docs-medata/README.md) | 🟢 Done | `openapi.yaml` MeData + `API_REFERENCE.md` — document `identity_verified` + coexistence note |
| **T03** | [`task-ids-15-02-t03-test-me-profile-opaque`](task-ids-15-02-t03-test-me-profile-opaque/README.md) | 🟢 Done | `test_me_profile.py`: key present; no-profile false; profile reflects persist; method fields still present |
| **T04** | [`task-ids-15-02-t04-story-acceptance-verification`](task-ids-15-02-t04-story-acceptance-verification/README.md) | 🟢 Done | AC-01/03/04 wire + docs + offline suite for touched |

## Точки в коде
- `src/core/api/me_response.py` — `build_me_data`
- `src/core/api/asgi_app.py` — verify route unchanged (`GET /me` only)
- `docs/runtime-docs/api-reference/openapi.yaml` + `API_REFERENCE.md` (MeData)
- `tests/test_me_profile.py`

## Dependencies
- **Requires Todo→Done:** VB-01 (Done pkg-000050).
