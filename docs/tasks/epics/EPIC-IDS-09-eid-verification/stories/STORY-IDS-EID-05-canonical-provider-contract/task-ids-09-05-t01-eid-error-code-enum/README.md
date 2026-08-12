## Task workspace — `task-ids-09-05-t01-eid-error-code-enum`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)
- Prerequisite: STORY-IDS-EID-03 Done ([`../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000018`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2)  
---

## Task: implement — `EidErrorCode` StrEnum and typed `EIDProviderError`

### Цель
Ввести каноническую таксономию ошибок провайдера (`EidErrorCode`) и типизировать `EIDProviderError(code=EidErrorCode.X)` — фундамент story Scope #1.

### Почему это важно
Story AC #1 и #4: ядро должно знать только канон; новые провайдеры мапят вендор-коды в enum, не добавляя веток в orchestrator.

### Факты из кода
1. [`base.py:24-29`](../../../../../../../src/core/providers/base.py) — `EIDProviderError` с `code: str = "EID_PROVIDER_ERROR"`, без StrEnum.
2. [`handlers.py:265-273`](../../../../../../../src/core/api/handlers.py) — все ошибки callback → `failure_reason="provider_error"`.
3. [`__init__.py`](../../../../../../../src/core/providers/__init__.py) — public re-exports provider types.

### Gap / Проблема
Нет `EidErrorCode`; код ошибки — произвольная строка, не канонический enum из backlog Scope.

### AC/DoD
- [x] (P0) `EidErrorCode` StrEnum в `providers/base.py` с values: `USER_CANCELLED`, `STATE_MISMATCH`, `TOKEN_EXCHANGE_FAILED`, `IDENTITY_VALIDATION_FAILED`, `MISSING_REQUIRED_CLAIM`, `COUNTRY_NOT_ALLOWED`, `METHOD_NOT_ALLOWED`, `PROVIDER_UNAVAILABLE`, `UNKNOWN`.
- [x] (P0) `EIDProviderError` принимает `code: EidErrorCode` (default `UNKNOWN`); `code` доступен как каноническое значение.
- [x] (P1) Export `EidErrorCode`, `EIDProviderError` from `core.providers`.
- [x] (P1) Story AC #1, #4 traceability.

### Где менять код
- `doge-identity-service/src/core/providers/base.py`
- `doge-identity-service/src/core/providers/__init__.py`

### Out of scope
- Orchestrator handling — t02
- Vendor→canon mapping в Authentigate — EID-02
- HTTP/redirect проброс кодов — EID-06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.providers.base import EidErrorCode, EIDProviderError; e = EIDProviderError('x', code=EidErrorCode.USER_CANCELLED); assert e.code == EidErrorCode.USER_CANCELLED"
.venv/bin/python -m pytest tests/test_eid_providers.py -m "not live_integration" -q
```
