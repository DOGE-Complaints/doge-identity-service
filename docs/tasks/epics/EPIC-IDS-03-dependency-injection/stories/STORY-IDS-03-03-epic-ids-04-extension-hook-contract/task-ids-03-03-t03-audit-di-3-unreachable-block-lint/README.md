## Task workspace — `task-ids-03-03-t03-audit-di-3-unreachable-block-lint`

- Story: [`../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md`](../STORY-IDS-03-03-epic-ids-04-extension-hook-contract.md)
- Audit source: [`../../../../../../analysis/epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) (DI-3)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_03_audit_2026_05_28`  
---

## Task: docs — unreachable EPIC-IDS-04 block и CI/linter

### Цель
Закрыть gap DI-3: проверить, флажит ли CI/linter закомментированный блок после `return` в `build_api_dependencies()`; при срабатывании — добавить suppress (`# noqa`); не удалять block (Story 3 contract).

### Почему это важно (риск)
Static analyzers (mypy, ruff `W0101`) могут падать на unreachable code; block intentional per EPIC-IDS-03 Story 3.

### Факты из кода
1. [`epic-ids-03-audit-2026-05-28.md`](../../../../../../analysis/epic-ids-03-audit-2026-05-28.md) DI-3 §Story 3.
2. [`src/core/api/dependencies.py:71–90`](../../../../../../../src/core/api/dependencies.py): `return ApiDependencies(...)` затем commented EPIC-IDS-04 target block (unreachable).
3. [`pyproject.toml`](../../../../../../../pyproject.toml): нет ruff/unreachable rules в текущей конфигурации.
4. [`test_build_api_dependencies_has_epic_hook_comments`](../../../../../../../tests/test_api_dependencies.py): верифицирует наличие block в файле.

### Gap / Проблема
Dead code по стандартам Python — intentional design; при strict CI нужен suppress или документированное «no action».

### AC/DoD
- [x] (P0) Проверены CI/linter (pyright, ruff если добавлен) на `dependencies.py` — зафиксирован результат в acceptance.
- [x] (P0) Linter не флажит unreachable — acceptance документирует «no action required» с evidence.
- [x] (P1) `test_build_api_dependencies_has_epic_hook_comments` по-прежнему проходит.

### Acceptance
- [acceptance-verification-task-ids-03-03-t03-audit-di-3-unreachable-block-lint.md](./acceptance-verification-task-ids-03-03-t03-audit-di-3-unreachable-block-lint.md) — PASS

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py` — только при необходимости `# noqa` на commented block

### Out of scope
- Удаление или перенос commented block (нарушает Story 3 AC)
- Реализация EPIC-IDS-04 factory

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q -k epic_hook
```
