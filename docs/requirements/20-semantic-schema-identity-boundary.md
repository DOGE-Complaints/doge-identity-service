# 20. Semantic Schema Runtime — identity boundary (no domain schemas)

Parent: docs/requirements backlog/REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md §4 (identity arrow), REQ3-FLOW-002, REQ3-AC-011, REQ3-SEC-004 (sensitive fields — not identity storage of node schemas)  
Parent-id: req3-semantic-schema-runtime  
Siblings: doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md (contract: Schema Runtime + packs + `schema_binding` / `geo_detail` live in gateway; identity **не** stores node models; FLOW-002 claim keys for schema policy **not required** for SSR package 01–25 Done — gateway D-SSR-3) · spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md (contract: none named — no sibling HTTP/field) · GPT UI/docs/requirements/REQ-45-semantic-schema-intake-envelope-compatibility.md (contract: none named for identity↔GPT schema runtime; existing OAuth/intake auth remains outside this REQ)  
Status: Accepted — boundary freeze (no identity code changes; AC-011 met via gateway SSR 01–25); PA.2 closed by operator 2026-09-01T10:12:26Z  

Дата: 2026-08-27; sibling-seam sync 2026-08-31T09:40:45Z; Status sync 2026-09-01T10:12:26Z  
Проект: doge-identity-service  
Фокус: freeze — identity **не** становится Schema Runtime; **без** новых identity endpoints в этом REQ

---

## 1) Goal

Сохранить разделение: identity = who / credentials; Schema Runtime = field validity/meaning; gateway = orchestration (REQ3-FLOW-002). Добавление новой semantic schema **не** требует изменений `doge-identity-service` (REQ3-AC-011). Подтверждено доставкой gateway SSR backlog **01–05, 08–25 Done** без identity tasks (sibling 51 package INDEX; D-SSR-3).

---

## 2) Scope / Out of scope

### In scope

- Document and keep the boundary in REQ/index so later gateway work cannot silently move node semantic models into identity.
- Allow gateway to **consume** existing identity verification/auth results as submitter/auth context (already outside schema policy) — this REQ does **not** add claim keys for schema field policy.

### Out of scope

- Implementing Schema Runtime, `structured_payload`, `geo_detail`, `NODE_SCHEMA_*`, clustering, processors in identity.
- New identity APIs, tables, or profile fields for node schemas.
- Storing PII-bearing node payloads / address depth in identity (contradicts primer + parent split; SEC-004 story fields stay gateway-side).
- Changing OAuth / phone verification / `verified_person_hash` as part of REQ3 SSR package.
- SPA board/map or GPT pack emit (siblings 16 / REQ-45).

---

## 3) Verified current state

| Fact | Path |
|------|------|
| Identity scope already excludes Story intake | `docs/requirements/02-scope-and-boundaries.md` — Story intake / drafts / submit → gateway |
| `SchemaRuntime` / `structured_payload` / `schema_id` / `geo_detail` / `NODE_SCHEMA_*` in identity-service | **Not found** (Grep `doge-identity-service`) |
| Gateway SSR 01–25 | Done without identity code changes (sibling 51 package; D-SSR-3) |
| Gateway intake submitter | introspection substitution in gateway handlers — **not** schema policy claims |
| Exact claims for schema field policy | **Not used** for current package (closed — see §6) |

---

## 4) Target behavior

1. New semantic schema/profile artifacts are published and executed in gateway runtime (sibling 51), not in identity.
2. Identity continues to answer who the subject is and what credentials are proven (FLOW-002).
3. Gateway Schema Runtime / `geo_intake` / Issue projection / SPA map eligibility do **not** require identity schema endpoints or claim expansions.
4. If a **future** wave needs identity context inside schema field policy, it stays MAY under FLOW-002 and MUST be a new explicit decision — not implied by this REQ.

---

## 5) Acceptance criteria

1. AC-IDS-REQ3-01: REQ3-AC-011 — adding / swapping a semantic schema (gateway pack / `NODE_SCHEMA_*`) does not require `doge-identity-service` code/schema changes (verified by SSR 01–25 delivery without identity tasks).
2. AC-IDS-REQ3-02: This REQ does not introduce identity endpoints, tables, or semantic schema storage.
3. AC-IDS-REQ3-03: REQ/index states FLOW-002 split (who vs what fields mean vs gateway lifecycle).
4. AC-IDS-REQ3-04: Sensitive story / geo payload fields are not relocated into identity tables (SEC-004 boundary).

---

## 6) Open questions

1. **Closed for SSR package 01–25 (and for spa-16 map / GPT-45 wire):** which identity claims gateway passes into schema **field** policy — **not required**; no list. Reopen only with explicit operator decision for a later wave.
2. **Closed:** whether SEC-004 story-field privacy needs identity-side logging change for SSR Done — parent lists logs/embeddings/indexes/projections on gateway side, not identity tables.

Remaining unknown only if a future FLOW-002 policy-context wave is opened — out of current sibling sync.

---

## 7) Dependencies

- Parent: FLOW-002, AC-011, SEC-004, §4 diagram.
- Sibling: gateway 51 (Schema Runtime SSOT; D-SSR-3).
- Existing: `02-scope-and-boundaries.md`, `15-story-authorization.md` (auth of stories, not semantic models).
