## Task workspace — `task-ids-12-01-t09-audit-f2-callback-ip-xff-trusted-proxy`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t08-audit-f1-backlog-sec-01-story-sync`](../task-ids-12-01-t08-audit-f1-backlog-sec-01-story-sync/README.md) (recommended order)
- Audit source: [`../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md`](../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md) (F2)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `override epic_ids_12_sec_01_audit_2026_06_26`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md`](../../../../../../analysis/epic-ids-12-sec-01-audit-2026-06-26.md) §F2  
---

## Task: implement — trusted proxy IP for callback rate limit (F2)

### Цель
Закрыть обход per-ip лимита на `GET /auth/{provider}/callback`: клиентский `X-Forwarded-For` не должен давать новый ключ `ip:{spoof}`.

### Почему это важно
Callback per-ip — анти-абьюз для публичного entry; спуфабельный XFF ослабляет именно эту защиту (audit F2 MEDIUM, security).

### Факты из кода
1. [`rate_limit_dependency.py:14-20`](../../../../../../../src/core/api/rate_limit_dependency.py) — `_client_ip` берёт **первое** значение `X-Forwarded-For` без проверки trusted proxy.
2. Callback wiring: [`asgi_app.py:323`](../../../../../../../src/core/api/asgi_app.py) `Depends(require_callback_rate_limit)`.
3. Key format: `ip:{_client_ip(request)}` — [`rate_limit_dependency.py:44-48`](../../../../../../../src/core/api/rate_limit_dependency.py).
4. eid/start per-user (JWT) — не затронут; только callback path.

### Gap / Проблема
Атакующий ротацией `X-Forwarded-For` обходит sliding-window per-ip на callback.

### AC/DoD
- [ ] (P0) `_client_ip` (или замена) не доверяет произвольному XFF от клиента; trusted-proxy hops через config (env в [`schema.py`](../../../../../../../src/core/config/schema.py)).
- [ ] (P0) Default/demo: без trusted proxy — `request.client.host` (без XFF).
- [ ] (P0) Offline-тест: spoof `X-Forwarded-For` не сбрасывает rate-limit key / не даёт обход N+1.
- [ ] (P1) Краткая запись deployment contract в [`04-security.md`](../../../../../../../runtime-docs/04-security.md) §8 (trusted proxy + callback IP).
- [ ] (P1) Regression: existing [`test_rate_limiting.py`](../../../../../../../tests/test_rate_limiting.py) green.

### Где менять код
- `doge-identity-service/src/core/api/rate_limit_dependency.py`
- `doge-identity-service/src/core/config/schema.py` (trusted proxy env)
- `doge-identity-service/tests/test_rate_limiting.py` (spoof case)
- `doge-identity-service/docs/runtime-docs/04-security.md` (§8 note)

### Out of scope
- `POST /auth/phone/request` (SEC-01b).
- Redis-backed limiter (O1 deployment note).
- Изменение pkg-000035 yaml.

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_rate_limiting.py -m "not live_integration" -q
```
