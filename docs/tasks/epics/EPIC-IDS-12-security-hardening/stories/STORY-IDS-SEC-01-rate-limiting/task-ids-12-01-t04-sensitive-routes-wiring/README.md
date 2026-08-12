## Task workspace — `task-ids-12-01-t04-sensitive-routes-wiring`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t03-rate-limit-dependency-429-envelope`](../task-ids-12-01-t03-rate-limit-dependency-429-envelope/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) Scope §чувствительные роуты; Story AC #1  
---

## Task: implement — wire sensitive routes rate limits

### Цель
Подключить rate-limit dependency к `POST /auth/eid/start` (per-user 5/10min) и `GET /auth/{provider}/callback` (per-ip) — Story AC #1.

### Почему это важно
G-1 HIGH gap: eID start без лимита ([`handlers.py:169`](../../../../../../../src/core/api/handlers.py)); callback публичный entry.

### Факты из кода
1. `POST /auth/eid/start` — [`asgi_app.py:283`](../../../../../../../src/core/api/asgi_app.py).
2. `GET /auth/{provider}/callback` — [`asgi_app.py:301`](../../../../../../../src/core/api/asgi_app.py) (not `/auth/eid/callback` literal).
3. `POST /auth/phone/request` — [`asgi_app.py:322`](../../../../../../../src/core/api/asgi_app.py) — **не wire** в pkg-000035 (operator follow-up).

### Gap / Проблема
Sensitive routes не защищены HTTP-level rate limit.

### AC/DoD
- [ ] (P0) Story AC #1: eid/start = 5 requests / 600s / user enforced.
- [ ] (P0) Callback per-ip limit 5/600s wired on `GET /auth/{provider}/callback`.
- [ ] (P1) Documented route table in code or runtime-docs (identity subset of RATE_LIMITS).
- [ ] (P1) `POST /auth/phone/request` explicitly out of this wave (follow-up).

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- phone/request HTTP limit (follow-up)
- Gateway `/stories`, `/gpt/...` (backlog «Вне scope»)

### Проверка
```bash
cd doge-identity-service
grep -n 'rate_limit\|check_rate' src/core/api/asgi_app.py
```
