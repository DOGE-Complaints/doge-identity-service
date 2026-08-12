## Task workspace — `task-ids-03-02-t03-singleton-behavior-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §6 Story 2 Acceptance Criteria  
---

## Task: tests — singleton behavior and env reload

### Цель
Pytest-покрытие AC Story 2: identity singleton, cache clear → new `id()`, monkeypatch env reload, startup logging (where automatable).

### Факты из кода
1. Story 2 AC — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L148-153.
2. Epic §8 steps 2-3 — build + singleton scripts ([`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L211-232).
3. [`tests/test_di_singleton.py`](../../../../../../../tests/test_di_singleton.py) — **не создавать** (EPIC-IDS-06, epic §5 L68, §8 step 5).

### Gap
Нет pytest для cache clear, env monkeypatch, parallel HTTP same deps id.

### AC/DoD
- [x] (P0) `get_api_dependencies() is get_api_dependencies()` — True.
- [x] (P0) После `_clear_api_dependencies_cache()` следующий вызов создаёт новый объект (другое `id()`).
- [x] (P0) `monkeypatch.setenv("LOG_LEVEL", "DEBUG"); _clear_api_dependencies_cache(); get_api_dependencies().config.log_level == "DEBUG"`.
- [x] (P1) При startup сервера лог содержит запись `configure_logging` уровня deps.config.log_level (см. lifespan).
- [x] (P1) Два параллельных HTTP запроса получают один и тот же `ApiDependencies` (verifiable через `id()` логирование).

### Acceptance
- [acceptance-verification-task-ids-03-02-t03-singleton-behavior-verification.md](./acceptance-verification-task-ids-03-02-t03-singleton-behavior-verification.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)

### Где менять код
- `doge-identity-service/tests/test_api_dependencies.py` (расширение)

### Out of scope
- Полный `tests/test_di_singleton.py` — EPIC-IDS-06
- Story 3 TODO hooks — t01 Story 3

### Команды проверки
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q
python3.11 -c "
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
_clear_api_dependencies_cache()
d1 = get_api_dependencies()
d2 = get_api_dependencies()
assert d1 is d2
print('singleton OK')
"
```
