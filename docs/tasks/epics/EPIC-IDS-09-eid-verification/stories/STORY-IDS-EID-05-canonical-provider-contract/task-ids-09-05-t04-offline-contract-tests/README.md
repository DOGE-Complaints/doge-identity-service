## Task workspace — `task-ids-09-05-t04-offline-contract-tests`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)
- Prerequisite: t01–t03 implemented

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000018`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2, F12)  
---

## Task: tests — offline error mapping and cross-provider dedup coverage

### Цель
Добавить offline-тесты: (1) orchestrator сохраняет `EidErrorCode` в failure path; (2) один `country`+`subject_hash` через разные `provider` names → одинаковый `verified_person_hash`.

### Почему это важно
Story AC #2, #3 (dedup test), #5 — без тестов канон контракта не verifiable.

### Факты из кода
1. [`test_eid_verification_flow.py`](../../../../../../../tests/test_eid_verification_flow.py) — e2e mock flow; `subject_hash="fixed-subject"` fixture pattern.
2. [`test_eid_providers.py`](../../../../../../../tests/test_eid_providers.py) — provider unit tests; asserts `mock-` prefix today.
3. Нет `test_canonical_provider_contract.py` — grep по `EIDProviderError` / cross-provider dedup в tests/.
4. t02 — orchestrator error branches; t03 — subject_hash contract.

### Gap / Проблема
Нет регрессии на различие `USER_CANCELLED` vs `UNKNOWN`; нет unit-теста cross-provider `verified_person_hash` dedup.

### AC/DoD
- [x] (P0) Test: `EIDProviderError(code=USER_CANCELLED)` в callback path → session/audit `failure_reason` содержит канонический код (not `provider_error`).
- [x] (P0) Test: unexpected `Exception` → `UNKNOWN` (or equivalent) failure_reason.
- [x] (P0) Test: same `country` + `subject_hash`, different `EIDVerificationResult.provider` values → identical `verified_person_hash` via `hash_secret`.
- [x] (P1) Offline suite green: `pytest -m "not live_integration" -q`.
- [x] (P1) Story AC #2, #3, #5 traceability.

### Где менять код
- `doge-identity-service/tests/test_canonical_provider_contract.py` (new)
- при необходимости: `tests/test_eid_verification_flow.py`, `tests/test_eid_providers.py` (mock prefix updates from t03)

### Out of scope
- Live integration / SPIKE-09
- HTTP redirect error marker — EID-06
- Story acceptance doc — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_canonical_provider_contract.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
