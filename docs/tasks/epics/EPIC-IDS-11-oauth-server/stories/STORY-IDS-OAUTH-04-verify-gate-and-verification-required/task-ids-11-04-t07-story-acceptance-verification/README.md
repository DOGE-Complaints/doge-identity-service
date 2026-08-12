## Task workspace — `task-ids-11-04-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: [`task-ids-11-04-t06-offline-oauth-verify-gate-tests`](../task-ids-11-04-t06-offline-oauth-verify-gate-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-OAUTH-04 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (5 checkboxes): relay, verify-gate, `verification_required` contract, HTTP separation, offline tests + gateway doc.

### Почему это важно
Story gate для pkg-000034; завершает OAUTH-04 wave и разблокирует downstream gateway integration.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) (5 checkboxes verbatim).
2. Tasks t01–t06 — implementation + tests.
3. Gateway contract touchpoint: [`09-gateway-expectations.md`](../../../../../../runtime-docs/09-gateway-expectations.md).
4. Optional: [`04-security.md`](../../../../../../runtime-docs/04-security.md) relay table row.

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: relay authorize→complete — evidence t01, t02, t06.
- [ ] (P0) Story AC #2: verify-gate unverified branch — evidence t03, t06.
- [ ] (P0) Story AC #3: `verification_required` 403 + `verify_url` — evidence t04, t05, t06.
- [ ] (P0) Story AC #4: verify-need ≠ OTP 400 — evidence t05, t06.
- [ ] (P0) Story AC #5: offline tests + gateway contract doc — evidence t06, `09-gateway-expectations.md`.
- [ ] (P1) `acceptance-verification-task-ids-11-04-t07-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 4; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md`
- `doge-identity-service/docs/runtime-docs/09-gateway-expectations.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Gateway repo enforcement
- Backlog file deletion
- eID branch

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
