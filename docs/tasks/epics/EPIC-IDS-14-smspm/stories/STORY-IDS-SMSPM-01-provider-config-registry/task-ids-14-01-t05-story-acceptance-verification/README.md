## Task workspace — `task-ids-14-01-t05-story-acceptance-verification`

- Story: [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md)
- Prerequisite: [`t01`](../task-ids-14-01-t01-smspm-settings-config/README.md), [`t02`](../task-ids-14-01-t02-smspm-descriptor-registry/README.md), [`t03`](../task-ids-14-01-t03-smspm-config-tests/README.md), [`t04`](../task-ids-14-01-t04-env-example-smspm-block/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000046`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SMSPM-01 parent acceptance criteria

### Цель
Story gate — закрыть все 5 parent AC verbatim; sync epic/bullrun/backlog INDEX; dashboard Remaining после Done (P3).

### Почему это важно
Завершает pkg-000046; без HTTP send (SMSPM-02 остаётся backlog).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md).
2. Tasks t01–t04 — settings, descriptor+registry, tests, `.env.example`.
3. Backlog source — [`STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md).
4. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Story parent AC всё ещё `[ ]` до финальной сверки t01–t04 и live pytest (P3).

### AC/DoD
- [x] (P0) Story AC #1: `SMS_PROVIDER=smspm` принимается; неизвестное имя отклоняется — evidence t02+t03.
- [x] (P0) Story AC #2: без HASH/TOKEN/FROM сервис не стартует с config-ошибкой — evidence t01+t03.
- [x] (P0) Story AC #3: `mock|file|telnyx` без SMSPM env не регрессирует — evidence t03.
- [x] (P0) Story AC #4: `.env.example` блок SMSPM + комментарий провайдеров — evidence t04.
- [x] (P0) Story AC #5: T01–T04 закрыты; descriptor в `ALL_SMS_PROVIDER_DESCRIPTORS` — evidence t02+t05.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green (P3 live).
- [x] (P1) `acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only — не в P1).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 1; bullrun + `smspm/INDEX.md` + root backlog INDEX; `identity-mvp-dashboard.md` Remaining at Done.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/backlog-stories/smspm/INDEX.md`
- `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`
- `doge-identity-service/docs/tasks/identity-mvp-dashboard.md` (Remaining — at P3 Done)

### Out of scope
- HTTP send / runbook / webhook (SMSPM-02/03/04)
- Product `src/` в этом таске

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
