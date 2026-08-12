## Task workspace — `task-ids-09-06-t04-offline-redirect-and-json-regression-tests`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)
- Prerequisite: t01–t03 (outcome type, dynamic route, redirect render)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000019`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) AC #5–#6 (tests)  
---

## Task: tests — offline redirect markers, safe fallback, EID-01 JSON regression

### Цель
Добавить/обновить offline-тесты: redirect `Location` + query markers, safe fallback 400 без open-redirect, unregistered provider `ConfigError`, EID-01 mock flow через `Accept: application/json`.

### Почему это важно
Story AC #5 и #6 требуют зелёного offline-набора и регрессии EID-01. Без тестов redirect-модель не верифицируется.

### Факты из кода
1. [`test_eid_verification_flow.py`](../../../../../../../tests/test_eid_verification_flow.py) — mock flow start→callback→me; callback ожидает JSON 200.
2. [`test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py) — transport-level eID callback assertions.
3. [`test_canonical_provider_contract.py`](../../../../../../../tests/test_canonical_provider_contract.py) — `EidErrorCode` mapping patterns (reuse for redirect error marker).
4. Baseline: 225 pytest offline (post EID-05).

### Gap / Проблема
Нет тестов на 303 redirect, query markers `eid_status`/`eid_error`, safe fallback без redirect.

### AC/DoD
- [x] (P0) Успешный mock callback (browser, без `Accept`) → 303 + `Location` содержит `return_url` и `eid_status=verified`.
- [x] (P0) Provider error path → 303 + `eid_status=error` + `eid_error=<canonical>` (напр. `USER_CANCELLED` через mock/patch).
- [x] (P0) Unknown session / missing safe `return_url` → 400, no `Location` header (open-redirect guard).
- [x] (P0) `GET /auth/unknown-provider/callback` → `ConfigError` path (500 JSON envelope per global handler).
- [x] (P0) EID-01 mock flow: callback с `Accept: application/json` → JSON 200 `status=verified`; full start→callback→me green.
- [x] (P1) Story AC #5, #6 (offline part) traceability.
- [x] (P1) Full offline suite green: `pytest -m "not live_integration"`.

### Где менять код
- `doge-identity-service/tests/test_eid_callback_redirect.py` (новый, предпочтительно)
- `doge-identity-service/tests/test_eid_verification_flow.py` (добавить `Accept: application/json` на callback)
- `doge-identity-service/tests/test_asgi_transport.py` (при необходимости)

### Out of scope
- Live integration / real provider — EID-02
- Runtime docs — t05
- Story acceptance gate — t06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_eid_callback_redirect.py tests/test_eid_verification_flow.py tests/test_asgi_transport.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
