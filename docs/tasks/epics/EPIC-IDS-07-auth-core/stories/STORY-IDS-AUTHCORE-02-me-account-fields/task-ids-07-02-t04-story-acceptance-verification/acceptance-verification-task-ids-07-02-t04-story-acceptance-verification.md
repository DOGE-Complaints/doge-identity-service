# Story acceptance gate — STORY-IDS-AUTHCORE-02-me-account-fields

- **Story:** Расширить `GET /me` полями аккаунта (`created_at` / `account_status`)
- **Package:** `pkg-000044-20260724-epic-ids-07-authcore-02-me-account-fields.yaml`
- **Result:** PASS
- **Date:** 2026-07-24T12:23:15Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `GET /me` `data.account_status == "active"` (всегда, включая no-profile). (`email` — приёмка в ONB-01.) | PASS | t01 [`me_response.py:34`](../../../../../../../src/core/api/me_response.py); t03 `test_me_with_valid_jwt_and_profile_returns_200_envelope`, `test_me_missing_profile_returns_200_not_verified_no_db_write` |
| `data.created_at` = ISO-8601 из `profiles.created_at` при наличии профиля; `null` — без профиля. **Никаких обращений к Supabase Auth** и **никакой записи в БД** (no-auto-provision сохранён). | PASS | t01 [`me_response.py:33,49`](../../../../../../../src/core/api/me_response.py); t03 missing-profile asserts `created_at is None` + no upsert |
| Нет новой миграции/колонки (D-CAB-1): `grep account_status supabase/bootstrap/` → пусто. | PASS | live grep empty (t01 DoD) |
| `openapi.yaml` `MeData` + `API_REFERENCE.md §6` обновлены (created_at nullable, account_status enum + пометка «MVP: active»). | PASS | t02 [`openapi.yaml:84-91`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml); [`API_REFERENCE.md §6`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) |
| `test_me_profile.py` покрывает оба кейса (профиль/без); полная offline-сюита зелёная. | PASS | t03: 5 passed in `test_me_profile.py`; offline `405 passed, 12 deselected` |

## Commands (live verification 2026-07-24)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
.venv/bin/python -m pytest tests/test_me_profile.py -q
# 5 passed
.venv/bin/python -m pytest -q -m "not live_integration"
# 405 passed, 12 deselected (2026-07-24T12:23:15Z)
rg -n 'account_status' supabase/bootstrap/ || true
# empty
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
