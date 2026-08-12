## Task workspace — `task-ids-13-01-t04-pv05-runbook-crosslinks-sequence`

- Story: [`../DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- Decision Ref: [`../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) «Sequence» + DoD #4

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000040`  
**Skill declared:** python-pro  
**Depends:** t02, t03

---

## Task: implement/docs — PV-05 runbook crosslinks and sequence

### Цель
Добавить cross-links и sequence block в секции t02/t03: ссылки на PV-05 story, runbook, requirements flow.

### Почему это важно
Story DoD #4: потребители должны найти флоу верификации из контракта lazy gate.

### Факты из кода
1. [`STORY-IDS-PV-05-verification-flow-api.md`](../../../../EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md) — API флоу 🟢.
2. [`onboarding-phone-verification-api.md`](../../../../../../../docs/runbook/onboarding-phone-verification-api.md) — no-frontend runbook.
3. [`19-phone-verification-flow.md`](../../../../../../../docs/requirements/19-phone-verification-flow.md) — requirements SSOT.

### Gap / Проблема
Lazy-gate секции (t02/t03) без ссылок на PV-05 + runbook (audit t01 DoD #4 FAIL).

### AC/DoD
- [x] (P0) Story DoD #4: cross-links на PV-05, runbook, req-19 в t02/t03 секциях.
- [x] (P1) Краткий sequence block (словами) согласован с story «Sequence».

### Где менять код
- [`docs/runtime-docs/09-gateway-expectations.md`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md) — cross-links в lazy-gate секции (t02).
- [`docs/runtime-docs/08-ui-expectations.md`](../../../../../../../docs/runtime-docs/08-ui-expectations.md) — cross-links в lazy verify секции (t03).

### Out of scope
- Правки PV-05 story или runbook body (только ссылки из runtime-docs).
- Код.

### Проверка
```bash
cd doge-identity-service
grep -n "PV-05\|onboarding-phone-verification\|19-phone-verification" docs/runtime-docs/08-ui-expectations.md docs/runtime-docs/09-gateway-expectations.md
```
