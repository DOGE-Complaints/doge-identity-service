## Task workspace — `task-ids-14-02-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: [`t01`](../task-ids-14-02-t01-smspm-sms-sender-send/README.md), [`t02`](../task-ids-14-02-t02-smspm-error-mapping/README.md), [`t03`](../task-ids-14-02-t03-smspm-descriptor-wire/README.md), [`t04`](../task-ids-14-02-t04-smspm-sender-offline-tests/README.md), [`t05`](../task-ids-14-02-t05-smspm-sender-live-skip-without-creds/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000047`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SMSPM-02 parent acceptance criteria

### Цель
Story gate — закрыть все 5 parent AC verbatim; sync epic/bullrun/backlog INDEX; dashboard Remaining после Done (P3).

### Почему это важно
Завершает pkg-000047; runbook/webhook остаются SMSPM-03/04.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md).
2. Backlog source — [`STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).
4. Request already stores message id — [`handlers.py:504-506`](../../../../../../../src/core/api/handlers.py).

### Gap / Проблема
Story parent AC всё ещё `[ ]` до финальной сверки t01–t05 и live pytest (P3).

### AC/DoD
- [x] (P0) Story AC #1: `SMS_PROVIDER=smspm` + valid creds `POST /auth/phone/request` delivers via SMSPM; client response without code — evidence t01+t03.
- [x] (P0) Story AC #2: success D-02-1 provider message id stored on phone session — evidence t01 + handlers.
- [x] (P0) Story AC #3: D-02-2 mapping; secrets/OTP/full MSISDN not in logs (D-02-7) — evidence t02+t04.
- [x] (P0) Story AC #4: offline T04 green; live T05 skip without creds — evidence t04+t05.
- [x] (P0) Story AC #5: `mock|file|telnyx` no regression; MVP without `report` (D-02-5) — evidence t01+t04.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green (P3 live).
- [x] (P1) `acceptance-verification-task-ids-14-02-t06-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only — не в P1).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 2; bullrun + `smspm/INDEX.md` + root backlog INDEX; `identity-mvp-dashboard.md` Remaining at Done.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/backlog-stories/smspm/INDEX.md`
- `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`
- `doge-identity-service/docs/tasks/identity-mvp-dashboard.md` (Remaining — at P3 Done)

### Out of scope
- Runbook / webhook (SMSPM-03/04)
- Product `src/` в этом таске
- SPIKE ops

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
