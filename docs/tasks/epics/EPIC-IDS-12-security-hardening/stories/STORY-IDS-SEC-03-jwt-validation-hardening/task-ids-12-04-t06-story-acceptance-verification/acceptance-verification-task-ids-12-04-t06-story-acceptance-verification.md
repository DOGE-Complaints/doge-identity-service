# Acceptance verification — task-ids-12-04-t06-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-26
- **Wave:** pkg-000038
- **Story:** STORY-IDS-SEC-03-jwt-validation-hardening

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Принято и задокументировано решение по `aud` | PASS | [`epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md`](../../../../../../../analysis/epic-ids-12-sec-03-jwt-aud-decision-2026-06-26.md); `supabase_validator.py` `aud` registry |
| Если валидировать: aud test | PASS | `test_wrong_aud_raises`, `test_missing_aud_raises` |
| Форма импорта ключа подтверждена; код и spec 09 совпадают | PASS | `OctKey.import_key(jwt_secret)`; `test_raw_octkey_import_is_canonical_for_supabase_hs256`; spec 09 |
| Расхождение G-5 устранено | PASS | spec 09 + `04-security.md` §1; no G-5 open notes |
| Регрессий нет: iss/sub/exp/role | PASS | full offline suite 379 passed |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 379 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
