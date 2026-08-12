## Task workspace — `task-ids-09-06-t01-eid-callback-outcome-dataclass`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)
- Prerequisite: STORY-IDS-EID-05 Done ([`../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000019`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md) Scope #1; [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F1)  
---

## Task: implement — `EidCallbackOutcome` dataclass and handler refactor

### Цель
Ввести доменный исход callback (`EidCallbackOutcome`) и перевести `handle_auth_eid_callback` на возврат этого типа вместо `(dict, int)` — фундамент story Scope #1 и AC #1.

### Почему это важно
Оркестратор не должен знать HTTP-представление (JSON vs redirect). Разделение domain outcome и transport render — prerequisite для t02–t03.

### Факты из кода
1. [`handlers.py:190-351`](../../../../../../../src/core/api/handlers.py) — `handle_auth_eid_callback` возвращает `tuple[dict, int]`; success JSON [`handlers.py:348-351`](../../../../../../../src/core/api/handlers.py).
2. [`handlers.py:266-302`](../../../../../../../src/core/api/handlers.py) — provider errors несут `EidErrorCode` в `failure_reason` и envelope `eid_error_code`.
3. [`base.py`](../../../../../../../src/core/providers/base.py) — `EidErrorCode` StrEnum (EID-05).
4. [`asgi_app.py:238-248`](../../../../../../../src/core/api/asgi_app.py) — route вызывает handler и всегда оборачивает в `_json_envelope`.

### Gap / Проблема
Нет `EidCallbackOutcome`; handler привязан к JSON envelope и HTTP status tuple.

### AC/DoD
- [x] (P0) `EidCallbackOutcome` dataclass: `outcome: Literal["verified","already_verified","failed"]`, `return_url: str | None`, `error_code: EidErrorCode | None`, `json_status: int`.
- [x] (P0) `handle_auth_eid_callback` возвращает `EidCallbackOutcome` (не `(dict,int)`).
- [x] (P0) Все ветки мапятся: verified → `outcome="verified"` + `return_url` из сессии; already_consumed → `already_verified`; session/provider/config errors → `failed` + `error_code` где применимо + корректный `json_status`.
- [x] (P1) Story AC #1 traceability.
- [x] (P1) Существующие unit/import paths не ломаются до t03 (временный shim в asgi допустим в t02).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py` (или новый модуль рядом, напр. `core/api/eid_callback.py`)
- При необходимости: `doge-identity-service/src/core/api/__init__.py` (re-export)

### Out of scope
- HTTP redirect / `Accept` negotiate — t03
- Динамический роут — t02
- Тесты redirect — t04
- Runtime docs — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.api.handlers import handle_auth_eid_callback, EidCallbackOutcome
assert 'EidCallbackOutcome' in str(EidCallbackOutcome)
"
.venv/bin/python -m pytest tests/test_eid_verification_flow.py tests/test_canonical_provider_contract.py -m "not live_integration" -q
```
