## Task workspace — `task-ids-14-04-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- Prerequisite: [`t01`](../task-ids-14-04-t01-smspm-delivery-route-handler/README.md), [`t02`](../task-ids-14-04-t02-smspm-delivery-ingest/README.md), [`t03`](../task-ids-14-04-t03-smspm-sender-report-url/README.md), [`t04`](../task-ids-14-04-t04-smspm-delivery-offline-tests/README.md), [`t05`](../task-ids-14-04-t05-smspm-delivery-env-docs/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000049`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SMSPM-04 parent acceptance criteria

### Цель
Story gate — закрыть все 6 parent AC verbatim; sync epic/bullrun/backlog INDEX; dashboard Remaining после Done (P3).

### Почему это важно
Завершает pkg-000049; confirm must stay ungated (D-04-5); no Ed25519.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md).
2. Backlog source — [`STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до сверки t01–t05 и pytest (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) Story AC #1: delivery statuses by provider message id; OTP-confirm flow unchanged (D-04-5) — evidence t02+t04.
- [x] (P0) Story AC #2: `OK` valid secret; 401 mismatch (D-04-1) — evidence t01+t04.
- [x] (P0) Story AC #3: replay/stale forward-only (D-04-3) — evidence t02+t04.
- [x] (P0) Story AC #4: audit without raw phone/OTP (D-04-6) — evidence t02+t04.
- [x] (P0) Story AC #5: `SMSPM_REPORT_URL` set → sender `report` (D-04-4) — evidence t03+t04.
- [x] (P0) Story AC #6: offline T06 green; env documented (T07) — evidence t04+t05.
- [x] (P1) `acceptance-verification-task-ids-14-04-t06-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only — не в P1).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 4; bullrun + `smspm/INDEX.md` + root backlog INDEX; `identity-mvp-dashboard.md` Remaining at Done.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-04-delivery-report-webhook/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/backlog-stories/smspm/INDEX.md`
- `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`
- `doge-identity-service/docs/tasks/identity-mvp-dashboard.md` (Remaining — at P3 Done)

### Out of scope
- SMSPM-03 live t04; SMSPM-05 draft
- SPIKE ops
- Invent AC; Ed25519; gate confirm

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
