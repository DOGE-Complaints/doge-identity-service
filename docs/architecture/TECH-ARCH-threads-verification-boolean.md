# Target technical architecture — verification boolean (REQ 21)

| Field | Value |
|-------|--------|
| **Focus** | Method-opaque **verified boolean** for consumers + attempt audit; node-selected integration execute (shell) |
| **Parent REQ** | [`../requirements/21-verification-boolean-and-audit.md`](../requirements/21-verification-boolean-and-audit.md) |
| **Parent product** | `docs/requirements backlog/REQ7-DOGEstonia-Threads-Entity-Social-Governance.md` (T-REQ7-05, D4, AC-REQ7-04) |
| **Interview** | [`../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md) |
| **Recorded** | 2026-09-21T19:09:10Z |
| **Implemented** | 2026-09-21 — EPIC-IDS-15 VB-01…03 Done (pkg-000050/051/052); migrations `20260921000001` + `00002` |
| **Mode** | Target technical architecture of the REQ focus — **not** implementation tasks / STORY / pkg |
| **Slug** | `threads-verification-boolean` |

**Levels:** functional = REQ `21` · this file = how the focus is realized in `doge-identity-service` · work items = backlog / P1.3 elsewhere.

---

## 1) Context & functional vs tech split

Identity **executes** the verification integration the node configured (phone or eID, named in the pack). It does **not** own the pack (gateway sibling `52`), thread rules, or REQ8 sanctions/voice.

**This wave (shell):** expose a method-opaque **verified boolean** on the existing consumer surface and keep attempt audit. Legacy `phone_verified` may coexist; it must not be the sole consumer contract after this REQ.

| Layer | Lives in | Content |
|-------|----------|---------|
| Functional / product | REQ `21` | Why, scope/OOS, DoD in product terms |
| Target tech (this doc) | `docs/architecture/` | Components, persist, wire, flows, verify |
| Work items | backlog STORY (other prompts) | Not here |

**Packaging / runtime image:** **N/A** for this child (no Git FS → image gap forced by REQ `21`).

---

## 2) Target technical architecture of the focus

### 2.1 Consumer surface

- **HTTP:** extend existing `GET /me` only — **do not invent a new path** (REQ AC-ID-THR-01; operator FOCUS LOCK).
- **As-is route:** `src/core/api/asgi_app.py` (`GET /me`); payload builder `src/core/api/me_response.py` (`build_me_data`).
- **Wire JSON key (locked):** `identity_verified` (boolean).
- **Product name:** «verified boolean» → wire mapping: product phrase ↔ `identity_verified`.
- **Semantics:** method-opaque — does **not** disclose phone vs eID. Provider payloads are not part of the check result for callers.

### 2.2 Persist

- **Model:** first-class persisted field on the user profile (same sense as wire `identity_verified`).
- **Not:** read-time `OR(phone_verified, eid_verified)` as the sole source of truth.
- **Physical name:** same as wire — `identity_verified` (Resolved; EPIC-IDS-15).
- **Implemented:** column + model + DB map + backfill (see §6).

### 2.3 Write policy

| Event | Effect on opaque field |
|-------|-------------------------|
| Successful phone verification path (counts toward gate) | Set `identity_verified = true` (and keep existing method-flag behavior) |
| Successful eID verification path | Set `identity_verified = true` (same) |
| Failure of either path | Do **not** set `true`; do **not** clear an already-`true` value |
| Sanctions / suspend | **Not** this field — REQ8 / `account_status` (as-is `me_response.py` always `"active"` for that key today) |

### 2.4 Backfill (one-shot at deploy)

For profiles that already have `phone_verified OR eid_verified` before this wave: set `identity_verified = true` once so go-live does not regress already-verified users (Uus Veerenni / spa lazy gate).

### 2.5 Legacy coexistence on `/me`

Keep emitting method-named flags (`phone_verified`, `eid_verified`, and related metadata) on the same `/me` `data` object during transition. After this REQ, **consumers must read `identity_verified`**, not method flags alone (parent D4, AC-ID-THR-03).

### 2.6 Audit

- Reuse existing attempt loggers: `_log_phone_audit` / `_log_eid_audit` (`src/core/api/handlers.py` ~114–176).
- **No** new event schema for «opaque flipped» in this shell.
- Audit **may** name the provider; the verified boolean **must not**.

### 2.7 Logical flows

```text
Node pack says phone|eID (owned by gateway — intake Open here)
  → Identity runs that integration (existing phone / eID paths)
  → attempt audit (existing loggers)
  → on success: persist method flags (as-is) + persist identity_verified=true
  → GET /me returns identity_verified (+ legacy method fields)
  → gateway / threads / spa gate on identity_verified only
```

Uus Veerenni target: pack validation type = phone; consumer-facing flag remains method-opaque `identity_verified`.

---

## 3) Ownership / contracts

| Concern | Owner |
|---------|--------|
| Pack block: validation type + integration name | Gateway `52` |
| Execute integration; persist opaque; expose on `/me` | **Identity** (this service) |
| Attempt audit (provider-aware) | Identity (existing phone/eID) |
| Read verified boolean on write path | Threads / gateway / spa callers |
| Thread rules, reactions, media floor | Threads / siblings — not this doc |
| Voice / sanction ladder | REQ8 — not this doc |

---

## 4) Runtime topology / packaging / env

- **Runtime:** existing Python identity service; no new start topology for this focus.
- **Packaging seam:** **N/A**.
- **Env:** no new pack-intake env invented here; pack reach mechanism remains Open (Gateway).

---

## 5) Verify surfaces

| Proof | Role |
|-------|------|
| Offline unit/contract tests | `identity_verified` present on `/me` data; set on success phone/eID; backfill behavior; legacy method fields still present; audit unchanged (no new event type) |
| Live integration / EE smoke | Optional later — **not** required to lock this architecture |
| Cross-service e2e (gateway/threads) | After sibling Architect Studio waves — not Identity-only DoD |

---

## 6) Implemented state (post EPIC-IDS-15)

| Area | Fact (path) |
|------|-------------|
| `/me` builder | `me_response.py:35` default false; `:51` from `profile.identity_verified`; method flags coexist |
| Profile model | `ProfileRecord.identity_verified` (`models.py`) |
| DB map | `db_supabase.py` serialize/parse + attach success PATCH `identity_verified: True` |
| Migrations | `supabase/migrations/20260921000001_profiles_identity_verified.sql`; backfill `…00002_…_backfill.sql`; bootstrap `000_full_init.sql` §5b |
| Phone/eID success | `attach_phone_verification` / `attach_eid_verification` (db + `repositories.py`) set opaque true; failure does not clear |
| Audit | `handlers.py` `_log_phone_audit` / `_log_eid_audit` — unchanged schema |
| API docs | `runtime-docs/api-reference/API_REFERENCE.md` §6; `openapi.yaml` MeData |
| Package | `docs/tasks/backlog-stories/threads-verification-boolean/` 3/3 Done · epic `EPIC-IDS-15` |
| Consumer seam | Canonical wire for gateway / threads / spa: **`identity_verified`** on Identity `GET /me` (not method flags alone). Legacy GPT/OAuth/story-draft may still use `phone_verified` until sibling cutover (e.g. GW-THR-03). |

---

## 7) Open questions

1. How pack validation type + integration name **reach** this service (sibling gateway `52`).
2. Whether eID runtime is available when a node selects eID (requirements index: phone = active gate).
3. ~~DB physical column name vs wire~~ — **Resolved:** same (`identity_verified`).
4. Revoke / clear opaque without clearing method flags (lifecycle beyond shell; not this wave DoD).

---

## 8) Not in this doc

- STORY keys, epic waves, task README, pkg YAML, P3.
- Gateway / Threads / Spa architecture bodies.
- Invented HTTP paths or API parameters for pack lock.
- REQ8 sanction/voice implementation.
