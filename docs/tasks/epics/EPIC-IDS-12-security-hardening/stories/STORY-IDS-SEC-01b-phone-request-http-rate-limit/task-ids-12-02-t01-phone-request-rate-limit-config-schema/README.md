## Task workspace — `task-ids-12-02-t01-phone-request-rate-limit-config-schema`

- Story: [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- Prerequisite: STORY-IDS-SEC-01 🟢 (pkg-000035 rate-limit infra)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000036`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) Scope §env-конфиг; Story AC #1  
---

## Task: implement — phone request rate limit config schema

### Цель
Добавить per-route config для `POST /auth/phone/request` (requests/window/per-user) в `AppConfig` и `rate_limit_config` — Story Scope §env-конфиг, AC #1.

### Почему это важно
Лимит не должен быть захардкожен; окно должно быть согласовано с `PHONE_RESEND_COOLDOWN_S` (Scope §2, analysis §4).

### Факты из кода
1. eid/callback keys only — [`rate_limit_config.py:21-36`](../../../../../../../src/core/security/rate_limit_config.py).
2. Env pattern: `RATE_LIMIT_EID_START_*`, `RATE_LIMIT_CALLBACK_*` — [`schema.py`](../../../../../../../src/core/config/schema.py).
3. Default cooldown: `phone_resend_cooldown_s=60` — [`schema.py`](../../../../../../../src/core/config/schema.py).
4. Split-analysis env names: `RATE_LIMIT_PHONE_REQUEST_REQUESTS` / `RATE_LIMIT_PHONE_REQUEST_WINDOW_S` — [`sec-01-g1-rate-limit-split-2026-06-26.md`](../../../../../../analysis/sec-01-g1-rate-limit-split-2026-06-26.md) §5.3.

### Gap / Проблема
Нет route key `POST /auth/phone/request` в `rate_limit_rules_for_config`.

### AC/DoD
- [ ] (P0) `ROUTE_AUTH_PHONE_REQUEST` + rule in `rate_limit_config.py` (per-user scope).
- [ ] (P0) `AppConfig` fields + env `RATE_LIMIT_PHONE_REQUEST_*` in `schema.py`.
- [ ] (P0) Policy note: window/limit documented vs `PHONE_RESEND_COOLDOWN_S` (не дублировать cooldown семантику).
- [ ] (P1) Traceability: Story AC #1 prerequisite for t02–t03.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/src/core/security/rate_limit_config.py`

### Out of scope
- Dependency wiring (t02–t03)
- Replacing OTP cooldown with 429

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.config.schema import load_config_from_env; from core.security.rate_limit_config import rate_limit_rules_for_config; c=load_config_from_env(); assert 'POST /auth/phone/request' in rate_limit_rules_for_config(c)"
```
