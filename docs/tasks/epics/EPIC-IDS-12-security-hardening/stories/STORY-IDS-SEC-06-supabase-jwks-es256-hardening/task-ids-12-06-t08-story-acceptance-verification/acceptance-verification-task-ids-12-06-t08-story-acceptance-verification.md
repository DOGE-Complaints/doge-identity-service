# Story acceptance gate — STORY-IDS-SEC-06-supabase-jwks-es256-hardening

- **Story:** Supabase-JWT валидатор: JWKS-only, DI, честные тесты, без мёртвого кода
- **Package:** `pkg-000042-20260704-epic-ids-12-sec-06-jwks-es256-hardening.yaml`
- **Result:** PASS
- **Date:** 2026-07-04T10:40:01Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Debug-инструментация отсутствует (W1) | PASS | `grep _debug_log\|3c4b9a\|post-fix src/` empty |
| src grep HS256/secret/sentinel empty | PASS | t02+t04; src gate OK |
| JwksCache DI; no internal httpx.Client; except narrowed | PASS | `providers.py`, `supabase_validator.py` |
| JWKS gate by real supabase_url; fail-closed empty URL | PASS | `test_empty_supabase_url_fails_closed_for_es256` |
| SUPABASE_JWT_SECRET removed; test_config_schema updated | PASS | `schema.py`, `.env.example`, pilot tests |
| Test harness ES256+mock-JWKS; 14 files green | PASS | `tests/supabase_jwt_harness.py`; 398 offline tests |
| Validator ES256/JWKS tests | PASS | `test_supabase_jwt_validator.py` (kid refresh, HS256 reject) |
| Docs 09/04/07/runbooks JWKS-only; runbook docs test | PASS | t07 doc sync; `test_supabase_runbook_docs.py` |
| Full offline pytest green | PASS | 398 passed, 12 deselected |
| (Optional live) ES256 `/me` | SKIP | operator live smoke |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
cd doge-identity-service && .venv/bin/python -m pytest -q -m "not live_integration"
# 398 passed, 12 deselected (2026-07-04T10:40:01Z)
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
