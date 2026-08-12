# Lazy phone gate — doc gap audit (baseline)

- **Wave:** pkg-000040
- **Story:** DOC-IDS-ONB-01-lazy-phone-gate-contract
- **Date:** 2026-06-26 (P3 t01, pre-edit baseline)

## Code facts (unchanged by this wave)

| Fact | Path |
|------|------|
| `/me.phone_verified` in response | [`me_response.py:29-45`](../../../../../../../src/core/api/me_response.py) |
| PV-05 routes | [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — `POST /auth/phone/request`, `POST /auth/phone/confirm` |
| Introspection `{active, sub, phone_verified}` | [`introspection.py`](../../../../../../../src/core/oauth/introspection.py) |

## Grep baseline (pre t02–t04)

```bash
grep -n "ленив\|lazy\|phone_verified\|защищён" docs/runtime-docs/08-ui-expectations.md docs/runtime-docs/09-gateway-expectations.md
```

- `09-gateway-expectations.md`: `phone_verified` in OAuth/GPT paradigm (L11–49); **no** heading «ленивый гейт телефона»; **no** explicit web lazy-by-action contract.
- `08-ui-expectations.md`: inline verify API (§3, L17–24); **no** sequence «защищённое действие → `phone_verified=false` → verify-экран».
- Neither file links to [PV-05 runbook](../../../../../../../docs/runbook/onboarding-phone-verification-api.md) or [STORY-IDS-PV-05](../../../EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md).

## Story DoD checklist (pre-edit)

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Gateway contract: consumer reads `phone_verified`, else verify | **FAIL** | `09-gateway-expectations.md` — introspection hints only; no dedicated lazy-gate section |
| 2 | UI verify screen on `phone_verified=false` | **FAIL** | `08-ui-expectations.md:17-24` — API flow only; no protected-action trigger |
| 3 | Canonical example (story create) + consumer enforce | **PARTIAL** | `09-gateway-expectations.md:39-49` — `stories:submit` + gateway enforce note; not framed as lazy web gate |
| 4 | Links PV-05 + runbook | **FAIL** | No refs to PV-05 story or `onboarding-phone-verification-api.md` in 08/09 |

## Target closure (t02–t04)

- t02 → DoD #1, #3 (gateway section)
- t03 → DoD #2, #3 (UI section + sequence)
- t04 → DoD #4 (cross-links in both sections)
