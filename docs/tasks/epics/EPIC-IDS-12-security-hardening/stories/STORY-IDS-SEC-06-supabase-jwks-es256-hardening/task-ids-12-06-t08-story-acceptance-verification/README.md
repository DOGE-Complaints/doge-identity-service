## Task workspace — `task-ids-12-06-t08-story-acceptance-verification`

- Story: [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Prerequisite: [`task-ids-12-06-t06-offline-jwks-validator-tests`](../task-ids-12-06-t06-offline-jwks-validator-tests/README.md), [`task-ids-12-06-t07-jwks-only-docs-sync`](../task-ids-12-06-t07-jwks-only-docs-sync/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000042`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) §Подзадачи T08; [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SEC-06 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (10 checkboxes): targeted greps = 0; offline suite green; docs synced; optional live `/me`.

### Почему это важно
Story gate для pkg-000042; завершает JWKS-only hardening wave; JWKS live-verify на Railway — см. [`run-and-healthcheck.md`](../../../../../../runbook/run-and-healthcheck.md).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md).
2. Tasks t01–t07 — audit, validator, DI, config, harness, validator tests, docs.
3. Backlog source — [`STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md).

### Gap / Проблема
Story parent AC ещё `[ ]` (кроме W1) до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1 (W1): debug grep — already `[x]`; re-verify empty.
- [ ] (P0) Story AC #2: src grep `_validate_hs256|OctKey|test-secret-for-demo|demo.local|supabase_jwt_secret|SUPABASE_JWT_SECRET` empty (oauth HS256 excluded).
- [ ] (P0) Story AC #3–#5: DI, JWKS gate, config removal — evidence t02–t04.
- [ ] (P0) Story AC #6–#7: harness + validator tests — evidence t05–t06.
- [ ] (P0) Story AC #8: docs — evidence t07.
- [ ] (P0) Story AC #9: `.venv/bin/python -m pytest -q -m "not live_integration"` green.
- [ ] (P1) Story AC #10 (optional live): ES256 Cloud token `/me` 200.
- [ ] (P1) `acceptance-verification-task-ids-12-06-t08-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3).
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 5; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-04/05
- New runtime features

### Проверка
```bash
cd doge-identity-service
grep -rn '_validate_hs256\|OctKey\|test-secret-for-demo\|demo\.local\|supabase_jwt_secret\|SUPABASE_JWT_SECRET' src/ && exit 1 || true
grep -rn '_debug_log\|3c4b9a\|post-fix' src/ && exit 1 || true
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
