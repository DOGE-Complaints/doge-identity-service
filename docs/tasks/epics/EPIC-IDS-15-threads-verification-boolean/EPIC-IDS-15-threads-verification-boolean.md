# EPIC-IDS-15 — Threads verification boolean (`identity_verified`)

> **ID:** `EPIC-IDS-15` · **Alias (backlog package):** `threads-verification-boolean` · **Статус:** 🟢 Done (VB-01 🟢 pkg-000050; VB-02 🟢 pkg-000051; VB-03 🟢 pkg-000052) · **Тип:** Функциональный (opaque verification flag)  
> **Source (backlog):** [`backlog-stories/threads-verification-boolean/INDEX.md`](../../backlog-stories/threads-verification-boolean/INDEX.md)  
> **P1 materialize (VB-01):** 2026-09-21T20:17:48Z · **P3 Done (VB-01):** 2026-09-21T20:24:31Z · **P1 materialize (VB-02):** 2026-09-21T20:36:40Z · **P3 Done (VB-02):** 2026-09-21T20:40:59Z · **P1 materialize (VB-03):** 2026-09-21T20:47:00Z · **P3 Done (VB-03):** 2026-09-21T20:51:27Z · **REQ:** [`21-verification-boolean-and-audit.md`](../../../requirements/21-verification-boolean-and-audit.md)  
> **Architecture:** [`TECH-ARCH-threads-verification-boolean.md`](../../../architecture/TECH-ARCH-threads-verification-boolean.md) (§2.1–2.7)  
> **Interview:** [`zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../../../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md)

## Назначение

First-class method-opaque флаг `identity_verified` на профиле: persist + backfill (VB-01), expose на `GET /me` (VB-02), set на success phone/eID (VB-03). Wire lock: существующий `/me`; pack intake / REQ8 / OAuth introspection rewrite — out of package (см. package INDEX).

## База (не дублировать в stories)

- REQ [`21-verification-boolean-and-audit.md`](../../../requirements/21-verification-boolean-and-audit.md)
- TECH-ARCH [`TECH-ARCH-threads-verification-boolean.md`](../../../architecture/TECH-ARCH-threads-verification-boolean.md)
- Package INDEX [`threads-verification-boolean/INDEX.md`](../../backlog-stories/threads-verification-boolean/INDEX.md)

## Locked decisions (epic-wide)

| ID | Решение | Обоснование |
|----|---------|-------------|
| **D-VB-1** | Physical/wire name = `identity_verified` (first-class column/attribute) | TECH-ARCH §2.2; **not** read-time OR |
| **D-VB-2** | One-shot backfill: `phone_verified OR eid_verified` → opaque true | TECH-ARCH §2.4 |
| **D-VB-3** | Failure paths не требуют clear-on-failure | TECH-ARCH §2.3 |
| **D-VB-4** | `/me` expose → VB-02; write hooks success → VB-03 | Package order; FOCUS LOCK |

Волна pkg-000052 materialize **только VB-03** (VB-01/VB-02 Done).

## Stories

| Story | Тема | Статус |
|-------|------|--------|
| [VB-01](stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) | Persist opaque + backfill | 🟢 Done (pkg-000050) |
| [VB-02](stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md) | Expose on `GET /me` | 🟢 Done (pkg-000051) |
| [VB-03](stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md) | Set on phone/eID success | 🟢 Done (pkg-000052) |

## Порядок

**VB-01** → **VB-02** · **VB-03** (оба после VB-01). Gateway sibling `52` — не этот эпик.

## Non-goals эпика

- Pack validation type + integration name intake (gateway `52`)
- New HTTP path / REQ8 sanctions / voice
- OAuth `phone_verified` introspection rewrite

### Story 1: STORY-IDS-VB-01 — Persist method-opaque `identity_verified` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md`](./stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md)
- **Source (backlog):** [`backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`](../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md)
- **Wave:** `pkg-000050` (P3 Done 2026-09-21T20:24:31Z)

### Story 2: STORY-IDS-VB-02 — Expose `identity_verified` on `GET /me` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md`](./stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md)
- **Source (backlog):** [`backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`](../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md)
- **Wave:** `pkg-000051` (P3 Done 2026-09-21T20:40:59Z)

### Story 3: STORY-IDS-VB-03 — Set `identity_verified` on phone/eID success — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](./stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- **Source (backlog):** [`backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- **Wave:** `pkg-000052` (P3 Done 2026-09-21T20:51:27Z)
