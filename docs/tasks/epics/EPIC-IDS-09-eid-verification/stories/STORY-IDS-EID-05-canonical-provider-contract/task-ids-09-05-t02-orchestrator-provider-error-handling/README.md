## Task workspace — `task-ids-09-05-t02-orchestrator-provider-error-handling`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)
- Prerequisite: t01 (`EidErrorCode`, typed `EIDProviderError`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000018`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2)  
---

## Task: fix — orchestrator distinguishes `EIDProviderError` vs unexpected `Exception`

### Цель
Заменить широкий `except Exception` в callback orchestrator на раздельную обработку `EIDProviderError` (сохранить канонический код) и fallback `UNKNOWN` для неожиданных ошибок.

### Почему это важно
Story AC #2: `USER_CANCELLED` должен быть отличим от generic `provider_error` в session `failure_reason` и audit.

### Факты из кода
1. [`handlers.py:263-281`](../../../../../../../src/core/api/handlers.py) — `except Exception` → `mark_failed(..., "provider_error")`, audit `failure_reason="provider_error"`.
2. [`handlers.py:83-111`](../../../../../../../src/core/api/handlers.py) — `_log_eid_audit` принимает `failure_reason: str | None`.
3. [`contracts.py:52`](../../../../../../../src/core/domain/contracts.py) — `mark_failed(session_id, reason: str)`.
4. t01 — `EIDProviderError` с `EidErrorCode`.

### Gap / Проблема
Orchestrator теряет канонический код; все provider failures схлопываются в `provider_error`.

### AC/DoD
- [x] (P0) `except EIDProviderError as e` → `mark_failed(session.id, e.code.value)` (или эквивалент str), audit `failure_reason=e.code.value`.
- [x] (P0) Отдельный `except Exception` → `mark_failed(..., EidErrorCode.UNKNOWN.value)` (или `unknown`), envelope без утечки internal details.
- [x] (P1) Error response envelope может не пробрасывать код наружу (HTTP redirect — EID-06); session/audit — SSOT для t04 tests.
- [x] (P1) Story AC #2 traceability.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`

### Out of scope
- HTTP redirect / query marker с кодом — EID-06
- Authentigate adapter mapping — EID-02
- Offline tests — t04

### Проверка
```bash
cd doge-identity-service
grep -n "EIDProviderError\|provider_error" src/core/api/handlers.py
.venv/bin/python -m pytest tests/test_eid_verification_flow.py -m "not live_integration" -q
```
