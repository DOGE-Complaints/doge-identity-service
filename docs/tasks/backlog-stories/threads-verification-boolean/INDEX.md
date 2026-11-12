# Threads verification boolean — backlog package

> Context: REQ [`21-verification-boolean-and-audit.md`](../../../requirements/21-verification-boolean-and-audit.md) · Arch [`TECH-ARCH-threads-verification-boolean.md`](../../../architecture/TECH-ARCH-threads-verification-boolean.md)  
> Interview: [`zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../../../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md)  
> Pipeline epic: [`EPIC-IDS-15-threads-verification-boolean`](../../epics/EPIC-IDS-15-threads-verification-boolean/EPIC-IDS-15-threads-verification-boolean.md) (VB-01/02/03 🟢 — pkg-000050/051/052; P3 VB-03 2026-09-21T20:51:27Z)

| Order | Story | Status | Depends |
|-------|-------|--------|---------|
| 1 | [STORY-IDS-VB-01-persist-identity-verified](STORY-IDS-VB-01-persist-identity-verified.md) | 🟢 Done · [pipeline](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/STORY-IDS-VB-01-persist-identity-verified.md) · pkg-000050 | — |
| 2 | [STORY-IDS-VB-02-me-expose-identity-verified](STORY-IDS-VB-02-me-expose-identity-verified.md) | 🟢 Done · [pipeline](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-02-me-expose-identity-verified/STORY-IDS-VB-02-me-expose-identity-verified.md) · pkg-000051 | VB-01 |
| 3 | [STORY-IDS-VB-03-set-opaque-on-verification-success](STORY-IDS-VB-03-set-opaque-on-verification-success.md) | 🟢 Done · [pipeline](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-03-set-opaque-on-verification-success/STORY-IDS-VB-03-set-opaque-on-verification-success.md) · pkg-000052 | VB-01 |

**Progress:** 3/3 Done (100%) · Wire lock: `identity_verified` on existing `GET /me` · Pack intake / REQ8 / OAuth introspection rewrite — out of package

**Nested tasks:** VB-01 t01–t05 🟢; VB-02 t01–t04 🟢; VB-03 t01–t06 🟢 under EPIC-IDS-15.

| Story | Nested |
|-------|--------|
| VB-01 | [t01–t05](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-01-persist-identity-verified/) 🟢 |
| VB-02 | [t01–t04](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-02-me-expose-identity-verified/) 🟢 |
| VB-03 | [t01–t06](../../epics/EPIC-IDS-15-threads-verification-boolean/stories/STORY-IDS-VB-03-set-opaque-on-verification-success/) 🟢 |

### Explicitly excluded

| Concern | Why |
|---------|-----|
| Pack validation type + integration name intake | Gateway sibling `52` |
| New HTTP path | REQ AC-ID-THR-01 / FOCUS LOCK |
| REQ8 sanctions / voice | Parent OOS |
| OAuth `phone_verified` introspection rewrite | Optional follow-up — not this wave `/me` consumer contract |
