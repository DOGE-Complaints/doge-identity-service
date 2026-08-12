# Story acceptance gate — STORY-IDS-SEC-04-service-role-isolation

- **Story:** Изоляция Supabase `service_role`: identity — единственный держатель
- **Package:** `pkg-000043-20260709-epic-ids-12-sec-04-service-role-isolation.yaml`
- **Result:** PASS
- **Date:** 2026-07-09T19:39:30Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Зафиксировано требование «identity — единственный держатель `service_role`; не в браузере» (в 04-security / 07-env / runbook) | PASS | t01: [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) §5.1; [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md); [`env-secrets-handbook.md`](../../../../../../../docs/runbook/env-secrets-handbook.md) |
| No-expose подтверждён (нет в логах/ответах/trace) — проверяемо | PASS | t02: [`test_service_role_no_expose.py`](../../../../../../../tests/test_service_role_no_expose.py) — 4 passed |
| Rotation runbook написан (Dashboard → identity env; триггеры) | PASS | t03: [`supabase-service-role-rotation.md`](../../../../../../../docs/runbook/supabase-service-role-rotation.md); linked from [`runbook/README.md`](../../../../../../../docs/runbook/README.md) |
| Ротация скоординирована с spa [SEC-01](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md) (если был фронт-bundle) | PASS | t04: runbook §Spa coordination + checklist |

## Commands (live verification 2026-07-09)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service && .venv/bin/python -m pytest -q -m "not live_integration"
# 402 passed, 12 deselected (2026-07-09T19:39:30Z)
grep -rn 'единственн\|identity-only' docs/runtime-docs/04-security.md docs/requirements/07-env-configuration-spec.md
grep -n 'SEC-01\|coordination' docs/runbook/supabase-service-role-rotation.md
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
