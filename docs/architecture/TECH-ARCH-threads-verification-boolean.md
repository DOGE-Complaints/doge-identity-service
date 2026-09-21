# Target technical architecture — verification boolean (REQ 21)

| Field | Value |
|-------|--------|
| **Focus** | Method-opaque **verified boolean** for consumers + attempt audit; node-selected integration execute (shell) |
| **Parent REQ** | [`../requirements/21-verification-boolean-and-audit.md`](../requirements/21-verification-boolean-and-audit.md) |
| **Parent product** | `docs/requirements backlog/REQ7-DOGEstonia-Threads-Entity-Social-Governance.md` (T-REQ7-05, D4, AC-REQ7-04) |
| **Interview** | [`../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md`](../analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md) |
| **Recorded** | 2026-09-21T19:09:10Z |
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
- **As-is gap:** `ProfileRecord` today has `phone_verified` / `eid_verified` only (`src/core/domain/models.py`); no opaque field yet.
- **Default physical name:** align with wire (`identity_verified`) unless implement wave explicitly diverges (Open residual below).

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

## 6) Coexistence with as-is (paths)

| Area | As-is | Target |
|------|--------|--------|
| `/me` builder | `me_response.py:17-51` — method flags; no opaque | Add `identity_verified` from profile |
| Profile model / DB map | `models.py` + `db_supabase.py` phone/eID fields | Add persisted opaque + migration/backfill |
| Phone/eID success handlers | Existing persist of method flags | Also set opaque `true` on success |
| Audit | `handlers.py:114-176` | Unchanged schema |
| Threads consumer seam | Reads «verified boolean» (field was Open in threads arch) | Canonical wire: `identity_verified` via Identity `/me` |

---

## 7) Open questions

1. How pack validation type + integration name **reach** this service (sibling gateway `52` — for Gateway O).
2. Whether eID runtime is available when a node selects eID (requirements index: phone = active gate).
3. Whether DB physical column name must diverge from wire `identity_verified` (default: same).
4. Revoke / clear opaque without clearing method flags (lifecycle beyond shell; not this wave DoD).

---

## 8) Not in this doc

- STORY keys, epic waves, task README, pkg YAML, P3.
- Gateway / Threads / Spa architecture bodies.
- Invented HTTP paths or API parameters for pack lock.
- REQ8 sanction/voice implementation.
