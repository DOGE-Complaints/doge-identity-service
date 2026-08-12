## Task workspace — `task-ids-03-03-t01-todo-epic-hooks-in-build-factory`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §6 Story 3  
---

## Task: implement — TODO EPIC-IDS-04/05 hook comments in build_api_dependencies

### Цель
Добавить документационный контракт в `build_api_dependencies()`: TODO-маркеры и закомментированный EPIC-IDS-04 target block из epic Outputs L164-182.

### Факты из кода
1. Story 3 AC (документация) — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L185-188.
2. Target block — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L164-182 (`provide_service_factory`, nine getters).
3. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — TODO-маркеры отсутствуют.

### Gap
Нет явных hooks для EPIC-IDS-04/05 в factory.

### AC/DoD
- [x] (P0) В EPIC-IDS-03 — комментарии `# TODO EPIC-IDS-04: replace with provide_service_factory(...)` стоят над хардкодным `StubBearerTokenAuth()`.
- [x] (P0) В EPIC-IDS-03 — комментарии `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks` стоят над `db_checks: dict[str, bool] = {}`.
- [x] (P1) Закомментированный block `provide_service_factory` + полный `return ApiDependencies(...)` из epic L164-182 присутствует в `dependencies.py`.

### Acceptance
- [acceptance-verification-task-ids-03-03-t01-todo-epic-hooks-in-build-factory.md](./acceptance-verification-task-ids-03-03-t01-todo-epic-hooks-in-build-factory.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`

### Out of scope
- Реальный импорт `provide_service_factory` — EPIC-IDS-04
- Supabase healthchecks runtime — EPIC-IDS-05

### Команды проверки
```bash
grep -n 'TODO EPIC-IDS-04\|TODO EPIC-IDS-05\|provide_service_factory' \
  doge-identity-service/src/core/api/dependencies.py
```
