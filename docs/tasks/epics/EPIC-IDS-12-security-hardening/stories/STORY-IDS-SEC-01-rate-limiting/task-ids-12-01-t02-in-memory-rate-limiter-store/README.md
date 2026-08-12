## Task workspace — `task-ids-12-01-t02-in-memory-rate-limiter-store`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t01-rate-limit-config-schema`](../task-ids-12-01-t01-rate-limit-config-schema/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md); spec 16 MVP in-memory  
---

## Task: implement — in-memory rate limiter store

### Цель
Реализовать MVP counter store (sliding or fixed window) keyed by `user:{sub}` / `ip:{addr}` — prerequisite для сквозного enforcement.

### Почему это важно
Spec 16 MVP: in-memory или Redis; backlog «Вне scope» для Redis — in-memory first.

### Факты из кода
1. No limiter in `src/core/` — verified gap in story «Точки в коде».
2. Config from t01 supplies `requests` + `window_s`.
3. Thread-safety: FastAPI async handlers — use asyncio-safe or lock-backed store.

### Gap / Проблема
Нет модуля, считающего запросы per key в окне и возвращающего `retry_after`.

### AC/DoD
- [ ] (P0) `core/security/rate_limit.py` — `check_rate_limit(key, rule) -> allowed | retry_after_s`.
- [ ] (P0) Keys: `user:{supabase_user_id}`, `ip:{client_ip}`.
- [ ] (P1) Window algorithm documented (fixed or sliding).
- [ ] (P1) Traceability: prerequisite Story AC #3 (t03).

### Где менять код
- `doge-identity-service/src/core/security/rate_limit.py` (new)

### Out of scope
- Redis backend
- HTTP 429 envelope (t03)
- Route wiring (t04)

### Проверка
```bash
cd doge-identity-service
test -f src/core/security/rate_limit.py
```
