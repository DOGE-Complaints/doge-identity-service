## Task workspace — `task-ids-13-01-t01-lazy-gate-doc-gap-audit`

- Story: [`../DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- Decision Ref: [`../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md); [`../../../../../../analysis/identity-onboarding-ux-2026-06-12.md`](../../../../../../analysis/identity-onboarding-ux-2026-06-12.md) §G3

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000040`  
**Skill declared:** python-pro  
---

## Task: verify — lazy phone gate doc gap audit

### Цель
Зафиксировать baseline перед правками: сопоставить «Что задокументировать» из story с фактическим содержимым `09-gateway-expectations.md` и `08-ui-expectations.md`.

### Почему это важно
P3 = gap-closure по verbatim DoD; без audit нельзя доказать, что gaps закрыты (precedent CLEANUP-03 t01).

### Факты из кода
1. [`me_response.py:42`](../../../../../../../src/core/api/me_response.py) — `/me` отдаёт `phone_verified`.
2. [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — маршруты PV-05 `/auth/phone/request`, `/auth/phone/confirm`.
3. [`09-gateway-expectations.md:20-49`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md) — introspection/`verification_required`; **нет** отдельной секции «ленивый гейт телефона».
4. [`08-ui-expectations.md:17-24`](../../../../../../../docs/runtime-docs/08-ui-expectations.md) — inline verify API; **нет** явного sequence «защищённое действие → `phone_verified=false` → verify».

### Gap / Проблема
Story DoD #1–#4 — checklist gaps (PASS/FAIL per item) до правок t02–t04.

### AC/DoD
- [x] (P0) Story DoD #1: audit — gateway contract for `phone_verified` (PASS/FAIL + line refs).
- [x] (P0) Story DoD #2: audit — UI verify expectation on `phone_verified=false` (PASS/FAIL).
- [x] (P0) Story DoD #3: audit — canonical example + consumer enforce wording (PASS/FAIL).
- [x] (P0) Story DoD #4: audit — PV-05 + runbook crosslinks (PASS/FAIL).

### Где менять код
- Audit-артефакт в этой папке (P3): gap checklist с line refs.
- Read-only baseline: [`09-gateway-expectations.md`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md), [`08-ui-expectations.md`](../../../../../../../docs/runtime-docs/08-ui-expectations.md).

### Out of scope
- Правки runtime-docs (t02–t04).
- Код Identity или gateway.

### Проверка
```bash
cd doge-identity-service
grep -n "ленив\|lazy\|phone_verified\|защищён" docs/runtime-docs/08-ui-expectations.md docs/runtime-docs/09-gateway-expectations.md
```
