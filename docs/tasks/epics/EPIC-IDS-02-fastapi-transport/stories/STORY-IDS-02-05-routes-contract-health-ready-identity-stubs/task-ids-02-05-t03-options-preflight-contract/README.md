## Task workspace — `task-ids-02-05-t03-options-preflight-contract`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done
**Wave:** `pkg-000003`  
---

## Task: implement — OPTIONS preflight coverage for protected endpoints

### Цель
Явно зарегистрировать OPTIONS handlers для защищённых endpoint-ов из Story 5 contract.

### AC/DoD
- [x] `OPTIONS /me` возвращает 200.
- [x] OPTIONS существуют для защищённых `/auth/eid/start`, `/oauth/*`, `/story-*`, `/gpt/actions/submit-story`.
- [x] OPTIONS не добавляются для public callback-only routes, где preflight не требуется.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Process
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
