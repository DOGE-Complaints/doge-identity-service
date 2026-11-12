## Task workspace — `task-ids-14-03-t05-story-acceptance-verification`

- Story: [`../STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- Prerequisite: [`t01`](../task-ids-14-03-t01-runbook-mode-c-env-table/README.md), [`t02`](../task-ids-14-03-t02-runbook-curl-smoke/README.md), [`t03`](../task-ids-14-03-t03-runbook-troubleshooting/README.md), [`t04`](../task-ids-14-03-t04-live-ee-smoke-run-summary/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** blocked  
**Wave:** `pkg-000048`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SMSPM-03 parent acceptance criteria

### Цель
Story gate — закрыть все 4 parent AC verbatim; sync epic/bullrun/backlog INDEX. **Если t04 BLOCKED — gate не PASS; story остаётся ⚪ Todo; AC #4 `[ ]`.** t01–t03 могут быть 🟢.

### Почему это важно
Завершает pkg-000048 только при реальном live evidence. Dashboard Remaining — только при P3 Done **и** AC #4 PASS.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../STORY-IDS-SMSPM-03-operator-runbook-smoke.md).
2. Backlog source — [`STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).
4. t04 BLOCKED rule — [`../task-ids-14-03-t04-live-ee-smoke-run-summary/README.md`](../task-ids-14-03-t04-live-ee-smoke-run-summary/README.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до сверки t01–t04 (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) Story AC #1: режим C + env-чеклист — evidence t01.
- [x] (P0) Story AC #2: live-smoke curl-путь; Telnyx и mock описаны (D-03-2) — evidence t02.
- [x] (P0) Story AC #3: troubleshooting rows — evidence t03.
- [ ] (P0) Story AC #4: live EE smoke + run-summary без секретов/PII — evidence t04 **PASS only**. If t04 BLOCKED → this AC stays open; gate Result not PASS.
- [ ] (P1) `acceptance-verification-task-ids-14-03-t05-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only — не в P1) **only if** AC #1–#4 PASS.
- [ ] (P1) If gate PASS: pipeline Meta `Status: 🟢 Done`; epic §Story 3; bullrun + `smspm/INDEX.md` + root backlog INDEX; `identity-mvp-dashboard.md` Remaining at Done.
- [x] (P1) Не править `src/`. Не мутировать pkg-000046/000047.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/backlog-stories/smspm/INDEX.md`
- `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`
- `doge-identity-service/docs/tasks/identity-mvp-dashboard.md` (Remaining — at P3 Done **only if** AC #4 PASS)

### Out of scope
- Webhook (SMSPM-04); SMSPM-05 draft
- Product `src/` в этом таске
- SPIKE ops
- Invented live PASS

### Проверка
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
rg -n 'режим C|SMS_PROVIDER=smspm' doge-identity-service/docs/runbook/phone-sms-verification.md
```
