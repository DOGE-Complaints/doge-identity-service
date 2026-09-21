# Interview report — REQ → target tech architecture (Identity / REQ 21)

| Field | Value |
|-------|--------|
| **Recorded** | 2026-09-21T19:09:10Z |
| **utc_date** | 2026-09-21 |
| **Chat** | Identity O (REQ7 step 3a) |
| **builder_project** | identity |
| **focus_folder** | doge-identity-service |
| **$requirementDoc** | `doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md` |
| **$archPackageSlug** | threads-verification-boolean |
| **$archDocMode** | auto → **single** |
| **Arch root** | [`../architecture/TECH-ARCH-threads-verification-boolean.md`](../architecture/TECH-ARCH-threads-verification-boolean.md) |

---

## 1) Inputs + use-case statement

**Inputs:** REQ `21`; operator FOCUS LOCK (extend `GET /me`; field name Open until answered; Identity ≠ pack/threads/REQ8; packaging N/A; no Gateway O until Phase 2 synthesis); profiles `identity` → `doge-identity-service`.

**Use case:** Child REQ7 identity shell needs method-opaque verified boolean on the consumer surface plus attempt audit, but wire/persist/coexistence were not path-level in the REQ — CTO/CPO target-arch SSOT before Gateway O and before story decomposition.

---

## 2) REQ level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech (functional-heavy shell) | Goal/Scope/AC product-facing; as-is paths in §3; Open wire name / pack intake / eID runtime in §6 | This prompt primary; extract tech into arch; keep REQ product-facing |

**Architecture zone before run:** `docs/architecture/` missing → create single `TECH-ARCH-threads-verification-boolean.md`.

**Packaging seam:** **N/A** (operator + REQ).

---

## 3) Verbatim decision log

### DP1 — Wire JSON field name on `GET /me`

- **Question:** Exact JSON key for method-opaque verified boolean on existing `/me` (no new path).
- **Options summary:** A `verified` · B `identity_verified` · C `person_verified` · Other (must stay method-opaque).
- **Options analytics (short):** A closest to product wording, higher collision risk with `email_verified`/`phone_verified`/`eid_verified` on same payload (`me_response.py`). B disambiguates service gate vs method/email flags, still opaque. C human «person» language but tension with product phrase and eID `verified_person_hash` vocabulary.
- **Architecture/project fit:** A fits with tension; B fits; C fits with tension; new path / method-named sole contract = conflicts FOCUS LOCK + AC-01/03.
- **Agent recommendation:** **B `identity_verified`**.
- **Operator decision:** **B** — recommendation **accepted**.
- **Answer (verbatim sense):** принимаю B / `identity_verified`.

### DP2 — Persist model

- **Question:** Dedicated profile field vs read-time OR vs phone-only mirror.
- **Options summary:** A dedicated persisted field · B `OR(phone, eid)` at read · C mirror `phone_verified` only · Other.
- **Analytics (short):** A matches «Persist success» (§2). B/C are aliases with tension vs persist and AC-04.
- **Fit:** A fits; B/C tension; pack-at-read conflicts (pack Unknown in identity).
- **Agent recommendation:** **A**.
- **Operator decision:** **A** — **accepted**.
- **Answer:** A) отдельное persisted-поле в профиле.

### DP3 — Write-on-success + backfill

- **Question:** When to set `true`; what about already-verified users.
- **Options summary:** A success phone\|eID → true; failure does not clear; one-shot backfill from `phone_verified OR eid_verified` · B no backfill · C phone-only write+backfill · Other.
- **Analytics (short):** A avoids go-live regressing existing phone users; supports later eID without wire change. B harsh cutover. C weak vs AC-04.
- **Fit:** A fits; B/C tension.
- **Agent recommendation:** **A**.
- **Operator decision:** **A** — **accepted**.
- **Answer:** Примаю А / Принимаю A.

### DP4 — Audit policy

- **Question:** Existing phone/eID attempt logs only vs extra opaque-flip event vs unified rewrite.
- **Options summary:** A existing loggers only · B + opaque set event · C replace with unified logger · Other.
- **Analytics (short):** A matches AC-05 precedent / no new schema. B/C invent or out-of-wave refactor.
- **Fit:** A fits; B tension; C conflicts shell scope.
- **Agent recommendation:** **A**.
- **Operator decision:** **A** — **accepted**.
- **Answer:** A.

### DP5 — Verify surfaces

- **Question:** What proves this architecture.
- **Options summary:** A offline unit/contract only · B offline + mandatory live · C docs-only · Other (e.g. gateway e2e in this chat).
- **Analytics (short):** A aligns with threads shell prove-via-tests; live optional later. B pulls SPIKE/live into arch DoD. C false-green. Cross-e2e here conflicts SEQUENCE.
- **Fit:** A fits; B/C tension; Gateway e2e conflicts.
- **Agent recommendation:** **A**.
- **Operator decision:** **A** — **accepted**.
- **Answer:** A.

### Locks without separate vote (FOCUS LOCK / REQ)

- Extend existing `GET /me`; do not invent new HTTP path.
- Legacy `phone_verified` may coexist; not sole consumer contract.
- Identity does not own pack, thread rules, or REQ8 sanctions.
- Packaging theme pack **N/A**.
- Do not open Gateway O until Phase 2 synthesis (completed in chat before materialize).

---

## 4) Open Unknowns

1. Pack validation type + integration name → identity intake (Gateway `52` / Gateway O).
2. eID runtime readiness when a node selects eID.
3. DB physical column name if ops diverge from wire (default: `identity_verified`).
4. Revoke/clear opaque without clearing method flags (beyond shell DoD).

---

## 5) Link matrix

| Artifact | Path |
|----------|------|
| REQ | `doge-identity-service/docs/requirements/21-verification-boolean-and-audit.md` |
| Arch root | `doge-identity-service/docs/architecture/TECH-ARCH-threads-verification-boolean.md` |
| This report | `doge-identity-service/docs/analysis/zeya888.req-target-tech-arch-interview-21-verification-boolean-and-audit-2026-09-21.md` |
| Threads seam (consumer) | `doge-threads/docs/architecture/threads-entity-shell/04-security-and-verify.md` (product: verified boolean; wire name locked here as `identity_verified`) |

---

## 6) Method notes

- **functional REQ ≠ target tech arch ≠ work items.**
- **Packaging N/A** for this run (not «Git ownership ≠ image packaging» applied).
- **Recommendation advisory; operator decides** — all five DPs accepted as recommended.
- **Name ≠ create:** no stub schemas, STORY, pkg, or product code in this materialize.
