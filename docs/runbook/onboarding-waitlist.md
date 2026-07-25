# Onboarding waitlist SSOT — non-EE phone interest

> **DOC-IDS-ONB-04** · Product spec: collect interest when dial prefix is not allowlisted  
> **Priority:** **LOW** / **post-MVP** for identity backend  
> **Depends on:** [DOC-IDS-ONB-02](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-02-disclosure-copy.md) / [`onboarding-copy.md`](./onboarding-copy.md) (waitlist UX copy)  
> **Not identity storage:** identity only refuses the number; email collection is outside this service.

---

## 1. Trigger (identity)

Foreign / non-allowlisted dial prefix on phone request:

| Piece | Fact |
|-------|------|
| Check | [`resolve_dial_prefix` / `assert_allowed_dial_prefix`](../../src/core/phone/e164.py) |
| Error | [`SmsErrorCode.COUNTRY_NOT_ALLOWED`](../../src/core/phone/base.py) (`"COUNTRY_NOT_ALLOWED"`) → HTTP 400 envelope |
| Allowlist | `PHONE_ALLOWED_DIAL_PREFIXES` ([`schema.py`](../../src/core/config/schema.py), default **`+372`**) |

Identity **does not** expose `/waitlist` and has **no** waitlist table under `supabase/`.

---

## 2. Decision — where we collect email

**Canon:** waitlist interest is collected **outside identity**: spa UI → dedicated **Waitlist API**.

| Layer | Role |
|-------|------|
| Identity | Signal only: `COUNTRY_NOT_ALLOWED` |
| Spa UI | Form after refusal ([`waitlistService.js`](../../../spa-app/src/services/waitlistService.js); SPA-ID-07 Done) |
| Durable store | `POST {VITE_WAITLIST_API_URL}/waitlist` when `VITE_WAITLIST_API_ENABLED=true` and URL set; otherwise **mock** (no durable store) |

Not chosen for identity: Supabase table in this repo, or identity log-event sink.

### Minimal fields (spa → Waitlist API payload as-built)

| Field | Required | Notes |
|-------|----------|--------|
| `email` | yes | Interest contact |
| `country` | yes | Desired country / dial context from UI |
| `organization` | no | Optional |
| `created_at` | API-side | Set by Waitlist API when durable; identity does not store |

Joining waitlist **must not** create an identity account, phone verification, or profile record.

---

## 3. UX message

EN canon for the refusal + waitlist invite — [`onboarding-copy.md`](./onboarding-copy.md) §2 Boundary (`COUNTRY_NOT_ALLOWED`). Do not invent a second copy string here.

---

## 4. Priority and promotion

| Item | Status |
|------|--------|
| Identity MVP | **Not a blocker** (LOW / post-MVP) |
| Spa waitlist UI | Already Done (SPA-ID-07); durable Waitlist API owner = outside identity |
| Expand `PHONE_ALLOWED_DIAL_PREFIXES` | Separate product decision (out of this spec) |

**Open an identity story only if** product requires an **identity-owned** `POST /waitlist` and a waitlist table in **identity** Supabase. Otherwise follow-up stays in spa-app / external Waitlist API.

---

## 5. Out of scope (this doc task)

- Implementing identity waitlist endpoints or migrations
- Changing allowlisted dial prefixes
- Spa FE code changes in this task

---

## 6. Related

- Copy SSOT: [`onboarding-copy.md`](./onboarding-copy.md)  
- UI expectations: [`08-ui-expectations.md`](../runtime-docs/08-ui-expectations.md)  
- Phone API: [`onboarding-phone-verification-api.md`](./onboarding-phone-verification-api.md)  
- Task: [DOC-IDS-ONB-04](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-04-non-ee-waitlist-spec.md)
