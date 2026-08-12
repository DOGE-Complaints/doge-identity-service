## Task workspace — `task-ids-12-03-t02-audit-ip-ua-hmac-hashing-helper`

- Story: [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- Prerequisite: STORY-IDS-SEC-01 🟢 (`_client_ip` in [`rate_limit_dependency.py`](../../../../../../../src/core/api/rate_limit_dependency.py))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000037`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) Scope §хэширование; Story AC #2, #5  
---

## Task: implement — audit IP/UA HMAC hashing helper and spec alignment

### Цель
Централизовать извлечение IP/UA из `Request` и HMAC-хэширование через `hash_secret` — Story Scope §хэширование, AC #2, #5.

### Почему это важно
Единый примитив для eID и phone audit; spec 16 пример использует plain sha256 — нужно зафиксировать HMAC как фактический выбор.

### Факты из кода
1. `hash_secret` HMAC-SHA256 — [`hashing.py:9-11`](../../../../../../../src/core/security/hashing.py).
2. IP extraction + trusted proxy — [`rate_limit_dependency.py:15-29`](../../../../../../../src/core/api/rate_limit_dependency.py) `_client_ip`.
3. Phone hash key pattern: `eid_secret` — [`handlers.py:555`](../../../../../../../src/core/api/handlers.py).
4. Spec 16 example sha256 — [`16-security-privacy-observability.md:151-152`](../../../../../../../docs/requirements/16-security-privacy-observability.md).

### Gap / Проблема
Нет shared helper для audit IP/UA → hash; алгоритм не задокументирован в as-built.

### AC/DoD
- [ ] (P0) Helper (напр. `audit_context.py`): extract client IP (reuse `_client_ip` logic or shared module) + `User-Agent` header.
- [ ] (P0) `hash_audit_value(plaintext, *, key)` wraps `hash_secret`; key from config (`eid_secret` or documented choice).
- [ ] (P0) Story AC #2: только hash в storage path, never raw IP/UA in event model fields from helper.
- [ ] (P1) Story AC #5: update [`16-security-privacy-observability.md`](../../../../../../../docs/requirements/16-security-privacy-observability.md) + [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) §audit — HMAC choice documented.
- [ ] (P1) Unit-level test for helper (deterministic hash given key + input).

### Где менять код
- `doge-identity-service/src/core/security/` (new `audit_context.py` or extend `hashing.py`)
- `doge-identity-service/src/core/api/rate_limit_dependency.py` (optional: extract shared `_client_ip`)
- `doge-identity-service/docs/requirements/16-security-privacy-observability.md`
- `doge-identity-service/docs/runtime-docs/04-security.md`

### Out of scope
- Handler wiring (t03–t04)
- PV-09 Supabase migration
- Raw IP/UA forensics storage

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/ -k "audit" -m "not live_integration" -q
grep -n "HMAC\|hash_secret" doge-identity-service/docs/requirements/16-security-privacy-observability.md
```
