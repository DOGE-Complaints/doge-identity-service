# Story acceptance gate — STORY-IDS-ONB-01-email-in-me-and-supabase-confirm

- **Story:** `email` в `/me` + требование Supabase «Confirm email»
- **Package:** `pkg-000045-20260724-epic-ids-13-onb-01-email-in-me.yaml`
- **Result:** PASS
- **Date:** 2026-07-24T18:57:53Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /me` возвращает `email` (из токена; `null`, если в токене нет). | PASS | t01 [`me_response.py:21`](../../../../../../../src/core/api/me_response.py); t03 profile + `test_me_email_null_when_jwt_has_no_email_claim` |
| `GET /me` возвращает `email_verified: true` (D-CAB-3, политика «токен ⇒ подтверждён»). | PASS | t01 [`me_response.py:22`](../../../../../../../src/core/api/me_response.py); t03 asserts `email_verified is True` |
| `supabase-project-setup.md` содержит обязательный пункт «включить Confirm email» (предусловие корректности `email_verified`). | PASS | t02 [`supabase-project-setup.md` §2a](../../../../../../../docs/runbook/supabase-project-setup.md) |
| `api-reference` (`openapi.yaml` `MeData` + `API_REFERENCE.md §6`) обновлён на `email` + `email_verified`. | PASS | t02 [`openapi.yaml:73-80`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml); [`API_REFERENCE.md` §6](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) |
| Offline-тест (`test_me_profile.py`) на `email` и `email_verified`; согласовано с AUTHCORE-02 (один билдер `/me`). | PASS | t03: 6 passed in `test_me_profile.py`; offline `406 passed, 12 deselected`; AUTHCORE-02 fields retained in [`me_response.py:35-36,50`](../../../../../../../src/core/api/me_response.py) |

## Commands (live verification 2026-07-24)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
.venv/bin/python -m pytest tests/test_me_profile.py -q
# 6 passed
.venv/bin/python -m pytest -q -m "not live_integration"
# 406 passed, 12 deselected (2026-07-24T18:57:53Z)
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
