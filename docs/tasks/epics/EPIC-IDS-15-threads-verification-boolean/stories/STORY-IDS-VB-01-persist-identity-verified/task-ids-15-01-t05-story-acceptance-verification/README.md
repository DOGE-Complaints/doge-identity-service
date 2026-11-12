## Task workspace — `task-ids-15-01-t05-story-acceptance-verification`

- Story: [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-01-t01-migration-identity-verified/README.md), [`t02`](../task-ids-15-01-t02-profile-model-and-db-map/README.md), [`t03`](../task-ids-15-01-t03-backfill-existing-verified/README.md), [`t04`](../task-ids-15-01-t04-offline-persist-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000050`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-VB-01 parent acceptance criteria

### Цель
Story gate — закрыть все 4 parent AC verbatim; sync epic/bullrun/backlog INDEX; dashboard Remaining после Done (P3).

### Почему это важно
Завершает pkg-000050; unlocks VB-02/VB-03 intake.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md).
2. Backlog source — [`STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до сверки t01–t04 и pytest (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) Story AC #1: Profile stores `identity_verified` bool (default false) — evidence t01+t02+t04.
- [x] (P0) Story AC #2: Backfill one-shot method OR → opaque true — evidence t03+t04.
- [x] (P0) Story AC #3: No clear-on-failure required/introduced — evidence t03 + code review.
- [x] (P0) Story AC #4: Offline tests map+backfill; `-m "not live_integration"` green for touched — evidence t04.
- [x] (P1) `acceptance-verification-task-ids-15-01-t05-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only — не в P1).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 1; bullrun + `threads-verification-boolean/INDEX.md` + root backlog INDEX; dashboard Remaining at Done.

### Где менять код
- Docs/index sync only at gate (no product source in this task beyond verification evidence)

### Out of scope
- Implementing t01–t04; VB-02/VB-03; P4 audit

### Проверка
```bash
cd doge-identity-service && python3 -m pytest -q -m "not live_integration"
rg -n 'identity_verified' doge-identity-service/src doge-identity-service/supabase
```
