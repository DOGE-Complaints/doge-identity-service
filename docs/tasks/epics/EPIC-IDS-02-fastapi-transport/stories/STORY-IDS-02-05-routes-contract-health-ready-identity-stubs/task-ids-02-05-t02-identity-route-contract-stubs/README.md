## Task workspace — `task-ids-02-05-t02-identity-route-contract-stubs`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done
**Wave:** `pkg-000003`  
---

## Task: implement — identity route table и NOT_IMPLEMENTED stubs

### Цель
Зарегистрировать identity route contract из Story 5 и stub-handlers с `NOT_IMPLEMENTED`/`next_epic`.

### AC/DoD
- [x] Route table содержит все paths из Story 5 (`/me`, `/auth/*`, `/oauth/*`, `/story-*`, `/gpt/actions/submit-story`).
- [x] Защищённые routes без auth дают 401, с stub auth — 501.
- [x] Stubs возвращают envelope с `code="NOT_IMPLEMENTED"`.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/src/core/api/handlers.py`

### Process
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
