## Task workspace — `task-ids-13-01-t02-gateway-lazy-phone-gate-section`

- Story: [`../DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../DOC-IDS-ONB-01-lazy-phone-gate-contract.md)
- Decision Ref: [`../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md`](../../../../../../backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) «Контракт гейта» + «Где enforce»

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000040`  
**Skill declared:** python-pro  
---

## Task: implement/docs — gateway lazy phone gate section

### Цель
Добавить в `09-gateway-expectations.md` секцию «ленивый гейт телефона»: consumer читает `GET /me` или introspection `{phone_verified}`; при `false` — не выполняет действие, ведёт на verify; enforce на потребителе.

### Почему это важно
Story DoD #1 и #3 (gateway side): контракт должен быть явным для gateway/spa.

### Факты из кода
1. [`me_response.py:29-45`](../../../../../../../src/core/api/me_response.py) — поле `phone_verified` в `/me`.
2. [`09-gateway-expectations.md`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md) — существующие introspection hints; нет lazy-gate секции.
3. Каноничный пример из story: создание/публикация стори (gateway).

### Gap / Проблема
Gateway consumers не имеют SSOT-секции для lazy phone gate (audit t01).

### AC/DoD
- [x] (P0) Story DoD #1: `09-gateway-expectations.md` описывает контракт `phone_verified` → verify redirect.
- [x] (P0) Story DoD #3: каноничный пример (story submit) + явно «enforce на потребителе».

### Где менять код
- [`docs/runtime-docs/09-gateway-expectations.md`](../../../../../../../docs/runtime-docs/09-gateway-expectations.md) — **новая секция** «ленивый гейт телефона».

### Out of scope
- Код gateway (другой репо).
- Полный список защищённых действий.

### Проверка
```bash
cd doge-identity-service
grep -n "ленив\|lazy\|phone_verified\|потребител\|enforce" docs/runtime-docs/09-gateway-expectations.md
```
