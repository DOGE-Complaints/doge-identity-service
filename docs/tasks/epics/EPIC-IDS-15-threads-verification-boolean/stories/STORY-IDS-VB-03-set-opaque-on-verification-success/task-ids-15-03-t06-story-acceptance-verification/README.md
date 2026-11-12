## Task workspace — `task-ids-15-03-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- Prerequisite: [`t01`](../task-ids-15-03-t01-attach-phone-sets-opaque/README.md) … [`t05`](../task-ids-15-03-t05-offline-success-failure-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000052`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-VB-03 parent acceptance criteria

### Цель
Story gate — закрыть AC-ID-THR-02/03/05 + offline tests; sync epic/bullrun/backlog INDEX (P3).

### Почему это важно
Завершает pkg-000052 / EPIC-IDS-15 product stories for opaque set-on-success.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md).
2. Backlog source — [`STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до сверки t01–t05 и pytest (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) AC-ID-THR-02: executes existing integrations; no pack/API invent — evidence t01/t02 (attach only).
- [x] (P0) AC-ID-THR-03: success persists opaque; audit remains — evidence t01–t04.
- [x] (P0) AC-ID-THR-05: existing audit functions; no new schema — evidence t04.
- [x] (P0) Offline tests success/failure — evidence t05; suite green for touched.
- [x] (P1) `acceptance-verification-task-ids-15-03-t06-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story VB-03; bullrun + package INDEX + root backlog INDEX.

### Где менять код
- Docs/index sync only at gate

### Out of scope
- Implementing t01–t05; P4 audit

### Проверка
```bash
cd doge-identity-service && python3 -m pytest -q -m "not live_integration"
rg -n 'identity_verified=True|identity_verified=true' doge-identity-service/src/core/infrastructure
```
