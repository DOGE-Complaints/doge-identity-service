## Task workspace — `task-ids-11-04-t04-verification-required-contract`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: [`task-ids-11-04-t03-oauth-verify-gate-phone-branch`](../task-ids-11-04-t03-oauth-verify-gate-phone-branch/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) Scope §канон 403; Story AC #3  
---

## Task: implement — `verification_required` contract module

### Цель
Зафиксировать канон payload `{error, reason, verify_url}` keyed on `phone_verified` для verify-need сигналов identity (Story AC #3).

### Почему это важно
Gateway и GPT-петля должны получать единый отказ с URL куда вести пользователя; сейчас контракт не определён в runtime.

### Факты из кода
1. `verification_required` не реализован (narrative only): [`04-security.md`](../../../../../../runtime-docs/04-security.md).
2. Gateway expectations: [`09-gateway-expectations.md`](../../../../../../runtime-docs/09-gateway-expectations.md).
3. Verify-need branch будет в complete-path (t03).

### Gap / Проблема
Нет модуля, собирающего канонический 403 body с `verify_url` под phone (не `eid_verified`).

### AC/DoD
- [ ] (P0) Story AC #3: модуль e.g. `core/oauth/verification_required.py` с `{ "error": "verification_required", "reason": "...", "verify_url": "..." }`.
- [ ] (P0) `verify_url` builder с `return_context` query param.
- [ ] (P0) Wire в OAuth complete verify-need path (identity only; **не** gateway enforcement).
- [ ] (P1) Под `phone_verified`, не `eid_verified`.

### Где менять код
- `doge-identity-service/src/core/oauth/verification_required.py` (new)
- `doge-identity-service/src/core/oauth/handlers.py` (wire)

### Out of scope
- Gateway repo enforcement
- HTTP status mapping separation (t05)
- eID branch

### Проверка
```bash
cd doge-identity-service
test -f src/core/oauth/verification_required.py
grep -n 'verification_required' src/core/oauth/*.py
```
