## Task workspace — `task-ids-15-02-t04-story-acceptance-verification`

- Story: [`../STORY-IDS-VB-02-me-expose-identity-verified.md`](../STORY-IDS-VB-02-me-expose-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-02-t01-me-response-identity-verified/README.md), [`t02`](../task-ids-15-02-t02-api-docs-medata/README.md), [`t03`](../task-ids-15-02-t03-test-me-profile-opaque/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000051`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-VB-02 parent acceptance criteria

### Цель
Story gate — закрыть AC-ID-THR-01/03/04 + docs/tests AC; sync epic/bullrun/backlog INDEX (P3).

### Почему это важно
Завершает pkg-000051; consumer wire contract for opaque flag.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-VB-02-me-expose-identity-verified.md`](../STORY-IDS-VB-02-me-expose-identity-verified.md).
2. Backlog source — [`STORY-IDS-VB-02-me-expose-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-02-me-expose-identity-verified.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до сверки t01–t03 и pytest (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) AC-ID-THR-01: no new HTTP path; wire key `identity_verified` on `/me` — evidence t01.
- [x] (P0) AC-ID-THR-03: opaque present; method flags may coexist — evidence t01+t03.
- [x] (P0) AC-ID-THR-04: single boolean regardless of method — evidence t01+t03.
- [x] (P0) Docs + offline tests updated; suite green for touched — evidence t02+t03.
- [x] (P1) `acceptance-verification-task-ids-15-02-t04-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only — не в P1).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story VB-02; bullrun + package INDEX + root backlog INDEX.

### Где менять код
- Docs/index sync only at gate (no product source beyond verification evidence)

### Out of scope
- Implementing t01–t03; VB-03; P4 audit

### Проверка
```bash
cd doge-identity-service && python3 -m pytest -q tests/test_me_profile.py -m "not live_integration"
rg -n 'identity_verified' doge-identity-service/src/core/api/me_response.py doge-identity-service/docs/runtime-docs/api-reference
```
