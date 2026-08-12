## Task workspace — `task-ids-13-01-t05-story-acceptance-verification`

- Story: [`../DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- Decision Ref: [`../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) DoD #1–#4; template [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000040`  
**Skill declared:** python-pro  
---

## Task: verify — story acceptance verification

### Цель
Формально закрыть DOC-IDS-ONB-01: прогнать все DoD #1–#4, зафиксировать grep/doc evidence в acceptance-артефакте.

### Почему это важно
Финальная точка story wave pkg-000040; docs-only story — acceptance по grep/doc evidence (precedent CLEANUP-03 t06, **без pytest gate**).

### Факты из кода
После t01–t04 ожидается:
1. `09-gateway-expectations.md` — lazy gate contract (DoD #1).
2. `08-ui-expectations.md` — verify screen expectation (DoD #2).
3. Каноничный пример + consumer enforce (DoD #3).
4. Cross-links PV-05 + runbook (DoD #4).

### Gap / Проблема
Нет формального acceptance report для DOC-ONB-01.

### AC/DoD
- [x] (P0) Story DoD #1: evidence — gateway contract in `09-gateway-expectations.md`.
- [x] (P0) Story DoD #2: evidence — UI verify expectation in `08-ui-expectations.md`.
- [x] (P0) Story DoD #3: evidence — canonical example + consumer enforce wording.
- [x] (P0) Story DoD #4: evidence — PV-05 + runbook links.
- [x] (P1) Создан `acceptance-verification-task-ids-13-01-t05-story-acceptance-verification.md` в этой папке (P3).
- [x] (P1) Pipeline story + bullrun sync (P3).
- [x] (P2) Optional: reconcile backlog epic row DOC-ONB-01 status.

### Где менять код
- Task-артефакты в этой папке (P3):
  - `acceptance-verification-task-ids-13-01-t05-story-acceptance-verification.md`
- [`../DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../DOC-IDS-ONB-01-lazy-phone-gate-contract.md) — DoD checkboxes + status Done (P3)
- [`bullrun-launch-index.md`](../../../../bullrun-launch-index.md) — story/task rows Done (P3)

### Out of scope
- pytest gate (docs-only wave).
- Код Identity или gateway.

### Проверка
```bash
cd doge-identity-service
grep -n "ленив\|lazy\|phone_verified\|потребител\|enforce\|PV-05\|onboarding-phone-verification" docs/runtime-docs/08-ui-expectations.md docs/runtime-docs/09-gateway-expectations.md
```
