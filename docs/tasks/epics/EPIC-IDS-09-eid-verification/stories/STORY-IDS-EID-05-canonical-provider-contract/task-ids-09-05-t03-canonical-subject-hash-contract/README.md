## Task workspace — `task-ids-09-05-t03-canonical-subject-hash-contract`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000018`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F12)  
---

## Task: implement — canonical `subject_hash` contract and runtime-docs

### Цель
Зафиксировать правило F12: `EIDVerificationResult.subject_hash` — provider-agnostic stable identity; provider name только provenance; `verified_person_hash` formula unchanged. Verify/align mock и runtime-docs.

### Почему это важно
Story AC #3: anti-Sybil — один человек через разные провайдеры должен давать одинаковый `verified_person_hash` при одинаковом `country` + `subject_hash`.

### Факты из кода
1. [`base.py:8-14`](../../../../../../../src/core/providers/base.py) — `EIDVerificationResult.subject_hash` без docstring rule.
2. [`handlers.py:283-286`](../../../../../../../src/core/api/handlers.py) — `verified_person_hash = hash_secret(f"{country}:{subject_hash}", ...)`.
3. [`mock_provider.py:65-71`](../../../../../../../src/core/providers/mock/mock_provider.py) — `subject_hash="mock-" + secrets.token_hex(8)` (prefix `mock-`).
4. [`06-eid-providers.md:37`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — документирует `subject_hash="mock-<random>"`.

### Gap / Проблема
Контракт subject_hash не задокументирован; mock/doc используют provider-name-like prefix, противоречит backlog «без префикса провайдера».

### AC/DoD
- [x] (P0) Docstring/contract comment на `EIDVerificationResult.subject_hash`: normalized stable id **without provider name prefix**; provider in separate `provider` field.
- [x] (P0) [`06-eid-providers.md`](../../../../../../../docs/runtime-docs/06-eid-providers.md) — правило identity + formula `verified_person_hash`; убрать/исправить `mock-` prefix narrative.
- [x] (P0) Mock `subject_hash` — provider-agnostic token (verify backlog note; align if `mock-` violates rule).
- [x] (P1) `handlers.py` formula **unchanged** (country:subject_hash only).
- [x] (P1) Story AC #3 doc part traceability.

### Где менять код
- `doge-identity-service/src/core/providers/base.py`
- `doge-identity-service/src/core/providers/mock/mock_provider.py`
- `doge-identity-service/docs/runtime-docs/06-eid-providers.md`

### Out of scope
- Cross-provider dedup unit test — t04
- Orchestrator error codes — t02
- EID-02 real provider subject mapping

### Проверка
```bash
grep -n "subject_hash\|verified_person_hash" doge-identity-service/src/core/providers/base.py doge-identity-service/docs/runtime-docs/06-eid-providers.md
grep -n "mock-" doge-identity-service/src/core/providers/mock/mock_provider.py
```
