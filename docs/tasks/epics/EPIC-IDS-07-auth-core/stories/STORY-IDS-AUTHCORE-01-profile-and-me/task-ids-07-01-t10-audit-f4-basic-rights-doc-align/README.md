## Task workspace — `task-ids-07-01-t10-audit-f4-basic-rights-doc-align`

- Story: [`../STORY-IDS-AUTHCORE-01-profile-and-me.md`](../STORY-IDS-AUTHCORE-01-profile-and-me.md)
- Audit source: [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) (F4)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000010`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-07-authcore-01-audit-2026-06-05.md) §F4  
---

## Task: fix — «базовые права» doc align (F4)

### Цель
Зафиксировать контракт «базовые права» для `GET /me`: минимальная реализация — поле `role` из JWT; без новой RBAC-матрицы. Согласовать story scope / runtime-doc с фактическим payload.

### Почему это важно
Scope story обещает «+ базовые права»; в коде только `role`. Без явного doc-align операторы ожидают `permissions`/`rights` массив.

### Факты из кода
1. [`me_response.py:17-34`](../../../../../../../src/core/api/me_response.py) — `data` включает `role` из `UserClaims`; нет `permissions` / `rights`.
2. [`models.py:16-19`](../../../../../../../src/core/domain/models.py) — `UserClaims.role` из JWT.
3. [`runtime-docs/01-api.md:24`](../../../../../../../runtime-docs/01-api.md) — «профиль + права» для `/me`.
4. Story Scope п.3 — «базовые права» без RBAC (t03 README).

### Gap / Проблема
Scope-partial: реализация минимальна и корректна для MVP, но не задокументирована как намеренный контракт.

### AC/DoD
- [x] (P0) В BULLRUN и/или [`01-api.md`](../../../../../../../runtime-docs/01-api.md) (или epic §) явно: «базовые права = `role` из JWT на этапе AUTHCORE-01».
- [x] (P0) Не вводить новую permission-систему в этом таске.
- [x] (P1) Pipeline story / epic Scope не противоречит (одна строка clarifying note допустима).
- [x] (P1) Тесты `/me` по-прежнему assert `role` при необходимости.

### Где менять код
- `doge-identity-service/runtime-docs/01-api.md` (предпочтительно)
- опционально: `doge-identity-service/docs/tasks/epics/EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md` §Story 1

### Out of scope
- RBAC / permission matrix.
- OAuth introspection (STORY-IDS-OAUTH-02).
- Расширение payload новыми полями без отдельного requirement.

### Проверка
```bash
grep -n "role\|права\|rights\|permissions" doge-identity-service/runtime-docs/01-api.md
grep -n "role" doge-identity-service/src/core/api/me_response.py
```
