## Task workspace — `task-ids-12-01-t01-rate-limit-config-schema`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) Scope §конфигурируемость; Story AC #1 prerequisite  
---

## Task: implement — rate limit config schema

### Цель
Добавить типизированную конфигурацию лимитов (requests/window/scope per route) в `AppConfig` — Story Scope §конфигурируемость.

### Почему это важно
Лимиты не должны быть захардкожены; spec 16 и story AC #5 требуют config-driven values.

### Факты из кода
1. Нет rate-limit полей в [`schema.py`](../../../../../../../src/core/config/schema.py) — только `phone_resend_cooldown_s` (default 60).
2. Spec targets: eid/start 5/600s/user; callback 5/600s/ip — [`16:38-43`](../../../../../../../requirements/16-security-privacy-observability.md).
3. eID-start: 5/10min/user — [`11:129`](../../../../../../../requirements/11-eid-verification-flow.md).
4. Env parsing pattern: `_int`, `_value` in [`schema.py`](../../../../../../../src/core/config/schema.py).

### Gap / Проблема
Нет `RateLimitRule` / per-route config keys для identity sensitive routes.

### AC/DoD
- [ ] (P0) `RateLimitRule` (requests, window_s, per: user|ip) + route-key map in config module.
- [ ] (P0) Defaults: `POST /auth/eid/start` → 5/600/user; `GET /auth/{provider}/callback` → 5/600/ip.
- [ ] (P1) Env overrides for limits/windows (documented keys).
- [ ] (P1) Traceability: prerequisite Story AC #1, #5 (t04, t06).

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- Optional: `doge-identity-service/src/core/security/rate_limit_config.py` (new)

### Out of scope
- Limiter store implementation (t02)
- FastAPI dependency (t03)
- `POST /auth/phone/request` HTTP limit (follow-up wave)

### Проверка
```bash
cd doge-identity-service
grep -n 'rate_limit\|RateLimit' src/core/config/schema.py src/core/security/*.py 2>/dev/null || true
```
