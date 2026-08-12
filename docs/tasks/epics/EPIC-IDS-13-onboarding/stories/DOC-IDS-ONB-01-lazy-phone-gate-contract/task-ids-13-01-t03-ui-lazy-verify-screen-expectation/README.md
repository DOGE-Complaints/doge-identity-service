## Task workspace — `task-ids-13-01-t03-ui-lazy-verify-screen-expectation`

- Story: [`../DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- Decision Ref: [`../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) «Sequence» + SPA verify

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000040`  
**Skill declared:** python-pro  
**Depends:** t01 (gap list)

---

## Task: implement/docs — UI lazy verify screen expectation

### Цель
Добавить в `08-ui-expectations.md` явное ожидание: защищённое действие → проверка `phone_verified` → verify-экран (PV-05 inline flow).

### Почему это важно
Story DoD #2 и #3 (spa side): spa-app должна знать, когда показывать verify.

### Факты из кода
1. [`08-ui-expectations.md:17-24`](../../../../../../../docs/runtime-docs/08-ui-expectations.md) — API-флоу verify есть; нет lazy-gate sequence.
2. PV-05 routes: `/auth/phone/request`, `/auth/phone/confirm` ([`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)).

### Gap / Проблема
Нет явного UX expectation «действие заблокировано → verify screen» (audit t01).

### AC/DoD
- [x] (P0) Story DoD #2: `08-ui-expectations.md` — verify-экран при `phone_verified=false`.
- [x] (P0) Story DoD #3: sequence словами (использует систему → действие → verify → действие разрешено).

### Где менять код
- [`docs/runtime-docs/08-ui-expectations.md`](../../../../../../../docs/runtime-docs/08-ui-expectations.md) — секция lazy verify expectation.

### Out of scope
- Реализация UI в spa-app.
- Код Identity.

### Проверка
```bash
cd doge-identity-service
grep -n "phone_verified\|verify\|ленив\|защищён" docs/runtime-docs/08-ui-expectations.md
```
