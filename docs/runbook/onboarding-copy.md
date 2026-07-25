# Onboarding copy SSOT — phone verify disclosure + boundary messages

> **DOC-IDS-ONB-02** · Identity onboarding UX copy  
> **Where shown:** web verify screen only (before phone input). GPT branch sees the same screen via redirect.  
> **Tone:** friendly, human; explain benefit; no legalese.  
> **Canon language:** **EN**. **ET / RU — follow-up** (not in this file yet).  
> **Source draft:** [`identity-onboarding-ux-2026-06-12.md`](../analysis/identity-onboarding-ux-2026-06-12.md) §2 (verbatim).

---

## 1. Disclosure (EN canon)

Shown on the web verify screen **before** the user enters a phone number.

**Title**

> One quick step — verify your phone

**Body**

> We ask for your phone number to keep DOGEstonia free of bots and bad actors, so the people you interact with are real. We currently support **Estonian numbers (+372)** only — this is part of how we protect the integrity of our ecosystem.  
> Your number is stored only as a secure hash, never shown to others, and used once to confirm it's really you.

---

## 2. Boundary messages (EN canon)

Tied to Identity API error codes (not free-form UI invent).

| Trigger | API signal | UX intent | Copy (EN) |
|---------|------------|-----------|-----------|
| Foreign / non-allowlisted dial prefix | [`SmsErrorCode.COUNTRY_NOT_ALLOWED`](../../src/core/phone/base.py) (`"COUNTRY_NOT_ALLOWED"`) — e.g. [`e164.py`](../../src/core/phone/e164.py) | Refusal + **waitlist** (collect email for geo expansion; mechanism → [`onboarding-waitlist.md`](./onboarding-waitlist.md)) | Right now we support Estonian numbers (+372) only — it's part of keeping our ecosystem safe. Want us to open your country? Leave your email and we'll let you know. |
| Number already linked to another account | HTTP **409** · envelope code **`profile_conflict`** ([`handlers.py`](../../src/core/api/handlers.py) phone confirm path) | Soft **«is this you?»** — no disclosure of the other account | This number is already in use. If it's you — sign in to that account; otherwise please use a different number. |

**Code refs**

- `COUNTRY_NOT_ALLOWED`: [`SmsErrorCode`](../../src/core/phone/base.py) in `src/core/phone/base.py`
- `profile_conflict` / 409: phone confirm conflict path in `src/core/api/handlers.py` (`envelope_code="profile_conflict"`)

---

## 3. Localization

| Locale | Status |
|--------|--------|
| **EN** | Canon (this file) |
| **ET** | Follow-up |
| **RU** | Follow-up |

SPA may already ship EN strings under `phone.disclosure.*` in [`identityDictionary.js`](../../../spa-app/src/i18n/identityDictionary.js); **this runbook is the product SSOT**. Aligning spa strings to this file is a spa follow-up (render out of scope for DOC-IDS-ONB-02).

---

## 4. Out of scope

- Rendering copy in spa-app UI
- Waitlist storage / form — SSOT [`onboarding-waitlist.md`](./onboarding-waitlist.md) ([DOC-IDS-ONB-04](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-04-non-ee-waitlist-spec.md))

---

## 5. Related

- Waitlist mechanism: [`onboarding-waitlist.md`](./onboarding-waitlist.md) (DOC-IDS-ONB-04)
- UX decisions: [`identity-onboarding-ux-2026-06-12.md`](../analysis/identity-onboarding-ux-2026-06-12.md) §2, §4 G4  
- UI contract: [`08-ui-expectations.md`](../runtime-docs/08-ui-expectations.md) §3 / §3b  
- Phone API runbook: [`onboarding-phone-verification-api.md`](./onboarding-phone-verification-api.md)
